# -*- coding:utf-8 -*-

import requests
import json
import sqlite3
import tools
import pandas as pd
from time import *

debug_path = 'D:\\code\\chaos\\weather.db'
#release_path = 'D:\\code\\api_demo\\tushare\\stock.db'
path = debug_path

with open('./地级行政区.json', encoding='utf-8') as f:
    city_jd = json.load(f)

p1 = ['北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江', '安徽', '福建']
p2 = ['山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川']
p3 = ['云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆', '台湾', '澳门', '香港']


class wea_db():    
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('create table cal (exc varchar(10) date varchar(10), open varchar(10))')        

    def commit(self):
        # 关闭Cursor:
        self.cursor.close()
        # 提交事务:
        self.conn.commit()
        # 关闭Connection:
        self.conn.close()

    def insert_data(self, table_name, data): # df['cal_date'].values, df['is_open'].values        
        #for d in date:
        #    self.cursor.execute('insert into cal (date, open) values (\'{}\', \'{}\')'.format(d, open))
        data.to_sql(table_name, con=self.conn, if_exists='append', index=False) # 复制dataframe数据入数据库， if_exists='append'为添加数据模式 

    def duplicate_data(self, table_name, filed_name): # 查询重复数据，cal为表名,cal_date为字段名
        self.cursor.execute("select * from {} group by {} having count(*)>1".format(table_name, filed_name))
        res = self.cursor.fetchall()
        print(res)
        
    def del_duplicate(self, table_name, filed_name): # 删除重复数据       
        self.cursor.execute("delete from {} where {}.rowid not in (select MAX({}.rowid) from {} group by {});".format(table_name, table_name, table_name, table_name, filed_name))
        #res = self.cursor.fetchall()
        #print(res)

# 传入城市名，返回当日天气情况列表
def today_wea(weaid, conf_item):
    url = 'http://api.k780.com'
    data = {
        'weaid': weaid,
        'app': 'weather.today',
        'appkey': tools.r_conf(item=conf_item, name='appkey'),
        'sign': tools.r_conf(item=conf_item, name='sign'),
        #'appkey': '10003',
        #'sign': 'b59bc3ef6191eb9f747dd4e83c99f2a4',        
        'format': 'json'
    }
    resp = requests.post(url, data=data)    
    jd = json.loads(resp.text)
    #print(jd)
    return {'city':jd['result']['citynm'], 'date':jd['result']['days'], 'weather':jd['result']['weather'], 'htemp':jd['result']['temp_high'], 'ltemp':jd['result']['temp_low'], 'pm':jd['result']['aqi'], 'wind':jd['result']['wind'], 'winp':jd['result']['winp'], 'hhumi':jd['result']['humi_high'], 'lhumi':jd['result']['humi_low']}     

# 传入省份列表，返回全部需要获取的城市数据
def get_cities(province):    
    cities = []
    for p in province:
        cities.extend(city_jd[p])
    return cities

def run():
    wea1 = []
    wea2 = []
    wea3 = []
    cities1 = get_cities(p1)
    cities2 = get_cities(p2)
    cities3 = get_cities(p3)
    w = wea_db(path)

    try:
        for c in cities1:
            wea1.append(today_wea(c, 'nowapi'))   
        w.insert_data('wea', pd.DataFrame(wea1))
        
        for c in cities2:
            wea2.append(today_wea(c, 'nowapi2'))  
        w.insert_data('wea', pd.DataFrame(wea2))
        
        for c in cities3:
            wea2.append(today_wea(c, 'nowapi3'))  
        w.insert_data('wea', pd.DataFrame(wea3))
    except Exception as e:
        print('err {}'.format(e))
    finally:
        w.commit()
    
if __name__ == "__main__":
    run()