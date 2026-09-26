#!/bin/bash
# 用法（在对拍文件夹里）: bash duipai.sh     ac.cpp = 暴力，wa.cpp = 要测的程序，gen.cpp = 造数据
# 比原版多三处：编译失败就停（不会拿旧程序对拍）；wa 超过 2 秒或崩溃会报 RE or TLE；第一行写明用 bash 运行
g++ gen.cpp -o gen -O2 || exit 1
g++ ac.cpp -o ac -O2 || exit 1
g++ wa.cpp -o wa -O2 || exit 1
for ((i = 1; ; i++)); do
    ./gen > 1.txt
    ./ac < 1.txt > 2.txt
    timeout 2 ./wa < 1.txt > 3.txt || { echo "RE or TLE on test $i"; break; }
    diff -w 2.txt 3.txt || { echo "wrong on test $i"; break; }
    echo "right on test $i"
done
