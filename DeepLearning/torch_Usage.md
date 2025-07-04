### with torch.no_grad()

在讲述with torch.no_grad()前，先从requires_grad讲起
#### **requires_grad**
```
在pytorch中，tensor有一个requires_grad参数，如果设置为True，则反向传播时，该tensor就会自动求导。
tensor的requires_grad的属性默认为False,若一个节点（叶子变量：自己创建的tensor）requires_grad被设置为True，
那么所有依赖它的节点requires_grad都为True（即使其他相依赖的tensor的requires_grad = False）。
```
```python
x = torch.randn(10, 5, requires_grad = True)
y = torch.randn(10, 5, requires_grad = False)
z = torch.randn(10, 5, requires_grad = False)
w = x + y + z
w.requires_grad

True
```
#### **volatile**

首先说明，该用法已经被移除，但为了说明torch.no_grad，还是需要讲解下该作用。
在之前的版本中，tensor（或者说variable，以前版本tensor会转化成variable，目前该功能也被废弃，直接使用tensor即可）还有一个参数volatile，
如果一个tensor的volatile = True，那么所有依赖他的tensor会全部变成True，反向传播时就不会自动求导了，因此大大节约了显存或者说内存。
既然一个tensor既有requires_grad，又有volatile，那么当两个参数设置相矛盾时怎么办？
volatile=True的优先级高于requires_grad，即当volatile = True时，无论requires_grad是Ture还是False，反向传播时都不会自动求导。
volatile可以实现一定速度的提升，并节省一半的显存，因为其不需要保存梯度。（volatile默认为False，这时反向传播是否自动求导，取决于requires_grad）
#### **with torch.no_grad**
上文提到volatile已经被废弃，替代其功能的就是with torch.no_grad。
作用与volatile相似，即使一个tensor（命名为x）的requires_grad = True，由x得到的新tensor（命名为w-标量）requires_grad也为False，且grad_fn也为None,
即不会对w求导。
例子如下所示：
```python
x = torch.randn(10, 5, requires_grad = True)
y = torch.randn(10, 5, requires_grad = True)
z = torch.randn(10, 5, requires_grad = True)
with torch.no_grad():
    w = x + y + z
    print(w.requires_grad)
    print(w.grad_fn)
print(w.requires_grad)

False
None
False
```
下面可以以一个具体的求导例子看一看：
```python
x = torch.randn(3, 2, requires_grad = True)
y = torch.randn(3, 2, requires_grad = True)
z = torch.randn(3, 2, requires_grad = False)
w = (x + y + z).sum()
print(w)
print(w.data)
print(w.grad_fn)
print(w.requires_grad)
w.backward()
print(x.grad)
print(y.grad)
print(z.grad)

tensor(0.0676, grad_fn=<SumBackward0>)
tensor(0.0676)
<SumBackward0 object at 0x0000026F076CE710>
True
tensor([[1., 1.],
        [1., 1.],
        [1., 1.]])
tensor([[1., 1.],
        [1., 1.],
        [1., 1.]])
None
```
可以看到当w的requires_grad = True时，是可以求导的，而且仅对设置了requires_grad = True的x和y求导，没有对z进行求导
```python
x = torch.randn(10, 5, requires_grad = True)
y = torch.randn(10, 5, requires_grad = True)
z = torch.randn(10, 5, requires_grad = True)
with torch.no_grad():
    w = (x + y + z)
    print(w.requires_grad)
    print(x.requires_grad)
    w.backward()
False
True
RuntimeError: element 0 of tensors does not require grad and does not have a grad_fn
```
link：https://blog.csdn.net/weixin_43178406/article/details/89517008


### to.device
It is necessary to have both the model, and the data on the same device, either CPU or GPU, for the model to process data. Data on CPU and model on GPU, or vice-versa, will result in a Runtime error.

You can set a variable device to cuda if it's available, else it will be set to cpu, and then transfer data and model to device :

import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)
data = data.to(device)

