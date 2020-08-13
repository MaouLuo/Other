from multiprocessing import Process, Queue
from random import randint
import requests
import threading
import re
import time
import datetime

def foo():
    
    a = 200
    def localnum():
    	#nonlocal a
    	a = 300
    	#print('local {0}'.format(a))
    localnum()
    print('foo {0}'.format(a))  # 200

def calculation():
    total = 0
    number_list = [x for x in range(1, 100000001)]
    #start = time()
    for number in number_list:
        total += number
    print(total)
    #end = time()
    #print('Execution time: %.3fs' % (end - start))

def task_handler(curr_list, result_queue):
    total = 0
    for number in curr_list:
        total += number
    result_queue.put(total)

def calculation_process():
	processes = []
	number_list = [x for x in range(1, 100000001)]
	result_queue = Queue()
	index = 0
    # 启动8个进程将数据切片后进行运算
	for _ in range(8):
		p = Process(target=task_handler,
	    	args=(number_list[index:index + 12500000], result_queue))
		index += 12500000
		processes.append(p)
		p.start()
	# 开始记录所有进程执行完成花费的时间
	#start = time()
	for p in processes:
		p.join()
	# 合并执行结果
	total = 0
	while not result_queue.empty():
		total += result_queue.get()
	print(total)
	#end = time()
	#print('Process Execution time: ', (end - start), 's', sep='')

def test():
	f = [x + y for x in 'ABCDE' for y in '1234567']
	#print(f)

	
	#re = {a:1}

	dic = {'a':1, 'b':12, 'c':11, 'd':21}

	for k,v in dic.items():
		print('key:{0}, v:{1}'.format(k,v)) 
	#print(re.key())

'''
def test1():
	bar = Bar('Processing', max=100, fill='@', suffix='%(percent)d%%')
	for i in range(100):
		time.sleep(0.1)
		bar.next()
	bar.finish()
'''

def test2():
	for _ in range(10):
	#	print(random() + 1)
		pass

def sever_test():
	url = 'https://sc.ftqq.com/SCU77831Td9cccdfd533462659d8d881e9408da945e1ffad3eb8a8.send'
	data = {
		'text': 'py'
	}
	resp = requests.post(url, data=data)
	print(resp.text)

def get_date():
	curr_time = datetime.datetime.now()
	print(curr_time.strftime("%Y%m%d"))

def get_sina_data():
	url = 'http://hq.sinajs.cn/list=sh600389'
	resp = requests.get(url, timeout=20)
	print(resp.text[0])

def bool2str():
	a = False
	b=''
	print('{} hahah'.format(a))
	if None == a:
		print('yes')
	else:
		print('no')
	#print(b is False)

def main():
	#get_date()
	#list_e = []
	#print(list_e is False)
	#get_sina_data()
	bool2str()


if __name__ == '__main__':
    main()
    