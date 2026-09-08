# Build report · Slice 20 · 2026-09-08

## SHIPPED

### Slice 20 — Ultimate Guide closed loop
- `tools-coverage`, `hook-coverage`, `prompt-consistency` bind probes (open the stack object)
- Fixture objects: `CLAUDE.md`, `post-compact-reinject.txt`, `Bash(rm -rf *)` allow (starts RED)
- `magnet guide-demo` — 5-row UG verdict table vs naive title; repo-blind flat; moved=5/5
- `check_docs` now scans `docs/screenshots/*.txt` (skips drift-demo's intentional fakes)
- Bakeoff FINDING when surface < 2/2 (cross-surface dupe — helicon science, not papered over)
- Screenshot sidecars re-derived; judge docs → **169** tests; list-probes **total 9**

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests | `python3 -m pytest -q` → 169 passed |
| check_docs | `magnet check-docs` → 13 claims PASS |
| guide-demo FINDING | `magnet guide-demo` → moved=5/5 · check-docs 13/13 unchanged |
| bind-demo | `magnet bind-demo` → effort 0→7/7 · deny 0→4/4 · repo-blind flat |
| Fixture untouched | `magnet probe tools-coverage` → 0/7 after guide-demo |
| list-probes | `magnet list-probes` → total 9 |
| bakeoff surface FINDING | `magnet bakeoff --no-write` → surface 1/2 FINDING line |
| Screenshot control | stale 113 made check_docs RED; after re-derive → PASS |
| pytest-pass-rate | `magnet probe pytest-pass-rate` → 168/168 (`-m "not slow"`) |
| Cold clone s20 | `/tmp/magnet-cold-s20` @ `68991cc` → 169 passed · guide-demo FINDING · JUDGE DEMO OK |
| SHIP GATE main | `git push origin main` → `dabe8c7` |

## WRONG

- **Surface arm still 1/2** — reviewer-agent demoted by overlap with `critique` command; printed as FINDING, not rewritten (helicon cross-surface dupe science).
- **Screenshot PNGs not re-rendered** — `.txt` sidecars updated; PNGs still show old frames until Oscar runs `scripts/render-screenshot.py`.
- **Bedrock cloud still BLOCKED** — no AWS creds in this VM.
- **Prediction still lexical** — "all tests still pass" → no-direction.
- **Agent Grinder still 1/12** at the real object.
- **guide-demo mid-slice showed check-docs 5/14** while docs/screenshots lagged — control went RED correctly (including the 113 sidecar gap this slice closed).
- **Parallel night branch `magnet recover` not merged** — left on `cursor/stack-magnet-night-5e60`; not this slice.
