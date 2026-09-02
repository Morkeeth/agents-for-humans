# CLOUD-RECEIPT · magnet-win-judges · 2026-09-02 (night 2)

---

## SHIPPED

- **`scripts/judge-demo.sh` PATH fix** — `export PATH="${HOME}/.local/bin:${PATH}"` after pip install (was failing cold clone with `magnet: command not found`)
- **`tests/test_judge_demo.py`** — structural + quick-mode integration (2 tests)
- **`_NIGHT-SCOPE.md`** + **`_HACK-CONTRACT.md`** — scope and contract summaries
- Doc counts re-derived: **73 pytest** (was 61, drift caught by `magnet check-docs`)
- `MAGNET_JUDGE_QUICK` mode for pytest-safe nested runs (no recursion)

Prior night artifacts (already on main): JUDGE-SCORECARD, DEVPOST-DESCRIPTION, BEDROCK-JUDGE-GUIDE, SCREENSHOTS, FILM-SCOUT, README For Judges.

---

## VERIFIED

```bash
python3 -m pytest -q                    # → 73 passed
bash scripts/judge-demo.sh              # → JUDGE DEMO OK
bash scripts/stranger-pass.sh           # → stranger pass OK
magnet check-docs                       # → 7 claims, all match
```

Cold clone (post-push):

```bash
git clone https://github.com/Morkeeth/agents-for-humans.git /tmp/magnet-cold-judge-post-push
cd /tmp/magnet-cold-judge-post-push && bash scripts/judge-demo.sh  # → JUDGE DEMO OK
```

---

## WRONG

1. **Prior push claimed judge-demo worked on cold clone — it did not.** PATH bug found by running `bash scripts/judge-demo.sh` in cloud VM (exit 127). Fixed tonight; post-push cold clone required to verify.
2. **Bedrock demonstrated locally by Oscar** — see `docs/BEDROCK-LIVE-RECEIPT-2026-09-02.md`; **not re-run in this cloud agent** (no AWS creds).
3. **Presentation 3/5** — Oscar must film 5-min video from FILM-SCOUT.
4. **AgentCore not deployed** — prep doc only.
5. **Scorecard avg 4.2/5** — not 5.0; Presentation gap until video.

---

## Path to winning score

| Action | Criterion lift |
|--------|----------------|
| Film `judge-demo.sh` + FILM-SCOUT | Presentation → 5 |
| Paste DEVPOST-DESCRIPTION | Presentation |
| Optional Bedrock on camera | Technical → 5 |
| builder.aws publish | +0.6 bonus |
