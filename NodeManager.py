# !usr/bin/env python3
# encoding:utf-8
"""
@project = Spiderbaike
@file = SpiderManager
@author = 'Easton Liu'
@creat_time = 2018/10/9 20:29
@explain:爬虫调度器

"""
# from queue import Queue
from time import sleep
from UrlManager import UrlManager
from DataOutput import DataOutput
from multiprocessing.managers import BaseManager
import pickle
from multiprocessing import  Process,Queue



class NodeManager(object):
    def __init__(self):
        self.urlmanager=UrlManager()
        self.dataoutput=DataOutput()

    def get_task(self):
        global url_q
        return url_q
    def get_result(self):
        global result_q
        return result_q


    def start_Manager(self,url_q,result_q):
        '''
        分布式管理器
        :param url_q: url队列,URL管理进程将URL传递给爬虫节点的通道
        :param result_q:结果队列，爬虫节点将数据返回给数据提取进程的通道
        :return:
        '''
        BaseManager.register('get_task_queue',callable=self.get_task)
        BaseManager.register('get_result_queue',callable=self.get_result)
        manager = BaseManager(address=('172.30.80.1',8001),authkey=b'lmj')
        return manager
    def url_manager_proc(self,url_q,conn_q,root_url):
        '''
        URL管理进程，把新的URL发送到url_q队列
        :param url_q:
        :param conn_q:数据提取进程将新的URL提交给URL管理进程的通道
        :param root_url:
        :return:
        '''
        url_manager = UrlManager()
        url_manager.add_new_url(root_url)
        while True:
            while(url_manager.has_new_url()):
                new_url = url_manager.get_new_url()
                url_q.put(new_url)
                print("已爬取%d个词条。"%url_manager.old_url_size())
                if (url_manager.old_url_size()>2000):
                    url_q.put('end')
                    print("发送结束消息")
                    url_manager.save_progress('new_urls.txt',url_manager.new_urls)
                    url_manager.save_progress('old_urls.txt',url_manager.old_urls)
                    return
            try:
                if not conn_q.empty():
                    urls = conn_q.get()
                    url_manager.add_new_urls(urls)
            except BaseException:
                sleep(0.1)
    def result_solve_proc(self,result_q,conn_q,store_q):
        '''
        数据提取进程，从result_q队列获取数据，提取新的URL放入到conn_q队列，把标题和只要放入到store_q队列
        :param result_q:
        :param conn_q:
        :param store_q:
        :return:
        '''
        while(True):
            try:
                if not result_q.empty():
                    content = result_q.get(True)
                    if content['new_urls']=='end':
                        print("数据提取进程收到结束消息")
                        store_q.put('end')
                        return
                    print(content['new_urls'])
                    conn_q.put(content['new_urls'])
                    store_q.put(content['data'])
                else:
                    sleep(0.1)
            except BaseException:
                sleep(0.1)
    def store_proc(self,store_q):
        '''
        数据存储进程，从store_q队列获取标题和摘要，调取存储器
        :param store_q:
        :return:
        '''
        out_put = self.dataoutput
        while True:
            if not store_q.empty():
                data = store_q.get(True)
                if data == 'end':
                    print("数据存储进程收到结束消息")
                    return
                out_put.mongodb('daidu',data)
            else:
                sleep(0.1)

if __name__=="__main__":
    url_q = Queue()
    conn_q = Queue()
    result_q = Queue()
    store_q = Queue()
    node = NodeManager()
    manager = node.start_Manager(url_q,result_q)
    url_manager_proc = Process(target=node.url_manager_proc,
                               args=(url_q,result_q,r'https://baike.baidu.com/item/网络爬虫/5162711'.encode('utf-8'),))
    result_solve_proc = Process(target=node.result_solve_proc,args=(result_q,conn_q,store_q))
    store_proc = Process(target=node.store_proc,args=(store_q,))
    url_manager_proc.start()
    result_solve_proc.start()
    store_proc.start()
    manager.get_server().serve_forever()



