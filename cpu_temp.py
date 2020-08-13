# -*- coding:utf-8 -*-

import configparser 
from serverj import ServerJ
import datetime

def r_conf(item, path='/home/pi/service/config.ini', name='token'):
#def r_conf(item, path='D:\\code\\service\\config.ini', name='token'):
    config = configparser.ConfigParser()
    config.read(path, encoding='utf-8')
    cont = config.get(item, name)
    return cont

def get_date():
    cur_time = datetime.datetime.now()
    date = cur_time.strftime("%Y-%m-%d %H:%M")
    #print(date-1)
    return date

def cur_temp():
    file = open('/sys/class/thermal/thermal_zone0/temp')
    temp = float(file.read()) / 1000
    file.close()
    date = get_date()
    cont = '{}    cpu:{:.3f}*C'.format(date, temp)
    with open(r'/home/pi/service/log/temp.log', 'a') as f:
        f.write(cont + '\r\n')
    print(cont)

    # 如果温度高于50，微信预警
    if temp > 50:    
        sj = ServerJ(title='树莓派温度过高', cont=cont , token=r_conf('sj'), debug=False)
        sj.run()

if __name__ == "__main__":
    cur_temp()
