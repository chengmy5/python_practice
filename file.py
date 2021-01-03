# f=open('E:/我司具有资质.txt', 'r', encoding='utf-8')
# content=f.read()
# qualification=content.split(',')
# print(qualification)
# f.close()
import os
# a=os.path.exists('E:file')
# b=os.path.exists('E:/bidding_information')
# os.makedirs('E:/bidding_information')
# print(a)
# print(b)

# from shutil import copy
#
# copy('E:/file/aa.txt','E:/file2')



# import requests
# import bs4
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
#
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#
# url='https://b2b.10086.cn/b2b/main/showBiao!showKaibiaoResult.html?ekp1APd1=5r4ygCLbjMRcG2jrQVDc_Z9gsfEszfyhsVf1ytXD15e5TsZfRs6V9UiFU1L8Xf79f55NxUyCaMd4TdebWNuGuQ1IL9bBkhWd48H87BrdBxKKuQ3LAnRU2uLFn0_1FzZaQ_Q2Z5X0oMiKGLPNH2hnNKdqThhqnIHlCDlkJUwNLKk.PvWpdgOTvLFNMkj593beUoRfoY8KuVrmOlbe5aLPsz5AP44VUZM92hlUXoWNCXIb981sp3WmRWQ7vjvKtnVuBJ2TzyFZnKwQ3ODxDknxE5vr0rvC2yibLl6aOG5HviZLjjb4oryZYcsn5.VUPDixJke7ySRjnjCbJ4lB8TDhnJdlJLUNrNK01Ea7IsjZ2cm7'
# data={}
# data['page.currentPage']='1'
# data['page.perPageSize']='20'
# data['noticeBean.companyName']=''
# data['noticeBean.title']=''
# data['noticeBean.startDate']='2020-12-01'
# data['noticeBean.endDate']='2021-01-02'
# res = requests.post(url,data,verify=False,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
#                                         'Cookie':'e01dcfc741ea014fb8=c08f0bdae7544ade9c4a3eb2a1f65840; saplb_*=(J2EE204290120)204290150; JSESSIONID=C4JaobR7R6oMSaktqddqIctcfS3BdgFmOC0M_SAP1TTcLgkNGtkASkg-T5gPsSgf; LS2cj8YxOIT5O=5zxbClB9UMBUvLNXJpy3sThzSUo6Kfp7SxTqPuhDUlH_mZDPUk9kxALIrU5JUfKqI2WZW_XDwLtMZ.IKGoFAPeA; LS2cj8YxOIT5P=5U5dv3mdB_aWqqqmCa1cW8q2ZN5FN9HzvDTOS2TlbL7IAcMCqU2XMbDntmD6T651jmRU7cw8elTBR2czBxbzYyI9mh18aTYIUedbc2oBs7uaW2vyIwj1gGPT3FK04zYP_e0rERhiJFTCt_ldtokkCTTiPev4NSz8xS8tVcaPpSZViS0WB.SviWLEbZW9dubiOG15Un5hXT_KyDtRiO_klOk2l.BwwYCACC147iaAGwHrry3.NRJV5lCktRIJouVCb8bfFujn8bU4b.f40eun78FcsetZLRXnm_WtfEBt.i.Y0N2L.QjFkZER7MTMqVSemW'})
# soup = bs4.BeautifulSoup(res.text, 'html.parser')
# print(res)



import openpyxl
import random

# print(str(random.uniform(0.32,0.3501))[:5])

# wb=openpyxl.load_workbook(r'E:\测试资料站点清单\ZTSJ_25测试资料.xlsx')
# ws=wb['Sheet1']
# name=ws['A']
# le=ws['B']
#
# a=[]
# b=[]
# for n in name:
#     a.append(n.value)
# for n in le:
#     b.append(n.value)
# a.pop(0)
# b.pop(0)
# print(a)
# print(b)


# wa=sheet_name['A2':'A10']
# for i in wa:
#     for j in i:
#
#         print(j.value)



import os
print(os.listdir('E:\测试资料站点清单'))
