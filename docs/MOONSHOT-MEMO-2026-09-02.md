# Moonshot memo · MAGNET · 2026-09-02

## GOAL

MAGNET wins Sep 14 Agents for Humans as the **Professional Agents** submission — stranger can cold-clone and see why `baseline` beats fake `helped`.

## Current model

Strands agent + SQLite adoption log + deterministic probes = measured helped/hurt/baseline for YOUR stack changes.

## External evidence

| Source | What it says | Confidence |
|--------|--------------|------------|
| Devpost rules | Strands SDK required; 5 criteria equally weighted | high |
| EYES panel 1 Sep | Grinder fails Strands gate; MAGNET fits | high |
| Own demo | naive `helped` on 1 reading vs magnet `baseline` | high (re-run `magnet demo`) |
| Hackathon update | "One workflow end-to-end" beats five half-features | high |

## Hypotheses (ranked)

1. **Receipt beats marketplace** — judges want adopt→probe→delta, not another skill store · kill: stranger-pass fails
2. **Embarrassment hunt scores** — `magnet eval` silent_null arm is differentiator · kill: eval flat vs naive
3. **Bedrock live run** — optional +0.5 on tech axis · kill: no AWS creds by Sep 13

## Refute result (2 Sep)

**Survives:** Hypothesis 1 — STRANGER-PASS + Strands tool dispatch on disk, 61 tests green.  
**Partial:** Hypothesis 3 — Bedrock path documented, never run in CI (honest in DEVPOST-READY).  
**Killed:** Submitting Agent Grinder as primary — wrong SDK for rubric.

## BUILD-PLAN (shipped tonight)

1. ✅ DEVPOST-READY.md
2. ✅ FILM-SCOUT-COMMANDS.md
3. ✅ OSCAR-CLICK-LIST-2026-09-02.md
4. ✅ BUILDER-AWS-DRAFT.md
5. Oscar: video + submit

## OPS

Oscar films · Builder ID · Devpost submit · optional Bedrock run.

## Explicitly NOT doing

| Could do | Why not now |
|----------|-------------|
| Grinder Strands wrapper | Compliance theater; wrong product |
| Hybrid repo merge | 13 days + wedding |
| Auto Devpost submit | Oscar gate |
