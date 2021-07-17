import os
import shutil

#设定文件路径
path='C:\\Users\\ASUS i5\\Desktop\\heros\\'

#对目录下的文件进行遍历
for category in os.listdir(path):
    newPath=path+category
    i=1
    for pic in os.listdir(newPath):
        new_name = pic.replace(pic, category+'_'+str(i)+'.jpg')
        os.rename(os.path.join(newPath, pic), os.path.join(newPath, new_name))
        src=os.path.join(newPath,new_name)
        dst=os.path.join(path,new_name)
        shutil.move(src,dst)
        i+=1