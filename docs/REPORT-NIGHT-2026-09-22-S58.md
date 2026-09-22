# REPORT · Slice 58 · 2026-09-22

## SHIPPED

- Ordinal digit from→to: `3rd to 4th` / `from 3rd to 4th` / `goes 3rd to 4th` /
  `3rd → 4th` / `3rd/5 to 4th/5` grade destination (and pop when claimed).
- Ordinal word from→to: `third to fourth` / `from third to fourth` /
  `first to second` / `third/five to fourth/five`.
- Equals targets: `equals 4/5` / `equal to` / `is equal to` / `must equal` /
  `should equal` / `== 4/5` / `equals four` / `equal to fourth`.
- Fixed THE LIE where `3rd/5 to 4th/5` invented raw=`5 to 4` by stealing
  digits around ordinal suffixes.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| `3rd to 4th` @4/@3 | `check_prediction` | held / missed; naive held @3 |
| `third to fourth` @3 | same | missed; naive held |
| `3rd/5 to 4th/5` raw | `claimed_target` | `3rd/5 to 4th/5` value=4 pop=5 (was `5 to 4`) |
| `equals 4/5` / `== 4/5` @3 | `check_prediction` | missed; naive held |
| `equals four` @3 | same | missed |
| Suite | `python3 -m pytest -q` | **469 passed, 1 skipped** (470) |
| Docs | `magnet check-docs` | **16 PASS** |
| Pred-demo | `python3 -m magnet.cli pred-demo` | **176/176** · embarrassed **92** |
| Cold scripts | `bash scripts/judge-demo.sh` · `bash scripts/stranger-pass.sh` | JUDGE DEMO OK · stranger pass OK |

## WRONG

- `is 4/5` / `was 4/5` / `reads 4/5` / `measures 4/5` / `lands on 4/5`
  still unbound — not in Slice 58 NOW; left for the next slice after
  re-deriving at the object.
- Ordinals above tenth (`eleventh` / `12th`) unbound — word map stops at ten.
- PNG sidecars not re-rendered (Pillow missing in this VM); `.txt` sidecars
  re-derived and check_docs green.
- Oscar gates (film · Devpost paste · submit) still closed.
