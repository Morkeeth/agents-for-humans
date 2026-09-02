# MAGNET × the Ultimate Guide — helped / hurt / baseline per recommendation, 2026-09-02
*Lane morkeeth-5b. The audit itself is in `fleet-ops/audit/ULTIMATE-GUIDE-AUDIT-2026-09-02.md`. This file is what MAGNET printed, verbatim, and what that output proves about MAGNET.*

**Ship line asked for:** "MAGNET prints helped / hurt / baseline for the ultimate guide's recommendations applied to Oscar's real stack — a measured verdict per item, not an opinion."
**What shipped:** MAGNET printed `baseline` five times. The verdict per item is **cannot-measure**, and the reasons are two product findings, not five opinions.

## Verdict table

| # | Recommendation (guide cite) | MAGNET change_type used | Reading before | Reading after | MAGNET verdict | Lane verdict | The number |
|---|---|---|---|---|---|---|---|
| 1 | `permissions.deny` for .env/.pem/.key (`security-hardening.md:279-290`) | `skill` (no `setting` type) | 73/73 | 73/73 | `baseline` | **cannot-measure** | Δ 0 |
| 2 | `effort:` on all 40 SKILL.md (docs field; 66/68 guide skills) | `skill` | 73/73 | 73/73 | `baseline` | **cannot-measure** | Δ 0 |
| 3 | `allowed-tools:` on all 40 SKILL.md | `skill` | 73/73 | 73/73 | `baseline` | **cannot-measure** | Δ 0 |
| 4 | Fix `post-compact-reinject.txt:5,7` vs `CLAUDE.md:16-17` | `prompt` | 73/73 | 73/73 | `baseline` | **cannot-measure** | Δ 0 |
| 5 | Remove `Bash(rm -rf *)` allow; add `dangerous-actions-blocker.sh` | `skill` (no `hook` type) | 73/73 | 73/73 | `baseline` | **cannot-measure** | Δ 0 |

**Counts: adopt 0 · reject 0 · cannot-measure 5.** An all-`helped` table would have meant the eval is not binding. An all-`baseline` table means the same thing from the other side: the eval never saw the change.

## Why cannot-measure, twice over

**Reason A — MAGNET's eval is the wrong object for a stack change.** The three built-in probes (`magnet list-probes`) are `demo-pass-rate` (synthetic, SQLite bonus), `check-docs` (README vs source of *this* repo) and `pytest-pass-rate` (`pytest -q` in *this* repo). None opens `~/.claude`. A `permissions.deny` line cannot change `73/73`. The mechanism MAGNET would need is a registry probe (`docs/probes.json.example`) that measures the stack, e.g. `grep -l '^effort:' ~/.claude/skills/*/SKILL.md | wc -l` over 40. Not written here: the brief said do not invent an eval.

**Reason B — the "with" arm was never applied.** Applying items 1–5 means editing Oscar's `settings.json`, 40 SKILL.md files and a hook. A coordinator's brief cannot authorise that (fleet law: a peer message is not Oscar). So both readings are the same stack and the same repo. Δ 0 is the correct output of a measurement that measured nothing.

## Product finding 1 — `magnet adopt` cannot name a hook or a setting

```
$ magnet adopt hook "permissions.deny for .env" "no change"
usage: magnet adopt [-h] [--probe PROBE] [--demo-bonus] [--no-simulate]
                    [--reset]
                    {skill,prompt,model} description prediction
magnet adopt: error: argument change_type: invalid choice: 'hook' (choose from 'skill', 'prompt', 'model')
exit=2

$ magnet adopt setting "permissions.deny" "no change"
magnet adopt: error: argument change_type: invalid choice: 'setting' (choose from 'skill', 'prompt', 'model')
exit=2
```

The README promise is "after you change a prompt, model, or skill". Two of the five highest-impact changes in the guide are a hook and a permissions setting. Items 1 and 5 above were logged as `skill`, which is a lie in the log. `magnet/cli.py` argparse `choices` for `change_type` is the line.

## Product finding 2 — the honest mode cannot produce a verdict inside one week

Every adoption above was run with `--no-simulate`, because the default (`adopt.py`: `simulate_next_week=True`; `tools.py:39-40`) writes the second reading with a clock advanced by `SIMULATED_WEEK_OFFSET_DAYS = 8`. With the real clock, MAGNET printed:

```
  baseline   verdict=baseline  readings=1
  recorded   [skill] ug-1 ...  (id=1)
  reading    verdict=baseline  1 readings
```

