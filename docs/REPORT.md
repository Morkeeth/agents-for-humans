# Build report · Slice 13 · 2026-09-02

## SHIPPED

- `magnet/stack.py` — inventory / gaps / rank / verify_declaration ported from
  the real object `Morkeeth/mountain-of-helicon` `helicon/magnet.py` (previously
  cited as measurement-bench 404)
- `magnet/bakeoff.py` — planted flood scored against four arms:
  magnet · naive_stars · naive_name · silent_null
- CLI: `magnet stack`, `magnet fit`, `magnet bakeoff`
- Cold-path fixture stack at `fixtures/stack/` (no `~/.claude` required)
- Judge-demo step 7/8 runs stack + bakeoff
- Architecture diagram extended with stack→gaps→rank→bakeoff
- 90 pytest tests (re-derived from `tests/test_*.py`)

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests green | `python3 -m pytest -q` → 90 passed |
| check_docs | `python3 -m magnet.cli check-docs` → 11 claims PASS |
| Stack inventory | `python3 -m magnet.cli stack` → EMPTY agents, UNCOVERED listed |
| Bakeoff | `python3 -m magnet.cli bakeoff --no-write` → magnet best; synonym 0/3 primary; claims 3/3; wine-liar False; naive_stars admits dupes+liar |
| Liar cannot buy rank | bakeoff + `tests/test_stack_bakeoff.py::test_claims_do_not_buy_score` |
| Name tie-break defect | `test_no_signal_items_are_not_ranked_by_name` + bakeoff FINDING on naive_name |
| Word-boundary ui≠guitar | `test_word_boundary_rejects_ui_in_guitar` |

## WRONG

- **First bakeoff run magnet recall was 0.0** — fixture left `planning`/`design`
  uncovered, so noise domains ("plan a wedding", "colour palette") filled top-20.
  Fixed by covering those caps on the fixture; the vocabulary-collision finding
  stays in the LOG.
- **`reproduce` stemmed to debug `repro`** — verify-receipt skill briefly covered
  debug by accident; description rewritten.
- **Surface arm 1/2** — `reviewer-agent` demoted by word-overlap with owned
  `critique` command (score −2). Not papered over.
- **Synonym primary still 0/3** — EXP-MAGNET-01 finding re-derived; claims tier
  recovers 3/3 without letting the wine-liar into primary.
- **Bedrock in cloud VM still BLOCKED** — no AWS credentials.
- **fleet-ops plan still 404** — used helicon magnet.py as the source object instead.
- **`sk-` substring ban is unsafe** — matches `task-inbox`; secrets test now uses
  `sk-ant-` / `sk_live` shapes.
