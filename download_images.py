import urllib.request
import os
import time
import base64
def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36')
    response = urllib.request.urlopen(req)
    html = response.read()
    return html

def get_page(url):
    html=url_open(url).decode('utf-8')

    a=html.find('current-comment-page')+23
    b=html.find(']',a)

    return html[a:b]
def find_images(page_url):
    html=url_open(page_url).decode('utf-8')
    img_addres=[]

    a=html.find('img src=')
    while a!=-1:
        b = html.find('.jpg', a, a + 255)
        if b!=-1:
            img_addres.append('http:'+html[a+9:b+4])
        else:
            b=a+9
        a=html.find('img src=',b)
    return img_addres

def save_images(folder,images_address):
    for each in images_address:
        filename=each.split('/')[-1]
        with open(filename,'wb') as f:
            img=url_open(each)
            f.write(img)

def page_code(num):
    now_date=time.strftime('%Y%m%d',time.localtime())#获取当天的年月日
    code=(now_date+'-'+str(num)).encode('utf-8')#将年月日与页码中间以‘-’进行拼接
    page_code=str(base64.b64encode(code),'utf-8')#将拼接好的字符串以base64方式加密
    return page_code
    # print(page_code)
    pass

def download_images(folder='OOXX',pages=10):
    os.mkdir(folder)
    os.chdir(folder)

    url='http://jandan.net/girl'
    page_num=int(get_page(url))
    for i in range(pages):
        page_num-=i
        pagecode=page_code(page_num)
        page_url=url+'/'+pagecode+'#comments'
        images_address=find_images(page_url)
        save_images(folder,images_address)


if __name__=='__main__':
    download_images()