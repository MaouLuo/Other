import pandas as pd

path = 'E:\\可视化\\输出文档\\中文名\\N2S结算单位汇总.xlsx'
sheet_name = ['开通N2S结算单位', '订单相关结算单位', '账单相关结算单位']
name_list = [
    '贺琳',     
'王雪纯',    
'向阳',      
'杨小兰' ,   
'钟思敏'   , 
'邹方玲' ,   
'黎月明' ,   
'卢翠香' ,   
'舒乐'  ,    
'祝梦婷' ,   
'李镇粤' ,   
'欧阳婷'  ,  
'张波'   ,   
'张小东' ,   
'蔡浩权' ,   
'贺根强'   ,  
'梁健森' ,   
'刘城林' ,   
'曾浩炫',    
'梁诗婷',    
'刘泽民',    
'彭英剑' ,   
'章振坤' ,   
'郑瀚'  ,    
'helin', 
'wangxuechun', 
'xiangyang', 
'yangxiaolan', 
'zhongsimin', 
'zoufangling', 
'liyueming', 
'lucuixiang', 
'shule', 
'zhumengting', 
'lizhenyue',    
'ouyangting',    
'zhangbo',      
'zhangxiaodong' ,   
'caihaoquan',    
'hegenqiang',     
'liangjiansen',    
'liuchenglin' ,   
'zenghaoxuan',    
'liangshiting',    
'liuzemin',    
'pengyingjian',    
'zhangzhenkun',    
'zhenghan',  
]


def main():
    ordata = pd.read_excel(path, sheet_name=0, usecols=0)
    sales = []
    bm_sale = []

    for i in range(ordata.shape[0]): # shape获取（行x高）
        name = ordata.loc[i,'sales_name']
        sales.append(name)
        #print(data)
    bm_sale = [n for n in list(set(sales)) if n in name_list]
    print(bm_sale)



main()