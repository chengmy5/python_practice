import time
import base64
import requests
import bs4
import os
import datetime
from selenium import webdriver
import json
import openpyxl
requests.packages.urllib3.disable_warnings()#关闭安全警告

dir='E:/招标公告/'#文件存储位置
#创建excel文件，用于保存招标公告信息
wb=openpyxl.Workbook()
ws=wb.active
ws.append(['序号','招标网站','项目名称','招标单位','项目概况','报名截止时间','资质要求','招标范围'])
wb.save(dir+'每日招标信息'+time.strftime('%Y%m%d',time.localtime())+'.xlsx')

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

def update_title(title):
    title = title.replace('/', '-')  # 去除标题中的/，避免创建文件时报错
    title = title.replace(' ', '')  # 去除标题中的空格，避免创建文件时报错
    title = title.replace('	', '')  # 去除标题中的/t，避免创建文件时报错
    return title

class GongXinBu:
    '''
    工信部
    '''
    @staticmethod
    def get_information(soup):
        '''
        从页面中获取并整理出所有招标公告的地址
        :param soup: 要查找的页面
        :return: 招标公告地址列表，公告标题
        '''
        targets=soup.find_all('td',class_='STYLE1')
        information_address=[]#存放所有招标公告地址的列表
        titles = []  # 存放所有招标公告标题的列表
        html=''
        for each in targets:
            # 遍历页面中所有包含招标公告标题的标签
            html+=str(each.a)#将这些标签存到一个字符串中
        a = html.find('<a href')#在字符串中找到所有a标签
        while a!=-1:
            #遍历所有a标签
            b = html.find('\')', a, a + 255)
            if b!=-1:
                address=html[a + 61:b]#获取招标公告所在地址
                address_arr=address.split('amp;')#去除地址中多余部分
                address=''.join(address_arr)#将地址重新拼接
                information_address.append(address)#将所有地址存到一个列表中
                title=html[html.find('>',a)+1:html.find('<',a+1)-14]
                titles.append(title)
            else:
                b=a+60
            a = str(html).find('<a href',b)
        return information_address,titles

    @staticmethod
    def information(soup,serialNum,webName,title,has_qualification):
        qualification=''
        for each in has_qualification:
            qualification+=each+','
        # 招标单位
        bidUnit = ''
        #项目概况
        projectOverview=''
        #报名截止时间
        endTime=''
        #招标范围
        bidScope=''
        #存放公告信息的列表
        information=[]
        information.append(serialNum)
        information.append(webName)
        information.append(title)
        # 获取招标人/招标代理机构
        a = soup.find('span', style='font-size:16px;float:right; clear:both;')
        if a == None:
            a = soup.find('span', style='font-size: 16px;float:right; clear:both;')
        if a != None:
            bidUnit = a.text.split('：')[1]
        information.append(bidUnit)
        # 获取项目概况
        b = soup.text.find('标段划分')
        if b==-1:
            b = soup.text.find('标包划分')
        if b==-1:
            b = soup.text.find('本项目划分')
        if b==-1:
            b = soup.text.find('不划分标包')
        if b == -1:
            b = soup.text.find('不划分标段')
        c=soup.text.find('。', b, b + 60)
        if c==-1:
            c = soup.text.find('，', b, b + 60)
        if c==-1:
            c = soup.text.find(' ', b, b + 60)
        if b!=-1:
            projectOverview=soup.text[b:c]
        information.append(projectOverview)
        #获取报名截止时间
        d=soup.text.find('投标截止时间为')
        e=soup.text.find('。',d)
        if d!=-1:
            d=soup.text.find('2',d,d+15)
            endTime=soup.text[d:e]
        information.append(endTime)
        information.append(qualification)
        #获取招标范围
        f=soup.text.find('招标内容:')
        if f==-1:
            f = soup.text.find('招标内容：')
        if f==-1:
            f = soup.text.find('招标范围:')
        if f==-1:
            f = soup.text.find('招标范围：')
        if f==-1:
            f = soup.text.find('采购内容:')
        if f==-1:
            f = soup.text.find('采购内容：')
        if f==-1:
            f = soup.text.find('项目主要内容：')
        if f==-1:
            f = soup.text.find('建设内容：')
        if f==-1:
            f = soup.text.find('招标规模及内容：')
        if f==-1:
            f = soup.text.find('项目概况：')
        g=soup.text.find('。',f,f+255)
        if f!=-1:
            bidScope=soup.text[f:g]
        information.append(bidScope)
        return information
    @staticmethod
    def open_bidding(bidding_informations,titles):
        qualification=get_qualification()# 获取公司资质文档
        #判断是否存在文件夹，如不存在则创建文件夹，以便存储文档
        addr=dir+'工信部招标公告/'
        if not os.path.exists(addr):
            os.makedirs(addr)
        #打开excel表，准备进行数据写入
        wb=openpyxl.open(dir+'每日招标信息'+time.strftime('%Y%m%d',time.localtime())+'.xlsx')
        ws=wb.active
        # 序号，从1开始
        serialNum = 1
        #网站
        webName='工信部'
        JSESSIONID='&JSESSIONID=B401DCA5686E1354B8DA790B46550AD4'#招标公告请求地址中的参数
        for each in bidding_informations:
            # 获取当前招标公告标题
            title = titles[bidding_informations.index(each)]
            title = update_title(title)
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
            #当前招标公告中我司具有的资质列表
            has_qualification=[]
            for item in qualification:
                #遍历从文档中读取的我司资质列表
                if content.find(item)!=-1:
                    #如果在投标人资格要求中找到我司具有的资质，则添加进当前招标公告中我司具有的资质列表
                    has_qualification.append(item)

            if len(has_qualification)>0:
                #如果当前招标公告中我司具有的资质列表长度大于0，则将此招标公告以html形式保存，并将当前招标公告中我司具有的资质列表以txt形式保存
                # f = open(addr+title+'.html','w',encoding ='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
                # f.write(str(soup))
                # f.close()
                information=GongXinBu.information(soup,serialNum,webName,title,has_qualification)
                ws.append(information)
                serialNum+=1
                # f = open(addr+ title + '_我司具有资质.txt', 'w', encoding='utf-8')
                # f.write(str(has_qualification))
                # f.close()
        #保存excel文档
        wb.save(dir+'每日招标信息'+time.strftime('%Y%m%d',time.localtime())+'.xlsx')

    def find_bidding_information(self):
        # 先获得时间数组格式的日期
        sevenDayAgo = (datetime.datetime.now() - datetime.timedelta(days=30))
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
        bidding_informations=GongXinBu.get_information(soup)
        #打开招标公告并判断是否符合公司具有资质
        GongXinBu.open_bidding(bidding_informations[0],bidding_informations[1])

