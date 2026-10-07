# AI MASTER INDEX｜模拟赛仓库接管入口

> **任何新 AI 接手本仓库，先读这里。**
>
> 这个仓库不是“题解合集”，而是小苏同学 CSP-S / OI 模拟赛的长期外部大脑。目标是能恢复：**题目是什么 → 赛时怎么想 → 写了哪几代代码 → 为什么错 → 后来如何证伪/证明 → 哪些分当时其实已经可拿 → 工具和环境怎样影响结果 → 下一场默认该怎么做。**

# 0. 30 秒状态

## 代码源七场

```text
Day1   45
Day2  130
Day3  204
Day4    0
Day5   15
Day6  115
Day7  145
```

合计：**654 / 2800**  
场均：**93.43**  
中位数：**115**  
最高：**204（Day3）**  
总体波动标准差约：**69.6**。

28 道代码源题中：
- 有提交：**21 / 28 = 75%**
- 满分 AC：**4 / 28**
- 非满分但拿到分：**9 题**
- 这些 partial 合计：**254 分**
- 提交但 0 分：**8 题**
- 完全未提交：**7 题**

这说明阶段增长不能只看“AC 数”：**654 分中有 254 分来自非满分 partial，部分分资产占比很高。**

## 另一体系：代码部落 NOI 金牌命题模拟赛1

**200 / 400：net100 + game100 + core0 + tree0。**

当时页面快照显示第 3 / 54，但很多 0 分账号尚未开始，所以**只称“实时榜单快照第3/54”**，禁止把 54 行直接当最终完赛样本。

---

# 1. 新 AI 的必读顺序

> **本文件是唯一 canonical 接管入口。第一步先读本文件，不要先随机翻某场比赛。**

## 第一层：规则与当前状态
1. 本文件
2. `模拟赛复盘总协议_v2.md`
3. `AI_HANDOFF.md`
4. `复盘产物覆盖矩阵.md`
5. `全题总表_2026-10-07.md`

## 第二层：跨场经验
6. `阶段总结_截至2026-10-07_七场代码源与Coderlands.md`
7. `错因档案.md`
8. `赛前执行卡.md`
9. `赛中研究协议.md`
10. `得分资产状态机.md`

## 第三层：证据系统
11. `tools/archive/代码源Day1-Day7_来源与交叉验证.md`
12. `tools/archive/归档采集与证据链_经验总结.md`
13. `证据阅读台账.md`
14. `Replay逐段考古协议.md`

## 第四层：赛场工程
15. `tools/vm/BAG_演化史与赛场工作流.md`
16. `tools/vm/虚拟机赛场工程经验.md`
17. `tools/vm/bag_v4_flat/SOURCE_MANIFEST.md`

---

# 2. Source of Truth：不同问题找不同证据

| 要回答的问题 | 第一事实源 | 第二事实源 | 禁止偷懒做法 |
|---|---|---|---|
| 最终多少分 | OJ record score / 测试点 | 题目列表 | 只看 verdict |
| 最终提交了什么 | OJ source / 正式提交目录 | VM 最后版本 | 拿工作区最后文件冒充提交 |
| 中间写过什么 | Replay file_changes | VM 历史版 | 从 final code 脑补 |
| 当时屏幕发生什么 | Replay screen | timeline | 用录音沉默推断“没干活” |
| 当时为什么这样想 | 录音原文 / notes | screen | 只看智能纪要 |
| 算法是否正确 | [P]证明 / [E]独立真值 | OJ-AC | “100分所以一定对” |
| checker/oracle 是否可靠 | 独立反例/交叉验证 | checker源码 | “有对拍所以没问题” |
| 排名难度 | 完整且同口径榜单 | 实时快照 | 把尚未开始账号算完赛选手 |

---

# 3. 32 题全局地图

统一入口：

- `全题总表_2026-10-07.md`
- `全题总表_2026-10-07.csv`

表内每题至少维护：
- 标题；
- 真实赛时得分；
- verdict；
- 当前正确题解闭合状态；
- 分析难度；
- 训练价值；
- 评测可信度；
- 赛时状态；
- 复盘完整度；
- 证据完整度；
- 下一步触发器。

**FULL待补不是坏事。**  
它表示仓库诚实知道自己的知识边界。后续 AI 不得为了“看起来齐全”伪造满分解。

---

# 4. 当前真正的成长轨迹

不能简单写成“分数越来越高”。

更准确的是**瓶颈逐场向后移动**：

