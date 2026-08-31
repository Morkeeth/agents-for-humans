# Build report · 2026-08-30

## SHIPPED

- Python package `magnet-agents-for-humans` with `magnet` CLI (`init`, `demo`, `eval`, `agent-run`, `probe`, `record`, `check-docs`)
- In-repo SQLite log at `.magnet/log.db` (probe readings + adoptions)
- Strands agent wiring: 4 tools (`run_probe`, `record_week`, `adopt_change`, `check_docs`) via `magnet.tools.build_strands_tools()`
- Reporter ported from `helicon/measure.py` science: value/pop, baseline when `<2` readings, helped/hurt with ↑/↓
- Cold demo: baseline 3/5 → adopt fake skill → 4/5 → `helped` receipt + naive vs magnet comparison (including embarrassing 1-reading case)
- **`magnet eval`**: 5-scenario matrix scoring naive (3/5), magnet (5/5), silent_null (1/5) against explicit ground truth
- **`magnet agent-run`**: deterministic 4-tool chain without Bedrock (run_probe → record_week → adopt_change → record_week → check_docs)
- `check_docs` probe: re-derives README tool count, tool names, and pytest counts in STRANGER-PASS/REPORT; exits non-zero on drift
- `docs/architecture.md` mermaid diagram
- `docs/STRANGER-PASS.md` with command output
- 1 pytest tests

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests green | `python3 -m pytest -q` → 48 passed in 0.96s |
| Cold demo exits 0 with receipt | `python -m magnet.cli demo` → exit 0, prints `verdict    helped` and 1-reading baseline case |
| Eval scores arms | `python -m magnet.cli eval` → magnet 5/5, naive 3/5, silent_null 1/5 |
| Agent-run 4-tool chain | `python -m magnet.cli agent-run` → exit 0, all 4 tool steps logged |
| check_docs passes on clean README | `python -m magnet.cli check-docs` → all claims PASS, exit 0 |
| check_docs catches tool drift | `pytest tests/test_check_docs_drift.py -q` → 2 passed |
| check_docs catches pytest count drift | `pytest tests/test_check_docs_pytest_count.py -q` → 2 passed |
| Log round-trip | `pytest tests/test_log.py -q` → 7 passed |
| Baseline on first reading | `pytest tests/test_reporter.py::test_first_reading_is_baseline -q` → passed |
| 4 Strands tools registered | `pytest tests/test_strands_tools.py -q` → 1 passed |
| Embarrassing naive vs magnet | `magnet demo` → `naive verdict helped` vs `magnet verdict baseline` after 1 reading |

## WRONG

- **`measurement-bench/magnet.py` was not accessible** (404). Reporter logic ported from `helicon/measure.py` in mountain-of-helicon — same baseline/delta science (`delta` None when `<2` measured readings), but not a byte-for-byte port of the cited file.
- **Strands agent loop was not exercised against Bedrock** — no AWS credentials in this environment. `magnet agent-run` proves the 4-tool chain deterministically; only the LLM orchestration path is unverified live.
- **Naive and MAGNET agree on the 2-reading demo** (both `helped`). The divergence is shown only after the first reading and on `unchanged`/`one_reading` scenarios in `magnet eval`.
- **`silent_null` (always baseline) scores 1/5** — it wins only on `one_reading`. It is included as the embarrassing conservative arm, not as a competitor to ship.
- **`check_docs` is repo-specific**, not a general doc-drift port of helicon.docdrift's full COUNT/LIST/EVAL suite. It checks tool count, tool names, and pytest counts in docs.
- **Demo probe is synthetic** (`skill_bonus` in SQLite), not a real eval harness. It proves the log loop, not that a skill helped in production.
- **`magnet` CLI may not be on PATH** after `pip install -e .` in some environments (`~/.local/bin`). STRANGER-PASS documents `python -m magnet.cli` fallback.
