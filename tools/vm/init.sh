#!/bin/bash
# 用法：cd ~/Desktop && ./init.sh     （需要 ~/Desktop/template.cpp 和 ~/Desktop/run.sh）
for i in 1 2 3 4; do
    mkdir -p T$i
    [ -e T$i/T$i.cpp ] || cp ~/Desktop/template.cpp T$i/T$i.cpp
    cp ~/Desktop/run.sh T$i/
done
echo "T1 到 T4 已建好"
