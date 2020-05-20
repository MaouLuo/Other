# -*- coding:utf-8 -*-

import requests
from multiprocessing import Process
import json
import threading

# 声明线程锁
threadLock = threading.Lock()

check_url = 'http://icanhazip.com/'  # 外网ip测试网站，返回ip信息

url = 'http://172.16.0.215:5000/'
protocol_type = 'http'
addr = '113.59.99.138:8910'
ip_list = [
    {"http":'113.59.99.138:8910'},
    {'http':'60.191.11.241:3128'},
    {'http':'121.40.237.0:8080'},
    {'http':'112.253.11.113:8000'},
    {'http':'60.191.11.249:3128'}
]

ip_list1 = [
    '113.59.99.138:8910',
    '60.191.11.241:3128',
    '121.40.237.0:8080',
    '112.253.11.113:8000',
    '60.191.11.249:3128'
]

def check_ip(i):
    #print('{0} check'.format(ip[0]))
    #print(ip['http'])    
    try:
        resp = requests.get(url=check_url, proxies={'http':ip_list1[i]}, timeout=15 )
    except TimeoutError:
        #print(ip['http'] + ' timeout')
        print('timeout')
    else:
        print(resp.text)

def main1():
    print('main run') 
      
    for i in range(5):
        #print(ip) 
        p = Process(target=check_ip,)
        p.start()   #让这个进程开始执行test函数里面的代码
        p.join(20)     #等进程p结束之后，才会继续向下走

def main():

    for i in range(5):
        print(ip_list1[i])

'''
    resp = requests.get(url=check_url, proxies={'http':'112.95.207.236:8888'}, timeout=30 )
    print(resp.text)
'''


class check_ip_Thread(threading.Thread):

    def __init__(self,name=None):
        threading.Thread.__init__(self,name=name)

    def run(self):
        print(threading.current_thread().name)

        while True:
            # 获取锁，用于线程同步
            threadLock.acquire()
            if len(ip_list) > 0:
                #print('less {0}'.format(len(ip_list)))
                #print('线程{}开始获取图组url'.format(self.threadId))
                ip = ip_list.pop()
                threadLock.release()  # 释放锁，开启下一个线程
            else:
                return 'ip pool is empty'

            try:
                resp = requests.get(url=check_url, proxies=ip, timeout=15 )
                if resp.status_code == '200':
                    print('{0} check'.format(resp.text))
            
            except TimeoutError:
                #print(ip['http'] + ' timeout')
                #print('timeout')
                pass
            except Exception as e:
                pass
                #print(e)
                


def main2():
    thread = check_ip_Thread()
    thread.start()
    thread.join()

if __name__ == '__main__':
    main2()