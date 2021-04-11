leetcode开局
https://leetcode-cn.com/problems/two-sum/
```java
public static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> H = new HashMap<>();
        //插入值和对应的索引
        //注意查找元素是否在哈希表的时间复杂度是O(1)!!!!!
        for (int i = 0; i < nums.length; i++) {//O(n)
            if (H.containsKey(target - nums[i])) {//O(1)，总共是O(n)
                return new int[]{H.get(target - nums[i]), i};
            }
            H.put(nums[i], i);
        }
        return new int[0];
    }
```
