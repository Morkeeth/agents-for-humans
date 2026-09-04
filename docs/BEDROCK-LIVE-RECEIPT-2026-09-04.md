# Bedrock live receipt · 2026-09-04

**Environment:** Cursor cloud agent VM (`cursor` hostname)  
**Repo head at probe:** `63830a3e201c14cda258982ea5264e18aa6ce584` (main tip when probe started)  
**Stamp:** 2026-09-03T23:50:49Z → 2026-09-04 receipt written after judge/stranger paths  
**Verdict: BLOCKED** — no AWS credentials in this environment. No live Bedrock output claimed.

---

## CLOUD VM · BLOCKED (this run)

Attempted the live path. It failed at the credential object, not at a proxy.

### Exact missing pieces

| Check | Command / control | Result |
|-------|-------------------|--------|
| `AWS_ACCESS_KEY_ID` | positive non-empty env | **MISSING** |
| `AWS_SECRET_ACCESS_KEY` | positive non-empty env | **MISSING** |
| `AWS_REGION` / `AWS_DEFAULT_REGION` | positive non-empty env | **MISSING** |
| `~/.aws/credentials` | file exists | **ABSENT** |
| Web identity token | `AWS_WEB_IDENTITY_TOKEN_FILE` + file | **ABSENT** |
| Container credentials URI | env present | **ABSENT** |
| EC2 IMDS instance profile | `curl -m 2 http://169.254.169.254/.../security-credentials/` | **ABSENT** (curl exit 28 timeout) |

### STS at the object

```bash
python3 -c "import boto3; print(boto3.client('sts').get_caller_identity())"
```

```
boto3 1.43.88
NoCredentialsError: Unable to locate credentials
sts_exit=2
```

botocore `Session().get_credentials()` → `None`.

### Live Bedrock attempt (not skipped)

```bash
python3 -m magnet.cli agent-run --model bedrock
```

**Before tonight's fix:** printed `DEGRADED` + **exit 0** (control read green).  
**After fix (this commit):** same banner, **exit 1**.

```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! STRANDS AGENT MODE 'bedrock' FAILED — FALLING BACK TO THE DETERMINISTIC CHAIN
!! NoCredentialsError: Unable to locate credentials
!! The result below did NOT come from an agent loop. It is DEGRADED.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
...
  status     DEGRADED (agent mode failed; see banner above)
bedrock_cli_exit=1
```

**NOT claimed:** `MODE: strands agent loop · Amazon Bedrock` with real tool choice.

### One-command probe (positive-evidence controls)

```bash
bash scripts/bedrock-live-or-blocked.sh
# → exit 2 · VERDICT: BLOCKED · exact_missing: AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_REGION
```

This script refuses the empty-input trap (`printf '' | grep -qv AWS_` exits 1 and looks like a hit). Every credential check requires positive presence.

### Model ID re-derived (not carried)

```bash
python3 -c "import importlib.metadata as m; from strands.models.bedrock import DEFAULT_BEDROCK_MODEL_ID; print(m.version('strands-agents'), DEFAULT_BEDROCK_MODEL_ID)"
```

```
strands-agents= 1.54.0
DEFAULT_BEDROCK_MODEL_ID= global.anthropic.claude-sonnet-4-6
```

(OPEN in `hack.md`: whether Oscar pins a different model id — not resolved here.)

---

## Judge-demo / stranger path (no keys)

Logged on this same VM after the Bedrock BLOCKED verdict.

| Path | Command | Exit | Tail signal |
|------|---------|------|-------------|
| Judge demo | `bash scripts/judge-demo.sh` | **0** | `JUDGE DEMO OK` |
| Stranger pass | `bash scripts/stranger-pass.sh` | **0** | `== stranger pass OK ==` |
| Full suite | `python3 -m pytest -q` | **0** | `119 passed` |
| Doc drift | `python3 -m magnet.cli check-docs` | **0** | `11 claims checked. All match source.` |
| Bedrock probe | `bash scripts/bedrock-live-or-blocked.sh` | **2** | `VERDICT: BLOCKED` |

