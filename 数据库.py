import pymysql
from pymysql import *
import openpyxl
conn=connect(host='localhost',user='root',password='123456',database='map',port=3306,charset='utf8')
cur=conn.cursor()
wb=openpyxl.load_workbook('C:/Users/ASUS i5/Documents/WeChat Files/wxid_d1v60j0t2bjr22/FileStorage/File/2021-01/网格26-4G(2)(1).xlsx')
ws=wb['网格26-4G']
i=1
for each in ws.rows:
    if i>1:
        a=each[0].value
        b=each[1].value
        c=each[2].value
        d=each[3].value
        e=each[4].value
        f=each[5].value
        sql='''
        insert into mapdata(latitude,longitude,communityName,communityId,RSRP,SINR) values ('{}','{}','{}','{}','{}','{}');
        '''.format(a, b, c, d, e, f)
        print(sql)
        cur.execute(sql)
        conn.commit()
    i+=1
cur.close()
conn.close()
# for each in ws.iter_rows(min_row=2,max_row=10000):
#     print("'"+each[2].value+"-"+str(i)+"':[",each[0].value,",",each[1].value,"],")
#     i += 1