# !usr/bin/env python3
# encoding:utf-8
"""
@project = Spiderbaike
@file = HtmlParser
@author = 'Easton Liu'
@creat_time = 2018/10/9 19:43
@explain:HTML解析器，提取新的URL以及词条的标题和摘要

"""
import re
from urllib import parse
from bs4 import BeautifulSoup

class HtmlParser(object):
    def parser(self,page_url,html_cont):
        '''
        解析网页内容，抽取URL和数据
        :param page_url:下载页面的URL
        :param html_cont:下载页面的数据
        :return:url和数据
        '''
        if page_url is None or html_cont is None:
            return None
        soup = BeautifulSoup(html_cont,'html.parser')
        new_urls = self._get_new_urls(page_url,soup)
        new_data = self._get_new_data(page_url,soup)
        return new_urls,new_data
    def _get_new_urls(self,page_url,soup):
        '''
        抽取新的URL集合
        :param page_url: 下载页面的URL
        :param soup:
        :return: 页面新的URL集合
        '''
        new_urls=set()
        links = soup.find_all('a',href=re.compile(r'/item/')) #正则出页面符合要求的URL列表
        for link in links:
            new_url = link['href']
            new_full_url = parse.urljoin(page_url,new_url) #拼接完整的URL
            new_urls.add(new_full_url)
        return new_urls
    def _get_new_data(self,page_url,soup):
        '''
        抽取有效数据
        :param page_url:下载页面URL
        :param soup:
        :return:有效数据
        '''
        data = {}
        data['url']=page_url
        title = soup.find('dd',class_="lemmaWgt-lemmaTitle-title").find('h1')
        data['title'] = title.get_text()
        summary = soup.find('div',class_="lemma-summary")
        data['summary'] = summary.get_text()
        return data



