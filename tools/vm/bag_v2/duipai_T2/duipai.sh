#!/bin/bash
# 用法（在 duipai_T2 里）：bash duipai.sh           对拍 ../problems/T2/T2.cpp（就是要交的那份）和 ac.cpp（暴力）
#                         bash duipai.sh 别的.cpp   换成对拍别的文件
# 要测的程序 freopen 开着也没关系，会自动用文件读写
k=$(basename "$PWD"); k=${k#duipai_}
src=${1:-../problems/$k/$k.cpp}
[ -e "$src" ] || { echo "找不到 $src"; exit 1; }
echo "对拍：$src  vs  ac.cpp（暴力）"
g++ gen.cpp -o gen -O2 -Wno-unused-result || { echo "gen.cpp 编译失败"; exit 1; }
g++ ac.cpp -o ac -O2 -Wno-unused-result || { echo "ac.cpp 编译失败"; exit 1; }
g++ "$src" -o wa -O2 -Wno-unused-result || { echo "$src 编译失败"; exit 1; }
fname () {  # fname 源码 in/out：取出没被注释的 freopen 里的文件名
    grep -E '^[[:space:]]*freopen' "$1" | grep -o "\"[^\"]*\\.$2\"" | head -1 | tr -d '"'
}
run () {  # run 程序 源码 输入 输出
    local fin fout
    fin=$(fname "$2" in)
    fout=$(fname "$2" out)
    if [ -n "${fin%.in}" ] && [ -n "${fout%.out}" ]; then
        mkdir -p work
        cp "$3" "work/$fin"
        rm -f "work/$fout"
        (cd work && timeout 2 "../$1")
        local r=$?
        cp "work/$fout" "$4" 2> /dev/null || : > "$4"
        return $r
    fi
    timeout 2 "./$1" < "$3" > "$4"
}
show () {
    echo "---- 输入（./gen $i 可以重现）----"
    head -c 600 1.txt
    echo "---- 暴力的输出 ----"
    head -c 300 2.txt
    echo "---- 你的输出 ----"
    head -c 300 3.txt
}
for ((i = 1; ; i++)); do
    ./gen $i > 1.txt
    [ -s 1.txt ] || { echo "gen 没有输出任何东西，先把 gen.cpp 写好"; break; }
    run ac ac.cpp 1.txt 2.txt || { echo "暴力在第 $i 组 RE 或超过 2 秒"; break; }
    [ -s 2.txt ] || { echo "暴力没有输出，先把 ac.cpp 写好"; break; }
    run wa "$src" 1.txt 3.txt || { echo "第 $i 组：RE 或超过 2 秒"; show; break; }
    diff -wq 2.txt 3.txt > /dev/null || { echo "第 $i 组答案不同"; show; break; }
    echo "right on test $i"
done
