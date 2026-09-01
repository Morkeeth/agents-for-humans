# _HACK-CONTRACT.md · MAGNET

Canonical contract lives in **`hack.md`**. This file is the portable summary for judges and agents.

---

## Seven parts (each one job)

| Part | Job |
|------|-----|
| NORTH STAR | What this is, in a sentence a stranger acts on |
| PROMISE LINE | What a user GETS + the one constraint |
| OPEN QUESTIONS | What is NOT decided — blocking ones stop the phase |
| CONSTITUTION | Rules this build may never break |
| PLAN | Risk-first slices — riskiest is slice 1 |
| NOW | Exactly one slice |
| LOG | What happened, including what failed |

**Rule:** A box is truth only when its done-when was **RUN**. If you tick it, say the command.

---

## NORTH STAR

The field has too many skills and no memory of what they did. MAGNET is the adoption log + eval runner for **your** agent stack.

## PROMISE LINE

After you change a prompt, model, or skill, a background agent re-runs your eval and tells you whether it helped — or prints **`baseline`** instead of inventing a trend.

**Constraint:** No number without the command, population, and timestamp (`3/5`, never `3`).

## FOUR FAILURES TO AVOID

1. **Run it, don't read it** — defects found by executing, not reading.
2. **Controls must go RED** — `grep -qv` on empty input returns 1; green on outage is a lie.
3. **Re-derive numbers** — never carry figures from prompts or stale docs.
4. **Open the object** — never rank by title/name; open the real artifact.

## REPORT FORMAT (mandatory third section)

- **SHIPPED** — what exists now
- **VERIFIED** — each claim + command at its object
- **WRONG** — what failed, unverified, or left broken (required)

## ONE COMMAND FOR JUDGES

```bash
bash scripts/judge-demo.sh
```

Scorecard: `docs/JUDGE-SCORECARD-2026-09-02.md` · Bedrock live: `docs/BEDROCK-LIVE-RECEIPT-2026-09-02.md`
