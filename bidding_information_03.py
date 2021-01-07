import time
import base64
import requests
import bs4
import os
import datetime
'''
中国电信-阳光采购网外部门户
'''
def get_qualification():
    '''
    读取公司资质文档
    :return: 公司所有资质的列表
    '''
    f = open('我司具有资质.txt', 'r', encoding='utf-8')
    content = f.read()
    qualification = content.split(',')
    f.close()
    return qualification

def get_information(soup):
    '''
    从页面中获取并整理出所有招标公告的地址
    :param soup: 要查找的页面
    :return: 招标公告地址列表
    '''
    targets=soup.find('table',class_='table_data').find_all('tr')
    information_address=[]#存放所有招标公告地址的列表
    titles=[]
    html=''
    for each in targets:
        # 遍历页面中所有包含招标公告标题的标签
        html+=str(each.a)#将这些标签存到一个字符串中
    a = html.find('<a href')#在字符串中找到所有a标签
    while a!=-1:
        #遍历所有a标签
        b = str(html).find('>', a, a + 255)
        if b!=-1:
            id=html[a + 27:html.find('\'',a+27)]#获取招标公告id
            encryCode=html[b-35:b-3]#获取招标公告encryCode
            title=html[html.find('>',a)+1:html.find('<',b+1)]#获取招标公告title
            titles.append(title)
            address='https://caigou.chinatelecom.com.cn/MSS-PORTAL/tenderannouncement/viewHome.do?encryCode='+encryCode+'&id='+id
            information_address.append(address)#将所有地址存到一个列表中
        else:
            b=a+60
        a = str(html).find('<a href',b)
    return information_address,titles


def open_bidding(bidding_informations,titles):
    qualification=get_qualification()# 获取公司资质文档
    #判断是否存在文件夹，如不存在则创建文件夹，以便存储文档
    addr='E:/中国电信-阳光采购网外部门户招标公告/'
    if not os.path.exists(addr):
        os.makedirs(addr)

    for each in bidding_informations:
        url = each  #拼接请求地址
        #添加请求头
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                 'Cookie':'name=value; JSESSIONID=0000vh8DlP73tkX4eqxUIgdBfLc:18djc0hbi; CaiGouServiceInfo=!UeKxfQXs2xckSd6U9I+YAUGJNqjObN2UWqGq5KyNRwNLC2NrGbYQfnzPfjeqkru0yaCZ0CSWUgas7pc='}
        #发起请求
        res = requests.post(url, verify=False, headers=headers)
        #接收返回页面
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        html=soup.text
        #获取投标人资格要求部分
        content=html[html.find('投标人资格要求'):html.find('招标文件的获取')]
        #获取当前招标公告标题
        title=titles[bidding_informations.index(each)]
        #当前招标公告中我司具有的资质列表
        has_qualification=[]
        for item in qualification:
            #遍历从文档中读取的我司资质列表
            if content.find(item)!=-1:
                #如果在投标人资格要求中找到我司具有的资质，则添加进当前招标公告中我司具有的资质列表
                has_qualification.append(item)

        if len(has_qualification)>0:
            #如果当前招标公告中我司具有的资质列表长度大于0，则将此招标公告以html形式保存，并将当前招标公告中我司具有的资质列表以txt形式保存
            f = open(addr+title+'.html','w',encoding ='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
            f.write(str(soup))
            f.close()
            f = open(addr+ title + '_我司具有资质.txt', 'w', encoding='utf-8')
            f.write(str(has_qualification))
            f.close()

def find_bidding_information():
    # 先获得时间数组格式的日期
    sevenDayAgo = (datetime.datetime.now() - datetime.timedelta(days=7))
    # 转换为其他字符串格式
    starting_time = sevenDayAgo.strftime('%Y-%m-%d')#获取七天前的日期作为起始时间
    ending_time = time.strftime('%Y-%m-%d', time.localtime())#获取当前时间为终止时间

    #请求地址  pagesize=每页展示条数
    url='https://caigou.chinatelecom.com.cn/MSS-PORTAL/announcementjoin/list.do?provinceJT=NJT'
    #请求参数
    data={}
    data['provinceJT']='NJT'#
    data['docTitle']=''#公告名称
    data['docCode']=''#公告编码
    data['provinceCode']=''#省份编码
    data['provinceNames']=''#省份名称
    data['startDate']=''#创建开始日期
    data['endDate']=''#创建结束日期
    data['docType']='TenderAnnouncement'#公告类型   招标公告
    data['paging.start']='1'#起始位置
    data['paging.pageSize']='100'#每页条数
    data['pageNum']='100'#每页条数
    #请求头
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
             'Cookie':'name=value; JSESSIONID=0000vh8DlP73tkX4eqxUIgdBfLc:18djc0hbi; CaiGouServiceInfo=!UeKxfQXs2xckSd6U9I+YAUGJNqjObN2UWqGq5KyNRwNLC2NrGbYQfnzPfjeqkru0yaCZ0CSWUgas7pc='}
    #发起请求
    res = requests.post(url,data,verify=False,headers=headers)
    #接收相应页面
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    #在页面中查找各个招标公告
    bidding_informations=get_information(soup)
    # for each in bidding_informations:
    #     print(each)
    #打开招标公告并判断是否符合公司具有资质
    open_bidding(bidding_informations[0],bidding_informations[1])

if __name__=='__main__':
    find_bidding_information()
