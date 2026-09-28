#!/bin/bash
# 用法（在 problems 里）：bash check.sh
# 交之前检查四题：能不能编译、freopen 开没开、改过以后有没有重新跑样例
tpl=09924b235453b0171499114f0b6c5f14
for k in T1 T2 T3 T4; do
    src=$k.cpp
    if [ ! -e "$src" ]; then echo "$k  ✗ 找不到 $src"; continue; fi
    if [ "$(md5sum < "$src" | cut -d' ' -f1)" = "$tpl" ]; then echo "$k  （还是空模板）"; continue; fi
    if g++ "$src" -o "/tmp/check_$k" -std=c++14 -O2 -Wall -Wno-unused-result 2> "/tmp/check_$k.log"; then
        w=$(grep -c "warning" "/tmp/check_$k.log")
        c="✓ 编译通过"
        [ "$w" -gt 0 ] && c="✓ 编译通过（$w 个警告）"
    else
        c="✗ 编译失败"
    fi
    fi_=$(grep -E '^[[:space:]]*freopen' "$src" | grep -o '"[^"]*\.in"' | head -1 | tr -d '"')
    fo=$(grep -E '^[[:space:]]*freopen' "$src" | grep -o '"[^"]*\.out"' | head -1 | tr -d '"')
    if [ -n "${fi_%.in}" ] && [ -n "${fo%.out}" ]; then f="✓ $fi_ / $fo"; else f="✗ freopen 没开或文件名没填"; fi
    if [ -e ".$k.样例结果" ] && [ "$(md5sum < "$src")" = "$(head -1 ".$k.样例结果")" ]; then
        r=$(tail -1 ".$k.样例结果")
        case "$r" in
            *全过*) r="✓ $r" ;;
            *) r="✗ $r" ;;
        esac
    else
        r="✗ 改过以后还没跑样例（bash run.sh $k）"
    fi
    echo "$k  $c  |  $f  |  $r"
done
