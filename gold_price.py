# -*- coding:utf-8 -*-

import requests
import json
import tools

local_path = 'D:\\code\\config.ini'
url = 'http://api.k780.com'
data = {
  'app' : 'finance.gold_price',
  'goldid' : '1053',
  'appkey' : tools.r_conf('nowapi', path=local_path, name='appkey'),
  'sign' : tools.r_conf('nowapi', path=local_path, name='sign'),
  'format' : 'json'
}

resp = requests.post(url, data=data)
a_result = json.loads(resp.text)

if a_result:
  if a_result['success'] != '0':      
    #print (a_result['result'])
    pass
  else:
    print (a_result['msgid']+' '+a_result['msg'])
else:
  print ('Request nowapi fail.')

last_price = a_result['result']['dtList']['1053']['last_price']
if float(last_price) < 400 :
    sj = tools.ServerJ('金价'+last_price, '', tools.r_conf('sj', path=local_path, name='token'), debug=True)
    sj.run()