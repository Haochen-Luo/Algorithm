### 求argmax 和one-hot
```python
xx = tf.constant([[1,2],[2,3]])
k = tf.math.argmax(xx,axis = -1)
print(k)
ten_hot = tf.one_hot(indices = k, depth =10)
print(ten_hot)
three_hot = tf.one_hot(indices = k, depth =3)
print(three_hot)
```
output
```

tf.Tensor([1 2], shape=(2,), dtype=int64)
tf.Tensor(
[[0. 1. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 1. 0. 0. 0. 0. 0. 0. 0.]], shape=(2, 10), dtype=float32)
tf.Tensor(
[[0. 1. 0.]
 [0. 0. 1.]], shape=(2, 3), dtype=float32)
```
