# BAG V4 Flat — Local Acceptance Notes

V4 corrects the V3.1 architecture: samples, manual debug cases and stress counterexamples are not separate systems. They are all flat testcase pairs in the same problem directory.

## Verified locally

- Real Day3 A accepted source + real problem_1874 sample archive, flattened into T1: 2/2 PASS.
- Active freopen final check: FILEIO OK.
- Intentional stress WA creates debug_001.in/out; after fixing main.cpp, ordinary bash run.sh automatically re-runs that counterexample and passes.
- 5000 flat .in/.out pairs: 5000/5000 PASS, ~20.79s wall in this container.
- 50,000,010-byte input: PASS; tested program ~0.97s with fast iostream, runner wall ~3.25s.
- Chinese / spaces / parentheses filenames: PASS using the uploaded Chinese sample archive after flattening.
- CE, TLE, empty generator, SPJ run-only mode: fault injection behaves correctly.
- ASan/UBSan on real Day3 A samples: PASS.
- reset.sh T3 with 5000 input files present: ~0.77s; old directory preserved under hidden .history.

## Code::Blocks

The current container does not have Code::Blocks installed, so GUI/debugger acceptance is not claimed here.
AC.cbp was parsed and contains exactly one project Unit: main.cpp.
Final Code::Blocks acceptance should run on the user's NOI Linux VM.
