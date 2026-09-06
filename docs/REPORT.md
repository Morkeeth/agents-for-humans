# Build report · Slice 15 · 2026-09-06

## SHIPPED

### Slice 15 — stack-bind
- `magnet/stack_bind.py` — `effort-coverage` + `deny-coverage` probes that open
  the stack object (SKILL.md frontmatter + settings.json deny patterns)
- `magnet/bind_demo.py` + `magnet bind-demo` — applies Ultimate Guide changes
  (`effort:` + `permissions.deny`) to a **temp copy** of fixtures/stack;
  proves repo-blind `check-docs` stays flat while stack probes move
- `magnet external-stack --stack <path>` — measure a stack you did not build
- Adopt receipts: stack probes print `measures stack`; repo probes still warn
  `measures repo only` for hook/setting changes
- Judge + stranger scripts call `bind-demo`
- `docs/EXTERNAL-STACK-RECEIPT.md` — anthropics/skills measured at the object

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests green | `python3 -m pytest -q` → 124 passed |
| check_docs | `magnet check-docs` → 11 claims PASS |
| bind-demo FINDING | `magnet bind-demo` → repo-blind unchanged; effort 0/7→7/7; deny 0/4→4/4 |
| Fixture untouched | `magnet probe effort-coverage` → 0/7 after bind-demo |
| External stack | `magnet external-stack --stack /tmp/anthropics-skills` → effort 0/19 |
| Hook+stack probe | `magnet adopt hook … --probe deny-coverage` → `measures stack` |
| Hook+repo probe | `magnet adopt hook … --probe demo-pass-rate` → `measures repo only` |
| list-probes | `magnet list-probes` → total 6 |
| Judge quick | `MAGNET_JUDGE_QUICK=1 bash scripts/judge-demo.sh` → JUDGE DEMO OK |

## WRONG

- **check-docs was 5/11 mid-slice** until the six judge docs were re-derived
  113→124. Found by running `magnet bind-demo` / `magnet check-docs`, not by
  reading. Fixed before ship.
- **anthropics/skills has no settings.json** — deny-coverage 0/4 is correct for
  a catalogue, not a full agent config; do not read it as "Anthropic failed
  deny hardening."
- **Bedrock cloud still BLOCKED** — NoCredentialsError on this VM.
- **fleet-ops plan still 404**.
- **SHIP GATE asked `git push origin main`** — cloud agent policy uses feature
  branch + PR; outward push to public main is Oscar's click. Branch:
  `cursor/stack-bind-probes-7019`.
- **Synonym bakeoff arm still 0/3 primary** — unchanged; claims tier recovers.
- **Screenshots under docs/screenshots/** still show 113 — not in the
  check_docs scan set; left stale on purpose (historical captures).
