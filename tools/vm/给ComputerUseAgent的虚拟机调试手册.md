> ⚠ **已作废**：这份文档里 Code::Blocks 的设置项名称没有按 20.03 版本核对，有几项在你的版本里根本不存在。Code::Blocks 的四个问题以同目录的《CodeBlocks四个问题_源码核实版.md》为准。

# 虚拟机调试手册（给 Computer Use Agent）

> 读者：替小苏同学操作电脑的 Computer Use Agent。
> 目标：把模拟赛用的 Linux 虚拟机调到"开赛就能用、全程不出幺蛾子"。
> 依据：2026-09-25 模拟赛的录音转写 + 虚拟机桌面导出。下面每个问题都标了录音里出现的时间点。

---

## 0. 先读：规则

1. **先拍快照**。动任何东西前，在虚拟机软件里拍一个快照，命名 `before-fix-日期`。
2. **不删用户文件**。桌面上的 `problems/`、`duipaiT*/`、`debug/` 等目录一律不删，只能新增。
3. **要装软件先问用户**。`sudo` 密码让用户自己输，Agent 不要代输，也不要记录。
4. **每改一项，就在 `~/Desktop/虚拟机修改记录.txt` 追加一行**：时间 / 改了什么 / 怎么验证的 / 结果。
5. **比赛进行中不要操作**。只在赛前或赛后操作。
6. 做完后按第 3 节的验收清单逐项打勾，把清单结果发给用户。

---

## 1. 已知环境

| 项目 | 值 | 来源 |
|---|---|---|
| 系统 | NOI Linux 2.0（Ubuntu 20.04） | 编译产物里是 `GCC: (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0` |
| 用户名 | `sutong`，桌面在 `/home/sutong/Desktop` | Code::Blocks 的 `debug.depend` |
| IDE | Code::Blocks，桌面上有个 `debug` 工程（`debug.cbp`，Debug 目标是 `-g`，Release 目标是 `-O2 -s`） | 导出文件 |
| 编辑器 | Sublime Text 也在用 | 录音 10:30 |
| 浏览器 | 用来打开 OJ | 录音 |
| 宿主机 | 大概率是 Windows | 用户平时环境 |
| 虚拟机软件 | **未知**，第一步先确认是 VMware 还是 VirtualBox | — |

先在虚拟机终端执行下面这条，把输出记进修改记录：

```bash
lsb_release -a; uname -r; nproc; free -h; df -h ~; echo $XDG_SESSION_TYPE; timedatectl | head -5; which codeblocks subl gnome-terminal xterm gdb
```

---

## 2. 问题清单（按优先级）

### P1｜Code::Blocks 运行的不是屏幕上这份代码（最致命）

**现象**（录音 55:26 至 57:28）：
- "我都不知道我这代码是不是我的"
- "我不小心删了个大括号，它是怎么编译起来的？"
- "每改一次代码之后，要退出一次编译器才能有用"

**最可能的原因**：Code::Blocks 里打开了 `debug` 工程，又单独打开了别的 `.cpp`。这时按 F9，编译运行的是**当前激活工程里的 main.cpp**，而不是屏幕上正在编辑的文件。

**Agent 要做的**：
1. 复现：打开 `debug` 工程，再单独打开一个故意写错语法的 `test.cpp`，按 F9，看看是不是照样"成功运行"。把结果记下来。
2. 把下面这条规则写进 `~/Desktop/比赛须知.txt`，并当面告诉用户：
   - **比赛时编译和测样例一律用终端里的 `run.sh`（见第 4 节），不用 Code::Blocks 的 F9。**
   - Code::Blocks 只在要断点调试时用：把代码整份粘进 `debug/main.cpp`，确认顶部 Build target 选的是 **Debug**（不是 Release）再调。
3. 顺手检查一下：导出里 `debug/bin/Release/debug` 在赛中（北京时间 19:37）被编译过，说明当时切到过 Release。**Release 是 `-O2 -s`，没有调试信息，断点停不下来**。把默认目标设回 Debug。

**验证**：在 `debug/main.cpp` 里改一行输出，按 F9，输出要跟着变。

### P2｜控制台窗口弹两个 / 一闪就退 / 不停下来

**现象**（录音 43:26 至 49:22、1:05:18、1:51:36、1:56:45）："F9 没反应""弹出来两个窗口，其中一个有用""为什么它直接退出了""换成这个终端它就没事了"。

**原因**：Code::Blocks 用来运行控制台程序的终端命令没配好。如果用 `gnome-terminal` 却没加 `--wait`，窗口会立刻返回或者多开一个。

**Agent 要做的**：
1. 打开 Settings → Environment → General settings，找到 "Terminal to launch console programs"，截图记下当前值。
2. 改成：`gnome-terminal --wait -t $TITLE -x`（前提是 `which gnome-terminal` 有输出）。如果只有 xterm，就用 `xterm -T $TITLE -e`。
3. 保存。关掉 Code::Blocks 时如果弹 "Default is changed, do you want to save it?"，选 **Yes**，让设置写盘。

