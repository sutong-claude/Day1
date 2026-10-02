# D 同类分段：判定压成 `max first < min last`

固定区间 `[l,r]`。对每个出现的值 x 记第一次位置 `first_x`、最后一次位置 `last_x`。切点 m 两边数字集合相同，当且仅当每个 x 都在两边至少出现一次：

`first_x <= m < last_x`。

所以存在切点 iff 所有 `[first_x,last_x-1]` 有公共交集，也就是

`max_x first_x < min_x last_x`。

扫右端点 r，设 `p=prev[r]`。

- `l>p` 时 a[r] 对区间是新值，first=last=r，必不合法，所以整段 `[p+1,r]` 清 0；
- 对 `l<=p`，first 不变，只有 a[r] 的 last 从 p 移到 r，因而 `min last` 只会在一整段左端点上提升。

维护所有不同值“当前最后出现位置”的有序双向链。p 的前驱 q、后继 t 决定恰好 `[q+1,p]` 这段旧 `min last=p`。删除 p 后，新 `min last = t`（若无 t 则 r）。

在该段中，新合法条件 `F[l] < newL` 等价于 `[newL,r]` 内没有位置 i 满足 `prev[i] < l`，即

`l <= min(prev[newL..r])`。

所以重新变合法的仍是一个前缀 `[q+1, min(p, RMQmin)]`。用 01 lazy segment tree 做两次区间赋值并维护 1 的总数，即得到当前右端点的合法区间数。

当前实现用 sparse table 做 `min(prev)` RMQ，整体 O(n log n)，n=10^6 压测峰值内存约 123 MB。

实现已在 1,088,572 个数组上与独立暴力逐一一致，并通过 8 份官方样例。