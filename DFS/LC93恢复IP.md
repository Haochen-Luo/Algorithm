```java
class Solution {
   List<String> res = new ArrayList<>();
    public List<String> restoreIpAddresses(String s) {
        dfs(0,"0","", s);
        return res;
    }

    public void dfs(int num,String tr,String temp,String remain){
        
            if (num==4){
                if (remain.equals("")&&Integer.parseInt(tr)>=0&&Integer.parseInt(tr)<=255&&!(tr.length()!=1&&tr.charAt(0)=='0')){
                    res.add(temp.substring(1));
                }else{
                    return;
                }
            }
            
        
        if (Integer.parseInt(tr)>=0&&Integer.parseInt(tr)<=255){
            if (tr.length()!=1&&tr.charAt(0)=='0'){
                return;
            }
            if(remain.length()>=1){
                dfs(num+1,remain.substring(0,1),temp+"."+remain.substring(0,1),remain.substring(1));}
            if(remain.length()>=2){
                dfs(num+1,remain.substring(0,2),temp+"."+remain.substring(0,2),remain.substring(2));}
            if(remain.length()>=3){
            dfs(num+1,remain.substring(0,3),temp+"."+remain.substring(0,3),remain.substring(3));}
        }


    }
}
```
