## 沿着某一个轴
```python
x = np.array([
    [[1,8,12],
     [2,9,12]],
    [[3,8,12],
     [4,9,12]],
    [[3,8,12],
     [4,9,12]],
     [[3,8,12],
     [4,9,12]],
])
print(x[:,:,0])
print(x[:,:,1])
print(x[:,:,2])
print((x.shape))
print("求和哪一个维度，哪一维度就没了")
print()
print(x.sum(axis = 0))
print((x.sum(axis = 0)).shape)
print()
print(x.sum(axis = 1))
print((x.sum(axis = 1)).shape)
print()
print(x.sum(axis = 2))
print((x.sum(axis = 2)).shape) 
```
```
output
>>>
[[1 2]
 [3 4]
 [3 4]
 [3 4]]
[[8 9]
 [8 9]
 [8 9]
 [8 9]]
[[12 12]
 [12 12]
 [12 12]
 [12 12]]
(4, 2, 3)
求和哪一个维度，哪一维度就没了

[[10 32 48]
 [14 36 48]]
(2, 3)

[[ 3 17 24]
 [ 7 17 24]
 [ 7 17 24]
 [ 7 17 24]]
(4, 3)

[[21 23]
 [23 25]
 [23 25]
 [23 25]]
(4, 2)
```
----------
## 拼接
```python
import numpy as np
a = np.array([[1,2,3],[1,2,3]])
b = np.array([[1,2,3],[1,2,3]])
c = np.concatenate((a,b),axis = 0)
print(c)
c = np.concatenate((a,b),axis = 1)
print(c)
"""
[[1 2 3]
 [1 2 3]
 [1 2 3]
 [1 2 3]]
[[1 2 3 1 2 3]
 [1 2 3 1 2 3]]
"""
```
## np.random.choice

Use np.random.choice.

Example of how to use np.random.choice():

np.random.seed(0)
probs = np.array([0.1, 0.0, 0.7, 0.2])
idx = np.random.choice(range(len(probs), p = probs)

