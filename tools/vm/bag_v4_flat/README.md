# BAG V4 Flat Integrated

This is the current experimental contest bag.

## Design principle

**One problem = one flat workspace.**

No `samples/`, no separate debug folder, no separate `duipai_T1/`.

Inside `T1/`:

- `main.cpp`: the only candidate/submission source
- `WA.cpp`: brute/oracle (legacy filename kept from the original bag)
- `gen.cpp`: generator
- `notes.txt`: contest research log
- `AC.cbp`: Code::Blocks project pointing only to `main.cpp`
- `run.sh`: unified runner
- `duipai.sh`: compatibility wrapper for stress testing
- official samples, manual debug cases, and stress counterexamples all live as flat `*.in + *.out/.ans`

Stress failures are written as `debug_XXX.in/out`, so they instantly become ordinary regression samples for the next `bash run.sh`.

## Commands

```bash
cd T1
bash run.sh              # run every flat testcase
bash run.sh s            # same cases under ASan/UBSan
bash duipai.sh 10000     # stress; failure becomes debug_XXX.in/out
bash run.sh c            # pre-submit exact compile + samples + freopen smoke

cd ..
bash reset.sh T1         # O(1)-style folder move to hidden .history, recreate T1
bash reset.sh all
bash reset.sh purge      # after archive, delete hidden history to reclaim disk
bash doctor.sh
```

## Tested

The local V4 test pass includes:

- real Day3 A accepted source + real `problem_1874.zip`, manually flattened: 2/2;
- active `freopen("Chant.in/out")` final check: FILEIO OK;
- stress failure -> `debug_001.in/out` -> after fix, ordinary `bash run.sh` regression PASS;
- 5000 flat input/output pairs: 5000/5000 PASS;
- 50,000,010-byte input: PASS (fast iostream program ~0.97s);
- Chinese / spaces / parentheses in filenames: PASS;
- CE/TLE/empty generator/SPJ run-only mode: detected correctly;
- ASan/UBSan sample run: PASS;
- resetting a folder containing 5000 input files: ~0.77s, old folder preserved in hidden history.

Code::Blocks GUI itself still needs final acceptance on the user's NOI Linux VM because the current test container does not have Code::Blocks installed.

The built ZIP is stored in ChatGPT Library at:
`/CSP-S比赛工具/BAG V4 Flat/bag_v4_flat_integrated.zip`.
