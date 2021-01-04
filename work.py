def sum(*args):
    sum=0
    for item in args:
        sum+=item
        pass
    return sum
print(sum(1,2,3,4,6))

def jishu(*args):
    li=[]
    i=0
    while i<len(args):
        li.append(args[i])
        i+=2
        pass
    return li
print(jishu(1,2,3,4,5,6,7,8,9))

def two(**kwargs):
    result={}
    for key,value in kwargs.items():
        if len(value)>2:
            result[key]=value[:2]
            pass
        else:
            result[key]=value
            pass
        pass
    return result
    pass

a=two(name='adssf',age='1234',pro='jishu')
print(a)