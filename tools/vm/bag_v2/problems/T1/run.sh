#!/bin/bash
# 用法（在 problems/Tk 里）：bash run.sh      编译 Tk.cpp，跑这个文件夹里所有样例（zip 会先自动解压）
#                           bash run.sh d    调试编译（-g + 越界/溢出检查），用来抓 RE
# freopen 开着也没关系，会自动用文件读写
k=$(basename "$PWD")
src=$k.cpp
[ -e "$src" ] || { echo "找不到 $src"; exit 1; }
for z in *.zip; do
    [ -e "$z" ] && unzip -n -q "$z"
done
if [ "$1" = d ]; then f="-g -fsanitize=address,undefined"; else f="-O2"; fi
g++ "$src" -o "$k" -std=c++14 -Wall -Wno-unused-result $f || { echo "编译失败"; exit 1; }
fin=$(grep -E '^[[:space:]]*freopen' "$src" | grep -o '"[^"]*\.in"' | head -1 | tr -d '"')
fout=$(grep -E '^[[:space:]]*freopen' "$src" | grep -o '"[^"]*\.out"' | head -1 | tr -d '"')
n=""
[ -n "${fin%.in}" ] && [ -n "${fout%.out}" ] && n=1 && echo "freopen 开着，用 $fin / $fout 测"
tot=0
ok=0
while IFS= read -r i; do
    a=${i%.in}.out
    [ -e "$a" ] || a=${i%.in}.ans
    [ -e "$a" ] || continue
    tot=$((tot + 1))
    s=$(date +%s%N)
    if [ -n "$n" ]; then
        mkdir -p work
        cp "$i" "work/$fin"
        rm -f "work/$fout"
        (cd work && timeout 10 "../$k")
        r=$?
        cp "work/$fout" my.out 2> /dev/null || : > my.out
    else
        timeout 10 "./$k" < "$i" > my.out
        r=$?
    fi
    t=$((($(date +%s%N) - s) / 1000000))
    if [ $r -eq 124 ]; then echo "$i  TLE（超过 10 秒）"
    elif [ $r -ne 0 ]; then echo "$i  RE（返回值 $r）  ${t}ms"
    elif diff -wq my.out "$a" > /dev/null; then
        ok=$((ok + 1))
        if [ $t -gt 1000 ]; then echo "$i  OK 但是 ${t}ms，超过 1 秒"; else echo "$i  OK  ${t}ms"; fi
    else echo "$i  WA  ${t}ms"; fi
done < <(find . -name "*.in" -not -path "./work/*" | sort)
[ $tot -eq 0 ] && echo "没找到样例（*.in 和同名 .out / .ans）"
res="样例 $ok / $tot 通过"
[ $ok -eq $tot ] && [ $tot -gt 0 ] && res="$res（全过）"
echo "$res"
# 给 check.sh 用：记下这次测的是哪个版本的源码
if [ "$1" != d ]; then
    md5sum < "$src" > .样例结果
    echo "$res" >> .样例结果
fi
