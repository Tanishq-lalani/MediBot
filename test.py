nums =[1,2,3,4]
n = len(nums)
ans = [1] * n
for i in range(1,n):
    ans[i] = ans[i-1] * nums[i-1]
print(ans)
