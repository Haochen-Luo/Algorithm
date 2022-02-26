类似最长上升子序列
```py
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        len_map = dict()
        for i in wordDict:
            if len(i) in len_map.keys():
                len_map[len(i)].append(i)
            else:
                len_map[len(i)] = [i]

        state = [0]*len(s)
        for curr_len in range(len(s)):
            if self.check(len_map,s[0:curr_len+1]):
                state[curr_len] = 1
            else:
                res_bool = False
                for idx in range(0,curr_len):
                    if  state[idx]==1:
                        if self.check(len_map,s[idx+1:curr_len+1]):
                            res_bool = True
                if res_bool:
                    state[curr_len]=1
        # print(state)
        if state[len(state)-1]==1:
            return True
        else:
            return False

    def check(self,len_map:dict,pattern:str):
        exist = False
        if len(pattern) not in len_map:
            return False

        for i in len_map[len(pattern)]:
            if i==pattern:
                exist = True
        return exist
```
