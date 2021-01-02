import os
import random
from shutil import copy

new_name=['广州开发区永茂西路搬迁D-ELH',
'亨元村微网格综合接入机房2新建48芯上联光缆2',
'姬堂村微网格综合接入机房1新建48芯上联光缆1',
'广州开发区LG科学城厂区（搬迁）E-ELW',
'广州开发区万科尚城E-ELW（优化）',
'广州开发区黄埔海关技术用房E-ELW',
'广州开发区永和禾丰（搬迁二）F-ELH',
'广州开发区黄埔花园（搬迁）1E-ELW（拉远1）',
'广州开发区黄埔花园（搬迁）1E-ELW（拉远7）',
'广州开发区黄埔花园（搬迁）1E-ELW（拉远4）',
'广州开发区黄埔花园（搬迁）1E-ELW（拉远12）',
'广州开发区黄埔花园（搬迁）1E-ELW（拉远2）',
'广州开发区黄埔花园（搬迁）1E-ELW（拉远8）',
'广州开发区黄埔花园（搬迁）1E-ELW（拉远5）',
'广州开发区黄埔花园（搬迁）1E-ELW（拉远9）',
'广州开发区黄埔花园（搬迁）1E-ELW（拉远6）',
'广州开发区黄埔花园（搬迁）1E-ELW（拉远10）',
'广州开发区大田山路D-ELH',
'广州开发区官路山DC-EDH （拉远3）',
'广州开发区官路山DC-EDH （拉远1）',
'广州开发区东江大道南（搬迁）F-ELH',
'广州开发区保利罗兰国际AE-ELW',
'镇龙大道微网格综合接入机房1新建48芯上联光缆2',
'镇龙大道微网格综合接入机房1新建48芯上联光缆1',
'广州开发区牛鼻山隧道E-ELW（优化）（拉远1）',
'广州开发区牛鼻山隧道E-ELW（优化）（拉远2）',
'广州开发区牛鼻山隧道E-ELW（优化）（拉远3）',
'万科东荟城（OLT下沉）（优化）',
'广州开发区黄埔花园（搬迁）1E-ELW（拉远3）',
]
new_lenght=[0.812,
1.502,
2.76,
1.218,
1.268,
0.558,
0.2,
0.68,
0.507,
0.568,
0.73,
0.73,
0.558,
0.629,
0.253,
0.456,
0.253,
1.725,
0.698,
0.568,
0.832,
0.253,
0.12,
0.466,
0.568,
1.218,
1.928,
0.355,
0.66
]
copy_name=['亨元村微网格综合接入机房1新建48芯上联光缆1', '坑围微网格综合接入机房1新建48芯上联光缆1', '夏园新圩微网格综合接入机房1新建48芯上联光缆1',
           '广州开发区万科城市之光E-ELW', '广州开发区中新知识城西F-ELH（优化）', '广州开发区九明地D-ELH', '广州开发区华盈商务大厦E-ELW',
           '广州开发区岭南学院东DC-EDH', '广州开发区岭南学院东DC-EFH', '广州开发区广州标致（搬迁）D-ELH', '广州开发区广州绿地城二期E-ELW',
           '广州开发区枫下村南DC-EDH', '广州开发区水西村西F-ELH（优化）', '广州开发区沧联中村F-ELH（优化）', '广州开发区港湾医院E-ELW',
           '广州开发区牛鼻山隧道E-ELW（优化）', '广州开发区石桥邻里汇E-ELW', '广州开发区碧桂园克拉广场E-ELW', '广州开发区科学城员工楼E-ELW',
           '广州开发区科学城绿地中央广场三期E-ELW', '广州开发区萝岗镇龙村口F-ELH', '广州开发区蔚蓝大厦（搬迁）E-ELW', '广州开发区雅居乐科学城四期E-ELW',
           '广州开发区黄埔新港2DC-EFH', '广州开发区黄埔花园（搬迁）E-ELW', '广州开发区黄竹园GS-EFH', '广州开发区黄陂F-ELH（优化）',
           '广州鱼茅路HE（微改光）', '新庄村微网格综合接入机房1新建48芯上联光缆1', '新庄村微网格综合接入机房2新建48芯上联光缆1',
           '萝岗范屋微网格综合接入机房2新建48芯上联光缆1', '鹏博士机房三层MD5机房新建48芯接入光缆1', '鹏博士机房三层MD5机房新建48芯接入光缆2']
