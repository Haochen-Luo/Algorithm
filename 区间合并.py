class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        res = []
        intervals.sort(key=lambda x:(x[0],x[1]))
        left = intervals[0][0]
        right = intervals[0][1]

        for i in range(1,len(intervals)):
            if right>=intervals[i][0]:
                right = max(intervals[i][1],right)

            else:
                res.append([left,right])
                left = intervals[i][0]
                right = intervals[i][1]
        res.append([left,right])
       
        return res
