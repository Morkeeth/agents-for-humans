# Screenshots · live sidecars re-derived 2026-09-05 (Slice 17)

Every live `.txt` below is produced by `bash scripts/capture-sidecars.sh` (command,
UTC stamp, branch, sha, interpreter on the header; `# exit=N` on the footer).
PNGs that exist were rendered from an earlier take by `scripts/render-screenshot.py`.

| Devpost slot | file | note |
|---|---|---|
| 1 required | `one-workflow.png` / `.txt` | **Dated film take** @ f690fd0 (112 tests). Not refreshed by capture-sidecars — re-film before submit if the suite moved. |
| 2 required | `agent-run.png` / `.txt` | Dated film take — re-capture before submit if the agent loop output changed. |
| 3 required | `eval.png` / `.txt` | Dated film take — scenario scores are stable; still re-derive before submit. |
| optional | `demo.png` / `.txt` | Dated film take. |
| optional | `history.png` / `.txt` | Dated film take. |

Live sidecars (gated by `magnet check-docs`):

| file | what |
|---|---|
| `pytest.txt` | Full suite — must match `def test_` count |
| `check-docs.txt` | Must include `sep14 entry ruling`; must not say `113` / `11 claims` |
| `drift-demo.txt` | Fake FAIL + this-repo PASS |
| `probe-pytest-pass-rate.txt` | `not slow` fraction |
| `list-probes.txt` | Built-in catalogue |
| `apply-eval.txt` | naive_fit vs magnet vs silent_null |
| `apply-demo.txt` | fit invents helped; --apply measures coverage |

```bash
bash scripts/capture-sidecars.sh
magnet check-docs   # must exit 0 — scans pytest.txt + check-docs.txt freshness
```

Numbers in this README are not authoritative — re-derive at the object.
