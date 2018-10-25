# !usr/bin/env python3
# encoding:utf-8
"""
@project = Spiderbaike
@file = DataOutput
@author = 'Easton Liu'
@creat_time = 2018/10/9 20:22
@explain:数据存储器

"""

import pymongo

class DataOutput(object):
    def mongodb(self,dbname,data):
        client = pymongo.MongoClient()
        db = client[dbname]
        db.baike.insert(data)
