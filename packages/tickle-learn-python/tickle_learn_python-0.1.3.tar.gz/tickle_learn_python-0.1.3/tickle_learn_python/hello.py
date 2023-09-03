def sayHello(name):
    return "Hello, "+name

def decimalToBinary(quo):
    result=[]
    binary=""
    while(quo>1):
        rem=quo%2
        result.append(rem)
        quo=int((quo-rem)/2)
    result.append(quo)
    result.reverse()
    for i in result:
        binary=binary+str(i)
    return binary


print(decimalToBinary(100))