这个目录下的代码会收录一些通用的但是自己无法快速一遍过的代码，或者自己写的冗长了的代码
比如快速排序，思路当然简单，但是自己如果一段时间不写又会无法快速写出来。


自己的版本。
```java
class Solution {
   public void merge(int[] nums1, int m, int[] nums2, int n) {
        int n1 = m-1;
        int n2 = n-1;
        int tail = m+n-1;
        while (tail!=-1){
            if(n1==-1){
                for(int i = tail;i>=0;i--){
                    nums1[i] = nums2[n2];
                    n2--;
                }
                return;
            }
            if(n2==-1){
                for(int i = tail;i>=0;i--){
                    nums1[i] = nums1[n1];
                    n1--;
                }
                return;
            }
            if(nums1[n1]>nums2[n2]){
                nums1[tail] = nums1[n1];
                n1--;
                tail--;
            }else {
                // System.out.println(tail);
                // System.out.println(n2);
                nums1[tail] = nums2[n2];
                n2--;
                tail--;
             }
        }
    }
}
```
优化代码风格后的版本
```java
class Solution {
   public void merge(int[] nums1, int m, int[] nums2, int n) {
        int n1 = m-1;
        int n2 = n-1;
        int tail = m+n-1;
        while (tail!=-1){
            if(n1==-1){
                nums1[tail--] = nums2[n2--];
            }else if(n2==-1){
                nums1[tail--] = nums1[n1--];
            }else if(nums1[n1]>nums2[n2]){
                nums1[tail--] = nums1[n1--];
            }else if(nums1[n1]<=nums2[n2]){
                nums1[tail--] = nums2[n2--];
            }
        }
    }
}
```
