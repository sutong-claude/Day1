g++ gen.cpp -o gen -O2
g++ ac.cpp -o ac -O2
g++ wa.cpp -o wa -O2
for ((i = 1;;i++)); do
    ./gen > 1.txt
    ./ac < 1.txt > 2.txt
    ./wa < 1.txt > 3.txt
    diff -w 2.txt 3.txt || { echo "wrong on test $i"; break; }
    echo "right on test $i"
done
