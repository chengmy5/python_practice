import requests
import datetime
import time
import os
import bs4
import openpyxl
requests.packages.urllib3.disable_warnings()#关闭安全警告

dir='E:/招标公告/'#文件存储位置
#判断是否存在文件夹，如不存在则创建文件夹，以便存储文档
if not os.path.exists(dir):
    os.makedirs(dir)
dir1='E:/招标公告_同专业更高等级资质/'#文件存储位置
#判断是否存在文件夹，如不存在则创建文件夹，以便存储文档
if not os.path.exists(dir1):
    os.makedirs(dir1)
#创建excel文件，用于保存招标公告信息
wb=openpyxl.Workbook()
ws=wb.active
ws.append(['招标网站','项目名称','招标单位','项目概况','报名截止时间','资质要求','招标范围'])
wb.save(dir+'每日招标信息'+time.strftime('%Y%m%d',time.localtime())+'.xlsx')
#创建excel文件，用于保存更高资质招标公告信息
wb1=openpyxl.Workbook()
ws1=wb1.active
ws1.append(['招标网站','项目名称','招标单位','项目概况','报名截止时间','资质要求','招标范围'])
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


class GuangDongYouXian:
    '''
    广东省有线招标
    '''

    @staticmethod
    def information(soup, webName, title, has_qualification):
        qualification = ''
        for each in has_qualification:
            qualification += each + ','
        # 招标单位
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
        bidUnit=soup.text[a:b+3]

        zbdljg = ['招标代理机构：','采购代理机构：']
        for item in zbdljg:
            c = soup.text.find(item)
            if c != -1:
                break
        b = soup.text.find('分公司', c + 14, c + 35)
        if b == -1:
            b = soup.text.find('公司', c + 14, c + 35)
        bidUnit += '/'+soup.text[c:b+3]
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
        # 判断是否存在文件夹，如不存在则创建文件夹，以便存储文档
        addr = dir+'广东省有线招标/'
        addr1 = dir1+'广东省有线招标/'
        if not os.path.exists(addr):
            os.makedirs(addr)
        if not os.path.exists(addr1):
            os.makedirs(addr1)
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
            f = open(addr + title + '.html', 'w', encoding='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
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
                f = open(addr1 + title + '.html', 'w',
                         encoding='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
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
            if (d.days < 191) & (item['type']=='采购公告'):
                GuangDongYouXian.open_bidding(item['link'], item['title'])
if __name__=='__main__':
    gdyx=GuangDongYouXian()
    gdyx.find_bidding_information()