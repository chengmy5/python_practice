import time
import base64
import requests
import bs4
import os
import datetime

'''
公司资质列表，现改为存储在文档中，需要时读取
qualification=['通信与广电一级','机电一级','建筑一级','市政公用一级','机电二级','建筑二级','市政公用二级','通信工程施工总承包一级','建筑机电安装工程专业承包三级','电力工程施工总承包三级',
               '环保工程专业承包三级','施工劳务','市政公用工程施工总承包','建筑工程施工总承包','消防设施工程专业承包','电子与智能化工程专业承包','钢结构工程专业承包','城市及道路照明工程专业承包',
               '建筑装修装饰工程专业承包','地基基础工程专业承包','广东省有线广播电视台工程设计（安装）许可证','信息系统集成及服务资质证书','信息通信建设企业服务能力证书'	,
               '承装(修、试)电力设施许可证','广东省安全技术防范系统设计、施工、维修资格证']
               '''

def get_information(soup):
    targets=soup.find_all('td',class_='STYLE1')
    information_address=[]
    html=''
    for each in targets:
        html+=str(each.a)
    a = str(html).find('<a href')
    while a!=-1:
        b = str(html).find('\')', a, a + 255)
        if b!=-1:
            address=html[a + 61:b]
            address_arr=address.split('amp;')
            address=''.join(address_arr)
            information_address.append(address)
        else:
            b=a+60
        a = str(html).find('<a href',b)
    return information_address

def open_bidding(bidding_informations):
    # 读取公司资质文档
    f = open('我司具有资质.txt', 'r', encoding='utf-8')
    content = f.read()
    qualification = content.split(',')
    f.close()
    #判断是否存在文件夹，如不存在则创建文件夹，以便存储文档
    addr='E:/工信部招标公告/'
    if not os.path.exists(addr):
        os.makedirs(addr)
    JSESSIONID='&JSESSIONID=B401DCA5686E1354B8DA790B46550AD4'
    for each in bidding_informations:
        each+=JSESSIONID
        each=each.encode('utf-8')
        each = str(base64.b64encode(each), 'utf-8')

        url = 'http://txzb.miit.gov.cn/DispatchAction.do?_QUERY_STRING='+each
        res = requests.post(url, verify=False, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Cookie': 'JSESSIONID=B401DCA5686E1354B8DA790B46550AD4; _const_cas_from_=favicon.ico'})
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        content = str(soup.find_all('div', id='ggdiv2'))
        title = str(soup.find_all('td', class_='STYLE1'))[47:-6]

        has_qualification=[]
        count_qualification=0
        for item in qualification:
            if content.find(item)!=-1:
                has_qualification.append(item)
                count_qualification+=1

        if count_qualification>0:
            # txt=filterHtmlTag(soup)
            # txt=replaceCharEntity(soup)
            f = open(addr+title+'.html','w',encoding ='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
            f.write(str(soup))
            f.close()
            f = open(addr+ title + '_我司具有资质.txt', 'w', encoding='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
            f.write(str(has_qualification))
            f.close()

def find_bidding_information():
    # 先获得时间数组格式的日期
    sevenDayAgo = (datetime.datetime.now() - datetime.timedelta(days=7))
    # 转换为其他字符串格式
    starting_time = sevenDayAgo.strftime('%Y-%m-%d')#获取七天前的日期作为其实时间
    ending_time = time.strftime('%Y-%m-%d', time.localtime())#获取当前时间为终止时间
    date_arr = starting_time.split('-')
    date_arr[1] = str(int(date_arr[1]) - 1)
    date_arr[2] = '01'
    starting_time = '-'.join(date_arr)#获取当前时间的前一个月01号为起始时间

    url='http://txzb.miit.gov.cn/DispatchAction.do?reg=denglu&pagesize=1000'
    data={}
    data['inqu_status-0-name']=''#搜索标题
    data['inqu_status-0-date1']=starting_time#起始时间
    data['inqu_status-0-date2']=ending_time#结束时间
    data['inqu_status-0-bulletinType']='1'#公告类型（1：招标公告 2：变更公告 3：资格预审公告 4：招标终止公告）
    data['inqu_status-0-supervisorCode']=''#监管单位编号，对应监管单位
    data['inqu_status-0-supervisorName']=''#监管单位：xx市通信管理局
    data['inqu_status-0-bidType']=''#项目类型
    data['inqu_status-0-unitRestrict']=''#招标人分类：（1、移动:10 2、电信:11 3、联通:12 4、其他:13）
    data['efFormEname']='POIX14'
    data['methodName']='initLoad'
    # data=urllib.parse.urlencode(data).encode('utf-8')
    res = requests.post(url,data,verify=False,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
                                        'Cookie':'JSESSIONID=B401DCA5686E1354B8DA790B46550AD4; _const_cas_from_=favicon.ico'})
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    bidding_informations=get_information(soup)
    open_bidding(bidding_informations)
    # print(soup)

if __name__=='__main__':
    find_bidding_information()

