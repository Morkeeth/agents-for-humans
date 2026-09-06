# External stack receipt · anthropics/skills · 2026-09-06

Measured a stack **we did not build**. Numbers re-derived at the object — do not
trust this file without re-running the commands.

## Object

```bash
git clone --depth 1 https://github.com/anthropics/skills.git /tmp/anthropics-skills
magnet external-stack --stack /tmp/anthropics-skills
```

Repo: [anthropics/skills](https://github.com/anthropics/skills) (public Agent Skills).
Opened 2026-09-06 on this cloud VM. Cold path does **not** require this clone —
`magnet bind-demo` uses `fixtures/stack` only.

## Readings (re-derived)

| Probe | Value | Command |
|-------|------:|---------|
| effort-coverage | 0/19 | `magnet probe effort-coverage --stack /tmp/anthropics-skills` |
| deny-coverage | 0/4 | `magnet probe deny-coverage --stack /tmp/anthropics-skills` |
| stack-coverage | 8/12 | `magnet probe stack-coverage --stack /tmp/anthropics-skills` |

Inventory (from the same run): skills=19 · commands=0 · agents=0 · hooks=0.
Uncovered caps: data, planning, review, security.
Empty surfaces: commands, agents, hooks.

## FINDING

Anthropic's published skills carry **zero** `effort:` frontmatter keys (0/19).
The Ultimate Guide audit treated `effort:` coverage as a hardening signal on a
local stack; against this public baseline the same probe reads empty. That is
not a ranking by name — every SKILL.md was opened and its frontmatter keys
counted.

`deny-coverage` is 0/4 because this repo has no `settings.json` deny list —
expected for a skills catalogue, not a full agent config. The probe still opens
the object and refuses to invent a pass.

## Naive arm (would lose the truth)

A title-only scanner that sees "skills" + "Agent Skills" and prints `helped` /
`complete` without opening frontmatter would green-light this stack. MAGNET
prints `0/19`.
