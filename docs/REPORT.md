# Build report · Slice 15–16 · 2026-09-06

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
- `docs/EXTERNAL-STACK-RECEIPT.md` — anthropics/skills + obra/superpowers

### Slice 16 — redact-scan + MAGNET_STACK
- `magnet/redact.py` + `magnet redact-scan` — secret-pattern scan that can go
  RED (planted secrets in tests) and must stay GREEN on this repo
- `MAGNET_STACK` env overrides default stack dir
- Stranger + judge scripts call `redact-scan`

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests green | `python3 -m pytest -q` → 130 passed |
| check_docs | `magnet check-docs` → 11 claims PASS |
| bind-demo FINDING | `magnet bind-demo` → repo-blind unchanged; effort 0/7→7/7; deny 0/4→4/4 |
| Fixture untouched | `magnet probe effort-coverage` → 0/7 after bind-demo |
| External anthropics | `magnet external-stack --stack /tmp/anthropics-skills` → effort 0/19 |
| External superpowers | `magnet external-stack --stack /tmp/superpowers` → effort 0/14 |
| redact-scan clean | `magnet redact-scan` → findings 0 · exit 0 |
| redact-scan RED | `tests/test_redact_scan.py` planted secret → exit 1 |
| Hook+stack probe | `magnet adopt hook … --probe deny-coverage` → `measures stack` |
| Cold clone (s15) | clone branch `cursor/stack-bind-probes-7019` → bind-demo + 124 pytest exit 0 at `fd74fc3` |
| Judge quick | `MAGNET_JUDGE_QUICK=1 bash scripts/judge-demo.sh` → JUDGE DEMO OK |

## WRONG

- **check-docs was 5/11 mid-slice-15** until the six judge docs were re-derived
  113→124 (then 130). Found by running, not reading.
- **redact-scan first went RED on our own test file** — literal PEM / aws_secret
  strings in `tests/test_redact_scan.py` matched. Fixed by assembling patterns at
  runtime. The control worked; we were the embarrassment.
- **allowlist false positive** — substring `example` inside `EXAMPLEKEY` skipped
  a planted secret. Fixed to word-boundary markers.
- **anthropics/skills and obra/superpowers have no settings.json** — deny 0/4
  is correct for a catalogue, not a full agent config.
- **Bedrock cloud still BLOCKED** — NoCredentialsError on this VM.
- **fleet-ops plan still 404**.
- **SHIP GATE asked `git push origin main`** — cloud agent policy uses feature
  branch + PR; outward push to public main is Oscar's click. Branch:
  `cursor/stack-bind-probes-7019`.
- **Screenshots under docs/screenshots/** still show 113 — not in the
  check_docs scan set; left stale on purpose (historical captures).
- **Cold clone after s16 not yet re-run** at the time this paragraph was
  written — re-derive after push.
