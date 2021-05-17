import time
import base64
import requests
import bs4
import os
import datetime
from selenium import webdriver
import json
import openpyxl
from pyquery import PyQuery
requests.packages.urllib3.disable_warnings()#关闭安全警告

dir='E:/招标公告'+time.strftime('%Y%m%d',time.localtime())+'/'#文件存储位置
#判断是否存在文件夹，如不存在则创建文件夹，以便存储文档
if not os.path.exists(dir):
    os.makedirs(dir)
dir1='E:/招标公告_同专业更高等级资质'+time.strftime('%Y%m%d',time.localtime())+'/'#文件存储位置
#判断是否存在文件夹，如不存在则创建文件夹，以便存储文档
if not os.path.exists(dir1):
    os.makedirs(dir1)
#创建excel文件，用于保存招标公告信息
wb=openpyxl.Workbook()
ws=wb.active
ws.append(['招标网站','项目名称','招标人','招标代理机构','项目概况','报名截止时间','资质要求','招标范围'])
wb.save(dir+'每日招标信息'+time.strftime('%Y%m%d',time.localtime())+'.xlsx')
#创建excel文件，用于保存更高资质招标公告信息
wb1=openpyxl.Workbook()
ws1=wb1.active
ws1.append(['招标网站','项目名称','招标人','招标代理机构','项目概况','报名截止时间','资质要求','招标范围'])
wb1.save(dir1+'每日招标信息_更高资质'+time.strftime('%Y%m%d',time.localtime())+'.xlsx')

