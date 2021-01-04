age=25
i=1
while i<=3:
    guess=int(input("你猜我几岁："))
    if guess==age:
        print("恭喜你猜对了")
        break
        pass
    if i==3:
        jx=input("你已经答错三次了，还要继续吗？(继续：y，退出：n)")
        if jx=='y':
            i=0
            pass
        elif jx=='n':
            pass
        pass
    i += 1
    pass
else:
    print("游戏结束")