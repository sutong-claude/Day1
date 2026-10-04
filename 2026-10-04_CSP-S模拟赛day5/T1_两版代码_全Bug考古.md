# Day5 T1《蜗蜗的三角画布》两版代码全 Bug 考古

> 本文只研究 Day5.zip 中的真实代码演化，不把“最终剩余 Bug”和“调试过程中出现过的 Bug”混为一谈。
>
> 结论先说：**第二版最后的核心 DP 已经接近正确，用户说“约 90%”是合理的。真正剩下的大问题高度集中在“怎样找第一个位置满足 endpoint 更大”这个查询器；最后 3:59 为抢 10 分临时加的 all-d=1 特判又额外引入了输出顺序 Bug。**

## 1. 证据范围

contest replay 的 `file_changes.jsonl` 保存了：
- `T1/main.cpp`：48 次保存，43 个不同代码状态；
- `T4(now T1)/main.cpp`：19 次保存，18 个不同代码状态。

把 61 个不同状态逐个做语法检查：
- 第一版 43 个不同状态中有 **11 个直接 CE**；
- 第二版 18 个不同状态 **全部能编译**。

这说明两个阶段完全不同：
- 第一版前半段大量是在和 STL 类型、iterator、key/value 语义打架；
- 第二版已经进入纯算法/索引/查询语义调试。

## 2. 正确数学对象

令
[
r_i=i+d_i.
]

三角形 i 的斜边是
[
y=r_i-x.
]

所有斜边斜率都为 -1，所以未来一个三角形 j 只有在
[
r_j>r_i
]
时才可能真正突破 i 的包络。若 (r_jle r_i)，它在重叠部分被 i 完全覆盖。

因此核心查询是：

[
oxed{operatorname{nxt}(i)=min{j>imid r_j>r_i}}
]

注意：
- 不是最小的 (r_j)；
- 不是最大的 (r_j)；
- 是**位置 j 最小**，并满足 endpoint 更大。

若 (j<r_i)，两三角形有正面积重叠，设 (h=j-i)：
[
f_i=f_j+h(2d_i-h).
]

若没有这样的 j，或 (jge r_i)，第 i 个三角形完整贡献：
[
f_i=d_i^2+f_{min(r_i,n+1)}.
]

**第二版最后已经基本把这一套递推写对。**

---

# 第一版：T1/main.cpp

## 3. 初始状态：一口气叠了很多编译/接口 Bug

第一份快照同时存在：

1. `up` 未声明；
2. `vector<pair<int,int>>` 上拿一个 int 去 `lower_bound`，比较类型不匹配；
3. `auto down = lower_bound(...)--` 的 iterator 操作本身就没有得到想要的“前一个”；
4. vector 根本没有维护有序，却准备二分；
5. `h=pos-i+1` 多 1；
6. backward DP 却在 fallback 中读 `lst[i-1]`；
7. 循环内部输出一次、循环结束后又准备输出，行数会多。

这不是一个“大 Bug”，而是七种不同层级的问题叠在同一版。

## 4. STL 容器接口连续出错

随后几分钟出现过：

8. `multimap<pair<int,int>>`：模板参数数量错误；
9. `multimap<int,int> p; p[i]=...`：multimap 没有 `operator[]`；
10. `p[i].insert(...)`：继续把 multimap 当 map/容器套容器；
11. `p.insert(i+d[i])`：multimap 需要 pair，不能只插 key；
12. 为了让 insert 编译，曾插成 `{i,i+d[i]}`，但此时 key/value 又和查询含义反了。

这些都在第一版中逐渐修掉。

## 5. iterator 的“前一个”被连续误解

代码曾出现：

```cpp
auto up = p.lower_bound(x)--;
```

这不会让 `up` 变成“前一个有效 iterator”；postfix -- 返回的是递减前的副本。

后来又出现：

```cpp
auto it = p.lower_bound(x);
auto up = it--;
```

此时真正被减的是 `it`，而 `up` 仍然是旧位置。

还出现：

```cpp
--up;
```

但没有先保证 `up != begin()`，有潜在 UB。

这段时间里“lower_bound / upper_bound / 前一个 / 后一个”来回切换，实际上是因为**当时还没有先写清楚查询对象究竟是什么**。

## 6. pair 的 first/second 语义多次翻转

第一版中至少反复出现过：

