# Stranger pass

Run on a fresh copy — no Oscar credentials, no network after `pip install`.

## Commands

```bash
git clone https://github.com/Morkeeth/agents-for-humans.git
cd agents-for-humans
pip install -e ".[dev]"
magnet demo
magnet eval
magnet agent-run
magnet list-probes
magnet history
pytest -q
magnet check-docs
magnet probe pytest-pass-rate   # real eval — run from CLI only
```

Alternative one-liner:

```bash
bash scripts/stranger-pass.sh
```

Alternative if `magnet` is not on PATH after install:

```bash
python -m magnet.cli demo
python -m magnet.cli eval
python -m magnet.cli agent-run
```

## `magnet demo` output (2026-08-31 05:41:44Z, real run on this branch)

```
MAGNET receipt

  change     demo-verification-skill
  probe      demo-pass-rate
  latest     4/5  (magnet probe demo-pass-rate)
  simulated  2026-09-08T07:41:44  (SIMULATED week — not a real read time)
  verdict    helped  ↑ +1 vs prior
  repro      magnet demo

  NOTE: week 2 is SIMULATED (clock advanced 8 days) so one run can
        show a helped/hurt verdict. Week 1 is a real reading.

  after 1 reading (embarrassing case):
    naive verdict      helped  ← invents optimism
    magnet verdict     baseline  ← refuses to trend

  after 2 readings (naive baseline arm):
    naive verdict      helped
    magnet verdict     helped

  readings             2
  first                3/5
  second               4/5
```

Exit code: **0** (verified: `python -m magnet.cli demo`)

## `magnet eval` output

```
MAGNET eval — arms scored against explicit ground truth
  ...
  naive        3/5
  magnet       5/5
  silent_null  1/5
  best arm     magnet (5/5)
```

Exit code: **0** (verified: `python -m magnet.cli eval`)

## `pytest -q` output

```
82 passed in 4.0s
```

Exit code: **0** (verified: `python3 -m pytest -q`)

## `magnet list-probes` output

```
MAGNET probes  (built-in + .magnet/probes.json)

  demo-pass-rate       [builtin]  magnet probe demo-pass-rate
  check-docs           [builtin]  python -m magnet.check_docs
  pytest-pass-rate     [builtin]  python3 -m pytest -q --tb=no

  total      3
```

Exit code: **0** (verified: `python -m magnet.cli list-probes`)

## `magnet probe pytest-pass-rate` output

```
pytest-pass-rate: 69/69
  command: python3 -m pytest -q --tb=no
```

Exit code: **0** (verified from CLI, not inside pytest — probe refuses recursion)

## `magnet history` output (after demo)

```
MAGNET history

  #N  ...
    change     [skill] demo-verification-skill
    probe      demo-pass-rate
    verdict    helped  (Δ 1)
    readings   2
```

Exit code: **0** (verified: `python -m magnet.cli history`)

## `magnet check-docs` output

```
[PASS] tool count: README claims 4 tools, source has 4
[PASS] tool run_probe: listed
...
5+ claims checked. All match source.
```

Exit code: **0** (verified: `python -m magnet.cli check-docs`)

## Drift catch (Qwen lesson)

When README claims `99 tools` but source has 4, `check_docs` exits 1:

```
pytest tests/test_check_docs_drift.py::test_check_docs_catches_wrong_tool_count -q
```

Verified: **1 passed**

When STRANGER-PASS claims `17 passed` but source has more tests than that, `check_docs` exits 1:

```
pytest tests/test_check_docs_pytest_count.py -q
```

Verified: **2 passed**
