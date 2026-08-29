# Build report · 2026-08-29

## SHIPPED

- Python package `magnet-agents-for-humans` with `magnet` CLI (`init`, `demo`, `probe`, `record`, `check-docs`)
- In-repo SQLite ledger at `.magnet/ledger.db` (probe readings + adoptions)
- Strands agent wiring: 4 tools (`run_probe`, `record_week`, `adopt_change`, `check_docs`) via `magnet.tools.build_strands_tools()`
- Reporter ported from measurement-bench / helicon.measure science: value/pop, baseline when `<2` readings, helped/hurt with ↑/↓
- Cold demo: baseline 3/5 → adopt fake skill → 4/5 → `helped` receipt + naive baseline arm comparison
- `check_docs` probe: re-derives README tool count and tool names; exits non-zero on drift
- `docs/architecture.md` mermaid diagram
- `docs/STRANGER-PASS.md` with command output
- 14 pytest tests

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests green | `pytest -q` → 14 passed |
| Cold demo exits 0 with receipt | `magnet demo` → exit 0, prints `verdict    helped` |
| Stranger path (no git metadata) | `cp -r … /tmp/magnet-cold && pip install -e . && magnet demo` → exit 0 |
| check_docs passes on clean README | `magnet check-docs` → 5 claims PASS, exit 0 |
| Ledger round-trip | `pytest tests/test_ledger.py -q` → 3 passed |
| Baseline on first reading | `pytest tests/test_reporter.py::test_first_reading_is_baseline -q` → passed |
| 4 Strands tools registered | `pytest tests/test_demo.py::test_four_strands_tools_exist -q` → passed |

## WRONG

- **`measurement-bench/magnet.py` was not accessible** (fleet-ops 404). Reporter logic was ported from `helicon/measure.py` in mountain-of-helicon instead — same baseline/delta science, but not a byte-for-byte port of the cited file.
- **Strands agent loop was not exercised against Bedrock** — no AWS credentials in this environment. Tools are wired and importable; only the LLM orchestration path is unverified live.
- **Naive baseline arm coincidentally agrees on the demo** (both say `helped` because there are two readings). The embarrassing case — naive says `helped` on one reading while MAGNET says `baseline` — is tested in unit tests but not shown in demo output.
- **`check_docs` is repo-specific**, not a general doc-drift port of helicon.docdrift's full COUNT/LIST/EVAL suite. It checks tool count + tool name presence only.
- **Demo probe is synthetic** (`skill_bonus` in SQLite), not a real eval harness. It proves the ledger loop, not that a skill helped in production.
