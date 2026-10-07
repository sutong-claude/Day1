# AI 接管指南（最新状态）

> **第一件事：先读 `模拟赛复盘总协议_v2.md` 和 `复盘产物覆盖矩阵.md`。**
>
> 本仓库不是普通题解库，而是用户全部 OI/CSP-S 模拟赛的长期“外部大脑”。

# 1. 项目目标

每场比赛都要尽可能恢复：

- 题面与子任务；
- 最终得分 / 排名 / 逐点；
- 赛时真实思维；
- 中间代码版本；
- 录音与 Replay；
- Debug / 环境事故；
- 正确不变量与错误猜想；
- 最小反例；
- 正解怎么从赛时思路继续推；
- 得分机会成本；
- 独立验证；
- 下一场执行协议。

**不能只看最终代码，也不能只写标准题解。**

# 2. 最新比赛状态

## 代码源系列

Day1～Day7：

**45 → 130 → 204 → 0 → 15 → 115 → 145**

Day7 的旧版结论正在 2026-10-06 二次取证后被纠正：

- A100，约35分钟；
- B45 RE；
- C/D未提交；
- 榜单 66/105；
- B **确实冻结过稳定朴素版**；
- B 赛时已经明确识别 `calc` 重扫是复杂度瓶颈，并想到“离线”；
- 真正没跨过的是“删除分裂 → 倒序加入 → DSU”；
- C 的 v=50 10分性质赛时已发现；
- D 的 N≤100 19分暴力赛时已发现，并口头判断“一定能拿”；
- 但 C10/D19 没有立即变成提交资产；
- D 后来实际写出过完整的 5000 候选算法，最后经过 Debug 证明算法不可行，才推倒。

所以 Day7 不能再简化成“B 吞掉后半场”。

## 代码部落 / NOI金牌命题模拟赛1

- 200/400；
- 当时榜单快照第3/54；
- net100 / game100 / core0 / tree0。

必须注意：
- 榜单 54 行里很多账号当时**尚未开始比赛**；
- 不能拿39个零分账号算“参赛者均分/中位数/非零率”；
- 旧版试卷画像中相关统计必须纠正。

新体系关键证据：
- net 官方100最终源码存在已独立复核的三点链 M=1 反例；
- game 最终代码 n≤7 全穷举145636实例0 mismatch；
- game 赛时并非“一次分类讨论写对”，而是经历多轮真实 Bug 修复；
- tree 最后没有可靠样例验证，VM 已证实下载/复制到 T4 的所谓样例包**输入格式根本不符合 tree 题面**；
- tree 代码本身仍有数学/实现漏洞，样例事故解释的是“为什么验证链被破坏”，不是替代码洗白。

# 3. 复盘必须继承 Claude 早期的完整九大块

完整结构见 `模拟赛复盘总协议_v2.md`：

1. 证据完整性；
2. 比赛总画像；
3. 个人能力定位；
4. 逐题复盘；
5. 争议点深挖；
6. 排名/同分段/机会成本；
7. 时间线/止损；
8. Skill沉淀；
9. 行动清单。

Day3 以后新增：
- 研究过程深挖；
- 赛时代码逐段解剖；
- 键盘/Replay分析；
- 结果核对；
- 资料完整性报告；
- 验证报告；
- 可视化回放；
- 关键历史代码版本。

后面的比赛不得缩水。

# 4. Replay v3 正确读取顺序

不要沿用旧版 handoff 的错误顺序。

捕捉器 `AI_READ_FIRST.txt` 明确要求：

1. `timeline.txt`
2. `file_changes.jsonl`
3. `screen_*.mkv`
4. `raw_keys.jsonl.gz`
5. `manifest.json`

解释：
- file_changes = 保存到磁盘的源码状态；
- screen = 鼠标、窗口、Debugger、网页、未保存状态的权威证据；
- raw_keys = 精确恢复输入与快捷键；
- 录音 = 数学思路/判断/犹豫。

**录音沉默 ≠ 没干活；最终文件短 ≠ 中途没写过完整算法。**

# 5. 每题必须回答

- 题目本质；
- 赛时状态；
- 第1代/第2代/...思路；
- 每代为何合理；
- 正确不变量；
- 第一处错误前提；
- 实现 Bug 与模型 Bug 分开；
- 最小反例；
- 正解突破口；
- 比赛时如何想到；
- partial 哪些是赛时已发现、哪些只是赛后 hindsight；
- 哪个版本应冻结；
- 下一次识别信号。

