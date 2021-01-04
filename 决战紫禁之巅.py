class Person:
    def __init__(self,name,blood):
        self.name=name
        self.blood=blood
        pass
    def __str__(self):
        return '【{}】还剩{}滴血'.format(self.name,self.blood)
        pass
    def tong(self,enemy):
        enemy.blood-=10
        print('【{}】砍了【{}】一刀,【{}】掉了10滴血'.format(self.name,enemy.name,enemy.name))
        pass
    def kan(self,enemy):
        enemy.blood -= 15
        print('【{}】砍了【{}】一刀,【{}】掉了15滴血'.format(self.name, enemy.name, enemy.name))
        pass
    def yao(self):
        self.blood+=10
        print('【{}】吃了一颗药，补了10点血'.format(self.name))
        pass
    pass
xmcx=Person('西门吹雪',100)
ygc=Person('叶孤城',100)
xmcx.kan(ygc)
print(xmcx)
print(ygc)
ygc.kan(xmcx)
print(xmcx)
print(ygc)