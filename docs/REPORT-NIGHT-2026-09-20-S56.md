# REPORT · Slice 56 · 2026-09-20

## SHIPPED

- Signed word-percent: `-twenty percent` / `minus twenty percent` are fall;
  `+twenty percent` / `plus twenty percent` are rise. Digit `-20%` already graded.
- Word arrows: `three → four`, `three -> four`, `one → zero`, `from three → four`
  grade latest against the named destination.
- THE LIE closed: bare-percent default invented rise/held on helped when the
  claim said fall; word arrows left no-direction while a destination sat.

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| `-twenty percent` hurt/−1 | `check_prediction` | held; helped → missed |
| `minus twenty percent` hurt/−20 | same | missed (abs); naive held |
| `three → four` @4/@3 | same | held / missed; naive held @3 |
| Suite | `python3 -m pytest -q` | re-derived at ship |
| Pred-demo | `python3 -m magnet.cli pred-demo` | **166/166** · embarrassed **82** |

## WRONG

- `minus_twenty_percent_missed` (helped on a fall claim) does not embarrass
  naive — fixed intent makes naive miss too; embarrassment is the absolute−20 row.
- `exactly four` / `exactly twenty` word targets still unbound (digit grades).
- `fifteen percent` still unbound (not in tens word list).
- PR create pending user approval; branch pushed, main merge is Oscar's click.
