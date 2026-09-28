#!/bin/bash
# 用法（在 problems 里）：bash run.sh T1      编译 T1.cpp，跑 T1/ 文件夹里所有样例（zip 会先自动解压）
#                        bash run.sh T1 d    调试编译（-g + 越界/溢出检查），出 RE 时用
# freopen 开着也没关系，会自动用文件读写来测
k=$1
[ -n "$k" ] || { echo "用法：bash run.sh T1"; exit 1; }
src=$k.cpp
[ -e "$src" ] || { echo "找不到 $src"; exit 1; }
mkdir -p "$k"
for z in "$k"/*.zip; do
    [ -e "$z" ] && unzip -n -q "$z" -d "$k"
done
if [ "$2" = d ]; then f="-g -fsanitize=address,undefined"; else f="-O2"; fi
g++ "$src" -o "$k/$k" -std=c++14 -Wall -Wno-unused-result $f || { echo "编译失败"; exit 1; }
fin=$(grep -E '^[[:space:]]*freopen' "$src" | grep -o '"[^"]*\.in"' | head -1 | tr -d '"')
fout=$(grep -E '^[[:space:]]*freopen' "$src" | grep -o '"[^"]*\.out"' | head -1 | tr -d '"')
file=0
[ -n "${fin%.in}" ] && [ -n "${fout%.out}" ] && file=1 && echo "freopen 开着，用 $fin / $fout 测"
tot=0
ok=0
while IFS= read -r i; do
    a=${i%.in}.out
    [ -e "$a" ] || a=${i%.in}.ans
    [ -e "$a" ] || continue
    tot=$((tot + 1))
    s=$(date +%s%N)
    if [ $file -eq 1 ]; then
        mkdir -p "$k/work"
        cp "$i" "$k/work/$fin"
        rm -f "$k/work/$fout"
        (cd "$k/work" && timeout 10 "../$k")
        r=$?
        cp "$k/work/$fout" "$k/my.out" 2> /dev/null || : > "$k/my.out"
    else
        timeout 10 "$k/$k" < "$i" > "$k/my.out"
        r=$?
    fi
    t=$((($(date +%s%N) - s) / 1000000))
    if [ $r -eq 124 ]; then echo "$i  TLE（超过 10 秒）"
    elif [ $r -ne 0 ]; then echo "$i  RE（返回值 $r）  ${t}ms"
    elif diff -wq "$k/my.out" "$a" > /dev/null; then
        ok=$((ok + 1))
        if [ $t -gt 1000 ]; then echo "$i  OK 但是 ${t}ms，超过 1 秒"; else echo "$i  OK  ${t}ms"; fi
    else echo "$i  WA  ${t}ms"; fi
done < <(find "$k" -name "*.in" -not -path "*/work/*" | sort)
[ $tot -eq 0 ] && echo "$k/ 里没找到样例（*.in 和同名 .out / .ans）"
res="样例 $ok / $tot 通过"
[ $ok -eq $tot ] && [ $tot -gt 0 ] && res="$res（全过）"
echo "$res"
# 给 check.sh 用：记下这次测的是哪个版本的源码
if [ "$2" != d ]; then
    md5sum < "$src" > ".$k.样例结果"
    echo "$res" >> ".$k.样例结果"
fi