def get_qualification(txt):
    '''
    读取公司资质文档
    :return: 公司所有资质的列表
    '''
    f = open(txt+'.txt', 'r', encoding='utf-8')
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
    def information(soup,webName,title,has_qualification):
        #去除内容中的HTML标签
        soup=soup.replace('<p class="MsoListParagraph" style="margin-left:28px;line-height:29px">','')
        soup=soup.replace('<p style="text-indent:35px;line-height:150%">','')
        soup=soup.replace('<p style="text-indent:32px;line-height:29px">','')
        soup=soup.replace('<p style="text-indent:32px;line-height:33px">','')
        soup=soup.replace('<p style="text-indent:28px">','')
        soup=soup.replace('</p>','')
        soup=soup.replace('<span style="font-family:宋体">','')
        soup=soup.replace('<span style="text-decoration:underline;">','')
        soup=soup.replace('<span style="background:yellow;background:yellow">','')
        soup=soup.replace('<span style="font-family: 宋体;font-size: 16px">','')
        soup=soup.replace('<span style=";font-family:宋体;font-size:16px">','')
        soup=soup.replace('<span style="font-size:16px;font-family:宋体">','')
        soup=soup.replace('<span style="font-family:Times New Roman">','')
        soup=soup.replace('<span style=";line-height:115%;font-family:宋体">','')
        soup=soup.replace('<span style="font-family:宋体;letter-spacing:0">','')
        soup=soup.replace('<span style="font-size:16px;font-family:仿宋_GB2312">','')
        soup=soup.replace('<span style=";font-family:宋体;letter-spacing:0;font-size:16px">','')
        soup=soup.replace('<span style=";font-family:宋体;font-size:14px;background:rgb(255,255,0);background:rgb(255,255,0)">','')
        soup=soup.replace('</span>','')
        soup=soup.replace('</strong>','')
        qualification=''
        for each in has_qualification:
            qualification+=each+','
        # 招标人
        bidPerson = ''
        # 招标代理机构
        bidUnit = ''
        #项目概况
        projectOverview=''
        #报名截止时间
        endTime=''
        #招标范围
        bidScope=''
        #存放公告信息的列表
        information=[]

        information.append(webName)
        information.append(title)
        # 获取招标人/招标代理机构
        a = soup.find('招标人为')
        bidPerson = soup[a+4:soup.find('，',a,a+30)]
        bidUnit=soup[soup.find('招标代理机构为',a)+7:soup.find('。')]
        information.append(bidPerson)
        information.append(bidUnit)
        # 获取项目概况
        xmgk=['标段划分','标包划分','本项目划分','不划分标包','不划分标段']
        for item in xmgk:
            b = soup.find(item)
            if b!=-1:
                break
        c=soup.find('。', b, b + 60)
        if c==-1:
            c = soup.find('，', b, b + 60)
        if c==-1:
            c = soup.find('：', b, b + 60)
        if c==-1:
            c = soup.find(' ', b, b + 60)
        if b!=-1:
            projectOverview=soup[b:c]
        information.append(projectOverview)
        #获取报名截止时间
        d=soup.find('投标截止时间为')
        if d==-1:
            d = soup.find('投标截止时间')
        if d == -1:
            d = soup.find('投标截止     时间为')
        if d!=-1:
            d=soup.find('2',d,d+15)
        e = soup.find('。', d)
        endTime=soup[d:e]
        information.append(endTime)
        information.append(qualification)
        #获取招标范围
        zbfw=['招标内容:','招标内容：','招标范围:','招标范围：','采购内容:','采购内容：','项目主要内容：','建设内容：','招标规模及内容：','项目概况：']
        for item in zbfw:
            f=soup.find(item)
            if f!=-1:
                break
        g=soup.find('。',f,f+255)
        if f!=-1:
            bidScope=soup[f:g]
        information.append(bidScope)
        return information

    @staticmethod
    def open_bidding(bidding_informations):
        qualification=get_qualification('我司具有资质')# 获取公司资质文档
        qualification1=get_qualification('同专业高等级资质')# 获取更高资质文档
        #网站
        webName='工信部'
        for each in bidding_informations:
            # 获取当前招标公告标题
            title = each['bulletinTitle']
            title = update_title(title)
            text=each['bulletinComment']
            #获取投标人资格要求部分
            content = text[text.find('投标人资格要求'):text.find('资格审查方法')]
            #当前招标公告中我司具有的资质列表
            has_qualification=[]
            for item in qualification:
                #遍历从文档中读取的我司资质列表
                if content.find(item)!=-1:
                    #如果在投标人资格要求中找到我司具有的资质，则添加进当前招标公告中我司具有的资质列表
                    has_qualification.append(item)
            if len(has_qualification)>0:
                #如果当前招标公告中我司具有的资质列表长度大于0，则将此招标公告以html形式保存，并将当前招标公告中我司具有的资质列表以txt形式保存
                f = open(dir+title+'.html','w',encoding ='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
                f.write(text)
                f.close()
                information=GongXinBu.information(text,webName,title,has_qualification)
                ws.append(information)
            else:
                for item in qualification1:
                    # 遍历从文档中读取的更高资质列表
                    if content.find(item) != -1:
                        # 如果在投标人资格要求中找到我司具有的资质，则添加进当前招标公告中更高资质列表
                        has_qualification.append(item)
                if len(has_qualification) > 0:
                    # 如果当前招标公告中我司具有的资质列表长度大于0，则将此招标公告以html形式保存，并将当前招标公告中我司具有的资质列表以txt形式保存
                    f = open(dir1 + title + '.html', 'w',encoding='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
                    f.write(text)
                    f.close()
                    information = GongXinBu.information(text, webName, title, has_qualification)
                    ws1.append(information)
        #保存excel文档
        wb.save(dir+'每日招标信息'+time.strftime('%Y%m%d',time.localtime())+'.xlsx')
        wb1.save(dir1+'每日招标信息_更高资质'+time.strftime('%Y%m%d',time.localtime())+'.xlsx')

    def find_bidding_information(self):
        # 先获得时间数组格式的日期
        sevenDayAgo = (datetime.datetime.now() - datetime.timedelta(days=10))
        # 转换为其他字符串格式
        starting_time = sevenDayAgo.strftime('%Y-%m-%d')#获取七天前的日期作为起始时间
        ending_time = time.strftime('%Y-%m-%d', time.localtime())#获取当前时间为终止时间

        #请求地址  pagesize=每页展示条数
        url='https://txzbqy.miit.gov.cn/zbtb/gateway/gatewayPublicity/bidBulletinList'
        #请求参数
        data={}
        data['bulletinTitle']=''#标题
        data['bulletinType']='22'
        data['fileBuyBeginTime']=''
        data['fileBuyEndTime']=''
        data['gatewayFlag']=0
        data['issueDate']=''
        data['issueDates']=[]
        data['limit']=500#每页条数
        data['occupationBeginDate'] = starting_time  # 发布日期-开始
        data['occupationEndDate'] = ending_time  # 发布日期-结束
        data['page']=1#第几页
        data['resource']=ending_time+' 23:59:59'#文件获取时间
        data['status']='11'
        #请求头
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                 'Content-Type':'application/json;charset=UTF-8',
                 'Referer':'https://txzbqy.miit.gov.cn/',
                 'Origin':'https://txzbqy.miit.gov.cn',
                 'Cookie':'jsessionid=rBQQsBroYJXh75cslLSKJkU_namom_KZUiYA'}
        #发起请求
        res = requests.post(url,json.dumps(data),verify=False,headers=headers)
        #接收相应页面
        # soup = bs4.BeautifulSoup(res.text, 'html.parser')
        js=res.json()
        # size=js['page']['totalCount']#总条数
        bidding_informations=js['page']['list']
        # #打开招标公告并判断是否符合公司具有资质
        GongXinBu.open_bidding(bidding_informations)

class ZhongGuoTieTa:
    '''
    中国铁塔在线商务平台
    '''
    def get_biddinglist(self):
        # 先获得时间数组格式的日期
        sevenDayAgo = (datetime.datetime.now() - datetime.timedelta(days=10))
        # 转换为其他字符串格式
        starting_time = sevenDayAgo.strftime('%Y-%m-%d')  # 获取七天前的日期作为起始时间
        url = "http://www.tower.com.cn/default/main/index/cn.chinatowercom.obp.main.index.obphomepage.queryNoticeDetails.biz.ext"  # 网站地址
        payload = {}  # 请求参数
        payload['cityInput'] = ''  # 城市
        payload['effectTime'] = starting_time  # 发布时间
        payload['failureTime'] = ''  # 有效截止日期
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
    def information(html, webName, title, has_qualification):
        html=PyQuery(html).text()

        qualification = ''
        for each in has_qualification:
            qualification += each + ','
        # 招标人
        bidPerson = ''
        # 招标代理机构
        bidUnit = ''
        # 项目概况
        projectOverview = ''
        # 报名截止时间
        endTime = ''
        # 招标范围
        bidScope = ''
        # 存放公告信息的列表
        information = []

        information.append(webName)
        information.append(title)
        # 获取招标人/招标代理机构
        zbr=['招标人：','招标人:','招 标 人：','招 标 人:','招\n标 人：','招     标     人：','招标人名称：','采购人：','采 购 人：','采购人:','采 购 人:']
        for item in zbr:
            a = html.find(item)
            if a!=-1:
                break
        b = html.find('\n', a + 15, a + 90)
        if b == -1:
            b = html.find(' ', a + 15, a + 90)
        bidPerson = html[a:b]
        bidPerson = bidPerson.replace(' ', '')
        bidPerson = bidPerson.replace('\n', '')
        information.append(bidPerson)
        zbdljg=['招标代理机构：','招标代理机构:','招 标 代 理 机 构：','招 标 代 理 机 构:','招标代理机构名称:','招标代理机构名称：','采购代理机构:','采购代理机构：','采购代理机构:','招标代理：','招标代理:',]
        for item in zbdljg:
            c = html.find(item, a - 100)
            if c!=-1:
                break
        d = html.find('\n', c + 10, c + 80)
        if d == -1:
            d = html.find(' ', c + 10, c + 80)
        bidUnit =html[c:d]
        bidUnit = bidUnit.replace(' ', '')
        bidUnit = bidUnit.replace('\n', '')
        information.append(bidUnit)
        # 获取项目概况
        xmgk=['标包划分','标包划分情况：','标段划分','标段划分情况：','不划分标包','不划分标段']
        for item in xmgk:
            e = html.find(item)
            if e != -1:
                break
        f = html.find('。', e, e + 60)
        if f == -1:
            f = html.find('：', e, e + 60)
        if f == -1:
            f = html.find('，', e, e + 60)
        if f == -1:
            f = html.find(' ', e, e + 60)
        if f == -1:
            f = html.find('；', e, e + 60)
        projectOverview = html[e:f]
        projectOverview = projectOverview.replace(' ', '')
        projectOverview = projectOverview.replace('\n', '')
        information.append(projectOverview)
        # 获取报名截止时间
        bmjzsj=['投标截止时间为','投标截止时间','投标文件的递交截止时间','电子投标文件的递交','递交截止时间','递交投标文件截止时间','投标文件递交截止时间','投标文件递交的截止时间','递交截止时间为']
        for item in bmjzsj:
            g = html.find(item)
            g = html.find('2', g, g + 60)
            if g != -1:
                break
        h = html.find('分', g, g + 70)
        if h == -1:
            h = html.find('，', g, g + 70)
        if h == -1:
            h = html.find('。', g, g + 70)
        if h == -1:
            h = html.find('\n', g, g + 70)
        endTime = html[g:h+1]
        endTime = endTime.replace(' ', '')
        endTime = endTime.replace('\n', '')
        information.append(endTime)
        information.append(qualification)
        # 获取招标范围
        zbnr=['招标内容:','招标内容：','招标内容为：','招标范围:','招标范围：','采购内容:','采购内容：','采购内容为：','项目主要内容：','建设内容：','招标规模及内容：','项目概况：','招标范围']
        for item in zbnr:
            j = html.find(item)

            if j != -1:
                break
        k = html.find('\n', j + 20, j + 255)
        if k == -1:
            k = html.find('。', j + 20, j + 255)
        if k == -1:
            k = html.find(' ', j + 20, j + 255)
        bidScope = html[j:k]
        bidScope = bidScope.replace(' ', '')
        bidScope = bidScope.replace('\n', '')
        information.append(bidScope)
        return information

    @staticmethod
    def bidding_detail(ids):
        qualification = get_qualification('我司具有资质')  # 获取公司资质文档
        qualification1 = get_qualification('同专业高等级资质')  # 更高资质文档
        # 网站
        webName = '中国铁塔在线商务平台'
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
                f = open(dir + title + '.html', 'w', encoding='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
                # 去除头尾多余部分
                top0 = html.find('<div class="header-main">')
                top = html[top0:html.find('</div>', top0 + 4500)]
                html = html.replace(top, '')
                foot0 = html.find('<div class="new_footer"')
                foot = html[foot0:html.find('</div>', foot0 + 440)]
                html = html.replace(foot, '')

                f.write(str(html))
                f.close()

                information = ZhongGuoTieTa.information(html, webName, title, has_qualification)
                ws.append(information)
            else:
                for item in qualification1:
                    # 遍历从文档中读取的更高资质列表
                    if content.find(item) != -1:
                        # 如果在投标人资格要求中找到我司具有的资质，则添加进当前招标公告中我司具有的资质列表
                        has_qualification.append(item)
                if len(has_qualification) > 0:
                    # 如果当前招标公告中我司具有的资质列表长度大于0，则将此招标公告以html形式保存，并将当前招标公告中我司具有的资质列表以txt形式保存
                    f = open(dir1 + title + '.html', 'w', encoding='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
                    # 去除头尾多余部分
                    top0 = html.find('<div class="header-main">')
                    top = html[top0:html.find('</div>', top0 + 4500)]
                    html = html.replace(top, '')
                    foot0 = html.find('<div class="new_footer"')
                    foot = html[foot0:html.find('</div>', foot0 + 440)]
                    html = html.replace(foot, '')

                    f.write(str(html))
                    f.close()

                    information = ZhongGuoTieTa.information(html, webName, title, has_qualification)
                    ws1.append(information)
            time.sleep(2)
        driver.quit()
        # 保存excel文档
        wb.save(dir + '每日招标信息' + time.strftime('%Y%m%d', time.localtime()) + '.xlsx')
        wb1.save(dir1 + '每日招标信息_更高资质' + time.strftime('%Y%m%d', time.localtime()) + '.xlsx')

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
    def information(soup, webName, title, has_qualification):
        qualification = ''
        for each in has_qualification:
            qualification += each + ','
        # 招标人
        bidPerson = ''
        # 招标代理机构
        bidUnit = ''
        # 项目概况
        projectOverview = ''
        # 报名截止时间
        endTime = ''
        # 招标范围
        bidScope = ''
        # 存放公告信息的列表
        information = []

        information.append(webName)
        information.append(title)
        # 获取招标人/招标代理机构
        zbr=['招标人：','招标人:','招 标 人：','招标人名称：']
        for item in zbr:
            a = soup.text.find(item)
            if a!=-1:
                break
        b=soup.text.find('分公司',a+8,a+30)
        if b==-1:
            b = soup.text.find('公司', a+8, a + 30)
        bidPerson=soup.text[a:b+3]
        bidPerson = bidPerson.replace(' ', '')
        bidPerson = bidPerson.replace('\n', '')
        information.append(bidPerson)
        zbdljg = ['招标代理机构：','招标代理机构名称：']
        for item in zbdljg:
            c = soup.text.find(item)
            if c != -1:
                break
        b = soup.text.find('分公司', c + 14, c + 35)
        if b == -1:
            b = soup.text.find('公司', c + 14, c + 35)
        bidUnit = soup.text[c:b+3]
        bidUnit=bidUnit.replace(' ','')
        bidUnit=bidUnit.replace('\n','')
        information.append(bidUnit)
        # 获取项目概况
        xmgk = ['标段划分', '标包划分', '本项目划分', '不划分标包', '不划分标段']
        for item in xmgk:
            e = soup.text.find(item)
            if e != -1:
                break
        f = soup.text.find('。', e, e + 60)
        if f == -1:
            f = soup.text.find('，', e, e + 60)
        if f == -1:
            f = soup.text.find(' ', e, e + 60)
        projectOverview = soup.text[e:f]
        projectOverview=projectOverview.replace(' ','')
        projectOverview=projectOverview.replace('\n','')
        information.append(projectOverview)
        # 获取报名截止时间
        bmjzsj=['投标文件提交截止时间：','投标截止时间为','递交的截止时间','开标时间：','投标截止时间']
        for item in bmjzsj:
            g = soup.text.find(item)
            if g!=-1:
                break
        if g != -1:
            g = soup.text.find('2', g, g + 25)
        h = soup.text.find('分', g)
        endTime = soup.text[g:h+1]
        information.append(endTime)
        information.append(qualification)
        # 获取招标范围
        zbfw = ['招标内容:', '招标内容：', '招标范围:', '招标范围：', '采购内容:', '采购内容：', '项目主要内容：', '建设内容：', '招标规模及内容：', '项目概况：', '项目概况']
        for item in zbfw:
            j = soup.text.find(item)
            if j != -1:
                break
        k = soup.text.find('。', j, j + 200)
        if k==-1:
            k = soup.text.find(' ', j, j + 200)
        if k==-1:
            k = soup.text.find('\n', j, j + 200)
        if j != -1:
            bidScope = soup.text[j:k]
        bidScope = bidScope.replace(' ', '')
        bidScope = bidScope.replace('\n', '')
        information.append(bidScope)
        return information

    @staticmethod
    def open_bidding(bidding_informations, titles):
        qualification = get_qualification('我司具有资质')  # 获取公司资质文档
        qualification1 = get_qualification('同专业高等级资质')  # 获取更高资质文档
        # 网站
        webName = '中国电信-阳光采购网外部门户'
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
                f = open(dir + title + '.html', 'w', encoding='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
                f.write(str(soup))
                f.close()
                information = ZhongGuoDianXin.information(soup, webName, title, has_qualification)
                ws.append(information)
            else:
                for item in qualification1:
                    # 遍历从文档中读取的更高资质列表
                    if content.find(item) != -1:
                        # 如果在投标人资格要求中找到我司具有的资质，则添加进当前招标公告中更高资质列表
                        has_qualification.append(item)
                if len(has_qualification) > 0:
                    # 如果当前招标公告中我司具有的资质列表长度大于0，则将此招标公告以html形式保存，并将当前招标公告中我司具有的资质列表以txt形式保存
                    f = open(dir1 + title + '.html', 'w',encoding='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
                    f.write(str(soup))
                    f.close()
                    information = ZhongGuoDianXin.information(soup, webName, title, has_qualification)
                    ws1.append(information)
        # 保存excel文档
        wb.save(dir + '每日招标信息' + time.strftime('%Y%m%d', time.localtime()) + '.xlsx')
        wb1.save(dir1 + '每日招标信息_更高资质' + time.strftime('%Y%m%d', time.localtime()) + '.xlsx')

    def find_bidding_information(self):
        # 先获得时间数组格式的日期
        sevenDayAgo = (datetime.datetime.now() - datetime.timedelta(days=10))
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
        data['startDate'] = starting_time  # 创建开始日期
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

class GuangDongYouXian:
    '''
    广东省有线招标
    '''

    @staticmethod
    def information(soup, webName, title, has_qualification):
        qualification = ''
        for each in has_qualification:
            qualification += each + ','
        # 招标人
        bidPerson = ''
        # 招标代理机构
        bidUnit = ''
        # 项目概况
        projectOverview = ''
        # 报名截止时间
        endTime = ''
        # 招标范围
        bidScope = ''
        # 存放公告信息的列表
        information = []

        information.append(webName)
        information.append(title)
        # 获取招标人/招标代理机构
        zbr=['招标人为','采购人：','招标人：','招 标 人：']
        for item in zbr:
            a = soup.text.find(item)
            if a!=-1:
                break
        b=soup.text.find('分公司',a+8,a+30)
        if b==-1:
            b = soup.text.find('公司', a+8, a + 30)
        bidPerson=soup.text[a:b+3]
        bidPerson=bidPerson.replace(' ','')
        bidPerson=bidPerson.replace('\n','')
        information.append(bidPerson)

        zbdljg = ['招标代理机构：','采购代理机构：']
        for item in zbdljg:
            c = soup.text.find(item)
            if c != -1:
                break
        b = soup.text.find('分公司', c + 14, c + 35)
        if b == -1:
            b = soup.text.find('公司', c + 14, c + 35)
        bidUnit = soup.text[c:b+3]
        bidUnit=bidUnit.replace(' ','')
        bidUnit=bidUnit.replace('\n','')
        information.append(bidUnit)
        # 获取项目概况
        xmgk = ['标段划分', '标包划分', '本项目划分', '不划分标包', '不划分标段','本招标项目划分']
        for item in xmgk:
            e = soup.text.find(item)
            if e != -1:
                break
        f = soup.text.find('。', e, e + 60)
        if f == -1:
            f = soup.text.find('，', e, e + 60)
        if f == -1:
            f = soup.text.find(' ', e, e + 60)
        projectOverview = soup.text[e:f]
        projectOverview=projectOverview.replace(' ','')
        projectOverview=projectOverview.replace('\n','')
        information.append(projectOverview)
        # 获取报名截止时间
        bmjzsj=['投标文件提交截止时间：','投标截止时间为','递交的截止时间','投标截止时间','递交响应文件截止时间','递交截止时间','递交纸质版响应文件截止时间','递交投标文件截止时间']
        for item in bmjzsj:
            g = soup.text.find(item)
            if g!=-1:
                break
        if g != -1:
            g = soup.text.find('2', g, g + 25)
        h = soup.text.find('分', g,g+30)
        if h==-1:
            h = soup.text.find('时', g,g+30)
        if h==-1:
            h = soup.text.find(' ', g,g+30)
        endTime = soup.text[g:h+1]
        information.append(endTime)
        information.append(qualification)

        # 获取招标范围
        zbfw = ['招标内容:', '招标内容：', '招标范围:', '招标范围：', '采购内容:', '采购内容：', '项目主要内容：', '建设内容：', '招标规模及内容：', '项目概况：', '项目概况']
        for item in zbfw:
            j = soup.text.find(item)
            if j != -1:
                break
        k = soup.text.find('。', j+10, j + 200)
        if k==-1:
            k = soup.text.find(' ', j+10, j + 200)
        if k==-1:
            k = soup.text.find('\n', j+10, j + 200)
        if j != -1:
            bidScope = soup.text[j:k]
        bidScope = bidScope.replace(' ', '')
        bidScope = bidScope.replace('\n', '')
        information.append(bidScope)
        return information

    @staticmethod
    def open_bidding(link, title):
        qualification = get_qualification('我司具有资质')  # 获取公司资质文档
        qualification1 = get_qualification('同专业高等级资质')  # 获取更高资质文档
        # 网站
        webName = '广东省有线招标'

        # 添加请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Cookie': 'ECSID=3dc9c8cc66d131b20bccb64c6d6a9230; acw_tc=781bad0716110406416792082e162eeac1fe488c546103cb59db3c7c0756f5'}
        # 发起请求
        res = requests.get(link, verify=False, headers=headers)
        # 接收返回页面
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        html = soup.text
        # 获取投标人资格要求部分
        tbr=['投标人资格要求','供应商必须具备以下资质','响应人资格要求','应答人资格要求','报价人资格条件','投标人资格条件','供应商资格条件']
        for item in tbr:
            a=html.find(item)
            if a!=-1:
                break
        zbwj=['招标文件的获取','谈判文件的获取时间','获取询价文件时间','比价文件的获取','报名和文件的获取','竞价文件获取','采购文件的获取','项目采购谈判文件的获取','获取谈判文件的时间']
        for item in zbwj:
            b=html.find(item)
            if b!=-1:
                break
        content = html[a:b]
        # 当前招标公告中我司具有的资质列表
        has_qualification = []
        for item in qualification:
            # 遍历从文档中读取的我司资质列表
            if content.find(item) != -1:
                # 如果在投标人资格要求中找到我司具有的资质，则添加进当前招标公告中我司具有的资质列表
                has_qualification.append(item)

        if len(has_qualification) > 0:
            # 如果当前招标公告中我司具有的资质列表长度大于0，则将此招标公告以html形式保存，并将当前招标公告中我司具有的资质列表以txt形式保存
            f = open(dir + title + '.html', 'w', encoding='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
            f.write(str(soup))
            f.close()
            information = GuangDongYouXian.information(soup, webName, title, has_qualification)
            ws.append(information)
        else:
            for item in qualification1:
                # 遍历从文档中读取的更高资质列表
                if content.find(item) != -1:
                    # 如果在投标人资格要求中找到我司具有的资质，则添加进当前招标公告中更高资质列表
                    has_qualification.append(item)
            if len(has_qualification) > 0:
                # 如果当前招标公告中我司具有的资质列表长度大于0，则将此招标公告以html形式保存，并将当前招标公告中我司具有的资质列表以txt形式保存
                f = open(dir1 + title + '.html', 'w',encoding='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
                f.write(str(soup))
                f.close()
                information = GuangDongYouXian.information(soup, webName, title, has_qualification)
                ws1.append(information)
        # 保存excel文档
        wb.save(dir + '每日招标信息' + time.strftime('%Y%m%d', time.localtime()) + '.xlsx')
        wb1.save(dir1 + '每日招标信息_更高资质' + time.strftime('%Y%m%d', time.localtime()) + '.xlsx')

    def find_bidding_information(self):
        # 获取当前时间
        today = time.strftime('%Y-%m-%d', time.localtime())
        d1 = datetime.datetime.strptime(today, '%Y-%m-%d')
        # 请求地址
        url = "https://www.gcable.com.cn/about-us/purchase/?json=1"
        # 请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Cookie': 'acw_tc=76b20f4516110367979744225e9ddf97264f252545a437e5d152f01c5d7a85; ECSID=3dc9c8cc66d131b20bccb64c6d6a9230'}
        # 发起请求
        res = requests.post(url, verify=False, headers=headers)
        soup = res.json()
        # 打开招标公告并判断是否符合公司具有资质
        for item in soup:
            #获取发布时间
            d2 = datetime.datetime.strptime(item['post-time'], '%Y-%m-%d')
            d = d1 - d2
            if (d.days < 11) & (item['type']=='采购公告'):
                GuangDongYouXian.open_bidding(item['link'], item['title'])

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
    def information(soup, webName, title, has_qualification):
        qualification = ''
        for each in has_qualification:
            qualification += each + ','
        # 招标人
        bidPerson = ''
        # 招标代理机构
        bidUnit = ''
        # 项目概况
        projectOverview = ''
        # 报名截止时间
        endTime = ''
        # 招标范围
        bidScope = ''
        # 存放公告信息的列表
        information = []

        information.append(webName)
        information.append(title)
        # 获取招标人/招标代理机构
        zbr=['招标人：','招 标 人：','招标单位','采购人信息','询价人名称：','采购人名称：','采购人信息','采购人：']
        for item in zbr:
            a = soup.text.find(item)
            if a != -1:
                break
        b=soup.text.find('分公司',a+10,a+30)
        if  b==-1:
            b=soup.text.find('公司',a+10,a+30)
        if  b==-1:
            b=soup.text.find('\n',a+10,a+30)
        if  b==-1:
            b=soup.text.find(' ',a+10,a+30)
        if a!=-1&b!=-1:
            bidPerson = soup.text[a:b + 3]
        bidPerson = bidPerson.replace(' ', '')
        bidPerson = bidPerson.replace('\n', '')
        information.append(bidPerson)
        zbdljg=['招标代理机构：','采购代理机构信息','代理机构：','招标代理：']
        for item in zbdljg:
            c=soup.text.find(item)
            if c!=-1:
                break
        b = soup.text.find('分公司', c + 10, c + 30)
        if b == -1:
            b = soup.text.find('公司', c + 10, c + 30)
        if b == -1:
            b = soup.text.find('\n', c + 10, c + 30)
        if b == -1:
            b = soup.text.find(' ', c + 10, c + 30)
        if c != -1 & b != -1:
            bidUnit += soup.text[c:b+3]
        bidUnit=bidUnit.replace(' ','')
        bidUnit=bidUnit.replace('\n','')
        information.append(bidUnit)
        # 获取项目概况
        xmgk = ['本项目划分','标段划分', '标包划分',  '不划分标包', '不划分标段']
        for item in xmgk:
            d = soup.text.find(item)
            if d != -1:
                break
        e = soup.text.find('。', d, d + 60)
        if e == -1:
            e = soup.text.find('，', d, d + 60)
        if e == -1:
            e = soup.text.find(' ', d, d + 60)
        if d != -1:
            projectOverview = soup.text[d:e]
        information.append(projectOverview)
        # 获取报名截止时间
        bmjzsj=['投标截止时间为','投标截止时间：','递交截止时间：','截止时间：','递交时间：','报价截止时间：','开标时间：','提交投标文件截止时间','投标文件递交的截止时间','投标截止时间']
        for item in bmjzsj:
            f = soup.text.find(item)
            if f!=-1:
                break
        if f != -1:
            f = soup.text.find('2', f, f + 30)
        g = soup.text.find('分', f,f+30)
        if g==-1:
            g = soup.text.find('（', f)
        if g==-1:
            g = soup.text.find(' ', f)
        if g==-1:
            g = soup.text.find('\n', f)
        if g==-1:
            g = soup.text.find('，', f)
        endTime = soup.text[f:g]
        endTime = endTime.replace('\n', '')
        information.append(endTime)
        information.append(qualification)
        # 获取招标范围
        zbfw = ['招标内容:', '招标内容：', '招标范围:', '招标范围：', '采购内容:', '采购内容：', '项目主要内容：', '建设内容：', '招标规模及内容：', '项目概况：','采购需求：','项目内容及需求：','报价内容：','工程内容：']
        for item in zbfw:
            h = soup.text.find(item)
            if h != -1:
                break
        j = soup.text.find('\n', h+35, h + 255)
        if j==-1:
            j = soup.text.find('。', h, h + 255)
        if j==-1:
            j = soup.text.find(' ', h, h + 255)
        if j==-1:
            j = soup.text.find('；', h, h + 255)
        if h!= -1:
            bidScope = soup.text[h:j]
        bidScope = bidScope.replace(' ', '')
        bidScope = bidScope.replace('\n', '')
        information.append(bidScope)
        return information

    @staticmethod
    def open_bidding(bidding_informations, titles):
        qualification = get_qualification('我司具有资质')  # 获取公司资质文档
        qualification1 = get_qualification('同专业高等级资质')  # 获取更高资质文档
        # 网站
        webName = '广东省机电设备招标中心'
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
                f = open(dir + title + '.html', 'w', encoding='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
                top = content[content.find('<div id="menu">'):content.find('</div>', content.find('<div id="manu">'))]
                content = content.replace(top, '')
                f.write(content)
                f.close()
                information = GuangDongJiDian.information(soup, webName, title, has_qualification)
                ws.append(information)
            else:
                for item in qualification1:
                    # 遍历从文档中读取的更高资质列表
                    if content.find(item) != -1:
                        # 如果在投标人资格要求中找到我司具有的资质，则添加进当前招标公告中更高资质列表
                        has_qualification.append(item)
                if len(has_qualification) > 0:
                    # 如果当前招标公告中我司具有的资质列表长度大于0，则将此招标公告以html形式保存，并将当前招标公告中我司具有的资质列表以txt形式保存
                    f = open(dir1 + title + '.html', 'w',encoding='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
                    f.write(str(soup))
                    f.close()
                    information = GuangDongJiDian.information(soup, webName, title, has_qualification)
                    ws1.append(information)
        # 保存excel文档
        wb.save(dir + '每日招标信息' + time.strftime('%Y%m%d', time.localtime()) + '.xlsx')
        wb1.save(dir1 + '每日招标信息_更高资质' + time.strftime('%Y%m%d', time.localtime()) + '.xlsx')

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
    # print('---------------------------开始获取广东省有线招标公告')
    # gdyx = GuangDongYouXian()
    # gdyx.find_bidding_information()
    # print('---------------------------广东省有线招标公告获取完毕')
    # print('---------------------------开始获取广东省机电设备招标中心招标文档')
    # gdjd=GuangDongJiDian()
    # gdjd.find_bidding_information()
    # print('---------------------------广东省机电设备招标中心招标公告获取完毕')