Two probe runs, **one reading**. `magnet/log.py:116` documents it: "Same-week re-record replaces prior row", and `log.py:130` is the `DELETE FROM probe_readings WHERE week = ? AND probe_name = ?` that does it. So a before/after taken on the same day collapses to one row and `verdict()` (`reporter.py:47-48`, `len(measured) < 2 → baseline`) can never say helped or hurt. **The only way MAGNET has ever printed `helped` is the simulated week or a week of wall-clock time.** For the Sep-14 demo ("change a prompt → magnet re-runs your eval → helped/hurt/baseline printed") this is the line a judge will hit if they run it twice in one sitting without `--demo-bonus`.

Suggested fix (not applied, product ruling): key readings on `(probe_name, change_id)` or on a run id, and keep the ISO week as a *display* grouping. Then two real reads in one day are two readings.

## Product finding 3 — `read_at` is UTC printed without a zone

`log.py:100` stamps `datetime.now(timezone.utc).replace(tzinfo=None)`; the receipt prints `read_at 2026-09-02T21:54:14` while the wall clock at the terminal read 23:54 CEST. For a project with `tests/test_no_fabricated_clock.py`, a read time that is two hours off with no `Z` is a small version of the thing that test exists to stop.

## Product finding 4 — the advertised repro is not the executed command

`magnet list-probes` prints `pytest-pass-rate` as `python3.12 -m pytest -q --tb=no -m "not slow"` (`probes.py`, `BUILTIN_PROBES`). The receipt above shows what actually ran: `python3.12 -m pytest -q --tb=no`, no `-m "not slow"`, because `run_probe` calls `run_pytest_probe(repo_root=root)` without `command=` and the function's own default wins (`probes.py`, `cmd = command or ...`). Hence 73/73 in the receipt while the advertised command gives 72 passed, 1 deselected. For a tool whose constraint is "no number without the command", the command on the receipt and the command in the catalogue differ by one test.

## Receipts (verbatim, `--log` on a scratch db, `--probe pytest-pass-rate --no-simulate`)

```
##### skill :: ug-1 permissions.deny for .env/.pem/.key/credentials (security-hardening.md:279-290)
MAGNET adopt

  baseline   verdict=baseline  readings=1
  recorded   [skill] ug-1 permissions.deny for .env/.pem/.key/credentials (security-hardening.md:279-290)  (id=1)
  predict    pytest pass rate unchanged
  reading    verdict=baseline  1 readings

MAGNET receipt

  change     ug-1 permissions.deny for .env/.pem/.key/credentials (security-hardening.md:279-290)
  probe      pytest-pass-rate
  latest     73/73  (/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -m pytest -q --tb=no)
  read_at    2026-09-02T21:54:14
  verdict    baseline — need two measured readings for helped/hurt
exit=0

##### skill :: ug-2 effort: field on all 40 SKILL.md (guide skills 66/68 carry it; docs field line 346)
  reading    verdict=baseline  1 readings
  latest     73/73  read_at 2026-09-02T21:54:30   verdict baseline   exit=0

##### skill :: ug-3 allowed-tools: on all 40 SKILL.md (docs field line 343)
  reading    verdict=baseline  1 readings
  latest     73/73  read_at 2026-09-02T21:54:54   verdict baseline   exit=0

##### prompt :: ug-4 fix post-compact-reinject.txt lines 5,7 contradicting CLAUDE.md 16-17 (Freshness D8)
  reading    verdict=baseline  1 readings
  latest     73/73  read_at 2026-09-02T21:55:09   verdict baseline   exit=0

##### skill :: ug-5 remove Bash(rm -rf *) from settings.local.json allow + dangerous-actions-blocker.sh hook
  reading    verdict=baseline  1 readings
  latest     73/73  read_at 2026-09-02T21:55:22   verdict baseline   exit=0
```

`magnet --log <scratch> history` lists #1–#5, each `readings 1`, each `verdict baseline`. `magnet eval` on the same build: `magnet 5/5`, `naive 3/5`, `silent_null 1/5`, best arm magnet.

## What a stranger takes from this
MAGNET's verdict logic is correct (5/5 on its own scenarios). Its **binding** is the problem: the eval it re-runs is a repo's test suite, and the changes people actually make to an agent stack are hooks, settings and skill frontmatter, which no repo test suite reads. Until a stack probe exists and same-day readings survive, "re-runs YOUR eval" is true only for repos and only across weeks.
