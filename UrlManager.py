# !usr/bin/env python3
# encoding:utf-8
"""
@project = Spiderbaike
@file = UrlManager
@author = 'Easton Liu'
@creat_time = 2018/10/9 19:14
@explain: URL管理器

"""
import pickle
import hashlib
class UrlManager(object):
    def __init__(self):
        self.new_urls=self.load_progress("new_urls.txt") #未爬取的URL集合
        self.old_urls=self.load_progress("old_urls.txt") #已爬取的URL集合
    def has_new_url(self):
        '''
        判断是否有未爬取的URL
        :return:
        '''
        return self.new_url_size() != 0
    def get_new_url(self):
        '''
        获取一个未爬取的URL
        :return:
        '''
        new_url = self.new_urls.pop()
        m = hashlib.md5()
        m.update(new_url)
        self.old_urls.add(m.hexdigest()[8:-8])
        return new_url
    def add_new_url(self,url):
        '''
        将新的URL添加到未爬取得URL集合中
        :return:
        '''
        if url is None:
            return
        m = hashlib.md5()
        m.update(url)
        url_md5 = m.hexdigest()[8:-8]
        if url not in self.new_urls and url_md5 not in self.old_urls:
            self.new_urls.add(url)
    def add_new_urls(self,urls):
        '''
        将新的URL集合添加到未爬取得URL集合中
        :return:
        '''
        if urls is None:
            return None
        for url in urls:
            self.add_new_url(url)
    def new_url_size(self):
        '''
        获取未爬取得URL集合大小
        :return:
        '''
        return len(self.new_urls)
    def old_url_size(self):
        '''
        获取已爬取得URL集合大小
        :return:
        '''
        return len(self.old_urls)
    def save_progress(self,data,path):
        '''
        序列化保存爬取进度
        :param data:要保存的数据
        :param path:文件路径
        :return:
        '''
        with open(path,'b+') as f:
            pickle.dump(data,f)
    def load_progress(self,path):
        '''
        反序列化加载进度文件
        :param path:
        :return:
        '''
        print("加载进度文件：%s"%path)
        try:
            with open(path,'rb') as f:
                tmp = pickle.load(f)
                return tmp
        except:
            print("无进度文件")
        return set()

if __name__=='__mian__':
    UrlManager()