```text
Day1
题意/总范围/复杂度
        ↓
Day2
时间分配/版本/交付
        ↓
Day3
checker/oracle 的证明边界
        ↓
Day4
状态闭合 + 真对拍 + 环境可靠性
        ↓
Day5
数学查询对象 → 数据结构接口
        ↓
Day6
必要条件/充分条件/实现契约
        ↓
Day7
正确 brute → 复杂度变换（offline / reverse / DSU）
        ↓
Coderlands
反例驱动闭合 + 捆绑 subtask + 正式 OI 交付
```

这意味着：
> 早期经常在“有没有正确思路”之前就失分；后期越来越多是**思路已接近甚至正确，但没有及时变成可提交、可验证、可冻结的得分资产**。

---

# 5. 当前最重要的 8 个跨场结论

## 5.1 先建立机械真值，再优化
如果连最机械 brute 都没有，就不要急着写漂亮优化。

## 5.2 “猜想可能不对”必须触发程序动作
出现这句话后 5 分钟内：
- brute；
- generator；
- 最小反例搜索；
- 或切题。

## 5.3 checker/oracle 也会错
Day3 checker、Day4 oracle、Coderlands tree 错格式样例都证明：
> 验证工具本身也是待验证对象。

## 5.4 OJ100 不等于 PROVED
Coderlands net 最终 100 源码有三点链 M=1 极小反例。

## 5.5 删除导致动态分裂，自动想“倒序”
Day7 B 的核心迁移：
`forward delete/split → reverse add/merge → DSU`。

## 5.6 已证明 partial 必须迅速物化
Day7 C10 / D19 已经赛时发现，但没有变成提交。
以后：
`PROVED → 10 分钟内 CODED → VERIFIED → FROZEN`。

## 5.7 捆绑评分的单位不是“测试点”
Coderlands tree raw tests 过不少，但每个 subtask 包都有错误，最终仍 0。
一次只闭合一个包。

## 5.8 工具的目标是减少选择，不是增加功能
BAG V4 最有价值的不是脚本多，而是：
`一题一目录 + 唯一 main.cpp + 一池 testcase`。

---

# 6. “逐段考古”以后必须怎样工作

以后读取录音 / Replay / VM / 历史源码，不允许：

> 一口气读完 → 聊天里总结 → 什么都没落盘。

正确循环：

```text
读一个高信息量片段
↓
定位时间 / 文件 / 保存版本
↓
写出当时假设
↓
找后来证据
↓
标 P/E/C/H/X
↓
立即追加到该场《逐段考古纪要.md》
↓
必要时同步改题解 / 错因档案 / 全题总表
↓
继续下一段
```

这样仓库会随着阅读逐步长出来，而不是“AI脑子里读过，仓库仍贫瘠”。

---

# 7. 复盘产物的“完工”不是一篇长报告

一场 4h 比赛材料丰富时，至少检查：

- README
- 结果核对
- 资料完整性
- 逐题题解
- 赛时全过程
- 研究过程深挖
- 赛时代码逐段解剖
- Replay × 录音交叉时间线
- 逐段考古纪要
- 历史代码版本
- 正解/partial代码
- brute/verifier
- 反例
- 题目质量/难度画像
- 榜单与机会成本
- 可视化
- 下一场执行动作

只留下“README + 一篇复盘 + final.cpp”视为未完成。

---

# 8. 当前仓库欠账优先级

## P0：知识闭合
1. Day4 B/C/D 满分题解仍未可靠闭合；
2. Day5 B/C/D 满分题解仍待补；
3. Day6 C 完整计数证明/实现需最终校验，D full 待补；
4. Day7 C/D full 待补；
5. Coderlands tree full 待可靠题解/独立证明。

## P0：过程考古
6. Day1/Day2 原始赛场过程资料比后期薄，需要尽可能从 Library / 旧对话补回；
7. Day4～Day6 将已有全过程文档进一步拆成 append-only《逐段考古纪要》。

## P1：可视化与数据
8. 建立跨场 score / submission / partial / evidence maturity 图；
9. 建立 32 题“难度 × 训练价值 × 当前闭合度”矩阵；
10. 每次阶段总结生成可下载 PDF。

---

# 9. 后续 AI 的工作习惯

**不要等用户再次提醒“你没看文件库”。**

每次要做阶段分析时：
1. 先查仓库；
2. 再查 File Library；
3. 找未使用原始证据；
4. 读后立即写纪要；
5. 强证据可推翻旧结论；
6. 保留修订痕迹；
7. 只在实际 commit 后说“仓库已更新”。

最后原则：

> **这个仓库的价值，不在于写了多少字，而在于下一位 AI 打开以后，不需要重新猜这七场比赛发生过什么。**


# 10. 固定教学/回答形态

用户要求“像高质量竞赛 PPT 一样讲题”，详细不等于文字墙。

