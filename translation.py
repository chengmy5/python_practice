import urllib.request
import urllib.parse
import json

def translate(word):

    url='http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    head={}
    head['User-Agent']='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    data={}
    data['i']=word
    data['from']='AUTO'
    data['to']='AUTO'
    data['smartresult']='dict'
    data['client']='fanyideskweb'
    data['salt']='16093097122972'
    data['sign']='d89103d9b056fc5d9905055d525faa5b'
    data['lts']='1609309712297'
    data['bv']='b396e111b686137a6ec711ea651ad37c'
    data['doctype']='json'
    data['version']='2.1'
    data['keyfrom']='fanyi.web'
    data['action']='FY_BY_CLICKBUTTION'
    data=urllib.parse.urlencode(data).encode('utf-8')
    # print(data)
    resopnse=urllib.request.urlopen(url,data)
    # resopnse.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36')
    html=resopnse.read().decode('utf-8')

    html=json.loads(html)
    print('原文为：{}'.format(html['translateResult'][0][0]['src']))
    print('译文为：{}'.format(html['translateResult'][0][0]['tgt']))



word=input('请输入要翻译的文字：')
translate(word)
