# External stack receipt · 2026-09-07

Measured stacks **we did not build**. Numbers re-derived at the object — do not
trust this file without re-running the commands. Cold path does **not** require
these clones; `magnet external-stack --stack fixtures/real-stacks/agentgrinder`
and `magnet redact-scan` are offline.

Capability term fix shipped tonight: bare `extract` → `extract method`
(anthropics/skills docx/pdf said "extracting" and invented refactor coverage).

## Agent Grinder (real clone)

```bash
git clone --depth 1 https://github.com/Morkeeth/agentgrinder.git /tmp/agentgrinder-real
magnet external-stack --stack /tmp/agentgrinder-real
```

| Probe | Value | Command |
|-------|------:|---------|
| stack-coverage | 1/12 | `magnet probe stack-coverage --stack /tmp/agentgrinder-real` |

Inventory: skills=1 · commands=0 · agents=0 · hooks=0.
Uncovered: data, debug, design, docs, planning, refactor, research, review, security, test-gate, verification.

**FINDING:** Companion product covers **1/12** capabilities (writing only) —
measured at the real object; matches `fixtures/real-stacks/agentgrinder`.
`naive_title` says `complete` because a `skills/` directory exists.

## anthropics/skills

```bash
bash scripts/foreign-stack.sh
# or: MAGNET_FOREIGN_STACK=/tmp/anthropics-skills bash scripts/foreign-stack.sh
```

| Probe | Value | Command |
|-------|------:|---------|
| stack-coverage | 7/12 | `magnet probe stack-coverage --stack /tmp/anthropics-skills` |

Inventory: skills=19 · commands=0 · agents=0 · hooks=0.
Uncovered: data, planning, refactor, review, security.

**FINDING:** Before `extract`→`extract method`, coverage falsely read **8/12**.
After the fix: **7/12**. `pdb-navigator` is **no-signal** here (debug already
covered by their skills) but **fills-gap** on `fixtures/stack` — fixture gaps
≠ foreign gaps. `wine-pairing` is no-signal on both. `naive_title` says complete.

## obra/superpowers

```bash
git clone --depth 1 https://github.com/obra/superpowers.git /tmp/superpowers
magnet external-stack --stack /tmp/superpowers
```

| Probe | Value | Command |
|-------|------:|---------|
| stack-coverage | 6/12 | `magnet probe stack-coverage --stack /tmp/superpowers` |

Inventory: skills=14 · commands=0 · agents=0 · hooks=0.
Uncovered: data, debug, docs, refactor, research, security.

**FINDING:** Same empty-title failure mode. MAGNET prints `6/12`.
`pdb-navigator` fills debug on this object (uncovered there).

## Redact-scan (embarrassment control)

```bash
magnet redact-scan   # must exit 0 on this repo
```

Planted secret in a temp tree exits 1 (see `tests/test_external_and_redact.py`).
First draft of that test went RED on our own source — control worked; we were
the embarrassment. Literals assembled at runtime now.

## Naive arm (loses the truth)

A title-only scanner that sees "Agent Skills" / "superpowers" without opening
SKILL.md invents `complete`. MAGNET opens every SKILL.md.

## Foreign-bind (Ultimate Guide probes · 2026-09-08)

```bash
magnet foreign-bind                                          # offline fixtures
magnet foreign-bind --stack /tmp/anthropics-skills --stack /tmp/superpowers
```

| Stack | effort | tools | deny | hook | naive_title |
|-------|-------:|------:|-----:|-----:|-------------|
| fixtures/stack | 0/7 | 0/7 | 0/4 | 0/2 | complete |
| fixtures/real-stacks/agentgrinder | 0/1 | 0/1 | 0/4 | 1/2 | complete |
| anthropics/skills (clone) | 0/19 | 0/19 | 0/4 | 1/2 | complete |
| obra/superpowers (clone) | 0/14 | 0/14 | 0/4 | 1/2 | complete |

**FINDING:** Marketplace and companion stacks that look complete by title carry
**zero** `effort:` / `allowed-tools:` frontmatter and **zero** sensitive deny
patterns when the object is opened. Numbers re-derived at the clones tonight —
do not carry them; re-run `magnet foreign-bind --stack …`.

## Repro

```bash
magnet redact-scan
magnet external-stack --stack fixtures/real-stacks/agentgrinder
bash scripts/foreign-stack.sh   # network once
```

Numbers above re-derived 2026-09-07 — do not carry them forward without re-running.
