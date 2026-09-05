# Build report · Slice 15–17 · 2026-09-05

## SHIPPED

### Slice 17 — screenshot sidecars can go RED
- Sidecars still claimed 113 tests / 11 claims while the suite moved; check_docs
  never looked at them (green on outage).
- `scripts/capture-sidecars.sh` re-derives live transcripts (writes via temp+mv —
  redirect-onto-self was truncating the file before check-docs read it).
- check_docs now scans `docs/screenshots/pytest.txt` and freshness of
  `check-docs.txt` (must include sep14 ruling; must not say 113/11).
- apply-eval / apply-demo sidecars captured.

### Slice 16 — ruling honesty + unmeasured probe exit
- README matched EYES (MAGNET submits; Grinder companion).
- `sep14 entry ruling` claim; `magnet probe` exits 1 when value is None.

### Slice 15 — apply-to-stack
- `magnet adopt --apply` · `apply-demo` · `apply-eval` (naive_fit 2/3, magnet 3/3).
- 133 pytest tests (re-derived from `tests/test_*.py`).

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests green | `python3 -m pytest -q` → 133 passed |
| check_docs | `magnet check-docs` → 14 claims PASS |
| Capture | `bash scripts/capture-sidecars.sh` → exit 0; pytest.txt `133 passed` |
| Probe non-slow | `magnet probe pytest-pass-rate` → 132/132 (1 slow deselected) — re-derive |
| Apply-eval | `magnet apply-eval` → magnet 3/3 |
| Dead probe | registry `false` → exit 1 |
| Cold clone s16 | `/tmp/magnet-cold-s16` → 131 passed (pre-s17) |

## WRONG

- **Screenshot control was not a control** until tonight — passed for weeks on
  stale 113 while the suite moved.
- **Capture redirect bug** — `> sidecar.txt` truncated the file before the
  command ran; found by running capture, not by reading the script.
- **Dated film takes** (`one-workflow` 112 @ f690fd0, demo/agent-run/eval/history
  PNGs) still stale — Oscar re-films; capture-sidecars deliberately skips them.
- Synonym bakeoff primary still 0/3; Bedrock cloud BLOCKED; `--apply` skill-only.
- **SHIP GATE `git push origin main`** — feature branch + PR only; Oscar merges.
- Agent Grinder VIDEO-SHOTLIST still says never show MAGNET (other repo).