class ZhongGuoTieTa:
    '''
    中国铁塔在线商务平台
    '''
    def get_biddinglist(self):
        url = "http://www.tower.com.cn/default/main/index/cn.chinatowercom.obp.main.index.obphomepage.queryNoticeDetails.biz.ext"  # 网站地址
        payload = {}  # 请求参数
        payload['cityInput'] = ''  # 城市
        payload['effectTime'] = '2020-12-01 00:00:00'  # 发布时间
        payload['failureTime'] = '2021-01-07 00:00:00'  # 有效截止日期
        payload['level'] = ''
        payload['noticeTitle'] = ''
        payload['page'] = {'begin': 0, 'length': 2000}
        payload['pageIndex'] = 0
        payload['pageSize'] = 2000  # 每页最大展示条数
        payload['provinceInput'] = ''
        payload['purchaseNoticeType'] = '2'
        payload['resultsNoticeType'] = '2'
        payload['sortField'] = ''
        payload['sortOrder'] = ''
        # 请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Referer': 'http://www.tower.com.cn/default/main/index/noticedetail.jsp?_operation=notice&_purchaseNoticeType=2&_resultsNoticeType=2',
            'content-type': 'application/json'}
        res = requests.post(url, data=json.dumps(payload), verify=False, headers=headers)  # 发起请求
        ids = []  # 存放所有招标公告id的列表
        a = res.text.find('id')
        while a != -1:
            a = res.text.find('id', a + 1)
            ids.append(res.text[a + 5:a + 37])
        ZhongGuoTieTa.bidding_detail(ids)

    @staticmethod
    def bidding_detail(ids):
        qualification = get_qualification()  # 获取公司资质文档
        # 判断是否存在文件夹，如不存在则创建文件夹，以便存储文档
        addr = dir+'中国铁塔在线商务平台招标公告/'
        if not os.path.exists(addr):
            os.makedirs(addr)
        driver_path = r'D:\driver\chromedriver.exe'
        driver = webdriver.Chrome(executable_path=driver_path)
        for each in ids:
            # 根据id遍历所有招标公告页面
            url = "http://www.tower.com.cn/default/main/index/noticedetail.jsp?_operation=notice&_notice=6&_id=" + each
            driver.get(url)
            html = driver.page_source
            # 获取当前招标公告标题
            t = html.find('<div class="content_title" id="_title">')
            title = html[t + 39:html.find('</div>', t)]
            title = update_title(title)
            # 获取投标人资格要求部分
            content = html[html.find('投标人资格要求'):html.find('资格审查方法')]
            # 当前招标公告中我司具有的资质列表
            has_qualification = []
            for item in qualification:
                # 遍历从文档中读取的我司资质列表
                if content.find(item) != -1:
                    # 如果在投标人资格要求中找到我司具有的资质，则添加进当前招标公告中我司具有的资质列表
                    has_qualification.append(item)
            if len(has_qualification) > 0:
                # 如果当前招标公告中我司具有的资质列表长度大于0，则将此招标公告以html形式保存，并将当前招标公告中我司具有的资质列表以txt形式保存
                f = open(addr + title + '.html', 'w', encoding='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
                top0 = html.find('<div class="header-main">')
                top = html[top0:html.find('</div>', top0 + 4500)]
                html = html.replace(top, '')
                foot0 = html.find('<div class="new_footer"')
                foot = html[foot0:html.find('</div>', foot0 + 440)]
                html = html.replace(foot, '')
                f.write(str(html))
                f.close()
                f = open(addr + title + '_我司具有资质.txt', 'w', encoding='utf-8')
                f.write(str(has_qualification))
                f.close()
            time.sleep(2)
        driver.quit()

class ZhongGuoDianXin:
    '''
    中国电信-阳光采购网外部门户
    '''
    @staticmethod
    def get_information(soup):
        '''
        从页面中获取并整理出所有招标公告的地址
        :param soup: 要查找的页面
        :return: 招标公告地址列表、公告标题列表
        '''
        targets = soup.find('table', class_='table_data').find_all('tr')
        information_address = []  # 存放所有招标公告地址的列表
        titles = []  # 存放所有招标公告标题的列表
        html = ''
        for each in targets:
            # 遍历页面中所有包含招标公告标题的标签
            html += str(each.a)  # 将这些标签存到一个字符串中
        a = html.find('<a href')  # 在字符串中找到所有a标签
        while a != -1:
            # 遍历所有a标签
            b = str(html).find('>', a, a + 255)
            if b != -1:
                id = html[a + 27:html.find('\'', a + 27)]  # 获取招标公告id
                encryCode = html[b - 35:b - 3]  # 获取招标公告encryCode
                title = html[html.find('>', a) + 1:html.find('<', b + 1)]  # 获取招标公告title
                titles.append(title)
                address = 'https://caigou.chinatelecom.com.cn/MSS-PORTAL/tenderannouncement/viewHome.do?encryCode=' + encryCode + '&id=' + id
                information_address.append(address)  # 将所有地址存到一个列表中
            else:
                b = a + 60
            a = str(html).find('<a href', b)
        return information_address, titles

    @staticmethod
    def open_bidding(bidding_informations, titles):
        qualification = get_qualification()  # 获取公司资质文档
        # 判断是否存在文件夹，如不存在则创建文件夹，以便存储文档
        addr = dir+'中国电信-阳光采购网外部门户招标公告/'
        if not os.path.exists(addr):
            os.makedirs(addr)

        for each in bidding_informations:
            url = each  # 拼接请求地址
            # 添加请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                'Cookie': 'name=value; JSESSIONID=0000vh8DlP73tkX4eqxUIgdBfLc:18djc0hbi; CaiGouServiceInfo=!UeKxfQXs2xckSd6U9I+YAUGJNqjObN2UWqGq5KyNRwNLC2NrGbYQfnzPfjeqkru0yaCZ0CSWUgas7pc='}
            # 发起请求
            res = requests.post(url, verify=False, headers=headers)
            # 接收返回页面
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            html = soup.text
            # 获取投标人资格要求部分
            content = html[html.find('投标人资格要求'):html.find('招标文件的获取')]
            # 获取当前招标公告标题
            title = titles[bidding_informations.index(each)]
            title = update_title(title)
            # 当前招标公告中我司具有的资质列表
            has_qualification = []
            for item in qualification:
                # 遍历从文档中读取的我司资质列表
                if content.find(item) != -1:
                    # 如果在投标人资格要求中找到我司具有的资质，则添加进当前招标公告中我司具有的资质列表
                    has_qualification.append(item)

            if len(has_qualification) > 0:
                # 如果当前招标公告中我司具有的资质列表长度大于0，则将此招标公告以html形式保存，并将当前招标公告中我司具有的资质列表以txt形式保存
                f = open(addr + title + '.html', 'w', encoding='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
                f.write(str(soup))
                f.close()
                f = open(addr + title + '_我司具有资质.txt', 'w', encoding='utf-8')
                f.write(str(has_qualification))
                f.close()

    def find_bidding_information(self):
        # 先获得时间数组格式的日期
        sevenDayAgo = (datetime.datetime.now() - datetime.timedelta(days=7))
        # 转换为其他字符串格式
        starting_time = sevenDayAgo.strftime('%Y-%m-%d')  # 获取七天前的日期作为起始时间
        ending_time = time.strftime('%Y-%m-%d', time.localtime())  # 获取当前时间为终止时间

        # 请求地址  pagesize=每页展示条数
        url = 'https://caigou.chinatelecom.com.cn/MSS-PORTAL/announcementjoin/list.do?provinceJT=NJT'
        # 请求参数
        data = {}
        data['provinceJT'] = 'NJT'  #
        data['docTitle'] = ''  # 公告名称
        data['docCode'] = ''  # 公告编码
        data['provinceCode'] = ''  # 省份编码
        data['provinceNames'] = ''  # 省份名称
        data['startDate'] = ''  # 创建开始日期
        data['endDate'] = ''  # 创建结束日期
        data['docType'] = 'TenderAnnouncement'  # 公告类型   招标公告
        data['paging.start'] = '1'  # 起始位置
        data['paging.pageSize'] = '1000'  # 每页条数
        data['pageNum'] = '1000'  # 每页条数
        # 请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
            'Cookie': 'name=value; JSESSIONID=0000vh8DlP73tkX4eqxUIgdBfLc:18djc0hbi; CaiGouServiceInfo=!UeKxfQXs2xckSd6U9I+YAUGJNqjObN2UWqGq5KyNRwNLC2NrGbYQfnzPfjeqkru0yaCZ0CSWUgas7pc='}
        # 发起请求
        res = requests.post(url, data, verify=False, headers=headers)
        # 接收相应页面
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        # 在页面中查找各个招标公告
        bidding_informations = ZhongGuoDianXin.get_information(soup)
        # 打开招标公告并判断是否符合公司具有资质
        ZhongGuoDianXin.open_bidding(bidding_informations[0], bidding_informations[1])

class GuangDongJiDian:
    '''
    广东省机电设备招标中心
    '''
    @staticmethod
    def get_information(soup):
        '''
        从页面中获取并整理出所有招标公告的地址
        :param soup: 要查找的页面
        :return: 招标公告地址列表、公告标题列表
        '''
        targets = soup.find_all('div', class_='border-dashed')
        information_address = []  # 存放所有招标公告地址的列表
        titles = []  # 存放所有招标公告标题的列表
        html = ''
        for each in targets:
            # 遍历页面中所有包含招标公告标题的标签
            html += str(each.a)  # 将这些标签存到一个字符串中
        a = html.find('<a href')  # 在字符串中找到所有a标签
        while a != -1:
            # 遍历所有a标签
            b = html.find('"', a + 12, a + 255)
            if b != -1:
                address = 'https://www.gdebidding.com' + html[a + 9:b]  # 获取招标公告所在地址
                information_address.append(address)  # 将所有地址存到一个列表中
                title = html[html.find('title', a) + 7:html.find('"', a + 60)]  # 获取招标公告title
                titles.append(title)  # 将所有招标公告title存到一个列表中
            else:
                b = a + 60
            a = str(html).find('<a href', b)
        return information_address, titles
    @staticmethod
    def open_bidding(bidding_informations, titles):
        qualification = get_qualification()  # 获取公司资质文档
        # 判断是否存在文件夹，如不存在则创建文件夹，以便存储文档
        addr = dir+'广东省机电设备招标公告/'
        if not os.path.exists(addr):
            os.makedirs(addr)

        for each in bidding_informations:
            url = each  # 拼接请求地址
            # 添加请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                'Cookie': 'JSESSIONID=B401DCA5686E1354B8DA790B46550AD4; _const_cas_from_=favicon.ico'}
            # 发起请求
            res = requests.get(url, verify=False, headers=headers)
            # 接收返回页面
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            # 获取投标人资格要求部分
            content = str(soup)
            # 获取当前招标公告标题
            title = titles[bidding_informations.index(each)]
            title=update_title(title)
            # 当前招标公告中我司具有的资质列表
            has_qualification = []
            for item in qualification:
                # 遍历从文档中读取的我司资质列表
                if content.find(item) != -1:
                    # 如果在投标人资格要求中找到我司具有的资质，则添加进当前招标公告中我司具有的资质列表
                    has_qualification.append(item)

            if len(has_qualification) > 0:
                # 如果当前招标公告中我司具有的资质列表长度大于0，则将此招标公告以html形式保存，并将当前招标公告中我司具有的资质列表以txt形式保存
                f = open(addr + title + '.html', 'w', encoding='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
                top = content[content.find('<div id="menu">'):content.find('</div>', content.find('<div id="manu">'))]
                content = content.replace(top, '')
                f.write(content)
                f.close()
                f = open(addr + title + '_我司具有资质.txt', 'w', encoding='utf-8')
                f.write(str(has_qualification))
            #     f.close()

    def find_bidding_information(self):
        # 请求地址
        url = 'https://www.gdebidding.com/zbxxgg/index.jhtml'
        # 请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
            'Cookie': 'clientlanguage=zh_CN'}
        # 发起请求
        res = requests.get(url, verify=False, headers=headers)
        # 接收相应页面
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        # 在页面中查找各个招标公告
        bidding_informations = GuangDongJiDian.get_information(soup)
        # 打开招标公告并判断是否符合公司具有资质
        GuangDongJiDian.open_bidding(bidding_informations[0], bidding_informations[1])
        # 获取招标公告最大页数
        maxPage = soup.find('select',
                            onchange="if(this.value==1){location='index.jhtml'}else{location='index_'+this.value+'.jhtml'}this.disabled='disabled'").find_all(
            'option')[-1]['value']
        page = 2
        while page <= int(maxPage):  # 遍历所有页，从第2页开始
            # 请求地址  page 第几页
            url = 'https://www.gdebidding.com/zbxxgg/index_' + str(page) + '.jhtml'
            # 请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
                'Cookie': 'clientlanguage=zh_CN'}
            # 发起请求
            res = requests.get(url, verify=False, headers=headers)
            # 接收相应页面
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            # 在页面中查找各个招标公告
            bidding_informations = GuangDongJiDian.get_information(soup)
            # 打开招标公告并判断是否符合公司具有资质
            GuangDongJiDian.open_bidding(bidding_informations[0], bidding_informations[1])
            page += 1


if __name__=='__main__':
    print('---------------------------开始获取工信部招标文档')
    gxb=GongXinBu()
    gxb.find_bidding_information()
    print('---------------------------工信部招标公告获取完毕')
    # print('---------------------------开始获取中国铁塔在线商务平台招标文档')
    # zgtt=ZhongGuoTieTa()
    # zgtt.get_biddinglist()
    # print('---------------------------中国铁塔在线商务平台招标公告获取完毕')
    # print('---------------------------开始获取中国电信-阳光采购网外部门户招标文档')
    # zgdx=ZhongGuoDianXin()
    # zgdx.find_bidding_information()
    # print('---------------------------中国电信-阳光采购网外部门户招标公告获取完毕')
    # print('---------------------------开始获取广东省机电设备招标中心招标文档')
    # gdjd=GuangDongJiDian()
    # gdjd.find_bidding_information()
    # print('---------------------------广东省机电设备招标中心招标公告获取完毕')
