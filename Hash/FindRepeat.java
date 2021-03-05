// https://leetcode-cn.com/problems/shu-zu-zhong-zhong-fu-de-shu-zi-lcof/solution/yuan-di-zhi-huan-shi-jian-kong-jian-100-by-derrick/
class Solution {
    public int findRepeatNumber(int[] nums) {
        int temp;
        for(int i=0;i<nums.length;i++){
            while (nums[i]!=i){
                if(nums[i]==nums[nums[i]]){
                    return nums[i];
                }
                temp=nums[i];
                nums[i]=nums[temp];
                nums[temp]=temp;
            }
        }
        return -1;
    }
}

作者：derrick_sun
链接：https://leetcode-cn.com/problems/shu-zu-zhong-zhong-fu-de-shu-zi-lcof/solution/yuan-di-zhi-huan-shi-jian-kong-jian-100-by-derrick/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

这种原地置换的想法确实挺精妙的。

1、题目明确说明了数组长度为n，范围为 n-1，也就是若无重复元素排序后下标0123对应的数字就应该是0123；

2、对数组排序，其实也就是让萝卜归位，1号坑要放1号萝卜，2号坑要放2号萝卜......排序过程中查找有无重复元素。先考虑没有重复元素的情况：

 nums[i]     3  1  0  2   萝卜   
     i       0  1  2  3   坑  
0号坑说我要的是0号萝卜，不要3号萝卜，所以会去和3号坑的萝卜交换，因为如果0号坑拿了3号坑的3号萝卜，那说明3号坑装的也肯定是别人家的萝卜，所以要跟3号坑换，换完是这样的：

 nums[i]     2  1  0  3   萝卜  
     i       0  1  2  3   坑 
然而0号坑还没找到自己的萝卜，它不要2号萝卜，又去和2号坑的萝卜交换，换完是这样的：

 nums[i]     0  1  2  3   萝卜 
     i       0  1  2  3   坑  
这时候刚好就是一一对应的，交换过程也不会出现不同坑有相同编号的萝卜。要注意交换用的是while，也就是0号坑只有拿到0号萝卜，1号坑才能开始找自己的萝卜。

3、如果有重复元素，例如：

 nums[i]     1  2  3  2    萝卜
     i       0  1  2  3    坑
同样的，0号坑不要1号，先和1号坑交换，交换完这样的：

 nums[i]     2  1  3  2    萝卜
     i       0  1  2  3    坑
0号坑不要2号萝卜，去和2号坑交换，交换完这样的：

 nums[i]     3  1  2  2    萝卜
     i       0  1  2  3    坑
0号坑不要3号萝卜，去和3号坑交换，交换完这样的：

 nums[i]     2  1  2  3    萝卜
     i       0  1  2  3    坑
0号坑不要2号萝卜，去和2号坑交换，结果发现你2号坑也是2号萝卜，那我还换个锤子，同时也说明有重复元素出现。

4、总结

其实这种原地交换就是为了降低空间复杂度，只需多要1个坑来周转交换的萝卜就好了，空间复杂度O（1）。
