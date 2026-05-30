def product(nums):
    forward=[]
    prd=1
    for i in nums:
        prd=prd*i
        forward.append(prd)
    print(forward)

    backward=[]
    prd=1
    for i in nums[::-1]:
        prd=prd*i
        backward.append(prd)
    backward=backward[::-1]
    print(backward)
    # core logic
    op=[]
    for i in range(nums)



product([1,2,3,4])

# assert product([1,2,3,4])==[24,12,8,6]
