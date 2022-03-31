## VISA考试最大
### Minimum number of groups of nodes such that no ancestor is present in the same group
Difficulty Level : Hard
Last Updated : 07 Jun, 2021
Given a tree of N nodes. The task is to form the minimum number of groups of nodes such that every node belong to exactly one group, and none of its ancestors are in the same group. The parent of each node is given (-1 if a node does not have a parent).
Examples: 

Input: par[] = {-1, 1, 2, 1, 4} 
Output: 3 
The three groups can be: 
Group 1: {1} 
Group 2: {2, 4} 
Group 3: {3, 5}
Input: par[] = {-1, 1, 1, 2, 2, 5, 6} 
Output: 5 

```py
# Python3 implementation of the approach
 
# Function to return the depth of the tree
def findDepth(x, child):
    mx = 0
     
    # Find the maximum depth
    # of all its children
    for ch in child[x]:
        mx = max(mx, findDepth(ch, child))
         
    # Add 1 for the depth
    # of the current node
    return mx + 1
 
# Function to return the minimum 
# number of groups required
def minimumGroups(n, par):
    child = [[] for i in range(n + 1)]
     
    # For every node create a list
    # of its children
    for i in range(0, n):
        if (par[i] != -1):
            child[par[i]].append(i)
    res = 0
    for i in range(0, n):
         
        # If the node is root
        # perform dfs starting with this node
        if(par[i] == -1):
            res = max(res, findDepth(i, child))
    return res
 
# Driver Code
array = [0, -1, 1, 1, 2, 2, 5, 6]
print(minimumGroups(len(array), array))
 
# This code is contributed
# by SidharthPanicker
```