默认顺序：

```text
题目卡片
→ 人话重述
→ 数据范围/子任务暗示
→ 赛时本人怎么想
→ 手玩小例子/大样例
→ 最机械 brute
→ brute 重复做了什么
→ 性质/等价改写
→ partial 梯度
→ full 为什么会被想到
→ 证明
→ 实现积木
→ 原代码最小修复
→ Hack/对拍
→ 下次看到什么自动想到什么
```

特别规则：
> 能沿用户原算法证明/最小修复，就先保护原路线；只有原算法本身被反例/证明杀死，才换成另一套标准解法。

Coderlands net 是校准案例：
- 赛时 best-first 主体是强候选；
- 已知确定 Bug 是直径数组 dummy 导致的中点 off-by-one；
- 同步剥叶是独立 full/proof/oracle；
- 不能把“发现一个实现反例”写成“整套赛时算法错误”。

# 11. 新 AI 最容易踩的 7 个事实坑

1. Day7 B **没有**从 00:38 连续做到 03:27：约 02:08 已切 C、02:14 已切 D。
2. Day7 B 不是“不会题意”：定义级 O(n²) brute 正确，且本人准确定位 calc 重扫组件、后来明确说到 offline。
3. Day7 D 最终短文件不是“没写”：历史版本有完整 D5000 候选，03:51 本人判定模型不可行后主动推倒。
4. Day6 C 赛时已经写出 contains both / only k-1 / only k / neither 四类；错在 forced/optional/impossible/off 语义压缩。
5. Day5 A 第二版后期不是“几十个 Bug 全没修”：主体几何/DP 已很接近，最大上游错误集中在 first-by-position query 被写成 search-by-value。
6. Coderlands net 最终 OJ100 源码有三点链 M=1 反例；OJ-AC 不能升格成 [P]。只修中点后，小树 exhaustive 126126 实例无 mismatch，但形式化等价证明仍应保留。
7. Coderlands “第3/54”只是实时页面快照，很多 0 分账号尚未开始；禁止当最终排名样本统计。

# 12. 当前施工与可交付物

- 工作分支：`chatgpt/oct7-stage-maintenance`
- Draft PR：#17
- 未经用户明确要求不要合并到长期分支。
- 阶段 PDF 已生成并保存到 ChatGPT Library：
  `/CSP-S比赛复盘/阶段报告/阶段成长与模拟赛资产报告_2026-10-07.pdf`
- 仓库内报告索引：`总览/报告/README.md`
- 可视化：`总览/可视化/阶段成长仪表盘.html`
- 下一场直接执行：`执行包/下一场比赛_赛前执行包.md`

# 13. 索引文件角色，避免重复真相

## Canonical
- AI 接管入口：**本文件**
- 逐段证据协议：`Replay逐段考古协议.md`
- 32题人类/证据总表：`全题总表_2026-10-07.md/.csv`

## 派生分析视图
- `总览/全题总表_32题.md/.csv`：用于数值难度/质量与可视化分析，不单独决定题解闭合状态。
- `总览/AI直接接手入口.md`：兼容旧链接，应该只指回本文件。
- `模拟赛考古纪要协议.md`：兼容旧链接，应该只指回 `Replay逐段考古协议.md`。

若派生视图与 canonical 冲突：
> 以 canonical + 最新原始证据为准，并修订派生视图。


# 14. 三包证据池施工入口（2026-10-07）

用户已经把后续需要长期挖掘的模拟赛原件固定成三包，并保存到 Library：

```text
/CSP-S模拟赛资料/原始三包/模拟赛资料_01_共03包.zip
/CSP-S模拟赛资料/原始三包/模拟赛资料_02_共03包.zip
/CSP-S模拟赛资料/原始三包/模拟赛资料_03_共03包.zip
```

后续不要再问“原始文件在哪”，也不要另找别的比赛包。

## 当前机器盘点

- depth≤3 inventory：9,073 rows；
- nested ZIP opened：195；
- open errors：0；
- duplicate nested-ZIP hash groups：34；
- duplicate ZIP appearances：169。

详细入口：

- `tools/archive/三包原始资料_处理台账.md`
- `tools/archive/三包递归扫描_统计摘要.md`
- `tools/archive/recursive_zip_inventory.py`
- `证据阅读台账.md`

## 固定推进方式

```text
inventory
→ content-hash 去重
→ 找唯一/版本分叉的高信息量对象
→ 读原件
→ 形成 P/E/C/H/X
→ 立即写比赛证据日志/题解
→ 更新处理台账
→ commit
```

进度可以极小，但禁止“读完只留上下文”。

