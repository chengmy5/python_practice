import urllib.request
width=int(input("请输入宽度："))
heigth=int(input("请输入高度："))

def download(w,h):
    '''
    根据输入的宽高下载一张猫咪图片
    :param w: 宽度
    :param h: 高度
    :return:
    '''
    response=urllib.request.urlopen("http://placekitten.com/{}/{}".format(w,h))
    cat_img=response.read()
    with open('cat_{}_{}.jpg'.format(w,h),'wb') as f:
        f.write(cat_img)

download(width,heigth)