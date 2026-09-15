---
doc: hack
project: MAGNET · Agents for Humans
phase: BUILD
event: AWS Strands · Devpost · Sun 14 Sep 2026 17:00 PDT · $40K
track: Professional Agents
ruling: Option A · MAGNET · Oscar 29 Aug 2026
---

# MAGNET — hack.md

> **Magnet to YOUR stack** — not a skill marketplace. After you change a prompt, model, or skill,
> a background agent re-runs **your** eval and prints helped/hurt/baseline.

## ⭐ NORTH STAR

The field has too many skills and no memory of what they did. MAGNET is the adoption log +
eval runner for **your** agent stack.

## PROMISE LINE

After you change a prompt, model, or skill, a background agent re-runs your eval and tells you
whether it helped — or prints **`baseline`** instead of inventing a trend.

## CONSTRAINT

No number without the command that produced it, the population it is out of, and when it was read.
(`3/5`, never `3`.)

## OPEN QUESTIONS

- Which real eval probes ship for Devpost demo beyond `demo-pass-rate` + `pytest-pass-rate` + stack/bakeoff? (blocking for production, not for cold path)
- Bedrock model ID for live Strands agent run? (Oscar click — not resolved here)

## CONSTITUTION

1. Promise line before code.
2. Port science from `measurement-bench` — do not rewrite.
3. In-repo SQLite adapter — NOT Helicon-only.
4. MIT licence.
5. No AWS spend beyond free tier without Oscar click.
6. No register/submit/video — Oscar only.

## PLAN (risk-first)

