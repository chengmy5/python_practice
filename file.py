# f=open('E:/我司具有资质.txt', 'r', encoding='utf-8')
# content=f.read()
# qualification=content.split(',')
# print(qualification)
# f.close()
import os
a=os.path.exists('E:file')
b=os.path.exists('E:/bidding_information')
# os.makedirs('E:/bidding_information')
print(a)
print(b)


