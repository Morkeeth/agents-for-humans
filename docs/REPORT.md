# Build report · 2026-08-29

## SHIPPED

- Python package `magnet-agents-for-humans` with `magnet` CLI (`init`, `demo`, `probe`, `record`, `check-docs`)
- In-repo SQLite ledger at `.magnet/ledger.db` (probe readings + adoptions)
- Strands agent wiring: 4 tools (`run_probe`, `record_week`, `adopt_change`, `check_docs`) via `magnet.tools.build_strands_tools()`
- Reporter ported from `helicon/measure.py` science: value/pop, baseline when `<2` readings, helped/hurt with ↑/↓
- Cold demo: baseline 3/5 → adopt fake skill → 4/5 → `helped` receipt + naive vs magnet comparison (including embarrassing 1-reading case)
- `check_docs` probe: re-derives README tool count and tool names; exits non-zero on drift (+ pytest drift catch)
- `docs/architecture.md` mermaid diagram
- `docs/STRANGER-PASS.md` with command output
- 17 pytest tests

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests green | `python3 -m pytest -q` → 17 passed |
| Cold demo exits 0 with receipt | `magnet demo` → exit 0, prints `verdict    helped` and 1-reading baseline case |
| check_docs passes on clean README | `magnet check-docs` → 5 claims PASS, exit 0 |
| check_docs catches drift | `pytest tests/test_check_docs_drift.py -q` → 2 passed |
| Ledger round-trip | `pytest tests/test_ledger.py -q` → 3 passed |
| Baseline on first reading | `pytest tests/test_reporter.py::test_first_reading_is_baseline -q` → passed |
| 4 Strands tools registered | `pytest tests/test_strands_tools.py -q` → 1 passed |
| Embarrassing naive vs magnet | `magnet demo` → `naive verdict helped` vs `magnet verdict baseline` after 1 reading |

## WRONG

- **`measurement-bench/magnet.py` was not accessible** (404). Reporter logic ported from `helicon/measure.py` in mountain-of-helicon — same baseline/delta science (`delta` None when `<2` measured readings), but not a byte-for-byte port of the cited file.
- **Strands agent loop was not exercised against Bedrock** — no AWS credentials in this environment. Tools are wired and importable; only the LLM orchestration path is unverified live.
- **Naive and MAGNET agree on the 2-reading demo** (both `helped`). The divergence is shown only after the first reading; the demo output now surfaces that case explicitly.
- **`check_docs` is repo-specific**, not a general doc-drift port of helicon.docdrift's full COUNT/LIST/EVAL suite. It checks tool count + tool name presence only.
- **Demo probe is synthetic** (`skill_bonus` in SQLite), not a real eval harness. It proves the ledger loop, not that a skill helped in production.
- **GitHub cold clone verified post-push:** `git clone https://github.com/Morkeeth/agents-for-humans.git /tmp/magnet-github-cold && pip install -e ".[dev]" && magnet demo && pytest -q` → exit 0 at `e798729`.
