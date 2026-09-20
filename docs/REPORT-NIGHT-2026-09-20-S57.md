# REPORT · Slice 57 · 2026-09-20

## SHIPPED

- Word targets: `exactly four`, `exactly four/five`, `exactly twenty`,
  `falls to four`, `reaches five`, `hits four`, `ends at four`.
- THE LIE closed: `exactly` alone made flat intent with no target → unchanged
  invented held at any latest; digit `exactly 4` already graded.
- Guard: `exactly twenty percent` stays percent-of-pop (not target=20).

## VERIFIED

| Claim | Command | Result |
|-------|---------|--------|
| `exactly four` @4/@3 | `check_prediction` | held / missed; naive held @3 |
| `falls to four` @4/@1 | same | held / missed; naive held @1 |
| `exactly twenty` @20/@19 | same | held / missed |
| `exactly twenty percent` | `claimed_target`/`claimed_percent` | tgt=None pct=20 |
| Pred-demo | `magnet pred-demo` | **172/172** · embarrassed **86** |
| Suite | `python3 -m pytest -q` | **461 passed, 1 skipped** |
| Docs | `magnet check-docs` | **15 PASS** |

## WRONG

- `fifteen percent` still unbound (not in tens word list).
- `must be four` (no exactly) still unbound.
- PR create pending Oscar approval; main merge is Oscar's click.
