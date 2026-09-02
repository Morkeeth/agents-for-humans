# Four MAGNET defects, fixed test-first — 2026-09-03 00:0x CEST
*Found 2026-09-02 by running MAGNET on a real stack change (`docs/ULTIMATE-GUIDE-MAGNET-2026-09-02.md`). Each row: the failing test, the fix, the before and after output at the CLI. Suite: 73 → 80 tests (`tests/test_magnet_bugs_2026_09_03.py`, 7 new; 6 were red on main, 1 was a guard that the fix must keep green).*

| # | Defect | Test (red on main @ c359b0a) | Fix |
|---|---|---|---|
| 1 | `magnet adopt hook\|setting` → argparse exit 2 | `test_adopt_accepts_hook_and_setting`, `test_receipt_says_when_a_builtin_probe_cannot_see_a_stack_change` | `constants.CHANGE_TYPES` adds `hook`, `setting`; `adopt.py` prints a `measures repo only` line when a built-in probe is asked to measure a stack change |
| 2 | `log.py` deleted the same-week row regardless of `change_id`, so `--no-simulate` printed `readings 1 · baseline` forever | `test_same_day_baseline_and_post_adoption_readings_both_survive`, `test_no_simulate_adopt_prints_a_verdict_not_baseline` (+ `test_same_week_re_record_of_the_same_run_still_replaces` guards the weekly rule) | `DELETE … WHERE week=? AND probe_name=? AND change_id IS ?` — a re-record of the same run replaces; baseline and post-adoption are different runs |
| 3 | `read_at` printed UTC with no zone (`21:54` on a `23:54` CEST clock) | `test_read_at_and_recorded_at_carry_a_zone` | `_now()` is aware UTC; naive `now=` is taken as UTC; stamps end `+00:00`; simulated rows in `demo.py`/`tools.py` use the same clock |
| 4 | `list-probes` advertised `-m "not slow"`, `run_probe` executed without it (and `str.split` would have broken the quotes) | `test_run_probe_executes_the_advertised_pytest_command` | `run_probe` passes `builtin_probe_command(PYTEST_PROBE)` with `scoped=False` (recursion guard kept); `shlex.split` |

`tests/test_no_fabricated_clock.py` was adapted to compare aware stamps to an aware ceiling; its intent (no `read_at` in the future) is unchanged. Six judge docs that print the test count were re-derived 73 → 80 by `magnet check-docs` (it failed first, as designed).

## Before → after, at the CLI

**1 — the verb.** Before (2026-09-02 23:5x):
```
$ magnet adopt hook "permissions.deny for .env" "no change"
magnet adopt: error: argument change_type: invalid choice: 'hook' (choose from 'skill', 'prompt', 'model')
exit=2
```
After:
```
$ magnet --log <scratch> adopt hook "PreToolUse secrets gate (check-secrets.sh)" "no change expected" --probe demo-pass-rate --no-simulate --reset
  recorded   [hook] PreToolUse secrets gate (check-secrets.sh)  (id=1)
  ...
  measures   repo only — demo-pass-rate reads this repo, not the stack; a hook change is invisible to it. Add a registry probe that reads the stack (docs/probes.json.example) to measure this adoption.
exit=0
```

**2 — two real reads in one sitting.** Before (five adoptions, `--no-simulate --probe pytest-pass-rate`, 2026-09-02):
```
  baseline   verdict=baseline  readings=1
  recorded   [skill] ug-1 ...  (id=1)
  reading    verdict=baseline  1 readings
  verdict    baseline — need two measured readings for helped/hurt
```
After:
```
$ magnet --log <scratch> adopt skill "demo-verification-skill" "pass rate rises by 1/5" --probe demo-pass-rate --demo-bonus --no-simulate --reset
  baseline   verdict=baseline  readings=1
  recorded   [skill] demo-verification-skill  (id=3)
  reading    verdict=helped  2 readings
  ...
  verdict    helped  ↑ +1 vs prior
```
No `SIMULATED` anywhere in that output.

