x=[1,2,3]
try:
    for i in range(len(x)+1):
        print(x.pop())
except:
    print("bro index out of range bro!!!")
# IndexError