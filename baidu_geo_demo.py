import requests
import json
import math

# t12

ak = 'HztsFGGG6FQAFP25kHT4gvgxNr4NkzHy'  # 服务端AK
# ak = 'vpEIKTctv6SCde3awTWXWWQuNp2g7oap'  # 浏览器端AK 


# 获取单点经纬
def geo_to_coordinate(address):
    fault_code = {1:'服务器内部错误',
                    2: '参数无效'}
    url = 'http://api.map.baidu.com/geocoder/v2/'
    params = { 'address' : address,           
                'ak' : ak,          
                'output': 'json'     }          # 输出结果设置为json格式
    res = requests.get(url,params)
    res.text
    jd = json.loads(res.text)                   # 将json格式转化为Python字典
    if jd['status'] != 0:
        try:
            content = [0, 0, fault_code[jd['status']]]
        except Exception as e:
            content = [0, 0, ('fault code:%d' %(jd['status']))]
    else:
        lng = round(jd['result']['location']['lng'], 6)
        lat = round(jd['result']['location']['lat'], 6)
        a = [lng, lat] 
        coor_str = str(lat) + ',' + str(lng)
        # 返回一个列表，6位float型纬度，6位float型经度度，str型经纬度（可直接用于地理编码参数）
        content = [lat, lng, coor_str]                 
    return content


# 经纬度获取地名
def coordinate_to_geo(coor):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    params = { 'location' : coor, #'35.658651,139.745415', #'26.080429,119.303470', # '35.658651,139.745415',           
                'ak' : ak,          
                'output': 'json',
                'latest_admin': 1,
                'language': 'zh-CN',
                'language_auto': 0     }         
    res = requests.get(url, params)
    res.text
    jd = json.loads(res.text)   
    if jd['status'] != 0:
        content = ('fault code:%d' %(jd['status']))
    elif jd['result']['formatted_address'] != '':        
        content =  jd['result']['formatted_address']
    else:
        content =  '查不到该地点'
    return content

# 通过经纬计算两点距离
def driving(address1, address2):
    fault_code = {1:'服务器内部错误',
                    2: '参数无效',
                    7: '无返回结果'}
    origin = geo_to_coordinate(address1)[2]
    destination = geo_to_coordinate(address2)[2]    
    url = 'http://api.map.baidu.com/directionlite/v1/driving'
    params = { 'origin' : origin,
               'destination' : destination,
               'ak' : ak,          
               }          
    res = requests.get(url, params)

    #完整访问URL
    #url = 'http://api.map.baidu.com/directionlite/v1/driving?origin=22.54845,114.06455&destination=32.99989,118.42930&ak=HztsFGGG6FQAFP25kHT4gvgxNr4NkzHy'
    #res = requests.get(url)    
    res.text
    jd = json.loads(res.text)
    # print(jd)
    if jd['status'] != 0:
        try:
            content = fault_code[jd['status']]
        except Exception as e:
            content = jd['message']
    else:
        content = float(jd['result']['routes'][0]['distance'] / 1000)
    return content
                
# 匹配场站
def station_match(origin):
    # 一级场站
    main_station = {'成都':'30.655822,104.081534', '武汉':'30.598467,114.311582', '厦门':'24.485407,118.096435'}
    main_city = ['成都', '武汉', '厦门']

    #  二级场站
    secondary_station = {'大朗':'22.912349,113.948207','杨浦':'31.265524,121.53252','胶州':'36.270349,120.039535'}
    secondary_city = ['大朗', '杨浦', '胶州']

    matching = False
    for city in main_city:
        dis = driving(origin, main_station[city])
        if dis <= 50:
            print('站到匹配站点：%s, 距离为：%d KM' %(city, dis))
            matching = True
            return
    if matching is not True:
        shortest_dis = 10000
        shortest_city = ''
        for city in secondary_city:
            dis = driving(origin, secondary_station[city])
            if shortest_dis > dis :
                shortest_dis = dis
                shortest_city = city
        print('最近站点：%s，距离为：%d KM' %(shortest_city, shortest_dis))
        return

def ip_to_geo(ip):
    fault_code = {1:'服务器内部错误'}
    url = 'http://api.map.baidu.com/location/ip'
    params = { 'ip' : ip,
               'ak' : ak, }          
    res = requests.get(url, params)
    res.text
    jd = json.loads(res.text)
    # print(jd)
    if jd['status'] != 0:
        try:
            content = fault_code[jd['status']]
        except Exception as e:
            content = ('fault code:%d' %(jd['status']))
    else:
        content = jd['address']
    return content


def main():

    while True:
        print('1、获取单点经纬度；2、计算两点行驶距离；3、输经纬返回地名；4、IP查地址：', end = '')
        case = input()
        if case == '1':
            print('输入查询地：', end = '')
            address = input()
            content = geo_to_coordinate(address)
            if content[0] is not 0 and content[1] is not 0:
                print('纬度：%f, 经度：%f' %(content[0], content[1]))
            else:
                print(content[2])
        elif case == '2':
            print('输入起始地：', end = '')
            address1 = input()
            print('输入目的地：', end = '')
            address2 = input()
            content = driving(address1, address2)
            if type(content) is str:
                print(content)
            else:
                print('%s KM'%(content))
        elif case == '3':
            print('请以 “纬度，经度” 格式输入：', end = '')
            coor = input()
            print(coordinate_to_geo(coor))
        elif case is '4':
            print('IP：', end = '')
            ip = input()
            print(ip_to_geo(ip))
        else:
            print('please input correct number!')
        print('---------------------------------------------------------')

        
        #station_match(origin_coordinate)
        
    

if __name__ == '__main__':
    main()

