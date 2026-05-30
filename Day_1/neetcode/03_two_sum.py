def two_sum(nums,target):
    seen=dict()
    for index,num in enumerate(nums):
        diff = target-num 
        if diff in seen:
            return [seen[diff],index]
        else:
            seen[num]=index

# approach
    # first create empty dict as seen {num:index}
    # enumerate the nums for index and num
    # calculate the diff
    # if diff in seen return
    # else add the num as key and index as value to the dict

assert two_sum([4,5,6,7],10)==[0,2]
assert two_sum([4,5,6,7],12)==[1,3]
print("all cases passed")