| # | Slice | Done when |
|---|-------|-----------|
| 0 | Repo + README + architecture diagram | clone works |
| 1 | Strands agent · 4 tools | `magnet demo` cold-runs |
| 2 | Port kernel from measurement-bench/magnet.py | tests green |
| 3 | Core loop: adopt → re-run → delta receipt | demo end-to-end |
| 4 | Stranger pass doc | STRANGER-PASS.md with command output |
| 5 | Eval harness + agent-run + check_docs pytest drift | `magnet eval` + `magnet agent-run` exit 0 |
| 6 | Real pytest probe + registry + history | `magnet probe pytest-pass-rate` + `magnet list-probes` + `magnet history` exit 0 |
| 7 | `magnet adopt` + stranger-pass script | `bash scripts/stranger-pass.sh` exit 0 |
| 8 | Devpost pack + film scout | DEVPOST-READY + FILM-SCOUT + OSCAR-CLICK-LIST on disk |
| 9 | Judge-winning path | `scripts/judge-demo.sh` + JUDGE-SCORECARD + DEVPOST-DESCRIPTION |
| 10 | Judge path verified + Bedrock local receipt | `judge-demo.sh` cold clone · cloud Bedrock BLOCKED |
| 11 | CI + production adopt + cold-clone verify | `.github/workflows/judge-demo.yml` green · `cold-clone-verify.sh` exit 0 |
| 12 | Drift demo + judge-doc scan + fundable wedge | `magnet drift-demo` exit 0 · check_docs scans 6 judge docs · `docs/FUNDABLE-WEDGE.md` |
| 13 | Stack-magnet + bakeoff vs naive stars/name | `magnet stack` · `magnet fit` · `magnet bakeoff` exit 0 · pytest green |
| 14 | Adopt+fit receipt + stack-coverage probe | `magnet adopt … --fit` prints fills/dupes · `magnet probe stack-coverage` · tests green |
| 15 | Stack-coverage closed loop + real-stack object + naive install arm | `magnet stack-demo` exit 0 · `magnet probe stack-coverage --stack …` works · tests green |
| 16 | Synonym vocab 1.1 + Grinder-ready receipt JSON | `magnet bakeoff` synonym 3/3 · wine-liar False · `magnet receipt` JSON · tests green |
| 17 | External-object honesty + redact-scan RED control | `extract`→`extract method` · anthropics 7/12 · `magnet redact-scan` RED on plant / GREEN on repo · `magnet external-stack` · foreign-stack.sh |
| 18 | Prediction check on adopt + history | `magnet adopt` prints prediction-held/missed · history shows outcome · tests green |
| 19 | Stack-bind probes + bind-demo vs repo-blind | `magnet bind-demo` · effort-coverage + deny-coverage · FINDING line · tests green |
| 20 | Ultimate Guide closed loop · remaining bind probes · guide-demo · screenshot drift control | `magnet guide-demo` exit 0 · tools/hook/prompt probes · check_docs scans screenshot sidecars · pytest green |
| 21 | Foreign-stack bind probes · open anthropics/superpowers objects · naive complete arm | `magnet foreign-bind` exit 0 · FINDING when foreign effort/deny/tools near 0 · pytest green |
| 22 | Hook control fix + foreign-harden closed loop on stacks we did not build | `magnet foreign-harden` exit 0 · hook-coverage 0/2 when settings.json missing · FINDING title-complete→apply→helped · pytest green |
| 23 | Foreign-hurt embarrassment + foreign hooks-layout honesty | `magnet foreign-hurt` exit 0 · naive helped on a magnet-hurt row · hooks-layout opens hooks/hooks.json · pytest green |
| 24 | Prediction fall-intent for strip titles + foreign-hurt prediction check | `magnet foreign-hurt` prints prediction-held on hurt rows · simplify/relax/remove → fall · pytest green |
| 25 | Prediction magnitude honesty + naive direction arm | `magnet pred-demo` · rises-by-2/5 with +1 → magnet missed / naive held · adopt wires claimed Δ · pytest green |
| 26 | Stay-at absolute level honesty | `magnet pred-demo` stay-at row · must-stay-at 5/5 with measured 4/5 → magnet missed / naive held · pytest green |
| 27 | Linux screenshot render + live sidecars + pred-demo stranger paste | `render-screenshot.py` finds DejaVu · `pred-demo.png` on disk · check-docs 13 PASS · pytest green |
| 28 | Absolute-level honesty without slash + remain/hold/keep + floor | `must stay at 5` @ latest 4 → missed · remain/hold grade · `at least 4/5` floor · `magnet pred-demo` embarrasses · pytest green |
| 29 | Adopt default real week (no fabricated SIMULATED) | bare `magnet adopt` prints no SIMULATED · `--simulate` opt-in · demo exit 0 · pytest green |
| 30 | Vacuous probe RED control + empty-allow hook honesty | empty skills → effort n/a or fail (not 0/0 success) · empty allow alone ≠ hook signal · pytest green |
| 31 | Stale Devpost sidecar refresh + check_docs RED on history/one-workflow | re-derive history.txt + one-workflow.txt (+ PNGs) · check_docs fails if history lacks outcome · pytest green |
| 32 | Rise lexicon recover/restore + one-workflow grades | `pass rate recovers by 1` → rise · held on Δ+1 · `scripts/one-workflow.sh` exit 0 · pytest green |
| 33 | Grinder receipt verify bridge | `magnet receipt --verify` re-probes · GREEN on match · RED on planted drift · pytest green |
| 34 | Grinder evidence export (no invented counts) | `magnet receipt --grinder` writes evidence JSON · no turns_typed invent · check_docs RED without receipt-demo FINDING · pytest green |
| 35 | Negation + ceiling + target-level honesty | `won't fall` → flat (not fall) · `at most 3/5` ceiling · `falls to 2/5` grades latest · `magnet pred-demo` embarrasses · pytest green |
| 36 | Percent-of-pop + exactly-level honesty | `improves by 20%` ≠ absolute 20 · grades Δ vs pop·pct · `exactly 4/5` target · pred-demo FINDING · pytest green |
| 37 | Doubles/halves vs prior honesty | `doubles`/`halves` grade prior=latest−Δ · pred-demo embarrasses direction-only · pytest green |
| 38 | Below-bound floor compounds | `won't fall below 3/5` opens floor · held only when latest≥bound · `stays above`/`never below` · pred-demo FINDING · pytest green |
| 39 | Percent syntax + triples/Nx ratio | `rises 20%` parses pct · triples/3x/2x grade prior · pred-demo FINDING · pytest green |

## NOW

**Slice 39 — Percent syntax + triples/Nx ratio.**

Done when:
1. `claimed_percent("rises 20%")` → 20 (was None — direction invented held on any rise)
2. `rises 20%` + Δ=+1 + pop=5 → held; Δ=+20 + pop=5 → missed
3. `triples` / `3x` / `2x` grade prior (2x ≡ double); pred-demo FINDING
4. pytest green · check-docs PASS

