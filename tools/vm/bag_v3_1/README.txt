BAG V3.1 - contest coding pack

The 3 commands you normally need
================================
Create a fresh contest workspace (safest):
    bash ~/Desktop/bag/new_contest.sh Day5 --open

Inside T1/T2/T3/T4 after pasting/extracting samples:
    bash run.sh

Before submitting:
    bash check.sh

Large-sample workflow
=====================
1) Edit ONLY main.cpp for the submission.
2) Download the official large-sample archive.
3) Fastest/lowest-risk choices:
   A. Extract/copy *.in + matching *.out/.ans into T1/samples/ (recommended), OR
   B. Drop the zip directly into T1/ or T1/samples/ (runner auto-extracts to .work).
4) Run:
       bash run.sh
It compiles the exact main.cpp, runs every sample recursively, compares tokens,
and smoke-tests active freopen using the exact submission binary.

Construction / SPJ sample
=========================
Exact official sample output may not be unique. Use:
    bash run.sh --mode none
This checks CE/RE/TLE without falsely requiring your output to equal the sample text.
Do NOT treat that as a correctness proof; use the problem checker/oracle separately.

Memory/UB debugging
===================
    bash run.sh --sanitize
Runs samples with ASan + UBSan (slower; use for debugging, not timing).

Stress test
===========
Write AC.cpp (independent brute/oracle) and gen.cpp (ONE non-empty testcase), then:
    bash duipai.sh
or:
    bash duipai.sh 10000
Optional memory guard:
    bash duipai.sh 10000 --memory-mb 1024
The runner refuses an empty generator and also refuses the dangerous case where BOTH
candidate and oracle output nothing on test 1. It warns if main.cpp and AC.cpp are identical.
A failure is preserved under failcase/ with input, outputs, stderr and source snapshots.

Instant restore / clean
=======================
Restore T1 while preserving the ENTIRE old T1 by atomic move under backups/:
    bash ~/Desktop/bag/restore.sh T1
Restore all four:
    bash ~/Desktop/bag/reset.sh
No large sample is silently deleted anymore.

Delete only generated build/cache files (keeps sources/samples/failcases):
    bash ~/Desktop/bag/clean.sh

First-time environment test
===========================
    bash ~/Desktop/bag/doctor.sh
    cd ~/Desktop/bag/T1 && bash selftest.sh

Roles
=====
main.cpp  = ONLY submission source
AC.cpp    = independent brute/oracle for stress testing
gen.cpp   = random/small-case generator
WA.cpp    = optional scratch; never used automatically
notes.txt = P/E/H/X research notes
samples/  = extracted official samples
AC.cbp    = Code::Blocks project, Unit=main.cpp, C++17 + O2 in Debug and Release

Safety built in
===============
- compile failure stops; stale binaries are deleted
- exact main.cpp is compiled before transformed test copies
- active freopen is tested with the exact binary
- generator/oracle/candidate timeouts
- optional stress memory limit
- no empty-generator fake green
- no both-empty-output fake green
- sample WA/RE/TLE keeps a forensic bundle
- zip traversal paths are rejected
- zip/sample paths with spaces, parentheses and Chinese names are supported
- .out/.ans/.answer plus uppercase variants are supported
- run outputs are reused/deleted on success instead of accumulating thousands of files
