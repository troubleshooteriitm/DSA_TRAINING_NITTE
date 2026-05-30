from collections import Counter
nums=[1,1,1,2,3,3,4,4,5,4,4]
k=3


mk=Counter(nums).most_common(k)#
# {4:4,1:3,3:2,2:1,5:1}
op=[]
for num,count in mk:
    op.append(num)
print(op)
