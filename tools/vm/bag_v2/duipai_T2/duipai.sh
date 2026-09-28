# 你原来的对拍脚本，加了 4 处（每处上面有一行注释）。用 bash duipai.sh 运行
k=T2
# 加 1：wa.cpp 自动换成 problems/T2.cpp（freopen 自动注释掉），测的就是你要交的那份
#       你手改过 wa.cpp 就不覆盖，直接拿 wa.cpp 拍
if [ -e .wa.md5 ] && [ "$(md5sum < wa.cpp)" != "$(cat .wa.md5)" ]; then
    echo "wa.cpp 被你改过，这次不覆盖（交之前记得把它挪回 problems/$k.cpp）"
else
    sed 's#^\([[:space:]]*\)freopen#\1//freopen#' ../problems/$k.cpp > wa.cpp
    md5sum < wa.cpp > .wa.md5
    echo "wa.cpp = problems/$k.cpp"
fi
# 加 2：编译失败就停，不拿旧程序拍
g++ gen.cpp -o gen -O2 || exit 1
g++ ac.cpp -o ac -O2 || exit 1
g++ wa.cpp -o wa -O2 || exit 1
for ((i = 1;;i++)); do
    ./gen > 1.txt
    # 加 3：gen 没输出就停（Day2 gen 还是空模板时“1000 组全对”是假的）
    [ -s 1.txt ] || { echo "gen 没有输出，先把 gen.cpp 写好"; break; }
    ./ac < 1.txt > 2.txt
    # 加 4：wa 崩溃或超过 2 秒就停；出错时把这组输入打出来
    timeout 2 ./wa < 1.txt > 3.txt || { echo "RE or TLE on test $i"; cat 1.txt; break; }
    diff -w 2.txt 3.txt || { echo "wrong on test $i"; echo "输入："; cat 1.txt; break; }
    echo "right on test $i"
done
