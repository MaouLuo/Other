# -*- coding:utf-8 -*-
# https://oapi.dingtalk.com/robot/send?access_token=796719934a205fb55623f2887305dcbaf31414e661117eb28f4bd140597a27b7

import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json

timestamp = str(round(time.time() * 1000))
secret = 'SECd815f97f9b5f3ddf04eb6f85ab7bfd3f64cb992968d7a0690d511ba2bc6d3ba5'
secret_enc = secret.encode('utf-8')
string_to_sign = '{}\n{}'.format(timestamp, secret)
string_to_sign_enc = string_to_sign.encode('utf-8')
hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
#print(timestamp)
#print(sign)

url = 'https://oapi.dingtalk.com/robot/send?access_token=796719934a205fb55623f2887305dcbaf31414e661117eb28f4bd140597a27b7&timestamp={}&sign={}'.format(timestamp, sign)
headers = {
    'Content-Type': 'application/json',
    #'timestamp':timestamp,
    #'sign':sign,
    #'access_token':'796719934a205fb55623f2887305dcbaf31414e661117eb28f4bd140597a27b7'
}


def main():
    

    #url = tools.r_conf('wxwork', name='release')
    
    data = {
        "msgtype":"text",
        "text":{
            "content": "hh dsdd csesdada"#"吃饭时间到啦~\n当前天气{}，气温{}".format(wea['wtNm'], wea['wtTemp']),
            #"mentioned_list":["@all"]
            }
    }
    requests.post(url, headers=headers, data=json.dumps(data))

main()

