# Code::Blocks 四个问题（源码核实版）

依据：Code::Blocks 20.03 源码（NOI Linux 2.0 基于 Ubuntu 20.04，装的就是 20.03），逐条找到了弹窗原文和触发它的代码。全部操作都在 Code::Blocks 界面里点，不需要敲终端命令。

## 结论

四个问题其实是两个原因加一个无害提示：

| 你遇到的 | 原因 | 怎么办 |
|---|---|---|
| ① 调试时提示“终端被关了，要不要停止” | 终端选了 gnome-terminal，调试器误以为窗口被关了 | 终端改回第一项 `xterm -T $TITLE -e` |
| ② 一运行就 return 0 | debug 工程开着时，F9 编译运行的是**工程里的 main.cpp**（空模板），不是你屏幕上那份 | 平时写题先关掉工程 |
| ③ 编译运行不自动保存 | 同 ②：只保存工程里的文件，你那份不在工程里 | 同 ② |
| ④ “Code::Blocks default has changed” | 窗口布局变了，问要不要记住，和代码无关 | 点 Yes；勾上 Don't annoy me again! 以后不再问 |

## ① Terminal/Console closed

**弹窗原文**（标题 Terminal/Console closed）：
> Detected that the Terminal/Console has been closed. Do you want to stop the debugging session?

**原因**：调试时 Code::Blocks 先打开一个终端窗口，记下这个终端程序的进程号，之后定时检查它还在不在，不在就认为你把窗口关了，弹这个框（源码 `debuggergdb.cpp` 的 `CheckIfConsoleIsClosed`）。

- gnome-terminal 的工作方式是：启动它时，它只是通知后台一个常驻程序去开窗口，自己马上退出。窗口还开着，但 Code::Blocks 记下的那个进程已经没了，于是误报。源码 `cbplugin.cpp` 里开发者自己写了注释：gnome-terminal 这类终端用共享的服务进程，启动的终端进程会立刻退出。
- 20.03 的下拉框第二项是 `gnome-terminal -t $TITLE -x`，没有 `--wait`，正好中招（Code::Blocks 后来的版本把这一项改成了带 `--wait`）。
- xterm 是一个窗口就是一个进程，窗口开着进程就在，不会误报。所以你说“只有换成第一个终端才有用”。

**怎么办**：Settings → Environment… → 左边 General settings → 最下面 “Terminal to launch console programs:” → 选第一项 `xterm -T $TITLE -e` → OK。

- xterm 里**鼠标选中就是复制，按鼠标中键（滚轮按下去）粘贴**；Ctrl+C 在终端里是“中断程序”，不是复制。
- 嫌 xterm 字小：那个框可以直接打字，改成 `xterm -fa Monospace -fs 14 -T $TITLE -e`（14 是字号）。
- 弹这个框时**不要**勾 Don't annoy me again!，否则以后会自动替你选。

## ② 一运行就 return 0

**原因**：F9 是 Build and run。源码 `compilergcc.cpp` 的 `DoBuild` 和 `Run`：只要有打开的工程（左边 Projects 里加粗的那个），就编译运行**这个工程**；只有没有工程时，才编译运行当前这个文件。

- 你赛前建的 debug 工程，main.cpp 是空模板（`main` 里只有 `return 0`），导出的赛前桌面里能看到。
- 所以你在 T1.cpp 里写代码、按 F9，编译运行的是 debug 的空模板，立刻显示 `Process returned 0 (0x0)`。
- 这也解释了你当时说的“这代码好像不是我的”“删了个大括号它还能编译”“每改一次要重启编译器才有用”（重启后工程没被重新打开，F9 才去编译当前文件）。

**怎么办**：
- 平时写题：左边 Projects 里右键 debug → Close project（或 File → Close project）。没有工程时，F9 就编译并运行你眼前这个文件。
- 要断点调试（20.03 的调试器需要工程）：把代码整份粘进 debug 的 main.cpp 再调，并确认工具栏上的 Build target 是 **Debug**。Release 是 `-O2 -s`，没有调试信息，断点停不下来；导出文件显示你赛中 19:37 编过一次 Release。

## ③ 编译运行后不自动保存

**原因**：和 ② 是同一件事。源码里，编译工程前只保存**属于这个工程的文件**（`m_pProject->SaveAllFiles()`）；没有工程时，编译前会先保存当前文件（`EditorManager::Save(file)`）。你那份 T1.cpp 不在 debug 工程里，所以既不保存也不编译。

**怎么办**：同 ②，关掉工程就好。顺手养成 Ctrl+S 的习惯。

## ④ “Code::Blocks default is changed” 和一堆 Yes/No

**弹窗原文**（标题 Layout changed）：
> The perspective 'Code::Blocks default' has changed. Do you want to save it?

- perspective 就是**窗口布局**：左边项目栏、下面日志栏这些面板摆在哪，日志栏当前选中哪个标签。`Code::Blocks default` 是默认布局的名字。
- 什么时候弹：每次开始调试、结束调试（Code::Blocks 会切到调试布局再切回来），以及关闭 Code::Blocks 时，只要布局变过就问。连下面日志栏从 Build log 自动跳到 Debugger 都算变过，所以非常频繁（源码 `main.cpp` 的 `DoCheckCurrentLayoutForChanges`）。
- **和代码没有任何关系，选什么都不会丢代码。**

**怎么办**：勾上框里的 **Don't annoy me again!**，再点 Yes，以后不再问。

关 Code::Blocks 时还可能问 `Workspace 'Default workspace' is modified. Do you want to save it?`，意思是“要不要记住现在打开了哪些工程和文件”，也和代码无关，点 Yes 就行。你当时遇到这么多弹窗，主要是因为 ② 逼得你每改一次就重启一次 Code::Blocks；② 解决了，这些也就少了。