**验证**：用 `debug` 工程跑一个读入一个数再输出的程序。要求只开一个窗口，能正常输入，结束后停在 "Press ENTER to continue"。

### P3｜关闭 Code::Blocks 时一连串 Yes/No 对话框

**现象**（录音 1:03:11、1:09:50、1:15:42、1:20:06）："又弹出来一堆东西让我点 yes no""你说啥都可以，你别给我罢工就行"。

**原因**：P1 逼得用户每改一次就重启 IDE，每次关都要问"保存工作区/工程吗"。另外 Sublime 和 Code::Blocks 同时开着同一个文件，也会反复问"文件在外部被修改，要重新加载吗"。

**Agent 要做的**：
1. P1 解决后，这个问题自然会少很多。
2. 在 Code::Blocks 的 Settings → Environment 里找和"退出时确认/保存工作区"有关的选项（不同版本名字不一样）。设成自动保存、不再询问。**找不到就别硬改，记下来就行。**
3. 找到"检测外部修改的文件"一类的选项，设为自动重新加载（不弹窗）。
4. 在 `比赛须知.txt` 写上：**同一个文件只在一个编辑器里开。**

### P4｜编辑器没有自动缩进

**现象**（录音 59:39）："为啥这连缩进都没有""这都不自动缩进的吗"。

**Agent 要做的**：Code::Blocks → Settings → Editor → General settings，勾上 Auto indent 和 Smart indent，Tab 宽度设为 4、用空格代替 Tab（用户的代码是 4 空格缩进）。Sublime 默认就有，不用动。

### P5｜终端命令复制粘贴不了，每次都手敲

**现象**（录音 1:15:42、3:40:31）："这个终端复制不了""这个指令复制粘贴不了，每次都得重打一遍"。录音 2:19 到 2:21 还因为手敲 `g++ …; ./T1 < 3-1.in > ans.out; diff …` 敲错好几次（"键盘敲太快了，终端卡死"）。

**Agent 要做的**：
1. 教给用户：gnome-terminal 里复制是 Ctrl+Shift+C，粘贴是 Ctrl+Shift+V；xterm 里选中就是复制，按鼠标中键粘贴；**按 ↑ 键调出上一条命令，按 Ctrl+R 搜索历史命令**。
2. 安装 `run.sh`（第 4 节）。装好后测样例只需要一条命令 `./run.sh T1`，从根上消灭手敲。
3. 宿主机和虚拟机之间的剪贴板共享：
   - VMware：确认装了 open-vm-tools-desktop（问用户后再装），在虚拟机设置里打开"共享剪贴板"
   - VirtualBox：装增强功能（Guest Additions），设备 → 共享粘贴板 → 双向

   这一项只在训练时有用，真实考场没有宿主机。

### P6｜鼠标突然没了

**现象**（录音 3:39:52）："为什么我鼠标没用了"。

**Agent 要做的**：
1. 告诉用户释放鼠标的热键：VMware 是 Ctrl+Alt，VirtualBox 是右 Ctrl。写进 `比赛须知.txt`。
2. 装好 P5 第 3 步的增强工具后，鼠标会自动在宿主机和虚拟机之间切换，不再被"抓住"。

### P7｜虚拟机卡顿（终端卡死、虚拟机卡死）

**现象**（录音 2:21:42、3:14:46）："终端卡死""虚拟机卡死了"。

**注意，要先纠正用户的一个误判**：录音 2:23 用户说 T1 跑 7 秒是"机子内核少，跑的慢"。**这不对**。那份代码用了 `std::distance` 在 multiset 上数个数，每次是 O(n)，整体接近 O(n³)。在一台正常的 4 核云服务器上重跑，n=2000 用了 9.2 秒，n=5000 超过 60 秒。而且单线程程序，核多也没用。所以不要为了"跑得快"去调虚拟机。调资源只是为了**界面不卡**。

**Agent 要做的**：
1. 关掉虚拟机后，在虚拟机软件里设：CPU 4 核（不超过宿主机物理核数的一半），内存 4 到 8 GB，显存/3D 加速按默认。
2. Windows 宿主机：电源计划改成"高性能"，比赛期间关掉大型软件（游戏、多开的浏览器、本地大模型）。
3. 在虚拟机里关掉 Ubuntu 的动画效果（可选）。

**验证**：开机后在终端连续快速敲字 30 秒，不能出现卡顿。`nproc` 和 `free -h` 显示的数值要和设置一致。

### P8｜系统时区错了 12 个小时

**证据**：虚拟机里所有文件时间比北京时间慢 12 小时，归档脚本也报"本地时区 America/New_York"。比如开赛是北京 19:04，文件时间显示的是 07:01。

