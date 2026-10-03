# BAG V3.1 实战 / 压力测试报告

日期：2026-10-03

## 结论

原始 `bag(1).zip` 不是一个可靠的正式比赛包。它的最大问题不是“功能少”，而是会产生**假安全感**：

- `gen.cpp` 为空时，旧 `duipai.sh` 仍可不停输出 `right on test ...`；
- 编译失败后可能继续执行旧二进制；
- 候选程序死循环时没有 timeout；
- 没有一键扫描 / 批量运行大样例；
- 没有稳定的 freopen 实测；
- 没有部分失败取证；
- 没有快速、安全的恢复机制。

`bag_v3_1_final.zip` 是在原包上按真实 CSP-S 比赛事故重建后的版本。

我不能严肃地证明它“世界第一”——这需要和其他所有人的私有竞赛环境做可复现基准。
但就**小苏同学当前的 NOI Linux / Code::Blocks / 大样例 / 对拍 / 高频恢复工作流**而言，
这是目前做出来的版本里最强、最稳、最贴近真实事故的一版。

---

## 1. 真正执行过的测试

### A. 原始包故障注入

原包实测：

1. 空 `gen.cpp`：约 10 秒内可产生数百条假的 `right on test`；
2. `main.cpp` 编译失败但旧 binary 还在：旧脚本继续跑旧程序；
3. `main.cpp` 死循环：旧脚本整套挂住；
4. 没有自动批量大样例流程。

这些不是“理论风险”，都已经实际复现。

### B. 真实比赛大样例工作流

使用 Day3 A 的真实已 AC 源码和真实 `problem_1874.zip`：

#### 直接把 ZIP 丢进 T1

运行：

```bash
bash run.sh
```

结果：

- 2 / 2 官方大样例通过；
- 自动解压；
- 自动匹配 `.in/.out`；
- 不需要手动改脚本。

#### 先解压到 `samples/`

再次运行：

- 2 / 2 通过。

说明用户希望的流程：

> 下载附件 → 解压 / 粘贴进去 → `bash run.sh`

已经真正打通。

### C. freopen 真提交形态

把真实 Day3 A 代码改成 active：

```cpp
freopen("Chant.in", "r", stdin);
freopen("Chant.out", "w", stdout);
```

`bash check.sh` 结果：

- exact `main.cpp` 编译成功；
- stdin 测试副本全部样例通过；
- 原始 exact binary 的真实文件 IO smoke test：`FILEIO: OK`；
- `CHECK: GREEN`。

也就是说，不需要为了本地测样例来回注释 freopen。

### D. 50 MB 单输入

人工生成：

- 输入：50,000,010 bytes；
- 25,000,000 个数据项。

结果：

- 正确；
- 程序执行约 1.02 秒；
- runner 总耗时约 3.20 秒；
- 成功样例输出不会在 `.work` 中无限堆积。

### E. 5000 对样例文件

生成：

- 5000 个 `.in`
- 5000 个 `.out`

结果：

- `5000 / 5000 PASS`
- 样例执行 wall time 约 21.1 秒；
- 总命令约 22.5 秒；
- `.work` 最后只保留编译缓存，没有留下 5000 份输出垃圾。

### F. 对拍 10,000 组

用独立的：

- `main.cpp`
- `AC.cpp`
- `gen.cpp`

分四批 seed 区间，各跑 2500：

- 2500 / 2500 PASS
- 2500 / 2500 PASS
- 2500 / 2500 PASS
- 2500 / 2500 PASS

总计：

**10,000 / 10,000 PASS**

速度约：

**127～132 tests/s**

这是每组都重新启动 generator / oracle / candidate 的强隔离模式，不是把 10000 组塞进一个进程糊过去。

### G. 故障注入

新版已实测识别：

- CE：立即停止；
- WA：指出第一个不同 token；
- RE：捕获非零返回码；
- TLE：按 timeout 杀掉；
- bad freopen：`FILEIO: NO_OUTPUT_FILE`；
- generator 为空：直接拒绝；
- candidate / oracle 同时空输出：直接拒绝“假绿”；
- oracle RE / TLE：单独报错；
- candidate RE / TLE：单独报错；
- 超内存：使用 `--memory-mb` 可拦截；
- stress WA：自动保存 input / main.out / ac.out / stderr / 三份源码；
- sample WA/RE/TLE：自动保存 forensic bundle。

### H. SPJ / 构造题

默认 token 比较时，一个“不同但可能合法”的构造输出会被判 WA。

使用：

```bash
bash run.sh --mode none
```

实测会改为：

- 只检查 CE / RE / TLE；
- 不会误要求输出文本和官方样例完全相同。

这解决了 Day3 B 这种构造题“官方 sample output 不唯一”的通用问题。

注意：`--mode none` **不是正确性证明**。构造合法性仍需题目 checker / 独立 oracle。

### I. ASan / UBSan

运行：

```bash
bash run.sh --sanitize
```

实测 sample runner 能以：

- AddressSanitizer
- UndefinedBehaviorSanitizer

运行样例。

