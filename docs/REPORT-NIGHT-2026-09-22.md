# REPORT · Night 2026-09-22 · Slices 58–60

## SHIPPED

What exists now that did not at the start of this night:

1. **Slice 58 — ordinals + equals**
   - Digit/word ordinal from→to (`3rd to 4th` / `third to fourth`)
   - Equals targets (`equals` / `equal to` / `==` / `equals four`)
   - Fixed digit-steal lie: `3rd/5 to 4th/5` invented `raw=5 to 4`

2. **Slice 59 — same-as invent-held + level readouts**
   - Fixed THE LIE: `same as 4/5` was flat with no target → held at any latest
   - Bound `is`/`reads`/`matches`/`lands on`/`finishes at`/`comes to`/
     `identical to` (+ word destinations)
   - Word ordinals `eleventh`/`twelfth`

3. **Slice 60 — readout verbs + 13th/14th words**
   - `amounts to`/`evaluates to`/`works out to`/`totals`/`posts`/`yields`/
     `nets`/`registers`/`comes in at`/`returns`
   - Word ordinals `thirteenth`/`fourteenth`

4. **Slice 61 — word ordinals 15–19**
   - `fifteenth`…`nineteenth` / `fifteen`…`nineteen`

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| S58 objects | `claimed_target` / `check_prediction` | grade; naive invents held |
| S59 `same as 4/5` @3 | `check_prediction` | magnet missed / naive held |
| S60 `amounts to 4/5` @3 | same | magnet missed / naive held |
| Suite | `python3 -m pytest -q` | **492 passed, 1 skipped** (493) |
| Docs | `magnet check-docs` | **16 PASS** |
| Pred-demo | `python3 -m magnet.cli pred-demo` | **201/201** · embarrassed **116** |
| Cold scripts | `bash scripts/judge-demo.sh` | JUDGE DEMO OK |
| Cold scripts | `bash scripts/stranger-pass.sh` | stranger pass OK |
| Demo | `magnet demo` | exit 0 |

## WRONG

- Soft hedges (`roughly`/`about`/`nearly` 4/5) unbound — not forced to exact.
- Word ordinals beyond fourteenth (except twentieth) still unbound.
- PNG screenshot sidecars not re-rendered (no Pillow in this VM).
- PR create via ManagePullRequest requires Oscar click (user settings).
- Bedrock live agent not run tonight (no AWS credentials — Oscar gate).
- Soft-hedge refusal is honesty, but a stranger claiming `approximately 4/5`
  still gets no-direction rather than a graded miss — left open.
