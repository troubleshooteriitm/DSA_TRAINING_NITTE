def two_sum_2(numbers,target):
    left,right=0,len(numbers)-1
    while left<right:
        sum=numbers[left]+numbers[right]
        if target==sum:
            return [left+1,right+1]
        elif sum<target:
            left+=1
        else:
            right-=1
assert two_sum_2([1,2,3,4],3)==[1,2]
print("all pass")