copy_value_1310=[1.65832,1.16854,2.47371,1.37256,1.38659,1.15328,2.00001,1.61139,1.99899,1.41175,1.18817,2.00002,1.65529,1.15512,
                 1.38263,1.47862,1.09826,1.55031,1.13648,1.35682,1.40089,2.02119,1.13287,1.73511,2.00191,1.40182,1.38615,1.41127,
                 1.45386,2.00012,1.77254,1.402287,1.13568]
copy_value_1550=[1.71563,1.15329,2.22548,1.39528,1.99999,1.15248,2.00002,1.36852,2.00101,1.99998,1.09824,1.99899,1.72591,1.11095,
                 1.41058,2.01157,1.06849,1.77081,1.10845,1.99989,1.48918,1.49055,1.10851,1.68256,2.01005,1.39597,2.01105,2.00012,
                 1.47211,2.00001,1.68325,1.37266,1.12155]

def get_addr(list,old_path,new_flie,new_path):
    if new_path[-1]=='1':
        i = 1
    elif new_path[-1]=='2':
        i = 10
    for each in list:
        old_path_full=os.path.join(old_path,each)
        new_path_full=os.path.join(new_path,new_flie+'('+str(i)+').SOR')
        copy(old_path_full,new_path_full)
        # print(old_path_full+'   '+new_path_full)
        i+=1

def copy_update_excel(old_dir,new_dir,file_name,data1,data2):
    print(old_dir+' '+new_dir+' '+file_name)
    print(data1,data2)
    pass
def copy_file():
    for each in new_name:
        num=random.randint(0,32)
        #先创建文件夹
        # os.makedirs('E:/ZTSJ-16/'+each+'/1310/1')
        # os.makedirs('E:/ZTSJ-16/'+each+'/1310/2')
        # os.makedirs('E:/ZTSJ-16/'+each+'/1550/1')
        # os.makedirs('E:/ZTSJ-16/'+each+'/1550/2')
        # #获取新创建的文件夹名称
        # new_path_1310_1='E:/ZTSJ-16/'+each+'/1310/1'
        # new_path_1310_2='E:/ZTSJ-16/'+each+'/1310/2'
        # new_path_1550_1='E:/ZTSJ-16/'+each+'/1550/1'
        # new_path_1550_2='E:/ZTSJ-16/'+each+'/1550/2'
        #
        # #获取要复制的文件列表
        # old_1310_1=os.listdir('E:/ZTSJ-05/'+copy_name[num]+'/1310/1/')
        # old_path='E:/ZTSJ-05/'+copy_name[num]+'/1310/1/'
        # get_addr(old_1310_1,old_path,each,new_path_1310_1)
        # old_1310_2=os.listdir('E:/ZTSJ-05/'+copy_name[num]+'/1310/2/')
        # old_path = 'E:/ZTSJ-05/' + copy_name[num] + '/1310/2/'
        # get_addr(old_1310_2, old_path, each, new_path_1310_2)
        # old_1550_1=os.listdir('E:/ZTSJ-05/'+copy_name[num]+'/1550/1/')
        # old_path = 'E:/ZTSJ-05/' + copy_name[num] + '/1550/1/'
        # get_addr(old_1550_1, old_path, each, new_path_1550_1)
        # old_1550_2=os.listdir('E:/ZTSJ-05/'+copy_name[num]+'/1550/2/')
        # old_path = 'E:/ZTSJ-05/' + copy_name[num] + '/1550/2/'
        # get_addr(old_1550_2, old_path, each, new_path_1550_2)

        old_dir='E:/ZTSJ-05/' + copy_name[num] + '/'
        new_dir='E:/ZTSJ-16/'+each+'/'
        flie_name=each+'.SOR'

        data1=new_lenght[new_name.index(each)]/copy_value_1310[num]
        data2=new_lenght[new_name.index(each)]/copy_value_1550[num]
        copy_update_excel(old_dir,new_dir,flie_name,data1,data2)


if __name__=='__main__':
    copy_file()