- `first = endpoint, second = index`
- 改成 `first = index, second = endpoint`
- `pos = (*up).first`
- 改成 `pos = (*up).second`
- `lst[(*up).first]`
- `lst[(*up).second]`

这也是为什么 Watches 里经常出现“我明明以为是位置，怎么出来的是 34”一类现象。

## 7. 几何公式的 off-by-one

早期写：

```cpp
int h = pos - i + 1;
```

正确应该是：

```cpp
int h = pos - i;
```

因为梯形横向宽度就是两个竖边 x 坐标之差。

这一条后来修掉。

## 8. 负面积不是“面积要 max(0)”

调试中一度出现：

```cpp
siz = max(h * (d1 + d2), 0LL);
```

这是在修症状。

如果 `h` 与 blocker 位置正确，进入重叠分支时本应满足 (0<h<d_i)，于是 (d_2=d_i-h>0)，不该靠 `max(0)` 救。

负数其实在提示：
> blocker/index 的语义已经错了。

后来这条症状补丁被撤掉，这是对的。

## 9. 第一版最后其实已经很强

第一版最终文件：

```cpp
auto up = p.lower_bound(i + d[i]);
...
int pos = mp[(*up).first];
...
int h = pos - i;
int siz = h * (d1 + d2);
lst[i] = lst[pos] + siz;
```

它已经做到：

- 从右往左 DP：对；
- endpoint (r_i=i+d_i)：对；
- 梯形二倍面积公式：对；
- 重叠后跳到 suffix `pos`：对；
- 重复 endpoint 用 `mp[key]=min(index)` 保存最近位置：这个局部设计也对；
- 两个官方样例：**全过**；
- 官方附件 2-1（所有 d_i=1，30 万行）：**30 万 / 30 万全过**。

所以第一版最后绝对不能描述成“到处都是 Bug”。

### 第一版最后真正的核心错误

它求的是：

[
K=min{r_jmid j>i, r_jge r_i},
]

然后再取这个 K 对应的最小位置。

但真正需要：

[
j^*=min{j>imid r_j>r_i}.
]

**先按值最小，再找位置** 与 **直接找位置最小** 完全不是一回事。

### 最小反例

[
d=[2,3,1],quad r=[3,5,4].
]

i=1 时：

- j=2，r=5；
- j=3，r=4。

正确 blocker 是 **位置 2**。

第一版 `lower_bound(3)` 却先挑 endpoint 最小的 4，于是选位置 3。

正确输出：
```
12
9
1
```

第一版：
```
5
9
1
```

这就是第一版最终最重要的剩余 Bug。

---

# 第二版：T4(now T1)/main.cpp

## 10. 第二版为什么明显比第一版干净

18 个不同状态全部通过语法检查。

也就是说，第一版那些：
- multimap API；
- pair first/second；
- iterator CE；
- 模板参数；
- 未声明变量；

基本已经不再出现。

第二版主要是在把 DP 递推重新写干净。

## 11. 第二版初期 Bug：d_i=1 时没有加入候选集合

最初 `p.push_back(r_i)` 在 `else` 内：

```cpp
if (d[i] == 1)
    ...
else {
    ...
    p.push_back(...);
}
```

于是 d_i=1 的三角形根本没有进入后续查询的数据结构。

很快把 push 移到 if/else 外，这个 Bug 被修掉。

## 12. overlap 以后跳错方向

早期出现：

```cpp
lst[i] = lst[i - h] + siz;
```

但 blocker 在右边：

[
j=i+h.
]

所以应该：

```cpp
lst[i] = lst[i + h] + siz;
```

这一条后来也修掉。

## 13. 无重叠时一度错误地写成 f[i+1]

早期：

```cpp
lst[i] = lst[i + 1] + d[i] * d[i];
```

如果 i 的大三角形把 i+1...r_i-1 的小三角形全包住，这样会重复计算。

正确是直接跳过被覆盖区间：

```cpp
lst[i] = lst[min(i + d[i], n + 1)] + d[i] * d[i];
```

这条是第二版相对第一版非常重要的模型完善。

## 14. h 曾经被当成 vector 中的排名距离

出现过：

```cpp
distance(p.begin(), it)
distance(p.end(), it)
distance(it, p.end()) + 1
distance(it, p.end()) - 1
distance(it, p.end()) - 2
```

这里其实是在不断试图从“vector 中的 iterator 位置”反推出“真实坐标差 j-i”。

这两者没有天然等价关系。

后来引入 `id[endpoint]`，直接写真实位置差，方向是对的。

