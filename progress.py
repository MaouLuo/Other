
import sys
import time
def progress(percent,width=50):
    '''进度打印功能'''
    if percent >= 100:
        percent=100
  
    show_str=('[%%-%ds]' %width) %(int(width * percent/100)*"#") #字符串拼接的嵌套使用
    print('\r%s %d%%' %(show_str,percent))
  
  
#=========应用==========
def test():	
	data_size=333 #定义传输的数据，实际应用中这个值改一下就可以了
	recv_size=0
	while recv_size < data_size:
	    time.sleep(0.1) #模拟数据的传输延迟
	    recv_size+=10 #每次收1024
	  
	    recv_per=int(100*recv_size/data_size) #接收的比例
	    progress(recv_per,width=30) #调用进度条函数，进度条的宽度默认设置为30

def test1():
	for i in range(11):
	    time.sleep(0.5)
	    print('\r当前进度：{0}{1}%'.format('▉'*i,(i*10)))
	print('加载完成！')


test()