def contains_duplicate(nums):
    return len(nums)!=len(set(nums))

assert contains_duplicate([1,2,3,4])==False
assert contains_duplicate([1,2,2,4])==True
print("all test cases passed")