### torch.cat
```python
import torch
a = torch.ones((2,3))
print(a)
b = torch.ones((2,3))
print(torch.cat((a,b),0))
print(torch.cat((a,b),1))
```
```
tensor([[1., 1., 1.],
        [1., 1., 1.]])
        
tensor([[1., 1., 1.],
        [1., 1., 1.],
        [1., 1., 1.],
        [1., 1., 1.]])
        
tensor([[1., 1., 1., 1., 1., 1.],
        [1., 1., 1., 1., 1., 1.]])
```

### torch.topk
```py
import torch
a = torch.tensor([1,44,23,12])
x = a.topk(3)
print(x)
```
计算topk的工具包
```py
def accuracy(scores, targets, k):
    """
    Computes top-k accuracy, from predicted and true labels.
    :param scores: scores from the model
    :param targets: true labels
    :param k: k in top-k accuracy
    :return: top-k accuracy
    """

    batch_size = targets.size(0)
    _, ind = scores.topk(k, 1, True, True)
    correct = ind.eq(targets.view(-1, 1).expand_as(ind))
    correct_total = correct.view(-1).float().sum()  # 0D tensor
    return correct_total.item() * (100.0 / batch_size)
import torch
a = torch.tensor(
    [[1,44,23,12],
     [2,3,4,5],
    [2,3,1,1],
     [1,2,1,1]])
target = torch.tensor([1,2,4,3])
values,indices = a.topk(2,dim = 1,largest = True)
print(a.view(-1))
t = target.view(-1,1)
print(t)
print('------')
print(t.expand_as(indices))
print(t.tile(2))
print('------')
print(indices)
print(indices.eq(t.expand_as(indices)))
```

torch.squeeze(i) unsqueeze(i)在哪里unsqueeze就在那里插入一个1的维度，squeeze减去i(i刚好为1)这一维度
```py
>>> a=torch.rand(2,1,3,1,4,1)
>>> a
tensor([[[[[[0.8910],
            [0.9806],
            [0.5027],
            [0.1167]]],


          [[[0.3550],
            [0.5119],
            [0.7651],
            [0.4108]]],


          [[[0.5503],
            [0.7516],
            [0.6234],
            [0.6540]]]]],




        [[[[[0.3190],
            [0.8547],
            [0.8613],
            [0.7470]]],


          [[[0.9893],
            [0.9485],
            [0.4787],
            [0.7272]]],


          [[[0.9856],
            [0.4083],
            [0.4830],
            [0.0464]]]]]])
>>> a.squeeze(0).shape
torch.Size([2, 1, 3, 1, 4, 1])
>>> a.squeeze(1).shape
torch.Size([2, 3, 1, 4, 1])
>>> a.squeeze(3).shape
torch.Size([2, 1, 3, 4, 1])
>>> a.squeeze(5).shape
torch.Size([2, 1, 3, 1, 4])
>>> a.shape
torch.Size([2, 1, 3, 1, 4, 1])
>>> a.unsqueeze(3).shape
torch.Size([2, 1, 3, 1, 1, 4, 1])
>>> a.unsqueeze(1).shape
torch.Size([2, 1, 1, 3, 1, 4, 1])
>>> a.unsqueeze(0).shape
torch.Size([1, 2, 1, 3, 1, 4, 1])
```
torch matmul vs mm 
matmul的泛用性更强。mm要求两个矩阵
```py
>>> a = torch.tensor([1,2,3,4])
>>> b = torch.tensor([[1,1,2,2],[0,1,1,1],[1,2,1,1],[3,4,5,1]])
>>> torch.mm(a,b)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: self must be a matrix
>>> torch.matmul(a,b)
tensor([16, 25, 27, 11])
>>> b
tensor([[1, 1, 2, 2],
        [0, 1, 1, 1],
        [1, 2, 1, 1],
        [3, 4, 5, 1]])
>>> a
tensor([1, 2, 3, 4])
>>> torch.mm(a.unsqueeze(0),b)
tensor([[16, 25, 27, 11]])
>>> torch.mm(a.unsqueeze(1),b)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: mat1 and mat2 shapes cannot be multiplied (4x1 and 4x4)
>>>
```
