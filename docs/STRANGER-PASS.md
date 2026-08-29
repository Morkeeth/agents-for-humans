# Stranger pass

Run on a fresh copy — no Oscar credentials, no network after `pip install`.

## Commands

```bash
git clone https://github.com/Morkeeth/agents-for-humans.git
cd agents-for-humans
pip install -e ".[dev]"
magnet demo
pytest -q
magnet check-docs
```

## `magnet demo` output (2026-08-29, cloud agent run)

```
MAGNET receipt

  change     demo-verification-skill
  probe      demo-pass-rate
  latest     4/5  (magnet probe demo-pass-rate)
  read_at    2026-09-06T21:08:29
  verdict    helped  ↑ +1 vs prior
  repro      magnet demo

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

Exit code: **0** (verified: `magnet demo`)

## `pytest -q` output

```
17 passed in 0.69s
```

Exit code: **0** (verified: `python3 -m pytest -q`)

## `magnet check-docs` output

```
[PASS] tool count: README claims 4 tools, source has 4
[PASS] tool run_probe: listed
[PASS] tool record_week: listed
[PASS] tool adopt_change: listed
[PASS] tool check_docs: listed

5 claims checked. All match source.
```

Exit code: **0** (verified: `magnet check-docs`)

## Drift catch (Qwen lesson)

When README claims `99 tools` but source has 4, `check_docs` exits 1:

```
pytest tests/test_check_docs_drift.py::test_check_docs_catches_wrong_tool_count -q
```

Verified: **1 passed**
