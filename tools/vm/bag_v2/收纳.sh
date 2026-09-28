#!/bin/bash
# 用法（赛后）：bash ~/Desktop/bag/收纳.sh 2026-09-27_day2
# 把桌面上除了 bag、存档、Day 开头的旧文件夹以外的东西，连同 Downloads 里的东西，
# 挪进 ~/Desktop/存档/<名字>/，再从 bag 复制一份干净的到桌面。挪之前会列出来让你确认
name=$1
[ -n "$name" ] || { echo "用法：bash ~/Desktop/bag/收纳.sh 日期_比赛名，比如 2026-09-27_day2"; exit 1; }
D=~/Desktop
dst=$D/存档/$name
[ -e "$dst" ] && { echo "$dst 已经存在，换个名字"; exit 1; }
cd "$D" || exit 1
items=()
for f in *; do
    case "$f" in
        bag|存档|Day[0-9]*) ;;
        *) [ -e "$f" ] && items+=("$f") ;;
    esac
done
dl=$(ls -A ~/Downloads 2> /dev/null | wc -l)
echo "要挪进 $dst 的："
printf '  桌面/%s\n' "${items[@]}"
echo "  Downloads 里的 $dl 个文件"
read -p "确认？(y/n) " a
[ "$a" = y ] || exit 0
mkdir -p "$dst/Desktop" "$dst/Downloads"
[ ${#items[@]} -gt 0 ] && mv -- "${items[@]}" "$dst/Desktop/"
[ "$dl" -gt 0 ] && mv ~/Downloads/* ~/Downloads/.[!.]* "$dst/Downloads/" 2> /dev/null
cp -r bag/debug bag/problems bag/duipai_T1 bag/duipai_T2 bag/duipai_T3 bag/duipai_T4 "$D/"
echo "收好了：$dst"
echo "桌面上已经放好一份干净的 debug、problems、duipai_T1～T4"
