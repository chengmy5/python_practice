import requests
import json
from selenium import webdriver
import time
import os
'''
中国铁塔在线商务平台
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

def get_biddinglist():
    url="http://www.tower.com.cn/default/main/index/cn.chinatowercom.obp.main.index.obphomepage.queryNoticeDetails.biz.ext"#网站地址
    payload = {} #请求参数
    payload['cityInput']=''#城市
    payload['effectTime']=''#发布时间
    payload['failureTime']='2021-01-07 00:00:00'#有效截止日期
    payload['level']=''
    payload['noticeTitle']=''
    payload['page']={'begin': 0, 'length': 2000}
    payload['pageIndex']=0
    payload['pageSize']=2000#每页最大展示条数
    payload['provinceInput']=''
    payload['purchaseNoticeType']='2'
    payload['resultsNoticeType']='2'
    payload['sortField']=''
    payload['sortOrder']=''
    #请求头
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
             'Referer': 'http://www.tower.com.cn/default/main/index/noticedetail.jsp?_operation=notice&_purchaseNoticeType=2&_resultsNoticeType=2',
             'content-type': 'application/json'}
    res = requests.post(url,data=json.dumps(payload),verify=False,headers=headers)#发起请求
    ids=[]#存放所有招标公告id的列表
    a = res.text.find('id')
    while a!=-1:
        a = res.text.find('id',a+1)
        ids.append(res.text[a+5:a+37])
    bidding_detail(ids)
    # print(ids)
def bidding_detail(ids):
    qualification = get_qualification()  # 获取公司资质文档
    # 判断是否存在文件夹，如不存在则创建文件夹，以便存储文档
    addr = 'E:/中国铁塔在线商务平台招标公告/'
    if not os.path.exists(addr):
        os.makedirs(addr)
    driver_path = r'D:\driver\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=driver_path)
    for each in ids:
        #根据id遍历所有招标公告页面
        url = "http://www.tower.com.cn/default/main/index/noticedetail.jsp?_operation=notice&_notice=6&_id="+each
        driver.get(url)
        html = driver.page_source
        # 获取当前招标公告标题
        t=html.find('<div class="content_title" id="_title">')
        title = html[t+39:html.find('</div>',t)]
        # 获取投标人资格要求部分
        content=html[html.find('投标人资格要求'):html.find('资格审查方法')]
        # 当前招标公告中我司具有的资质列表
        has_qualification = []
        for item in qualification:
            # 遍历从文档中读取的我司资质列表
            if content.find(item) != -1:
                # 如果在投标人资格要求中找到我司具有的资质，则添加进当前招标公告中我司具有的资质列表
                has_qualification.append(item)
        if len(has_qualification)>0:
            #如果当前招标公告中我司具有的资质列表长度大于0，则将此招标公告以html形式保存，并将当前招标公告中我司具有的资质列表以txt形式保存
            f = open(addr+title+'.html','w',encoding ='utf-8')  ##ffilename可以是原来的txt文件，也可以没有然后把写入的自动创建成txt文件
            top0=html.find('<div class="header-main">')
            top=html[top0:html.find('</div>',top0+4500)]
            html=html.replace(top,'')
            foot0=html.find('<div class="new_footer"')
            foot=html[foot0:html.find('</div>',foot0+440)]
            html=html.replace(foot,'')
            f.write(str(html))
            f.close()
            f = open(addr+ title + '_我司具有资质.txt', 'w', encoding='utf-8')
            f.write(str(has_qualification))
            f.close()
        time.sleep(2)
    driver.quit()

if __name__=='__main__':
    get_biddinglist()

