```py
import  torch
a = torch.ones(1,3)*3
b = torch.ones(1,2,3)
print(a)
print(b)
a = a.unsqueeze(1)
z = a+b
print(
    z
)
```

output
```
tensor([[3., 3., 3.]])
tensor([[[1., 1., 1.],
         [1., 1., 1.]]])
tensor([[[4., 4., 4.],
         [4., 4., 4.]]])
```