2026-10-07 第一轮已经用 recorder 源码证明：
Replay v3.0.0 的 pause 不会停止 raw EV_KEY 持久化，且 FileTracker 存在 baseline / polling / skip 边界。后续所有 Replay 解释都应读取：
`tools/vm/Replay采集脚本_源码考古与能力边界.md`。


# 15. 三包深挖当前增量（Day4–Day7）

当前已从“目录级 inventory”推进到“正式提交版本级对齐”。

## 新增 canonical 工具/证据

- `tools/archive/replay_submission_matcher.py`：用严格 normalized source content 将 OJ source 映射到 file_changes snapshot；无 exact match 时返回非零，不允许猜。
- `tools/archive/旧VM快照_血缘与Day3Day4迁移.md`：识别 VM 快照重复、路径迁移和真正分叉。
- Day6：`回放数据/file_changes_语义版本时间线_20261005_101100.md`
- Day7：`回放数据/file_changes_完整版本时间线_20261006_080043.md`

## 新的 Source-of-Truth 强化规则

对于“正式提交了什么”，优先级改成：

```
OJ record source
→ exact match 到 Replay file_changes snapshot
→ submission附近 screen/timeline
→ VM final workspace 只作赛后状态
```

Day6 C/D 和 Day4 A/D 已证明 final VM workspace 会在提交后漂移。

## Day4 事故已具体化

A 的 OJ Compile Error 已由源码 diff 定位到坏掉的 traditional IO 行：
`freopen ("Thermokinesis.out, "w", stdout);`

赛后 VM 又把该行注释，因此“打开最后文件能编译”不能推翻提交 CE。

## Day6 Debug 对照

- B：实现层快速修净，但数学 predicate 没变真；
- D：`phi(1)→phi(2)→phi(6)` 最小探针直接推动边界契约修复并得到稳定15分 brute；
- C：正确四分类真实进入代码，随后因为语义压缩发生退化。

所以以后 Debug 价值的判断标准不是“运行/修改次数”，而是是否得到新不变量、区分假设、修正契约或产出可冻结分数。

## 当前下一优先级

1. Day3 `keystream/events_20261001_184442.jsonl` 做高信息量片段考古；
2. Day4 recovered keyboard 与 Day4 A/B/D submitted/post-submit 分叉继续对齐；
3. Day5 Replay/VM 原件继续定位并做 exact submission mapping；
4. 给递归 inventory 增加 content-sha 的 path-move 识别，减少快照重复劳动；
5. 继续挖 checker/stress/archive 脚本与同名不同 SHA 对象。


# 16. Day3 / Day5 新闭合（2026-10-07）

## Day3 checker 因果链已由官方样例直接证明

不再只写“checker 不验证 NO”。

已实测原版：
- T2/AC.cpp
- T2/checker.cpp
- sample1～8

sample7 case4：
candidate NO / official YES；checker 跳过并整份 green。

而 OJ B65 submitted algorithm body 与 T2/AC.cpp 完全一致（仅 freopen comment state 不同）。

所以 canonical 结论：
> Day3 B 的官方样例本来就包含最终算法主体的反例；验证器覆盖缺口让反例没有转化成赛时反馈。

工具：
tools/archive/checker_coverage_probe.py

## Day5 主 capture 已进入提交级考古

canonical：
03包 → Day6.zip → Desktop/CSP-S/Day5/contest_capture/20261004_090304

关键：
- 99 条 file_changes；
- A 第一交实际是 T2/WA.cpp 417B special；
- B15 是 T2/main.cpp 简单正确 partial；
- C RE→RE→WA 把输入/IO/算法层分开；
- T4(now T1) 是真实赛场路径；
- A 第二代共19次保存；
- final traditional IO 多次在 OJ 网页链中最后修改。

入口：
2026-10-04_CSP-S模拟赛day5/回放数据/Replay与六次OJ提交映射_20261004_090304.md

## submission matcher 证据等级

tools/archive/replay_submission_matcher.py 现在必须区分：

1. exact：正式 source 与 snapshot 内容一致；
2. body_without_freopen：仅移除 traditional IO 行后主体一致。

第二类可以证明“算法主体对应”，但不能证明“最后本地验证的字节就是上传字节”。

## 新的交付硬规则

OJ 提交页不是编辑器。

    本地正式 IO
    → 保存
    → 编译
    → 文件 IO 样例
    → VERIFIED/FROZEN
    → 原样提交

网页中再改一个字符，状态立即回退为 MODIFIED_UNVERIFIED。

该规则已同步：
- 赛前执行卡 第20条；
- 得分资产状态机 提交一致性补丁。