**Oscar gates (not this agent):** film · Devpost paste · submit.

## LOG

- 2026-09-15 · Slice 39 START · ran object: `rises 20%` → percent=None, direction-only held on Δ=+1 and Δ=+20 alike. `triples`/`3x`/`2x` unknown. Building percent-syntax + Nx ratio.
- 2026-09-15 · Slice 38 SHIP · below-bound floor (`won't fall below`) · stays above exclusive · no lower than flat+floor · pred-demo 41/41 embarrassed 17 · `python3 -m pytest -q` → 303 passed · check-docs 16 PASS · `git push origin main` → `d90c9b56c759054f42b6dda97a17cec7d3247b9d`
- 2026-09-15 · Slice 38 START · ran object: `won't fall below 3/5` → floor=None, unchanged@latest=2 → prediction-held — invents held while below the named bound. `stays above`/`never below`/`no lower than` unbound (latter even intent=fall). Building below-bound floor compounds.
- 2026-09-15 · Slice 37 SHIP · doubles/halves vs prior=latest−Δ · pred-demo 36/36 embarrassed 15 · `python3 -m pytest -q` → 295 passed · check-docs 16 PASS · `git push origin main` → `07d2d585130aceb7b2bfd634576c242dc7cecef8`
- 2026-09-15 · Slice 37 START · ran object: `doubles`/`halves` → unknown. Building prior=latest−Δ grade so direction-only cannot invent held on a non-double rise.
- 2026-09-15 · Slice 36 SHIP · percent-of-pop (20%≠absolute 20) · exactly 4/5 target · pred-demo 32/32 embarrassed 13 · `python3 -m pytest -q` → 288 passed · check-docs 16 PASS · `git push origin main` → `81198739841264f00a3e2478bf4bf0bc0a76f9a6`
- 2026-09-15 · Slice 36 START · ran object: `claimed_magnitude("improves by 20%")` → amount=20 (strips `%`); Δ+1/pop5 → missed; Δ+20/pop5 → held — invents that percent means absolute points. `exactly 4/5` → no-direction. Building percent-of-pop grade + exactly target.
- 2026-09-15 · Slice 35 SHIP · won't-fall → flat · ceiling at-most · falls-to/reaches target · improves lexicon · pred-demo 28/28 embarrassed 11 · `python3 -m pytest -q` → 281 passed · check-docs 16 PASS · `git push origin main` → `7495fbadb9d8e5e333007dbc9b701da8ad36033b`
- 2026-09-15 · Slice 35 START · ran objects: `won't fall`+unchanged → missed (intent=fall); `won't fall`+hurt → held — magnet invents that "won't fall" means fall. `at most 3/5` → no-direction. `falls to 2/5`+latest 3 → held on direction alone. Building negation flat + ceiling dual-of-floor + target-level grade.
- 2026-09-14 · Slice 34 SHIP · `magnet receipt --grinder` evidence v1 · no COUNT_FIELDS · check_docs receipt-demo FINDING · pytest green · cold main OK · `git push origin main` → `bfcca63`.
- 2026-09-14 · Slice 34 START · opened Agent Grinder `contract.py`: COUNT_FIELDS require real ints; inventing turns_typed would lie. Building evidence sidecar that carries magnet verify+prediction without fabricating grind counts. `git push origin main` → `37d3014`.
- 2026-09-14 · Slice 33 SHIP · `magnet receipt --verify` re-probes · GREEN match / RED planted · `magnet receipt-demo` FINDING · `--json` alias · `python3 -m pytest -q` green · check-docs PASS.
- 2026-09-14 · Slice 33 START · opened `magnet receipt` JSON — Grinder-ready schema exists but never re-probes. A stale log can print helped forever. Building `--verify` that opens the probe object.
- 2026-09-14 · Slice 32 SHIP · recover/restore/regain/rebound rise · `pass rate recovers by 1` prediction-held on Δ+1 · `scripts/one-workflow.sh` · honest pytest paste N+M · `python3 -m pytest -q` → 255 passed, 1 skipped · check-docs 15 PASS · one-workflow 254/254→253/254→254/254 recovers held.
- 2026-09-14 · Slice 32 START · ran object: `prediction_intent("pass rate recovers by 1")` → `unknown` · adopt → `no-direction` while Δ +1 and claimed amount=1. DEMO-ONE-WORKFLOW.md still says recovers; Slice 31 sidecar papered over with `rises by 1`. Building rise lexicon + live one-workflow script.
- 2026-09-12 · Slice 31 SHIP · history+one-workflow sidecars re-derived with outcome · check_docs RED without outcome · `python3 -m pytest -q` → 246 passed · check-docs 15 PASS · cold clone `/tmp/magnet-cold-s31` @ `1e57c56` 246 passed · check-docs 15 PASS · JUDGE DEMO OK · `git push origin main` → `c697a29`.
- 2026-09-12 · Slice 31 START · opened `docs/screenshots/history.txt` @ f690fd0 — no `outcome`/`claimed Δ` while live `magnet history` prints both. check_docs 13 PASS while blind. Building sidecar refresh + check_docs RED control.
- 2026-09-12 · Slice 30 SHIP · vacuous n/a+exit 1 · empty allow:[] ≠ hook 1/2 · `magnet vacuous-demo` FINDING · `python3 -m pytest -q` → 243 passed · check-docs 13 PASS · cold clone `/tmp/magnet-cold-s30` @ `7da6b5f` 243 passed · vacuous-demo FINDING · effort n/a exit 1 · JUDGE DEMO OK · `git push origin main` → `c00bd87`.
- 2026-09-12 · Slice 30 START · ran objects: effort empty → 0/0 exit 0; hook allow:[] → 1/2. Building vacuous RED + empty-allow honesty.
- 2026-09-12 · Slice 29 SHIP · adopt default real week · `--simulate` opt-in · bare adopt no SIMULATED · `python3 -m pytest -q` → 232 passed · check-docs 13 PASS · cold clone `/tmp/magnet-cold-s29` @ `4504e44` 232 passed · bare adopt no SIMULATED · JUDGE DEMO OK · `git push origin main` → .
- 2026-09-12 · Slice 29 START · ran object: bare `magnet adopt … --demo-bonus --reset` prints `(SIMULATED week)` and future `simulated` stamp. Same-day readings already survive. Flipping default to real week; `--simulate` opt-in; `--no-simulate` kept as no-op for old docs.
- 2026-09-12 · Slice 28 SHIP · stay-at without /pop · remain/hold/keep/unchanged-at · floor `at least` · `magnet pred-demo` 15/15 embarrassed 7 · `python3 -m pytest -q` → 227 passed · check-docs 13 PASS · cold clone `/tmp/magnet-cold-s28` @ `ecc179f` 227 passed · pred-demo FINDING · JUDGE DEMO OK · `git push origin main` → `bc7a58b`.
- 2026-09-12 · Slice 28 START · ran objects: `claimed_level("must stay at 5")` → None → check_prediction held @ latest 4/5 (lie). `remain at 4/5` / `hold at 190/190` → level parsed, intent unknown → no-direction. `unchanged at 5/5` → flat, no level. Building absolute-level honesty pack.
- 2026-09-11 · Slice 27 SHIP · Linux fonts in render-screenshot.py · pred-demo.png + check-docs/pytest PNGs · `python3 -m pytest -q` → 212 passed · check-docs 13 PASS · cold clone `/tmp/magnet-cold-s27` @ `fab2443` 212 passed · pred-demo FINDING · JUDGE DEMO OK · `git push origin main` → `fab2443`.
- 2026-09-11 · Slice 27 START · opened render-screenshot.py — only macOS Menlo paths; PIL missing in base env. Building Linux font candidates + live sidecar refresh + pred-demo stranger paste.
- 2026-09-11 · Slice 26 SHIP · stay-at absolute level · `magnet pred-demo` 10/10 · embarrassed 3 · `python3 -m pytest -q` → 209 passed · check-docs 13 PASS · cold clone `/tmp/magnet-cold-s26` @ `f293b38` 209 passed · pred-demo FINDING · JUDGE DEMO OK · `git push origin main` → `f293b38`.
- 2026-09-11 · Slice 26 START · `claimed_magnitude("must stay at 190/190")` → amount=None. Flat held on unchanged even when latest value ≠ claimed level. Building stay-at absolute check + pred-demo row.
- 2026-09-11 · Slice 25 SHIP · magnitude check · `magnet pred-demo` FINDING · `python3 -m pytest -q` → 206 passed · check-docs 13 PASS · cold clone `/tmp/magnet-cold-s25` @ `8354a7c` 206 passed · pred-demo FINDING · JUDGE DEMO OK · `git push origin main` → `8354a7c`.
- 2026-09-11 · Slice 25 START · ran `check_prediction("pass rate rises by 2/5", "helped", 1)` → prediction-held (lie). Direction-only invents held when claimed fraction is wrong. Building magnitude check + pred-demo embarrassment arm + flat lexicon for "still pass".
- 2026-09-10 · Slice 24 SHIP · fall lexicon simplify/streamline/relax/remove · `foreign-hurt` prediction-held 4/4 · `python3 -m pytest -q` → 190 passed · check-docs 13 PASS · cold clone `/tmp/magnet-cold-s24` @ `54b2f79` JUDGE DEMO OK · `git push origin main` → `54b2f79`.
- 2026-09-10 · Slice 24 START · prediction_intent("simplify skill frontmatter") → unknown (cannot grade hurt). Extending fall lexicon; wire check into foreign-hurt rows.
- 2026-09-10 · Slice 23 SHIP · `magnet foreign-hurt` naive-helped on 4/4 magnet-hurt · `hooks-layout` 3/3 vs UG hook 0/2 · list-probes total 10 · `python3 -m pytest -q` → 189 passed · check-docs 13 PASS · cold clone `/tmp/magnet-cold-s23` @ `f79a14f` JUDGE DEMO OK · `git push origin main` → `f79a14f`.
- 2026-09-10 · Slice 23 START · opened obra/superpowers `hooks/hooks.json` (SessionStart) — UG hook-coverage stays 0/2 correctly but was silent that hooks exist. Building foreign-hurt (naive helped on magnet hurt) + hooks-layout probe.
- 2026-09-10 · Slice 22 SHIP · hook control fix (empty dir 0/2) · `magnet foreign-harden` findings 2/2 offline · anthropics effort 0/19→19/19 · `python3 -m pytest -q` → 183 passed · check-docs 13 PASS · cold clone `/tmp/magnet-cold-s22` @ `643cbed` JUDGE DEMO OK · `git push origin main` → `643cbed`.
- 2026-09-10 · Slice 22 START · opened anthropics/skills + obra/superpowers + live agentgrinder: hook-coverage scored 1/2 with NO settings.json (empty allow invented "hardened"). guide-demo --stack foreign already moves 4/5 but never prints the before-lie. Building foreign-harden + hook control fix.
- 2026-09-08 · Slice 21 SHIP · `magnet foreign-bind` findings 2/2 offline · anthropics effort 0/19 tools 0/19 · superpowers 0/14 · naive_title=complete · cold clone `/tmp/magnet-cold-s21` JUDGE DEMO OK @ 1281155 · `git push origin main` → `ec3a084`.
- 2026-09-08 · Slice 21 START · open anthropics/skills + obra/superpowers objects for bind probes; fixture Agent Grinder as offline arm.
- 2026-09-08 · Slice 20 SHIP · `magnet guide-demo` moved=5/5 · tools/hook/prompt probes · check_docs scans screenshots (113 RED→PASS) · bakeoff surface 1/2 FINDING · list-probes total 9 · `python3 -m pytest -q` → 169 passed · check-docs 13 PASS · cold clone `/tmp/magnet-cold-s20` JUDGE DEMO OK @ 68991cc · `git push origin main` → `dabe8c7`.
- 2026-09-08 · Slice 20 START · opened Ultimate Guide object: items 3–5 still cannot-measure; screenshot sidecars still claim 113 (control gap); bakeoff surface 1/2 is helicon cross-surface dupe on reviewer-agent↔critique — will FINDING, not rewrite.
- 2026-09-07 · Slice 19 SHIP · `magnet bind-demo` FINDING · effort 0→7/7 · deny 0→4/4 · check-docs flat · list-probes total 6 · `python3 -m pytest -q` → 159 passed. · cold clone `/tmp/magnet-cold-s19` 159 passed · bind-demo FINDING · JUDGE DEMO OK @ 03d289a · `git push origin main` → `d902156` · tip `0df0ba7`.
- 2026-09-07 · Slice 19 START · open Ultimate Guide defect object: repo probes cannot see hook/setting/frontmatter; bind probes must open the stack.
- 2026-09-07 · Slice 18 SHIP · `magnet/prediction.py` · adopt prints prediction-held/missed · history shows outcome · `python3 -m pytest -q` → 148 passed · check-docs 11 PASS · pytest-pass-rate 147/147 · cold clone `/tmp/magnet-cold-s18` 148 passed · JUDGE DEMO OK @ 655014d.
- 2026-09-07 · Slice 18 START · port prediction intent/check from helicon S3 spirit; wire adopt + history.
- 2026-09-07 · Slice 17 SHIP · `extract`→`extract method` · anthropics 8/12→7/12 · `magnet redact-scan` GREEN · planted RED · `magnet external-stack` · foreign-stack.sh · Grinder real 1/12 · superpowers 6/12 · `python3 -m pytest -q` → 139 passed · check-docs 11 PASS · surface 1/2 left (helicon science) · cold clone `/tmp/magnet-cold-s17` JUDGE DEMO OK.
- 2026-09-07 · Slice 17 FAIL then FIX · redact-scan went RED on `tests/test_external_and_redact.py` itself (literal api_key assign in source). Assembled plant at runtime.
- 2026-09-07 · Slice 17 START · opened real objects: Agent Grinder 1/12 (matches fixture) · anthropics/skills 8/12 with bare `extract` · obra/superpowers 6/12 · helicon source confirms cross-surface dupe penalty — surface 1/2 not rewritten.
- 2026-09-07 · Slice 16 START · synonym vocab experiment at bakeoff object: tight expansion → recall 0.5→0.875, synonym 3/3, wine-liar False, fixture still 8/12.
- 2026-09-07 · Slice 16 SHIP · TAG_VOCAB 1.1 · `magnet receipt` JSON · `python3 -m pytest -q` → 130 passed · check-docs 11 PASS · judge-demo OK.
- 2026-09-07 · Slice 15 START · ran objects: `magnet probe stack-coverage --stack <path>` → argparse exit 2 (receipt lied) · `magnet adopt … --probe stack-coverage --fit` → fit fills-gap + verdict unchanged 8/12 (skill never installed) · real `Morkeeth/agentgrinder` stack → 1/12 (writing only).
- 2026-09-07 · Slice 15 SHIP · `magnet stack-demo` exit 0 · gap 8→9/12 helped · dupe/noise magnet unchanged vs naive helped · `magnet probe --stack` exit 0 · cold clone branch `/tmp/magnet-cold-s15` → 123 passed · check-docs 11 PASS.
- 2026-08-29 · Repo created · cloud ambitious lane launched.
- 2026-08-29 · `fleet-ops/plans/agents-for-humans-hack.md` not accessible (404) · reporter science from `helicon/measure.py` (mountain-of-helicon).
- 2026-08-29 · Merged scaffold from `cursor/magnet-adoption-ledger-080a` into main worktree.
- 2026-08-29 · Demo enhanced: 1-reading embarrassing case (naive `helped` vs magnet `baseline`) · `python3 -m pytest -q` → 17 passed · `magnet demo` → exit 0.
- 2026-08-29 · `test_check_docs_drift.py` added · drift on fake `99 tools` claim exits 1.
- 2026-08-29 · Strands Bedrock agent loop not run — no AWS credentials in cloud VM.
- 2026-08-29 · `git push origin main` → `e798729` · GitHub cold clone `/tmp/magnet-github-cold` → `magnet demo` exit 0 · `pytest -q` → 17 passed.
- 2026-08-30 · Slice 5: `magnet/eval.py` (naive 3/5, magnet 5/5, silent_null 1/5) · `magnet/agent_run.py` (4-tool chain no Bedrock) · check_docs re-derives pytest count from `tests/test_*.py` · `python3 -m pytest -q` → 26 passed · `python3 -m magnet.cli eval` → exit 0 · `python3 -m magnet.cli agent-run` → exit 0 · `python3 -m magnet.cli check-docs` → exit 0 (after doc counts updated).
- 2026-08-30 · `git push origin main` → `f74799d` · GitHub cold clone `/tmp/magnet-cold-post` → 26 passed · demo/eval/agent-run/check-docs exit 0.
- 2026-09-01 · Slice 6-7 shipped · `git push origin main` → `2d38525` · cold clone `/tmp/magnet-cold-final` → 61 passed · `bash scripts/stranger-pass.sh` → exit 0 · `magnet demo` → helped receipt.
- 2026-09-02 · Slice 8: Devpost pack (EYES ruling: MAGNET submits, Grinder product) · `bash scripts/stranger-pass.sh` → OK · docs/DEVPOST-READY, FILM-SCOUT, OSCAR-CLICK-LIST, BUILDER-AWS-DRAFT, MOONSHOT-MEMO · architecture AWS section.
- 2026-09-02 · Slice 9: Judge path · `bash scripts/judge-demo.sh` → JUDGE DEMO OK · JUDGE-SCORECARD (4.0/5 honest) · DEVPOST-DESCRIPTION paste · BEDROCK-JUDGE-GUIDE · pushed main.
- 2026-09-02 · **Live Bedrock (local)** · `magnet agent-run --model bedrock` exit 0 · 5 tools dispatched · `docs/BEDROCK-LIVE-RECEIPT-2026-09-02.md` · Technical 5/5.
- 2026-09-02 · Slice 10: Cloud VM · `bash scripts/judge-demo.sh` → JUDGE DEMO OK · `python3 -m pytest -q` → 63 passed · STS → `NoCredentialsError` · cloud Bedrock BLOCKED.
- 2026-09-02 · Slice 10 fix: `judge-demo.sh` PATH (`~/.local/bin`) — cold clone was failing `magnet: command not found` · `tests/test_judge_demo.py` (2 tests) · cold clone `/tmp/magnet-cold-judge-post-push` → JUDGE DEMO OK.
- 2026-09-02 · Slice 11 fix: pytest-pass-rate excludes `@pytest.mark.slow` · cold-clone test uses `MAGNET_JUDGE_QUICK` · fixes 300s timeout on GitHub cold clone.
- 2026-09-02 · Slice 11 verified: CI green (run 33575676849) · `bash scripts/judge-demo.sh` → JUDGE DEMO OK · `python3 -m pytest -q` → 69 passed.
- 2026-09-02 · Slice 12: check_docs scans 6 judge/devpost docs · found 63→69 drift in 4 files · `magnet drift-demo` · CI cold-clone step · `docs/FUNDABLE-WEDGE.md` · `python3 -m pytest -q` → 73 passed · `magnet check-docs` → 11 claims PASS · `magnet drift-demo` → fake exit 1, real exit 0.
- 2026-09-02 · CI FAIL run 33610787132: `test_log.py` banned word `ledger` in FUNDABLE-WEDGE.md · fixed · `git push origin main` → `024d611`.
- 2026-09-02 · Slice 13 START · opened real object `Morkeeth/mountain-of-helicon` `helicon/magnet.py` (previously cited measurement-bench 404) · EXP-MAGNET-01: name-tiebreak invented 0.875 recall; synonym arm fails; claims must not buy score.
- 2026-09-02 · Slice 13 FAIL then FIX · first `magnet bakeoff` → magnet recall 0.0 (planning/design uncovered; noise "plan a wedding" / "colour palette" filled top-20) · covered those caps on fixtures/stack · `reproduce` stemmed to debug `repro` — rewritten · re-run: magnet 0.5 recall p@3=1.0 noise=0; naive_stars 0.375 with dupes+liar; synonym primary 0/3 claims 3/3 · `python3 -m pytest -q` → 90 passed · check-docs 11 PASS.
- 2026-09-02 · Slice 13 cold clone `/tmp/magnet-cold-s13` (branch) → demo/stack/bakeoff/pytest exit 0 · push `8027d79`.
- 2026-09-02 · Slice 14: `magnet adopt --fit` · `stack-coverage` probe 8/12 · judge-demo step extended · `python3 -m pytest -q` → 98 passed · check-docs 11 PASS.
- 2026-09-02 · **DEFECT found by running:** `tool_adopt_change` applied demo +1/5 whenever probe was `demo-pass-rate`, ignoring `apply_demo_bonus=False` — wine-pairing noise got `helped` while fit said `no-signal`. Fixed: bonus is opt-in only; scripted agent plan passes `apply_demo_bonus=True` explicitly · `python3 -m pytest -q` → 100 passed.
