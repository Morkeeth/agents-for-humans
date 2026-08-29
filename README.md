# MAGNET · Agents for Humans

**Professional Agents track · AWS Strands · Devpost Sep 14 2026**

> After you change a prompt, model, or skill, a background agent re-runs your eval and tells you
> whether it helped — or prints **`baseline`** instead of inventing a trend.

**Constraint:** No number without the command, population, and timestamp (`3/5`, never `3`).

## Quick start

```bash
pip install -e .
magnet init
magnet demo
```

Cold path — no keys, no network:

```bash
git clone https://github.com/Morkeeth/agents-for-humans.git
cd agents-for-humans
pip install -e .
magnet demo
```

## Strands agent · 4 tools

| Tool | Job |
|------|-----|
| `run_probe` | Run your eval; return value/pop + repro command |
| `record_week` | Store this week's reading in the SQLite ledger |
| `adopt_change` | Record a prompt/model/skill change + prediction |
| `check_docs` | Re-derive README numbers; exit non-zero on drift |

Ledger lives in-repo at `.magnet/ledger.db` — not Helicon-only.

## Verify

```bash
pytest
magnet check-docs
```

See `hack.md` for the build contract and `docs/architecture.md` for the flow diagram.
