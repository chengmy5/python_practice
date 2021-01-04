# import requests
# import bs4
# import re
#
# res=requests.get("https://www.bilibili.com/")
# soup=bs4.BeautifulSoup(res.text,"html.parser")
# targets=soup.find_all('div',class_='video-card-reco')
# for each in targets:
#     print(each.div.a.img.alt)

import urllib.request
response = urllib.request.urlopen("http://txzb.miit.gov.cn/DispatchAction.do;jsessionid=EE12F55F7BCAEBA90D8F6B31142E81B5?efFormEname=POIX11")
html=response.read()
html=html.decode('UTF-8')
print(html)