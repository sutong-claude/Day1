# B local checker 的关键边界

checker 源码开头原文含义：NO 会被跳过；这个程序不判断是否存在解。

核心分支：
- 输出 NO：直接 Skipped，计数后 continue。
- 输出 YES l r：真正执行 reverse，然后栈约简；不为空则 WA，空则 construction valid。

因此它只能证明“你给出的 YES 构造合法”，不能证明“你输出的 NO 确实无解”。

Day3 sample7 正是因此出现假绿：你的第4组 NO 与官方 YES 冲突，checker 仍返回0。
