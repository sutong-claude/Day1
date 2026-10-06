# Day7 原始材料与验证说明

## 已摄入的用户材料

本轮完整处理：

1. Day7.zip
   - 1369 个 ZIP 条目；
   - 约 610 MB 解压体积；
   - 当前比赛 recorder 目录为 Desktop/contest_capture/20261006_080043；
   - 读取 timeline、file_changes、manifest，并抽取/检查屏幕录像；
   - 不把 raw_keys 或屏幕录像上传公开仓库。

2. Day7_原文.docx
   - 47 页；
   - 主录音转写，约 4 小时；
   - 逐段用于重建赛时思路。

3. 2026-10-05 19_58 记录_原文.docx
   - 54 页；
   - 与主录音同场的另一版转写；
   - 作为 ASR 交叉校对，不把两份内容误当两场比赛。

4. 代码源新 OJ day7 完整归档 ZIP
   - 92 个条目；
   - 核对四题题面、subtask HTML rowspan、两份本人提交、测试点状态、原始页面和诊断。

5. day7 AI 提示词纯文本
   - 3179 行；
   - 用于快速索引题面/源码/测试表；
   - 关键 subtask 和分数仍回原 HTML / OJ 测试表核对。

6. 智能纪要
   - 仅作辅助导航；
   - 不用它替代原录音。

## Recorder 状态

- start：2026-10-06T08:00:43
- end：2026-10-06T12:00:52
- stop：Ctrl+Alt+Q
- screen：ffmpeg 1fps
- session screen 段编号覆盖 screen_000 到 screen_024
- 屏幕中点拼图已人工浏览，能看到 T1 → T2 → C/D 题面 → T4 代码 → 最终 B 提交的整体流程。

## 代码演化

file_changes：
- T1/main.cpp：8 次保存
- T2/main.cpp：17 次保存，16 个独立内容
- T2/WA.cpp：113.35 分钟时冻结
- T3/main.cpp：0 次
- T4/main.cpp：20 个独立状态

## OJ 核对

最终：
- A 100 Accepted
- B 45 Runtime Error
- C 0，无提交
- D 0，无提交

B：
- subtask1 20 AC
- subtask2 25 AC
- subtask3 两个隐藏点约 227 MiB RE，整档 0

## 赛后验证

### A
赛时代码即 OJ 100。

### B full DSU
已写反向加点 + DSU 版本。
赛后使用小随机树，与 O(n²) 定义直译 oracle 做随机交叉验证，一致。

### C partial
v=50 公式与端点固定公式已写入 25 分 special 文件。
其中 r=1,k=1,v=80 对应官方 4/5。

### D brute
N<=100 O(n³) oracle 已跑官方三个样例：
- 6 2
- 2 3
- 0 1
全部一致。

## 隐私

不上传：
- raw_keys
- 完整屏幕视频
- VM 用户目录
- 录音原文全文

公开仓库只保存从这些证据中提炼的：
- 时间线
- 代码考古
- 题解/partial
- 验证结论
- 下一场规则
