# -*- coding: UTF-8 -*-

import os.path
import requests
import tools
import json
import time

today = tools.get_date('%Y%m%d')
temp_path = './{}.json'.format(today)

if os.path.isfile(temp_path):
    with open(temp_path, 'r', encoding='utf-8') as f:
        jd = json.load(f)
    for s in jd:
        print('province:{} temp:{}'.format(s[0], s[2]))
else:
    with open('./省会1.json', 'r', encoding='utf-8') as f:
        jd = json.load(f)
    cities = []        
    for c in jd:
        cities.append([c['name'], c['city'][0]['name']])
    for i in range(0,len(cities)):
        cities[i].append(int(i))
    with open(temp_path, 'w', encoding='utf-8') as f:
        json.dump(cities, f, ensure_ascii=False)

    #print('{} {}'.format(i['name'], i['city'][0]['name']))
#print(len(cities))


    
#print(cities)
