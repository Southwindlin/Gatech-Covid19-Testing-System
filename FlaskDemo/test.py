a = 3
def s(a):
    return a+1
b = c if (c:=s(a))==4 else c+1
print(b,c)