用于抓越界 / UB，不用于正式性能计时。

### J. 中文 / 空格 / 括号 / 嵌套目录

实测：

- 中文目录；
- 目录带空格；
- 目录带括号；
- ZIP 名带中文 / 空格 / 括号；
- ZIP 内嵌套目录；
- sample 文件名带中文 / 空格 / 括号；
- `.ans`

均可运行。

### K. 恶意 ZIP 路径

构造 ZIP 内：

```text
../../../../ESCAPE_TEST.in
```

V3.1 会直接拒绝：

```text
unsafe zip path
```

不会写出工作目录。

### L. 快速恢复

旧 V3 的 `restore.sh` 发现了真实 bug：

> reset T1 时，sample 会消失，而且备份里没有 sample。

V3.1 改成：

- 把整个旧 `T1` 在同一文件系统内直接 `mv` 到 `backups/`；
- 再复制空白 template。

8 MB sample 实测：

- 完整 sample 保留；
- failcase 保留；
- source / notes 全保留；
- 恢复约 **18.5 ms**；
- 没有复制一份大样例造成双倍磁盘占用。

### M. 快速创建

命令：

```bash
bash ~/Desktop/bag/new_contest.sh Day5 --open
```

实测：

- 创建 T1～T4；
- 中文 / 空格 / 括号比赛名正常；
- 二次创建同名目录会安全拒绝；
- `--open` 会把 `T1/AC.cbp` 传给 `codeblocks`。

### N. Code::Blocks 项目

当前测试容器没有安装 Code::Blocks GUI，本次无法诚实声称“我在这个容器里实际点开 GUI 编译”。

做了两层替代验证：

1. 解析 `AC.cbp`，确认唯一 Unit 为 `main.cpp`；
2. 按 `.cbp` 中真实 Debug / Release flags 分别执行：
   - `-std=c++17`
   - `-O2`
   - `-Wall`
   - `-Wextra`
   - Debug 额外 `-g`

两种 target 均编译并运行成功。

另外 V3.1 的 `selftest.sh` 已加入：
- 如果机器上存在 `codeblocks` 且有 X11 DISPLAY，
- 自动执行 Code::Blocks batch build，
- 并检查 `bin/Debug/main` 是否真实生成。

所以在用户的 NOI Linux VM 上运行：

```bash
cd ~/Desktop/bag/T1
bash selftest.sh
```

就能做最后一层**真实 Code::Blocks**验证。

---

## 2. 推荐比赛流程

### 开赛前

```bash
bash ~/Desktop/bag/doctor.sh
cd ~/Desktop/bag/T1 && bash selftest.sh
```

第一次确认环境通过即可。

### 新比赛最快创建

```bash
bash ~/Desktop/bag/new_contest.sh Day5 --open
```

### 每题

只写：

```text
T1/main.cpp
```

大样例解压后直接扔：

```text
T1/samples/
```

然后：

```bash
bash run.sh
```

### 构造 / SPJ

```bash
bash run.sh --mode none
```

### 怀疑越界 / UB

```bash
bash run.sh --sanitize
```

### 对拍

写好：

```text
AC.cpp
gen.cpp
```

然后：

```bash
bash duipai.sh
```

或：

```bash
bash duipai.sh 10000
```

### 交之前

```bash
bash check.sh
```

只有 `CHECK: GREEN` 再上传 `main.cpp`。

### 赛后 / 需要瞬间复原

```bash
bash ~/Desktop/bag/restore.sh T1
```

或：

```bash
bash ~/Desktop/bag/reset.sh
```

旧目录完整保留到 `backups/`。

---

## 3. “是不是最优方案？”

对于你当前实际习惯：

> 下载大样例 → 解压 → 粘贴到题目目录 → 写代码 → 一条命令测全部 → 有问题对拍 → 最后 check

我认为这是一个非常好的主流程，而且比“手动复制命令、手动改 freopen、手动一组一组测”稳定得多。

我更推荐把样例放 `T1/samples/`，原因只有一个：

> T1 根目录永远保持干净，比赛越到后面越不容易混文件。

但 runner 也支持你直接把 zip / `.in/.out` 丢到 T1 根目录，作为最快应急方式。

---

## 4. 仍不能吹成“世界第一”的原因

目前仍有三类无法由通用包自动解决的东西：

1. **SPJ / checker 的语义正确性**：通用 runner 不知道题目真正合法条件；
2. **oracle 自身写错**：Day4 B 已经证明“有 brute ≠ brute 正确”；
3. **真实 Code::Blocks GUI 人机流程**：本容器没有 Code::Blocks，需在 NOI Linux VM 跑 `selftest.sh` 完成最后验收。

所以准确说法是：

> **BAG V3.1 已经通过大规模工程压力测试，是目前针对你的比赛工作流最可靠的一版；但“世界第一”不能靠口号证明。**

如果 NOI Linux VM 上 `selftest.sh` 最后显示：

```text
Code::Blocks=PASS
```

那么它就完成了从“容器级工程测试”到“你真实比赛环境”的最后一环。
