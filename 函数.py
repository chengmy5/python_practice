# def printMessage():
#     '''
#     无参函数
#     :return:
#     '''
#     print('小张的身高是%d'%185)
#     print('小张的体重是%d'%65.5)
#     print('小张的爱好是%s'%'打球')
#     print('小张的专业是%s'%'编码')
#     pass
# printMessage()

def printMessage(name,height,weight,hobby,pro):
    print('%s的身高是%f'%(name,height))
    print('%s的体重是%f'%(name,weight))
    print('%s的爱好是%s'%(name,hobby))
    print('%s的专业是%s'%(name,pro))
    pass
printMessage('小李',180,60.1,'上网冲浪','土木')

a=1
print(type(a))