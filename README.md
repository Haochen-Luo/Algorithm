# This repository is used for storing classical alg template
----------------------------------------------------
1. Sort
2. Divide and conquer
3. Dynamic programming

## please refer some engineer and coding experience to 代码细节.md, such as boundaries...

## TODO
1. 编辑距离会写代码但是思想值得再研究一下[已完成！]
2. 括号生成再研究研究https://leetcode-cn.com/problems/generate-parentheses/submissions/
3. 格雷编码的公式证明，优先级很低
4. 如果面试后端，(尤其是字节跳动)，好好背书！！！都是八股，背熟就好，重点看wake-up[https://github.com/Haochen-Luo/Waking-Up] 那里，太多今年字节面试的原题
	1. 操作系统： https://github.com/Snailclimb/JavaGuide/blob/master/docs/operating-system/basis.md
	2. 计算机网络：https://github.com/wolverinn/Waking-Up/blob/master/Computer%20Network.md
	3. 数据库: https://github.com/rbmonster/learning-note/blob/master/src/main/java/com/toc/MYSQL.md#8

![image](https://user-images.githubusercontent.com/46443218/114380120-994d5280-9b81-11eb-837b-a474d8ed999d.png)

### python的列表生成细节
慎用乘法，第二个列表我们本意是给第一个添加12，但是全都加了
```py
print([0]*12)
a = [0]*12
for i in range(len(a)):
    a[i] = i
print(a)
b = [[]]*12
b[0].append(12)
print(b)
```

output
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
[[12], [12], [12], [12], [12], [12], [12], [12], [12], [12], [12], [12]]

```

原因何在？本质是相同的对象
```
for i in b:
    print(id(b))
```
```
2104361415496
2104361415496
2104361415496
2104361415496
2104361415496
2104361415496
2104361415496
2104361415496
2104361415496
2104361415496
2104361415496
2104361415496
```

正确做法
```
b = [[] for _ in range(12)]
b[0].append(12)

print(b)
```

```
[[12], [], [], [], [], [], [], [], [], [], [], []]
```
#### Java反转字符串
```java
public void reverse(StringBuilder sb, int left, int right) {
        while (left < right) {
            char tmp = sb.charAt(left);
            sb.setCharAt(left++, sb.charAt(right));
            sb.setCharAt(right--, tmp);
        }
    }
```
作者：LeetCode-Solution
链接：https://leetcode.cn/problems/reverse-words-in-a-string/solution/fan-zhuan-zi-fu-chuan-li-de-dan-ci-by-leetcode-sol/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

### 
在 Java 中，参数传递是 值传递，对象类型变量在传参的过程中，复制的是变量的地址。这些地址被添加到 res 变量，但实际上指向的是同一块内存地址，因此我们会看到 66 个空的列表对象。解决的方法很简单，在 res.add(path); 这里做一次拷贝即可。

修改的部分：

```java
if (depth == len) {
    res.add(new ArrayList<>(path));
    return;
}
```
```py
if depth == size:
    res.append(path[:])
    return
```
作者：liweiwei1419
链接：https://leetcode.cn/problems/permutations/solution/hui-su-suan-fa-python-dai-ma-java-dai-ma-by-liweiw/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
