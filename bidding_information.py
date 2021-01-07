import time
import base64
import requests
import bs4
import os
import datetime
'''
工信部
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
    targets=soup.find_all('td',class_='STYLE1')
    information_address=[]#存放所有招标公告地址的列表
    html=''
    for each in targets:
        # 遍历页面中所有包含招标公告标题的标签
        html+=str(each.a)#将这些标签存到一个字符串中
    a = str(html).find('<a href')#在字符串中找到所有a标签
    while a!=-1:
        #遍历所有a标签
        b = str(html).find('\')', a, a + 255)
        if b!=-1:
            address=html[a + 61:b]#获取招标公告所在地址
            address_arr=address.split('amp;')#去除地址中多余部分
            address=''.join(address_arr)#将地址重新拼接
            information_address.append(address)#将所有地址存到一个列表中
        else:
            b=a+60
        a = str(html).find('<a href',b)
    return information_address


def open_bidding(bidding_informations):
    qualification=get_qualification()# 获取公司资质文档
    #判断是否存在文件夹，如不存在则创建文件夹，以便存储文档
    addr='E:/工信部招标公告/'
    if not os.path.exists(addr):
        os.makedirs(addr)

    JSESSIONID='&JSESSIONID=B401DCA5686E1354B8DA790B46550AD4'#招标公告请求地址中的参数
    for each in bidding_informations:
        each+=JSESSIONID
        each=each.encode('utf-8')
        each = str(base64.b64encode(each), 'utf-8')#将地址参数进行utf-8编码

        url = 'http://txzb.miit.gov.cn/DispatchAction.do?_QUERY_STRING='+each  #拼接请求地址
        #添加请求头
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Cookie': 'JSESSIONID=B401DCA5686E1354B8DA790B46550AD4; _const_cas_from_=favicon.ico'}
        #发起请求
        res = requests.post(url, verify=False, headers=headers)
        #接收返回页面
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        #获取投标人资格要求部分
        content = str(soup.find_all('div', id='ggdiv2'))
        #获取当前招标公告标题
        title = str(soup.find_all('td', class_='STYLE1'))[47:-6]
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
    url='http://txzb.miit.gov.cn/DispatchAction.do?reg=denglu&pagesize=1000'
    #请求参数
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
    #请求头
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
             'Cookie':'JSESSIONID=B401DCA5686E1354B8DA790B46550AD4; _const_cas_from_=favicon.ico'}
    #发起请求
    res = requests.post(url,data,verify=False,headers=headers)
    #接收相应页面
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    #在页面中查找各个招标公告
    bidding_informations=get_information(soup)
    #打开招标公告并判断是否符合公司具有资质
    open_bidding(bidding_informations)

if __name__=='__main__':
    find_bidding_information()