# 6. 证据等级

- [P] / PROVED
- [E] / BRUTE-VERIFIED
- [C] / statement-checker fact
- [H] / HYPOTHESIS
- [X] / COUNTEREXAMPLE
- OJ-AC 仅表示官方数据通过

禁止 OJ-AC 自动升级 PROVED。

# 7. 仓库完工定义

完整4小时比赛原则上至少检查是否需要：

- README
- 复盘报告
- 题解
- 全过程复现
- 研究过程深挖
- 赛时代码逐段解剖
- Replay×录音时间线
- 结果核对
- 资料完整性报告
- 验证报告
- 赛时代码 + 关键历史版
- 正解代码
- 暴力/验证脚本
- 原始材料索引
- 可视化

根目录同步：
- README
- 错因档案
- 赛前执行卡
- 阶段总结
- 本文件
- 覆盖矩阵

具体缺项见 `复盘产物覆盖矩阵.md`。

# 8. 隐私

不能公开：
- raw keyboard；
- clipboard；
- 原始 screen 录像；
- 未脱敏账号页；
- 个人身份/联系方式/地址等。

但是**不公开 ≠ 不读取**。

正确做法：
- 私有原件作为证据；
- 仓库存 capture ID、文件清单、时间节点、脱敏结论、关键源码。

# 9. 已知必须纠正的旧结论

1. Day7 不是“D最后25分钟才开始”。
2. Day7 B 不是“没冻结 partial”；稳定版保存过 WA.cpp。
3. Day7 B 不是“没意识到复杂度”；赛时明确说 calc 慢，并想到离线。
4. Day7 不能再写“赛时已知 score floor=174”。正确状态是 A100[SCORED] / B?[FROZEN] / C10[PROVED] / D19[PROVED]；174只是在已知最终B45后的赛后反事实。
5. 新体系榜单的39个0分行很多是尚未开始账号，不能做最终参赛者统计。
6. 新体系 tree 的错误测试文件不是简单“旧目录污染”；Replay 证明赛时确实从下载包复制进 T4 并用于验证，但格式与题面不符。

# 10. 最后一条

如果用户指出“你没看录音 / 没解 ZIP / 没看捕捉器”，不要争辩。

先重新取证，再改仓库。

**仓库里的错误分析也必须允许被后来的更强证据推翻。**


# 11. 2026-10-07 新增接管信息

## 七场代码源原始归档重新交叉验证

不要只沿用旧总结数字。现有：

- `tools/archive/代码源Day1-Day7_归档证据清单.csv`
- `tools/archive/代码源Day1-Day7_来源与交叉验证.md`

record score 可直接恢复：

`45 → 130 → 204 → 0 → 15 → 115 → 145`

Day7 后续以 2026-10-06 15:10 新归档为主；它包含 105 行榜单。旧 04:07 版只做归档工具差异对照。

## BAG

当前推荐是 `tools/vm/bag_v4_flat/`。

理解重点：
- V4 强不在脚本多；
- 强在一份 main.cpp + 一池 testcase；
- 官方样例 / 手工 Debug / stress 反例全部自动进入同一回归系统；
- 工具目标是让正确动作成为默认动作。

先读：
- `tools/vm/BAG_演化史与赛场工作流.md`
- `tools/vm/虚拟机赛场工程经验.md`

## Coderlands

底层 OJ 引擎未确认。

禁止仅凭 Vue / Element UI 写成 Hydro/HUSTOJ 改版。

当前可靠的是 DOM 采集规格，见：

`tools/archive/Coderlands_平台与采集路径初步勘查.md`

后续应先做正常登录浏览器 DOM adapter；观察到真实只读 API 后再升级数据层，禁止猜接口。


## 接手控制平面（10/7）

第一入口改为：
`总览/AI直接接手入口.md`

全 32 题统一索引：
- `总览/全题总表_32题.md`
- `总览/全题总表_32题.csv`

阶段经验：
- `总览/每场比赛经验纪要.md`
- `总览/阶段数据与预测.md`
- `总览/可视化/阶段成长仪表盘.html`

下一场直接执行：
- `执行包/下一场比赛_赛前执行包.md`

考古新增硬规则：
- `模拟赛考古纪要协议.md`
- 读取原始证据后必须 append-as-you-read；
- 不得只把智能纪要当作已读原始材料；
- OJ-AC、[P]、[E]、[H]、[X] 必须区分。


# 12. 三包长期原始资料池（2026-10-07 固定）

后续模拟赛仓库持续经营只从以下三包继续做原始证据考古：

