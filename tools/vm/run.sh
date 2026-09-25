#!/bin/bash
# 用法（在题目文件夹里）:
#   ./run.sh T1      编译 T1.cpp（-O2），跑当前文件夹所有 *.in，和同名 .out/.ans 比对，报 OK/WA/TLE/RE + 耗时
#   ./run.sh T1 d    调试模式编译（-g + 越界/溢出检查），用来抓 RE 和未定义行为
p=$1
if [ "$2" = d ]; then f="-g -fsanitize=address,undefined"; else f="-O2"; fi
g++ $p.cpp -o $p -std=c++14 -Wall $f || exit 1
for i in *.in; do
    [ -e "$i" ] || { echo "没有 .in 文件"; break; }
    a=${i%.in}.out
    [ -e "$a" ] || a=${i%.in}.ans
    s=$(date +%s%N)
    timeout 10 ./$p < "$i" > my.out
    r=$?
    t=$(( ($(date +%s%N) - s) / 1000000 ))
    if [ $r -eq 124 ]; then echo "$i  TLE (>10s)"
    elif [ $r -ne 0 ]; then echo "$i  RE (返回值 $r)  ${t}ms"
    elif diff -wq my.out "$a" > /dev/null; then echo "$i  OK   ${t}ms"
    else echo "$i  WA   ${t}ms"; fi
done
