# Stranger pass

Run on a fresh copy — no Oscar credentials, no network after `pip install`.

## Commands

```bash
git clone https://github.com/Morkeeth/agents-for-humans.git
cd agents-for-humans
pip install -e ".[dev]"
magnet demo
pytest -q
```

## `magnet demo` output (2026-08-29)

```
MAGNET receipt

  change     demo-verification-skill
  probe      demo-pass-rate
  latest     4/5  (magnet probe demo-pass-rate)
  read_at    2026-09-06T21:04:42
  verdict    helped  ↑ +1 vs prior
  repro      magnet demo

  baseline arm (naive): always optimistic on <2 readings
  naive verdict        helped
  magnet verdict       helped

  readings             2
  first                3/5
  second               4/5
```

Exit code: **0**

## `pytest -q` output

```
15 passed in 0.36s
```

Exit code: **0**

## `magnet check-docs` output

```
[PASS] tool count: README claims 4 tools, source has 4
[PASS] tool run_probe: listed
[PASS] tool record_week: listed
[PASS] tool adopt_change: listed
[PASS] tool check_docs: listed

5 claims checked. All match source.
```

Exit code: **0**
