import tushare as ts


token = '305399e563d2a2ae6b48efe5ec38eeeea11599aca8c7d77816a2baa1'
# ts.set_token('305399e563d2a2ae6b48efe5ec38eeeea11599aca8c7d77816a2baa1')
pro = ts.pro_api(token)

# df = pro.query('trade_cal', exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
# print(df)

data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
print(data)