**3 — the zone.** Before: `read_at    2026-09-02T21:54:14` (wall clock 23:54 CEST). After: `read_at    2026-09-02T22:06:06+00:00` (wall clock `2026-09-03T00:06:06 CEST`, same instant).

**4 — the advertised command.** Before: receipt command `… -m pytest -q --tb=no` → `73/73`, while `list-probes` showed `… -m pytest -q --tb=no -m "not slow"`. After:
```
$ magnet probe pytest-pass-rate
pytest-pass-rate: 79/79
  command: /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -m pytest -q --tb=no -m "not slow"
```
79 of 80 because one test is marked slow and the advertised command deselects it; the receipt and the catalogue now name the same command.

**`magnet demo` twice in one sitting (00:06:19 CEST), both runs byte-identical apart from nothing:**
```
  latest     4/5  (magnet probe demo-pass-rate)
  simulated  2026-09-10T22:06:19+00:00  (SIMULATED week — not a real read time)
  verdict    helped  ↑ +1 vs prior
  readings             2
  first                3/5
  second               4/5
exit=0
```
The demo still uses the simulated week and says so. `--no-simulate` on `adopt` is now the honest route to the same verdict.

**`bash scripts/stranger-pass.sh`** (full, not quick): `11 claims checked. All match source.` → `== stranger pass OK ==`.

## Defects 5 and 6 — found recording the demo, fixed 00:2x

| # | Defect | Test (red first) | Fix |
|---|---|---|---|
| 5 | `magnet history` judged every adoption row on the probe's LATEST reading, so "drop the rule" (its own reading 80/81, hurt) printed `helped (Δ 1)` once the next adoption recovered | `test_history_row_binds_to_its_own_reading`, `test_history_row_shows_its_own_latest_value` | `history.readings_for_adoption()` cuts the series at the reading carrying the row's `change_id`; a row with no bound reading keeps the old whole-series verdict |
| 6 | the suite ran `pip install -e ".[dev]"` (stranger-pass.sh, judge-demo.sh) and repointed the machine's editable `magnet` to whichever checkout ran the eval; judge-demo's quick mode also called the `magnet` console script, i.e. whatever install was current | `test_stranger_pass_under_test_does_not_pip_install`, `test_judge_demo_under_test_does_not_pip_install` (run with `PIP_REQUIRE_VIRTUALENV=1`, which makes any surviving `pip install` exit 3) | both scripts skip the install and print `install skipped` under their QUICK variable; judge-demo shadows `magnet` with `python3 -m magnet.cli` in quick mode |

Before, `magnet history` on the demo log:
```
  #1  change [prompt] drop the never-invent rule from SYSTEM_PROMPT
    latest     81/81  (pytest)
    verdict    helped  (Δ 1)
    readings   3
```
After:
```
  #1  change [prompt] drop the never-invent rule from SYSTEM_PROMPT
    latest     80/81  (pytest)
    verdict    hurt  (Δ -1)
    readings   2
  #2  change [prompt] restore the never-invent rule
    latest     81/81  (pytest)
    verdict    helped  (Δ 1)
    readings   3
```
Before, the scripts under test with `PIP_REQUIRE_VIRTUALENV=1`: `MAGNET judge demo — installing...` / `ERROR: Could not find an activated virtualenv (required).` exit 3. After: `(quick mode — install skipped; magnet imported from this checkout)` … `== stranger pass OK ==`, and `pip show` reports the same editable location before and after the suite. Suite 82 → 86, six judge docs re-derived.

## Left open, on purpose
- (Closed by Cursor's `cursor/stack-magnet-bakeoff-5608`, commit "Fix demo-bonus always-on", once merged.) `tools.py` `tool_adopt_change` sets the demo bonus whenever the probe is `demo-pass-rate`, with or without `--demo-bonus`. So a hook adoption measured on the demo probe prints `helped` by construction (see the after-output of #1). The new `measures repo only` line sits under it, but the verdict line is still a lie for a stack change. Product ruling: either make the bonus opt-in only, or refuse `demo-pass-rate` for `hook`/`setting`.
- `adopt` still simulates the next week by default. Now that same-day reads survive, the default fabricates a week for no reason. Flipping the default changes the recorded demo; Oscar's call.
