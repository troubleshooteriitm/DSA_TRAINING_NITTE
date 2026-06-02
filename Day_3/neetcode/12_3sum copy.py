def _3sum(nums):
        res=[]
        nums.sort()
        for i,num in enumerate(nums):
            if i>0 and num==nums[i-1]:
                continue
            l,r=i+1,len(nums)-1
            while l<r:
                sum=num+nums[l]+nums[r]
                if sum>0:
                    r-=1
                elif sum<0:
                    l+=1
                else:
                    res.append([nums[l],nums[r],num])
                    l+=1
                    while nums[l]==nums[l-1] and l<r:
                        l+=1
        print(res)
        return res



assert _3sum([-1,0,1,2,-1,-4])==[[-1,-1,2],[-1,0,1]]
print("all cases passed!")