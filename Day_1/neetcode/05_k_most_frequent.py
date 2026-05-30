from collections import Counter
def k_most_frequent(nums,k):
    mk=Counter(nums).most_common(k)
    op=[]
    for num,count in mk:
        op.append(num)
    return op
    


assert k_most_frequent([1,2,3,2,3,3],2)==[3,2]
assert k_most_frequent([1,1,1,2,3,3,4,4,5,4,4],3)==[4,1,3]
