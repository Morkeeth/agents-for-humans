# Build report · 2026-09-01

## SHIPPED

- Python package `magnet-agents-for-humans` with `magnet` CLI (`init`, `demo`, `eval`, `agent-run`, `probe`, `record`, `check-docs`, **`list-probes`**, **`history`**)
- In-repo SQLite log at `.magnet/log.db` (probe readings + adoptions)
- Strands agent wiring: 4 tools via real `strands.Agent` event loop + `ScriptedLocalModel` (no spend)
- Reporter: value/pop, baseline when `<2` readings, helped/hurt with ↑/↓
- Cold demo + naive vs magnet embarrassing case
- **`magnet eval`**: naive 3/5, magnet 5/5, silent_null 1/5
- **`pytest-pass-rate` probe**: runs real `pytest -q`, parses passed/total from subprocess output (not docs)
- **`.magnet/probes.json` registry**: add YOUR eval commands without code changes (see `.magnet/probes.json.example`)
- **`magnet history`**: adoption timeline with verdicts from SQLite
- `check_docs`: re-derives README tool count, tool names, pytest counts in **all judge/devpost docs**
- **`magnet drift-demo`**: live Qwen lesson — fake repo fails, real repo passes
- `docs/FUNDABLE-WEDGE.md` — investor one-pager for Sep 14
- `docs/architecture.md`, `docs/STRANGER-PASS.md`
- 86 pytest tests
- **GitHub Actions** `.github/workflows/judge-demo.yml` — judge-demo + stranger-pass + cold-clone on every push
- **`scripts/cold-clone-verify.sh`** — post-push GitHub clone kill-bar

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests green | `python3 -m pytest -q` → 86 passed |
| CI workflow | `.github/workflows/judge-demo.yml` runs `bash scripts/judge-demo.sh` |
| Cold clone verify | `bash scripts/cold-clone-verify.sh file://$PWD` → COLD CLONE OK |
| Cold demo | `python -m magnet.cli demo` → exit 0, `verdict helped` + 1-reading baseline case |
| Eval arms | `python -m magnet.cli eval` → magnet 5/5, naive 3/5, silent_null 1/5 |
| Strands agent loop | `python -m magnet.cli agent-run` → 5 tools dispatched, not DEGRADED |
| Real pytest probe | `python -m magnet.cli probe pytest-pass-rate` → 73/73 from subprocess |
| Stranger pass script | `bash scripts/stranger-pass.sh` → exit 0 |
| `magnet adopt` | `python -m magnet.cli adopt skill … --demo-bonus --reset` → receipt |
| Probe registry | `python -m magnet.cli list-probes` → 3 built-ins |
| History | `python -m magnet.cli history` → adoption + verdict after demo |
| check_docs clean | `python -m magnet.cli check-docs` → all PASS (11 claims incl. judge docs) |
| Drift demo | `python -m magnet.cli drift-demo` → fake FAIL, real PASS |
| Cold clone | `git clone … && pip install -e ".[dev]" && magnet demo` → exit 0 |

## WRONG

- **`measurement-bench/magnet.py` still 404** — reporter ported from `helicon/measure.py`, not byte-for-byte from cited file.
- **Bedrock in cloud VM BLOCKED** — `NoCredentialsError` on STS; live run verified on Oscar local only (`docs/BEDROCK-LIVE-RECEIPT-2026-09-02.md`).
- **`pytest-pass-rate` refuses to run inside pytest** (detects `PYTEST_CURRENT_TEST`) — must invoke from CLI; this is intentional anti-recursion, not a bug, but strangers may find it surprising.
- **Registry parsers are minimal** (`pytest_summary`, `value_pop`, `exit_code`, `regex:`) — not a full port of helicon docdrift.
- **Demo probe remains synthetic** for the cold path; `pytest-pass-rate` is the real eval but runs the whole suite (slow on large repos).
- **`magnet` CLI may not be on PATH** after install — use `python -m magnet.cli`.