**Agent 要做的**（需要用户输 sudo 密码）：
```bash
sudo timedatectl set-timezone Asia/Shanghai
timedatectl
```
**验证**：`date` 显示的时间和宿主机右下角一致。同时检查浏览器（归档脚本在浏览器里跑）显示的时区也变成上海了。

### P9｜Sublime Text 弹更新提示

**现象**（录音 3:17:36）："差点给我点了，差点给 Sublime Text 更新了"。

**Agent 要做的**：Sublime → Preferences → Settings，在右边用户设置里加上 `"update_check": false,`，保存。

### P10｜赛前准备的东西一次都没用上

**证据**：录音 04:21 到 09:24（约 5 分钟），用户赛前手工建了 `duipaiT1` 到 `duipaiT4` 四个对拍文件夹和一个 `debug` 工程。导出文件的时间显示，四个对拍文件夹里的 `ac.cpp`/`wa.cpp`/`gen.cpp` 从赛前一天到赛后**一直是空模板**，比赛中一次都没用。

**Agent 要做的**：
1. 在 `~/Desktop` 放一个 `init.sh`（内容见第 4 节）。赛前执行一次，就建好 `T1` 到 `T4` 四个文件夹，每个里面有模板 `Tx.cpp` 和 `run.sh`。
2. 对拍文件夹保留，但不再提前建四份，要用时再复制。

---

## 3. 验收清单（全部做完后发给用户）

| # | 项目 | 验证方法 | 结果 |
|---|---|---|---|
| 1 | 快照已拍 | 快照列表里能看到 | ☐ |
| 2 | P1 复现结论已记录，默认 Build target 是 Debug | 改代码按 F9，输出跟着变 | ☐ |
| 3 | 控制台终端配置正确 | 只弹一个窗口，结束后停住 | ☐ |
| 4 | 自动缩进打开 | 输入 `{` 回车后自动缩进 4 格 | ☐ |
| 5 | run.sh 已安装并测过 | 在 T1 目录执行 `./run.sh T1`，输出 OK/WA 列表 | ☐ |
| 6 | init.sh 已安装并测过 | 在临时目录执行，生成 T1 到 T4 | ☐ |
| 7 | 剪贴板共享可用（训练用） | 宿主机复制一段文字，虚拟机终端能粘贴 | ☐ |
| 8 | 鼠标不再被抓住 | 移出虚拟机窗口不用按热键 | ☐ |
| 9 | 资源已调整 | `nproc` / `free -h` 截图 | ☐ |
| 10 | 时区是 Asia/Shanghai | `timedatectl` 截图 | ☐ |
| 11 | Sublime 不再提示更新 | 设置文件截图 | ☐ |
| 12 | 修改记录和比赛须知已写好 | 两个 txt 都在桌面上 | ☐ |

---

## 4. 要放进虚拟机的两个脚本

### 4.1 `run.sh`：一键编译 + 跑全部样例

把本仓库 `tools/vm/run.sh` 的内容原样放到虚拟机的 `~/Desktop/run.sh`，然后执行 `chmod +x ~/Desktop/run.sh`。

用法：在题目文件夹里执行 `./run.sh T1`。它会编译 `T1.cpp`，把文件夹里所有 `*.in` 跑一遍，和同名的 `.out`（或 `.ans`）比对，每个样例打印 OK / WA / TLE / RE 和耗时。`./run.sh T1 d` 是调试模式，会检查数组越界和整数溢出。

注意：B 题这种**多解题（special judge）**不能直接 diff，会全报 WA，要用题目给的 checker 检查。

**考场手敲版**（真实考场不能带文件，让用户背下这 5 行，开考 2 分钟内敲完）：
```bash
g++ $1.cpp -o $1 -O2 -std=c++14 -Wall || exit 1
for i in *.in; do
  timeout 10 ./$1 < $i > my.out
  diff -wq my.out ${i%.in}.out > /dev/null && echo "$i OK" || echo "$i WA/TLE/RE"
done
```

### 4.2 `init.sh`：赛前一键建题目文件夹

```bash
#!/bin/bash
# 用法：cd ~/Desktop && ./init.sh
for i in 1 2 3 4; do
    mkdir -p T$i
    [ -e T$i/T$i.cpp ] || cp ~/Desktop/template.cpp T$i/T$i.cpp
    cp ~/Desktop/run.sh T$i/
done
echo "T1 到 T4 已建好"
```

`~/Desktop/template.cpp` 用用户现在的模板（`原始的Desktop/problems/T1.cpp` 那份，`#include <bits/stdc++.h>`、`#define int long long`、`signed main ()` 那套）。

**赛时流程**（写进 `比赛须知.txt`）：
1. 下载样例 zip，解压到对应的 `Tx/` 文件夹
2. 在 Sublime 或 Code::Blocks 里写 `Tx/Tx.cpp`
3. 在终端 `cd ~/Desktop/Tx`，执行 `./run.sh Tx`
