# BAG V3.2 FLAT — 一体化赛场工作目录

## 核心纠正

V3.1 仍然没完全吃透真实工作流：它把样例放在 `samples/`，并保留了 `WA.cpp / check.sh / duipai.sh / runner.py` 等多入口。

V3.2 的原则是：

> **一题一个目录；一个 main.cpp；样例直接平铺；debug / 样例 / 对拍 / 提交检查都操作同一份 main.cpp。**

可见目录固定为：

```
T1/
  main.cpp
  AC.cpp
  gen.cpp
  notes.txt
  AC.cbp
  run.sh
  case1.in
  case1.out
  case2.in
  case2.ans
  official.zip
  .bag/        # 隐藏内部状态、缓存和失败取证
```

没有 `samples/`。
没有 `WA.cpp`。
没有独立 `debug/`。
没有多套 candidate。

## 唯一入口

```bash
bash run.sh          # 跑平铺样例
bash run.sh d        # 同一 main.cpp + ASan/UBSan
bash run.sh p 10000  # 同一 main.cpp 对拍 AC.cpp + gen.cpp
bash run.sh n        # SPJ / 构造题只跑不比文本
bash run.sh c        # 交前检查
```

## Code::Blocks

`AC.cbp` 同时显示：
- main.cpp
- AC.cpp
- gen.cpp
- notes.txt

但只有 main.cpp 参与 Build / F9。AC/gen/notes 只是同项目内快速编辑。

## 大样例

正式推荐：
1. 下载；
2. 解压；
3. 将 `.in/.out/.ans` 直接平铺粘到 T1；
4. `bash run.sh`。

也支持 ZIP 直接丢 T1，内部在隐藏 `.bag/extracted/` 解压。

## 已实测

- 平铺中文/空格/括号样例 PASS；
- 中文 ZIP 且 ZIP 内中文嵌套目录 PASS；
- ASan/UBSan PASS；
- stress 3000/3000 PASS；另一轮继续跑到 7500 组仍全绿后因外部工具时限终止；
- WA 会保存 main/AC/gen/notes + 输入输出到隐藏 `.bag/failcase/`；
- 空 generator 拒绝假绿；
- restore 会整目录原子移动到 backups，样例和 notes 全保留。

## 设计目标

不是“功能最多”，而是减少比赛时的心智分叉：
- 写代码永远只找 main.cpp；
- 测样例永远只 run.sh；
- Debug 永远同一个 run.sh；
- 对拍永远同一个 main.cpp；
- 笔记就在同一 Code::Blocks 项目；
- 官方数据就在当前目录平铺。
