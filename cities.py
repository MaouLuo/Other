# -*- coding: UTF-8 -*-

import os.path
import requests
import tools
import json
import time

def get_cities():
    province = []
    with open('./省会1.json', 'r', encoding='utf-8') as f:
        jd = json.load(f)
    for p in jd:
        province.append(p['name'])
    #print(province)


    cities = {}
    for p in province:
        cities[p] = []

    #print(cities)


    with open('./cities.json', 'r', encoding='utf-8') as f:
        jd = json.load(f)

    #bar = tools.Bar(len(jd['result']['datas']))
    i = 0
    for v in jd['result']['datas'].values():    
        if (v['area_1'] in province) and (v['area_2'] not in cities[v['area_1']]):
            i += 1
            cities[v['area_1']].append(v['area_2'])
        
    print(i)

    with open('地级行政区.json', 'w', encoding='utf-8') as f:
            json.dump(cities, f, ensure_ascii=False)

def set_group():
    num = 5
    maxnum = 100
    

