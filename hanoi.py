# def hanoi(n,x,y,z):
#     '''
#     解决汉诺塔问题
#     :param n:
#     :param x:
#     :param y:
#     :param z:
#     :return:
#     '''
#     if n==1:
#         print(x,'------->',z)#如果只有一层，直接从x处移动到z处
#         pass
#     else:
#         hanoi(n-1,x,z,y)#将前n-1个盘子从x移动到y上
#         print(x,'------->',z)#将最底下的最后一个盘子从x移动到z上
#         hanoi(n-1,y,x,z)#将前n-1个盘子从y移到z上
#         pass
#     pass
# hanoi(5,'x','y','z')
# import os
# print(os.getcwd())

import easygui
print(easygui.__file__)
