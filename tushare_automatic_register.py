import requests
from bs4 import BeautifulSoup

html = 'http://tushare.pro/captcha?action=register'
login_html = 'https://tushare.pro/login'


'''
resp = requests.post(html, timeout=5)
print(resp)
'''

resp = requests.get(html, timeout=5)
print(resp.html)

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',

}

data = {
    'account': '285933134@qq.com',
    'password': 'lz_910521',
    'captcha': 'apxw'
}