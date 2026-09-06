# External stack receipt · 2026-09-06

Measured stacks **we did not build**. Numbers re-derived at the object — do not
trust this file without re-running the commands. Cold path does **not** require
these clones; `magnet bind-demo` uses `fixtures/stack` only.

## anthropics/skills

```bash
git clone --depth 1 https://github.com/anthropics/skills.git /tmp/anthropics-skills
magnet external-stack --stack /tmp/anthropics-skills
```

| Probe | Value | Command |
|-------|------:|---------|
| effort-coverage | 0/19 | `magnet probe effort-coverage --stack /tmp/anthropics-skills` |
| deny-coverage | 0/4 | `magnet probe deny-coverage --stack /tmp/anthropics-skills` |
| stack-coverage | 8/12 | `magnet probe stack-coverage --stack /tmp/anthropics-skills` |

Inventory: skills=19 · commands=0 · agents=0 · hooks=0.
Uncovered: data, planning, review, security.

**FINDING:** Anthropic's published skills carry **zero** `effort:` frontmatter
keys (0/19). Every SKILL.md was opened; keys counted at the object.

## obra/superpowers

```bash
git clone --depth 1 https://github.com/obra/superpowers.git /tmp/superpowers
magnet external-stack --stack /tmp/superpowers
```

| Probe | Value | Command |
|-------|------:|---------|
| effort-coverage | 0/14 | `magnet probe effort-coverage --stack /tmp/superpowers` |
| deny-coverage | 0/4 | `magnet probe deny-coverage --stack /tmp/superpowers` |
| stack-coverage | 6/12 | `magnet probe stack-coverage --stack /tmp/superpowers` |

Inventory: skills=14 · commands=0 · agents=0 · hooks=0.
Uncovered: data, debug, docs, refactor, research, security.
No `settings.json` in the repo root (deny 0/4 expected).

**FINDING:** Same empty `effort:` reading as anthropics/skills. A title-only
scanner that sees "skills framework" and prints complete would green-light both.
MAGNET prints `0/14`.

## Naive arm (loses the truth)

A title-only scanner that sees "Agent Skills" / "superpowers" without opening
frontmatter invents a pass. MAGNET's probe opens every SKILL.md.
