import time
import base64
import requests
import bs4
import os
import datetime
'''
广东省机电设备招标中心
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
    :return: 招标公告地址列表、公告标题列表
    '''
    targets=soup.find_all('div',class_='border-dashed')
    information_address=[]#存放所有招标公告地址的列表
    titles = []  # 存放所有招标公告标题的列表
    html=''
    for each in targets:
        # 遍历页面中所有包含招标公告标题的标签
        html+=str(each.a)#将这些标签存到一个字符串中
    a = html.find('<a href')#在字符串中找到所有a标签
    while a!=-1:
        #遍历所有a标签
        b = html.find('"', a+12, a + 255)
        if b!=-1:
            address='https://www.gdebidding.com'+html[a + 9:b]#获取招标公告所在地址
            information_address.append(address)#将所有地址存到一个列表中
            title=html[html.find('title',a)+7:html.find('"',a+60)]#获取招标公告title
            titles.append(title)#将所有招标公告title存到一个列表中
        else:
            b=a+60
        a = str(html).find('<a href',b)
    return information_address,titles


def open_bidding(bidding_informations,titles):
    qualification=get_qualification()# 获取公司资质文档
    #判断是否存在文件夹，如不存在则创建文件夹，以便存储文档
    addr='E:/广东省机电设备招标公告/'
    if not os.path.exists(addr):
        os.makedirs(addr)

    for each in bidding_informations:
        url = each  #拼接请求地址
        #添加请求头
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Cookie': 'JSESSIONID=B401DCA5686E1354B8DA790B46550AD4; _const_cas_from_=favicon.ico'}
        #发起请求
        res = requests.get(url, verify=False, headers=headers)
        #接收返回页面
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        #获取投标人资格要求部分
        content = str(soup)
        #获取当前招标公告标题
        title = titles[bidding_informations.index(each)]
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
            top=content[content.find('<div id="menu">'):content.find('</div>',content.find('<div id="manu">'))]
            content=content.replace(top,'')
            f.write(content)
            f.close()
            f = open(addr+ title + '_我司具有资质.txt', 'w', encoding='utf-8')
            f.write(str(has_qualification))
            f.close()

def find_bidding_information():
    #请求地址
    url='https://www.gdebidding.com/zbxxgg/index.jhtml'
    #请求头
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
             'Cookie':'clientlanguage=zh_CN'}
    #发起请求
    res = requests.get(url,verify=False,headers=headers)
    #接收相应页面
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    # 在页面中查找各个招标公告
    bidding_informations=get_information(soup)
    #打开招标公告并判断是否符合公司具有资质
    open_bidding(bidding_informations[0],bidding_informations[1])
    #获取招标公告最大页数
    maxPage=soup.find('select',onchange="if(this.value==1){location='index.jhtml'}else{location='index_'+this.value+'.jhtml'}this.disabled='disabled'").find_all('option')[-1]['value']
    page=2
    while page<=int(maxPage):  #遍历所有页，从第2页开始
        # 请求地址  page 第几页
        url = 'https://www.gdebidding.com/zbxxgg/index_'+str(page)+'.jhtml'
        # 请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
            'Cookie': 'clientlanguage=zh_CN'}
        # 发起请求
        res = requests.get(url, verify=False, headers=headers)
        # 接收相应页面
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        # 在页面中查找各个招标公告
        bidding_informations=get_information(soup)
        #打开招标公告并判断是否符合公司具有资质
        open_bidding(bidding_informations[0],bidding_informations[1])
        page+=1

if __name__=='__main__':
    find_bidding_information()
