# The one workflow — change a prompt, MAGNET re-runs your eval, reads helped / hurt / baseline
*For the Sep 14 video. One workflow, nothing else on screen. Recorded run below: 27 seconds wall clock on `fable/magnet-bugs-2026-09-03` @ 4af3757 (+ this commit), 2026-09-03 00:13:50–00:14:17 CEST. Every line of output is pasted from that run, unedited.*

**Your eval** is the repo's test suite. It includes `tests/test_prompt_contract.py`, two lines that pin the one rule MAGNET's system prompt must carry. **The prompt** is `SYSTEM_PROMPT` in `magnet/tools.py`. Drop the rule, the eval drops by one, MAGNET says `hurt`. Put it back, MAGNET says `helped`. Nothing is simulated; `--no-simulate` on every call.

## Commands (6, in order — from the repo root, clean tree)

```bash
M="python3 -m magnet.cli --log .magnet/demo-one.db"

# 1  baseline: run YOUR eval once, unchanged
$M record pytest-pass-rate

# 2  the one prompt change: drop the rule from SYSTEM_PROMPT
sed -i '' 's/ — never invent a trend from one reading//' magnet/tools.py

# 3  adopt the change: MAGNET re-runs the eval and prints the verdict
$M adopt prompt 'drop the never-invent rule from SYSTEM_PROMPT' 'pass rate unchanged' --probe pytest-pass-rate --no-simulate

# 4  put the rule back
git checkout -- magnet/tools.py

# 5  adopt the restore: re-run, verdict again
$M adopt prompt 'restore the never-invent rule' 'pass rate recovers by 1' --probe pytest-pass-rate --no-simulate

# 6  the log
$M history
```

`python3 -m magnet.cli` rather than the `magnet` console script so the code you just edited is the code that runs (the editable install can point at another checkout; see "Known" below).

## What the screen shows (pasted)

```
### 1  $ python3 -m magnet.cli --log .magnet/demo-one.db record pytest-pass-rate
recorded pytest-pass-rate: verdict=baseline readings=1

### 2  $ sed -i '' 's/ — never invent a trend from one reading//' magnet/tools.py
-    "and report helped, hurt, or baseline — never invent a trend from one reading. "
+    "and report helped, hurt, or baseline. "

### 3  $ python3 -m magnet.cli --log .magnet/demo-one.db adopt prompt 'drop the never-invent rule from SYSTEM_PROMPT' 'pass rate unchanged' --probe pytest-pass-rate --no-simulate
MAGNET adopt

  recorded   [prompt] drop the never-invent rule from SYSTEM_PROMPT  (id=1)
  predict    pass rate unchanged
  reading    verdict=hurt  2 readings

MAGNET receipt

  change     drop the never-invent rule from SYSTEM_PROMPT
  probe      pytest-pass-rate
  latest     80/81  (/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 -m pytest -q --tb=no -m "not slow")
  read_at    2026-09-02T22:14:08+00:00
  verdict    hurt  ↓ -1 vs prior
  repro      magnet adopt prompt 'drop the never-invent rule from SYSTEM_PROMPT' 'pass rate unchanged' --probe pytest-pass-rate

### 4  $ git checkout -- magnet/tools.py

### 5  $ python3 -m magnet.cli --log .magnet/demo-one.db adopt prompt 'restore the never-invent rule' 'pass rate recovers by 1' --probe pytest-pass-rate --no-simulate
MAGNET adopt

  recorded   [prompt] restore the never-invent rule  (id=2)
  predict    pass rate recovers by 1
  reading    verdict=helped  3 readings

MAGNET receipt

  change     restore the never-invent rule
  probe      pytest-pass-rate
  latest     81/81  (/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 -m pytest -q --tb=no -m "not slow")
  read_at    2026-09-02T22:14:17+00:00
  verdict    helped  ↑ +1 vs prior
  repro      magnet adopt prompt 'restore the never-invent rule' 'pass rate recovers by 1' --probe pytest-pass-rate

### wall clock: baseline 9s · hurt 9s · helped 9s · total 27s
```

The three rows in the log, straight from SQLite (`select id, recorded_at, value, population, change_id from probe_readings`):

```
1|2026-09-02T22:13:59+00:00|81|81|
2|2026-09-02T22:14:08+00:00|80|81|1
3|2026-09-02T22:14:17+00:00|81|81|2
```

81 not 82 because `tests/test_cold_clone_verify.py` is marked `slow` and the advertised probe command deselects it.

## On camera
- Say the prediction out loud before step 3: "I predict unchanged." MAGNET says `hurt`. That is the product: the log holds what you predicted next to what happened.
- The numbers to say once: `81/81 → 80/81 → 81/81`. Never say a percentage.
- Do not show `magnet demo`. It uses a labelled simulated week; this workflow needs none.

## Fixed the same night (see `docs/MAGNET-BUGS-2026-09-03.md`, defects 5 and 6)
- `magnet history` now binds each row to the reading recorded for its own adoption: row #1 ("drop the rule") prints `hurt (Δ -1)`, row #2 `helped (Δ 1)`.
- `scripts/stranger-pass.sh` and `scripts/judge-demo.sh` no longer run `pip install -e .` under test, so running the eval never repoints the machine's `magnet`. The `python3 -m magnet.cli` form above stays the right one for a live demo from an edited checkout.
