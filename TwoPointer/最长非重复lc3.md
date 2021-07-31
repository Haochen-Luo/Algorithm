注意右移动指针的时候要break
```java
public static int lengthOfLongestSubstring(String s) {
        if(s.length()==1||s.length()==0){
            return s.length();
        }
        int res = 0;
        HashSet<Character> h = new HashSet<>();
        int right = 1;
        h.add(s.charAt(0));
        for(int i = 0;i<s.length();i++){
            while(!h.contains(s.charAt(right))){
                h.add(s.charAt(right));
                right++;
                if(right==s.length()){
                    break;
                }
            }
            res = Math.max(h.size(),res);
            h.remove(s.charAt(i));
            //可以中止移动，因为从右往左移动而且右指针达到了最右侧，再继续枚举一定是递减的，不会获得最大值
            if(right==s.length()){
                break;
            }
        }
        return res;

    }
```