- `/CSP-S模拟赛资料/原始三包/模拟赛资料_01_共03包.zip`
- `/CSP-S模拟赛资料/原始三包/模拟赛资料_02_共03包.zip`
- `/CSP-S模拟赛资料/原始三包/模拟赛资料_03_共03包.zip`

它们已经保存到 ChatGPT Library，不再依赖本次聊天附件生命周期。

接手先读：

1. `tools/archive/三包原始资料_处理台账.md`
2. `tools/archive/三包递归扫描_统计摘要.md`
3. `tools/archive/recursive_zip_inventory.py`
4. `证据阅读台账.md`

2026-10-07 depth≤3 首轮 inventory：

- 9,073 rows；
- 195 个 nested ZIP 成功打开；
- 0 个 ZIP open error；
- 34 组重复 nested-ZIP 内容哈希；
- 169 个 ZIP 路径落在重复哈希组里。

所以后续工作单位优先改成：
`content hash + provenance + contest mapping + extraction status`，
不要把重复 VM 快照里的相同 ZIP 当成全新材料重复分析。

Replay recorder 源码审计已新增：

- `tools/vm/Replay采集脚本_源码考古与能力边界.md`
- `tools/vm/replay_recorder/contest_replay_capture_v3.0.1.patch`

其中 v3.0.0 已证明存在 pause/raw 语义缺口；以后解释 raw_keys 与 timeline 冲突时必须先查 recorder 版本与 pause status。


# 13. 2026-10-07 三包深挖第二轮

## Day7 主 capture 已做 file_changes 全量版本考古

入口：
- `2026-10-06_CSP-S模拟赛day7/回放数据/file_changes_完整版本时间线_20261006_080043.md`
- `2026-10-06_CSP-S模拟赛day7/逐段考古纪要.md` E-D7-011/012

关键事实：
- 59 条 file_changes；
- B stable→失败重写→exact rollback→WA.cpp freeze→最终只补 IO；
- C 没有 T3/main.cpp 保存事件，最终仍 starter template；
- D 有 20 个 main 保存状态，1663B 候选后主动推倒到 583B；
- capture 早期出现的 `CSP-S/Day6/foo*.cc` 属历史目录事件，不应计入 Day7 T1~T4 研究量。

## Day6 已完成“正式提交源码 ↔ Replay snapshot”精确映射

入口：
- `2026-10-05_CSP-S模拟赛day6/回放数据/file_changes_语义版本时间线_20261005_101100.md`
- `tools/archive/replay_submission_matcher.py`

四份 OJ source 均得到唯一 exact normalized-content match：
- A → T1 save #9；
- B → T2 save #6；
- C → T3 save #30；
- D → T4 save #10。

新硬规则：
> VM 最终工作区不能默认当正式提交源码；先用 OJ source 与 file_changes 内容精确匹配。

Day6 额外新证据：
- B 12 分钟内把实现/类型错误修干净，但错误数学 predicate 不变；
- D 主动用 `phi(1), phi(2), phi(6)` 做最小微型探针，随后修边界与 leftover prime 条件；
- C 四分类真实进入代码的窗口约 13:30～13:32，后来发生语义退化。

## 旧 VM 血缘已闭合到 Day3→Day4

入口：
`tools/archive/旧VM快照_血缘与Day3Day4迁移.md`

03包：
- `虚拟机.zip` 410 文件；
- `虚拟机(1).zip` 595 文件；
- 338 个同路径共同文件中 310 个同 SHA，只有 28 个同路径内容变化；
- 旧快照根 T1～T4 有 60 个文件在新快照 `Desktop/Day3/T1~T4` 中原 SHA 迁移保存。

因此旧快照要做 path-move/content-hash 去重，不能重复读 310 个纯副本。

## Day4 新钉死事实

- A OJ CE 的具体原因已定位：正式提交的 `freopen ("Thermokinesis.out, "w", stdout);` 字符串引号错误；赛后 VM 版本已把两行 freopen 注释，所以只看最终本地文件会漏掉事故。
- B OJ source 与 `虚拟机(1).zip!Desktop/T2/main.cpp` 完全一致。
- D OJ submitted source 与 VM 后续版发生结构性分叉，不能互相替代。

## Recorder baseline 措辞修正

v3.0.0 的 FileTracker **有** `_seed_state()` fingerprint 基线；缺的是“启动时把全部现有文件内容写入 file_changes 的 initial snapshot”。以后禁止简写成“没有 baseline”。
