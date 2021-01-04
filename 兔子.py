# def rabbit(mon):
#     res=[]
#     res.append(1)
#     res.append(1)
#     i=1
#     while i<=mon:
#
#     pass

def rabbit(mon):
    if mon==1 or mon==2:
        return 1
    else:
        return rabbit(mon-1)+rabbit(mon-2)
    pass

print(rabbit(40))