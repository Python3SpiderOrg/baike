# !usr/bin/env python3
# encoding:utf-8
"""
@project = Spiderbaike
@file = HtmlDownloader
@author = 'Easton Liu'
@creat_time = 2018/10/9 19:32
@explain:HTML下载器，下载网页

"""

import requests

class HtmlDownloader(object):
    def __init__(self):
        self.headers ={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
        }
    def download(self,url):
        if url is None:
            return
        rec = requests.get(url,headers=self.headers)
        if rec.status_code == 200:
            rec.encoding='utf-8'
            return rec.text
        return None

