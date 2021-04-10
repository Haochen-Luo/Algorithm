nn.CrossEntropyLoss

This criterion combines LogSoftmax and NLLLoss in one single class.

https://pytorch.org/docs/stable/nn.html

代码实例验证

```python
import   torch
y = torch.LongTensor([0])
z = torch.Tensor([[0.2,0.1,-0.1]])
criterion = torch.nn.CrossEntropyLoss()
loss = criterion(z,y)
print(loss)
# tensor(0.9729)
```
以上的结果如何手动复现？
1. 首先要是softmax
```python
z = torch.softmax(z,1)
print(z)
# tensor([[0.3780, 0.3420, 0.2800]])
```
2. 再就是negative log likelihood

2.1 likelihood已经求出来了就是tensor([0.3780])

2.2 其次要是log
```python
print(torch.log(torch.Tensor([0.3780])))
# tensor([-0.9729])
```
3. 最后是negative
```python
print(-torch.log(torch.Tensor([0.3780])))
# tensor([0.9729])
```
或者就按照官方的说法
```python
y = torch.LongTensor([0])
z = torch.Tensor([[0.2,0.1,-0.1]])
criterion = torch.nn.CrossEntropyLoss()
print("log softmax",torch.nn.functional.log_softmax(z,dim =1))
# output: log softmax tensor([[-0.9729, -1.0729, -1.2729]])
log_softmax = torch.nn.functional.log_softmax(z,dim =1)
print(torch.nn.NLLLoss()(log_softmax,y))
# tensor([0.9729])
```
损失依旧是tensor([0.9729])

**可以发现和交叉熵完全一样**

所以交叉熵损失因为one hot encoding的缘故可以从

![image](https://user-images.githubusercontent.com/46443218/114267324-b69fe680-99f2-11eb-8375-0785c6f07e1f.png)

化简为真实标签label对应的liklihood（这里比如这里的真实标签为0，对应的likelihood0.2）的softmax，取log，加负号！！
就是这么简单

最后提一句，NLLLoss是一个很傻的损失
单纯one-hot encoding对应的真实标签元素取负号，并不会取对数啥的，单纯加个负号。
这也就是为何是logsoftmax+NLLLoss,取对数在logsoftmax里完成了，NLLLoss只是加个负号
```python
z = torch.softmax(z,1)
print(z)
# tensor([[0.3780, 0.3420, 0.2800]])
y = torch.LongTensor([0])
print(torch.nn.NLLLoss()(z,y))
# tensor(-0.3780)
print(torch.nn.functional.nll_loss(z,y))
# tensor(-0.3780)
```

注意以上结论皆基于多分类问题，多标签问题有待于继续探索（不过目前也没做什么多标签的任务啊）
 
