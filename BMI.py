high=float(input("请输入您的身高(米):"))
weight=float(input("请输入您的体重(公斤):"))
bmi=weight/(high**2)
if bmi<18.5:
    print("过轻")
    pass
elif 18.5<=bmi<25:
    print("正常")
    pass
elif 25<=bmi<28:
    print("过重")
    pass
elif 28<=bmi<32:
    print("肥胖")
    pass
elif 32<=bmi:
    print("严重肥胖")
    pass
print(bmi)