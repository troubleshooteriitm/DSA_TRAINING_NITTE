def encode(strs):
    op=""
    for i in strs:
        op+=str(len(i))+'#'+i
    return op


def decode(str):
    op=[]
    while str:
        ind=str.find("#") 
        num=int(str[:ind]) 
        op_string=str[ind+1:num+ind+1]
        op.append(op_string)
        str=str[num+ind+1:]
    return op



assert encode(["Hello","World"])=="5#Hello5#World"
assert encode(["Gokulakrishnan","Shashwath"])=="14#Gokulakrishnan9#Shashwath"
assert decode(encode(["Hello","World"]))==["Hello","World"]
assert decode(encode(["Gokulakrishnan","Shashwath"]))==["Gokulakrishnan","Shashwath"]

print("all test cases passed")