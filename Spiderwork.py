# !usr/bin/env python3
# encoding:utf-8
"""
@project = Spiderbaike
@file = SpiderManager
@author = 'Easton Liu'
@creat_time = 2018/10/9 20:29
@explain:爬虫调度器

"""
from time import sleep
from UrlManager import UrlManager
from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser
from DataOutput import DataOutput
from multiprocessing.managers import BaseManager


class Spiderwork(object):
    def __init__(self):
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        server_addr = '172.21.23.221'
        print("Connect to server %s"%server_addr)
        self.m = BaseManager(address=(server_addr,8001),authkey=b'lmj')
        self.m.connect()
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
    def crawl(self):
        while(True):
            try:
                if not self.task.empty():
                    url = self.task.get()
                    if url == 'end':
                        print("收到控制器发送的停止爬虫消息")
                        self.result.put({'new_urls':'end','data':'end'})
                        return
                    print("正在解析数据%s"%url)
                    content = self.downloader
                    new_urls,data = self.parser.parser(url,content)
                    return self.result.put({'new_urls':new_urls,'data':data})
            except Exception as e:
                print(e)
                print("爬取失败")
if __name__=='__main__':
    spider = Spiderwork()
    spider.crawl()





