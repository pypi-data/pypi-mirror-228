def decimalToBinary(num):
    result=[]
    quo=num
    while(quo>1):
        rem=num%2
        result.append(rem)
        quo=(quo-rem)/2
    result.append(rem)
    return result.reverse

