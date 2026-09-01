# Architecture

MAGNET wires a **Strands agent** to an **in-repo SQLite adoption log** and **deterministic probes**.
After you change a prompt, model, or skill, the agent re-runs your eval and prints
`helped`, `hurt`, or **`baseline`** — never a trend from one reading.

```mermaid
flowchart LR
    U[User change event<br/>prompt / model / skill] --> A[Strands Agent<br/>4 tools]
    A --> RP[run_probe]
    A --> RW[record_week]
    A --> AC[adopt_change]
    A --> CD[check_docs]
    RP --> PR[Probe runner<br/>value/pop + command]
    RW --> DB[(SQLite log<br/>.magnet/log.db)]
    AC --> DB
    PR --> DB
    DB --> DS[Decision surface<br/>helped / hurt / baseline]
    CD --> README[README claims]
    README --> SRC[Source truth<br/>re-derived at read time]
    SRC -->|drift| FAIL[exit 1]
```

## Data flow

1. **Baseline** — `record_week` runs `run_probe`, stores `{value, population, command, week}`.
2. **Change** — `adopt_change` records `{change_type, description, prediction}` linked to a probe.
3. **Re-run** — next `record_week` stores a second reading.
4. **Receipt** — reporter compares two *measured* readings:
   - `<2 readings` → **`baseline`**
   - delta matches direction → **`helped`** (↑)
   - delta opposes direction → **`hurt`** (↓)

## Components

| Module | Role |
|--------|------|
| `magnet/tools.py` | Strands `@tool` wrappers |
| `magnet/log.py` | SQLite schema + round-trip |
| `magnet/reporter.py` | value/pop, baseline, helped/hurt (ported from measurement-bench science) |
| `magnet/probes.py` | `demo-pass-rate`, `check-docs`, **`pytest-pass-rate`** (real eval) |
| `magnet/registry.py` | Load YOUR probes from `.magnet/probes.json` |
| `magnet/history.py` | Adoption timeline / decision surface |
| `magnet/demo.py` | One-command cold demo |

## Naive baseline arm

`reporter.naive_verdict()` always returns `helped` on fewer than two readings — the two-hour team bug MAGNET exists to catch. The demo prints both verdicts side by side.

## AWS path (optional · Oscar click)

| Mode | Command | AWS services | Cost |
|------|---------|--------------|------|
| **Local scripted** *(default, CI)* | `magnet agent-run --model local` | none | $0 |
| **Bedrock** *(live LLM chooses tools)* | `magnet agent-run --model bedrock` | Amazon Bedrock | yes |
| **Deterministic fallback** | `magnet agent-run --model none` | none | $0 |

The Strands agent loop is identical in all modes — only the model provider changes. Bedrock has **never** been run in CI; document honestly on Devpost if only local mode is demonstrated in the video.

```mermaid
flowchart TB
    subgraph local [Default · no AWS]
        LA[Strands Agent] --> LT[ScriptedLocalModel]
    end
    subgraph aws [Optional · Oscar creds]
        BA[Strands Agent] --> BR[Amazon Bedrock]
    end
    LA --> Tools[4 tools → SQLite log]
    BA --> Tools
```

