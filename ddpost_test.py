# -*- coding:utf-8 -*-
# https://oapi.dingtalk.com/robot/send?access_token=796719934a205fb55623f2887305dcbaf31414e661117eb28f4bd140597a27b7
import tools
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json

class Dingding():
    def __init__(self, *path):
        if path:
            self.secret = tools.r_conf(item='dingding', path=path[0], name='secret')
            print(0)
        else:
            print(1)
            self.secret = tools.r_conf(item='dingding', name='secret')
        
        self.headers = {
            'Content-Type': 'application/json',
        }

    def get_url(self):
        timestamp = str(round(time.time() * 1000))
        self.secret = 'SECd815f97f9b5f3ddf04eb6f85ab7bfd3f64cb992968d7a0690d511ba2bc6d3ba5'
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        url = 'https://oapi.dingtalk.com/robot/send?access_token=796719934a205fb55623f2887305dcbaf31414e661117eb28f4bd140597a27b7&timestamp={}&sign={}'.format(timestamp, sign)
        #print(timestamp)
        #print(sign)
        return url

    def send_text(self, cont):
        data = {
            "msgtype":"text",
            "text":{
                "content": cont#"吃饭时间到啦~\n当前天气{}，气温{}".format(wea['wtNm'], wea['wtTemp']),
                #"mentioned_list":["@all"]
                }
        }
        requests.post(self.get_url(), headers=self.headers, data=json.dumps(data))



def main():
    dd_msg = Dingding()
    dd_msg.send_text('ni hao ya')
 
    

main()