## 15. 3:05 左右的 RE 根因不是 long long 溢出

当时程序有：

```cpp
lst[i + d[i]]
lst[i + h]
```

而 (d_ile10^9)，数组只有约 (10^6)。

所以只要 i+d_i 很大，就直接越界。

这正对应录音中的“怎么 RE / 哪个数组越界”。

随后加：

```cpp
lst[min(i + d[i], n + 1)]
lst[min(i + h, n + 1)]
```

RE 根因才真正修掉。

与此同时把：

```cpp
#define int long long
```

改成：

```cpp
#define int unsigned long long
```

其实并不是必要修复。(10^9)^2=10^18 仍在 signed long long 范围内。

unsigned 不一定立即错，但会让负数 underflow 变成巨大正数，反而可能掩盖 Debug 信号。

## 16. h 的定义最后才彻底修正

引入 id 后最初写：

```cpp
h = i + d[i] - id[*it];
```

这是“当前右端点到候选位置的距离”。

真正梯形宽度应是：

```cpp
h = id[*it] - i;
```

3:20 左右改成这一版以后，核心几何递推已经相当接近最终正确解。

## 17. 3:01 开始第二版已经能过两个官方样例

实际把历史快照重新编译运行：

- 约 3:01 的版本：样例 1 全对、样例 2 全对；
- 3:07、3:08、3:20 的版本也继续两个样例全对。

所以后面不是“代码还一团乱麻”。

更准确地说：

> 样例可见的实现 Bug 已经基本修完，剩下的是大数据才能卡出的查询语义 Bug。

## 18. 第二版最后核心代码到底还差什么

3:20 左右的核心是：

```cpp
auto it = upper_bound(p.begin(), p.end(), r[i]);

if (it != p.end() && id[*it] < r[i]) {
    int h = id[*it] - i;
    ...
    lst[i] = lst[i + h] + siz;
} else {
    lst[i] = lst[min(r[i], n + 1)] + d[i] * d[i];
}
```

除去“怎样得到 it”，后面的 DP 基本正确。

### 剩余核心 Bug A：p 根本没有排序

p 是：

```cpp
p.push_back(r[i]);
```

处理顺序是 n,n-1,...,1。

因此 p 的值序列一般完全无序。

但 `upper_bound` 要求搜索区间满足有序/partition 条件。

### 最小反例

[
d=[2,2,2],quad r=[3,4,5].
]

处理 i=1 时，p 中按插入顺序是：

```
[5,4]
```

不是有序数组。

正确输出：
```
10
7
4
```

第二版核心：
```
8
7
4
```

这是纯粹的“无序 vector 二分”反例。

### 剩余核心 Bug B：即使把 p 排序，也仍然不够

假设把 p 真正排序。

`upper_bound(r_i)` 得到的是：
> endpoint 值中最小的一个大于 r_i 的值。

但题目需要：
> 所有 endpoint 大于 r_i 的位置中，位置最小的那个。

仍然是“最小值”与“最小位置”的区别。

继续用：

[
d=[2,3,1], r=[3,5,4]
]

即使 p 排序成 [4,5]：

`upper_bound(3)` 仍先选 endpoint=4（位置3），而真正 blocker 是 endpoint=5（位置2）。

所以**排序只能修一半**。

## 19. id[endpoint]=index 本身不是主要 Bug

之前容易误判：
> unordered_map 会丢掉重复 endpoint，所以错。

这句话不严谨。

因为你从右往左处理：

```cpp
id[r[i]] = i;
```

对同一个 endpoint，后写入的是更小、更靠左的 index。

对于“已经处理的右侧位置”，它恰好保存该 endpoint 最近的位置。

所以：
- **查询某一个固定 endpoint 时，id 的这个语义基本合理；**
- 真正缺的是：要在**所有 endpoint > r_i** 中取最小 index。

也就是说你实际上已经差一点走到：

> endpoint 做 key，index 做 value，区间查询最小 index。

这正是线段树 / Fenwick(min) / 单调栈可以解决的东西。

## 20. 第二版 3:20 的“90%”评价是合理的

把程序分层：

1. 几何模型：对；
2. (r_i=i+d_i)：对；
3. suffix DP：对；
4. 重叠梯形公式：对；
5. 无重叠跳到 r_i：对；
6. h=pos-i：对；
7. n+1 边界：对；
8. d_i=1 单独递推：对；
9. **查询 first position：错。**

