//最大子序列和
class Solution {
    //f[i]表示前i个元素和的最大值
    public int maxSubArray(int[] nums) {
        int max = Integer.MIN_VALUE;
        //初始化old，即为f[0]
        int pre = 0;
       
        for(int i = 0;i<nums.length;i++){
            //current即为f[i]
            //f[i] = max(f[i-1],0)+f[i]
            int current = Math.max(pre,0)+nums[i];
            max = Math.max(current,max);
            pre = current;
        }
        return max;

    }
}
