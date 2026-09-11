# Screenshots · re-captured 2026-09-11 on main (Slice 27)

Every `.png` is rendered from the `.txt` beside it by `scripts/render-screenshot.py`
(DejaVu Sans Mono / Menlo 28 px on a dark ground, nothing edited). Linux font
candidates were added so cloud hosts can re-render without macOS Menlo.
Each per-command `.txt` opens with the command and the time/branch, and closes
with `# exit=N`. Re-derive: run the first line of the `.txt`, then
`pip install -e ".[screenshots]" && python3 scripts/render-screenshot.py <txt> <png>`.

| Devpost slot | file | caption |
|---|---|---|
| 1 required | `one-workflow.png` | Change one prompt, MAGNET re-runs your eval (historical capture — counts in sidecar are from that run) |
| 2 required | `agent-run.png` | Real Strands Agents SDK: agent turns + tools dispatched, local scripted model, mode printed |
| 3 required | `eval.png` | Scored against ground truth on 5 scenarios: naive 3/5, magnet 5/5, silent_null 1/5 |
| optional | `demo.png` | MAGNET refuses to trend on one reading (naive `helped` vs magnet `baseline`); week 2 labelled SIMULATED |
| optional | `history.png` | Adoption log after `magnet agent-run` |
| optional | `pred-demo.png` | Magnitude + stay-at honesty: naive invents held on wrong claim; magnet misses |
| optional | `check-docs.png` | Doc drift gate — 13 claims match source |
| optional | `pytest.png` | Full suite green (re-derive count with `python3 -m pytest -q`) |

Other sidecars: `list-probes.txt`, `drift-demo.txt` (fake repo drifts exit 1 — intentional),
`probe-pytest-pass-rate.txt` (slow test deselected by `-m "not slow"` — re-derive with
`magnet probe pytest-pass-rate`).

Companion text: `docs/DEVPOST-DESCRIPTION.md`, `docs/VIDEO-SHOTLIST.md`, `docs/DEMO-ONE-WORKFLOW.md`.