Judge demo also printed (re-derived this run, not carried):

- `pytest-pass-rate` adopt reading `118/118` (`-m "not slow"`)
- bakeoff: magnet recall `0.5` p@3=`1.0` noise=`0` · naive_stars `0.375` with dupes+liar · silent_null `0.0`
- stack-coverage `8/12`
- eval arms: magnet `5/5`, naive `3/5`, silent_null `1/5`

### Stranger / judge cold path (no AWS)

```bash
git clone https://github.com/Morkeeth/agents-for-humans.git
cd agents-for-humans
pip install -e ".[dev]"
bash scripts/judge-demo.sh      # must print JUDGE DEMO OK
bash scripts/stranger-pass.sh   # must print stranger pass OK
```

Bedrock is optional and separate:

```bash
bash scripts/bedrock-live-or-blocked.sh
# exit 0 = LIVE · exit 2 = BLOCKED with exact missing env · exit 1 = control failure
```

---

## LOCAL · prior LIVE (not re-run here)

Oscar local machine 2026-09-02: `magnet agent-run --model bedrock` exit 0, 5 tools via Strands event loop. Full capture: `docs/BEDROCK-LIVE-RECEIPT-2026-09-02.md`. **This cloud VM cannot re-verify that run** — no credentials.

---

## To unblock cloud LIVE

1. Add Cursor cloud secrets (or `~/.aws/credentials` / IAM role):
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION` (e.g. `us-east-1`)
2. Enable Bedrock model access for the account/region (SDK default above, unless Oscar pins another id).
3. Re-run:
   ```bash
   python3 -c "import boto3; print(boto3.client('sts').get_caller_identity()['Account'])"
   magnet agent-run --model bedrock
   bash scripts/bedrock-live-or-blocked.sh   # must print VERDICT: LIVE · exit 0
   ```
4. Replace this receipt's CLOUD section with the LIVE capture (MODE line + tools dispatched + exit 0). Do not edit the BLOCKED section away — append.

**Spend:** AWS Bedrock tokens cost money. Constitution: no spend beyond free tier without Oscar click. This run spent **$0** (never reached Bedrock).

---

## SHIPPED this session (beyond the receipt)

1. **`cmd_agent_run` exits 1 on `DEGRADED`** — found by running bedrock with no creds (was exit 0).
2. **`scripts/bedrock-live-or-blocked.sh`** — positive-evidence preflight; exit 2 BLOCKED / 0 LIVE / 1 control failure.
3. **Tests:** `test_cli_bedrock_degraded_exits_nonzero`, `test_cli_local_agent_run_still_exits_zero`, `tests/test_bedrock_preflight.py` (4) · suite **119** `def test_` (was 113).

---

## WRONG

1. **Cloud still cannot produce live Bedrock output** — BLOCKED is honest, not a win.
2. **Exit-0-on-DEGRADED lived until tonight** — shouted in the banner since 2026-09-02 but the process exit lied green; found only by running, not by reading.
3. **Prior cloud receipt (2026-09-02) skipped `magnet agent-run --model bedrock` entirely** — said it "would fail"; running it tonight was what exposed the exit-code defect.
4. **Bedrock model ID still OPEN** in `hack.md` (Oscar click) — we re-derived the SDK default only.
5. **Screenshot sidecars under `docs/screenshots/` still print 113** — not in `check_docs` scan list; left stale rather than silently rewriting film artifacts. Judge-scanned docs are 119.
6. **No Devpost submit, no film, no builder.aws publish** — Oscar click only (constitution).
7. **Preflight log append on re-run** — first `bedrock-live-or-blocked.sh` left `/tmp/magnet-bedrock-probe/sts.txt`; second run used `>>` and double-printed STS/model lines. Truncate fixed in follow-up commit. Verdict was still correct (exit 2).

---

## Scorecard impact

Technical Implementation stays grounded on: real Strands local loop (judge-demo step 3) + prior local Bedrock LIVE receipt + tonight's honest cloud BLOCKED + fixed DEGRADED exit. Do not claim cloud Bedrock ran.