所以从“结构模块”看，确实接近只剩最后一个查询器。

这和“官方大数据输出只有少量行相同”不矛盾：
> 一个核心查询器错，会让 f[i] 链式传播，导致后面大量答案全错；并不代表每一行代码都有 Bug。

## 21. 最后 3:59 为抢 10 分又引入一个新 Bug

原本 3:20 核心版本对于 all d_i=1：

```cpp
lst[i]=lst[i+1]+1;
```

其实是正确的。

官方 2-1 附件 30 万行：
**30 万 / 30 万全对。**

但最后加：

```cpp
if (all d_i == 1) {
    for (int i=n; i>=1; --i)
        cout << n-i+1 << '\n';
}
```

输出顺序变成：

```
1
2
3
...
n
```

题目要求第 1 行是 suffix 1，所以正确应：

```
n
n-1
...
1
```

结果这个“保 10 分”的 emergency patch 反而把**本来已经全对的 10 分子任务打没了**。

这是和核心算法 Bug 完全不同的一类：最后交付阶段新引入的回归。

---

# 22. 两版最终状态的真实对比

| 模块 | 第一版最终 | 第二版 3:20 核心 |
|---|---|---|
| 编译 | ✅ | ✅ |
| 两个官方样例 | ✅ 全过 | ✅ 全过 |
| all d=1 30万行 | ✅ 全过 | ✅ 全过 |
| endpoint 建模 | ✅ | ✅ |
| 梯形面积 | ✅ | ✅ |
| suffix DP | 基本成型 | ✅ 更干净 |
| n+1 边界 | 较隐式 | ✅ 明确 |
| blocker 查询 | ❌ 按值最小 | ❌ 无序二分 + 按值最小 |
| 最后 emergency special | 无 | 3:59 新增后 ❌ |

所以“第二版最后剩下的代码基本正确”这个判断应该保留。

---

# 23. 为什么会感觉“调出了成千上百个 Bug”

因为这场其实有两种 Bug：

### A. 真正的独立实现 Bug
前 1～3 小时确实很多：
- CE；
- STL API；
- pair 语义；
- iterator；
- off-by-one；
- DP 下标；
- 越界；
- h 定义。

这些大多数后来都被你修掉了。

### B. 一个核心模型 Bug 产生很多表面症状
最后剩下的是：

> 我要“最小位置”，代码却一直按“endpoint 值”组织查询。

于是一个核心错会在不同样例上表现为：
- 多算；
- 少算；
- 某一行对、下一行错；
- blocker 看起来“不是我想的那个”；
- 迭代器“怎么跑这里”；
- 大样例只有少量行匹配。

这不是又冒出十个新 Bug，而是同一个 query mismatch 在不同状态下显形。

---

# 24. 从第二版到 AC 的最小改动思想

你的 DP 可以基本保留，只换查询器。

## 方案 A：最贴近你的写法——endpoint 值域线段树

处理 i 从 n 到 1。

每个 endpoint r_j 对应一个位置 j。

线段树维护：
> 每个 endpoint 值区间内，已经出现位置的最小 index。

查询：
[
min{jmid r_j>r_i}
]

就是压缩 r 后，对 ((r_i,+infty)) 做区间最小值。

这几乎就是你 `upper_bound + id` 思路的正确数据结构化。

## 方案 B：更漂亮——单调栈

这是经典 Next Greater：

```cpp
while (!st.empty() && r[st.back()] <= r[i])
    st.pop_back();

nxt[i] = st.empty() ? n+1 : st.back();
st.push_back(i);
```

得到 first j>i with r_j>r_i。

后面的 DP 仍用你第二版已经写出的式子。

---

# 25. 最终结论

如果问“整个调试过程中出现过多少 Bug”：
- 按独立错误机制计，**20+ 是保守数**；
- 按每次代码状态中出现/修掉的具体错误计，**30+ 完全合理**。

但如果问“第二版 3:20 左右最终核心还剩多少 Bug”：
- 不能说还有几十个；
- **核心上主要就是 blocker 查询器这一大类；**
- 3:59 临时 partial 又额外引入一个 all-d=1 输出顺序 Bug。

因此正确描述应该是：

> **前半场确实调掉了很多真 Bug；到第二版后期，代码主体已经接近正确。之所以大数据仍大面积错，不是因为还剩一百个小 Bug，而是剩下的那个查询器 Bug 位于 DP 的上游，会把大量 f[i] 连锁污染。**
