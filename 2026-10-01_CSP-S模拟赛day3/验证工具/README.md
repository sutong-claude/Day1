# Day3 本地验证工具

四个 `stress_*.cpp` 都包含两份彼此独立的实现：赛后算法与小数据暴力。随机种子固定，便于复现。

```bash
g++ -std=c++17 -O3 stress_A.cpp -o stress_A && ./stress_A
g++ -std=c++17 -O3 stress_B.cpp -o stress_B && ./stress_B
g++ -std=c++17 -O3 stress_C.cpp -o stress_C && ./stress_C
g++ -std=c++17 -O3 stress_D.cpp -o stress_D && ./stress_D
```

当前版本默认各做 1,000,000 组随机测试，并在随机测试前额外做可承受范围内的完全穷举：

- A：值域 1..4、n<=7 全数组；
- B：二字母 n<=16 全串 + 三字母 n<=9 全串；
- C：n<=5 全标号树 × 全优先级排列；
- D：值域 3、n<=10 全数组。

B 的构造还应额外用题目 `checker.cpp` 验证输出区间；注意 checker **不会验证 NO**，所以不能替代 stress_B 的暴力判定。