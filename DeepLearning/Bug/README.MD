I had a similar problem.
Here is my code that made the mistake.

https://github.com/davda54/sam/issues/10
```py
output, logit_map = model(image)

loss = 0
for t in range(num_tasks):
    loss_t, acc_t = get_loss(output, target, t, device, cfg)
    loss += loss_t
    loss_sum[t] += loss_t.item()
    acc_sum[t] += acc_t.item()

optimizer.zero_grad()
loss.backward()
optimizer.first_step(zero_grad=True)
output, logit_map = model(image)

for t in range(num_tasks):
    loss_t, acc_t = get_loss(output, target, t, device, cfg)
    loss += loss_t
    loss_sum[t] += loss_t.item()
    acc_sum[t] += acc_t.item()
loss.backward()
optimizer.second_step(zero_grad=True)
I think it is probably due to this issue

The loss variable for the first backward and the loss variable for the second backward must be different.
I forgot to initialize the variables.

Or check if you forgot to let the model predict the results again

I had a similar problem.
Here is my code that made the mistake.

output, logit_map = model(image)

loss = 0
for t in range(num_tasks):
    loss_t, acc_t = get_loss(output, target, t, device, cfg)
    loss += loss_t
    loss_sum[t] += loss_t.item()
    acc_sum[t] += acc_t.item()

optimizer.zero_grad()
loss.backward()
optimizer.first_step(zero_grad=True)
output, logit_map = model(image)

for t in range(num_tasks):
    loss_t, acc_t = get_loss(output, target, t, device, cfg)
    loss += loss_t
    loss_sum[t] += loss_t.item()
    acc_sum[t] += acc_t.item()
loss.backward()
optimizer.second_step(zero_grad=True)
```
I think it is probably due to this issue

The loss variable for the first backward and the loss variable for the second backward must be different.
I forgot to initialize the variables.

#### Or check if you forgot to let the model predict the results again!!!!
