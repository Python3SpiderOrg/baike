# !usr/bin/env python3
# encoding:utf-8
"""
@project = Spiderbaike
@file = test
@author = 'Easton Liu'
@creat_time = 2018/10/10 16:59
@explain:

"""
import random,time
from  queue import Queue
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support

task_num=10
task_queue = Queue(task_num)
result_queue = Queue(task_num)
# def get_task():
#     return task_queue
# def get_result():
#     return result_queue
def get_task_queue():
    global task_queue
    return task_queue
def get_result_queue():
    global result_queue
    return result_queue

class QueueManager(BaseManager):
    pass
def win_run():
    QueueManager.register('get_task_queue',callable=lambda :task_queue)
    QueueManager.register('get_result_queue',callable=lambda :result_queue)
    manager = QueueManager(address=('127.0.0.1',8081),authkey=b'lmj')
    freeze_support()
    manager.start()
    task = manager.get_task_queue()
    result = manager.get_result_queue()
    for i in range(10):
        n = random.randint(0,10000)
        print("Put task %d..."%n)
        task.put(n)
    print("Try get result...")
    for i in range(10):
        r = result.get(True)
        print("Result is %d"%r)
    manager.shutdown()
    print("Master exit...")
if __name__=='__main__':
    freeze_support()
    win_run()