# Screenshots · captured 2026-09-03 13:57 to 13:58 CEST on main @ f690fd0

Every `.png` is rendered from the `.txt` beside it by `scripts/render-screenshot.py` (Menlo 30 px on a dark ground, nothing edited). Each per-command `.txt` opens with the command that produced it and the time, branch and interpreter it ran under, and closes with `# exit=N`; `one-workflow.txt` closes with the wall clock and the three SQLite rows instead. Re-derive any of them: run the first line of the `.txt`, then `python3 scripts/render-screenshot.py <txt> <png>`.

| Devpost slot | file | caption |
|---|---|---|
| 1 required | `one-workflow.png` | Change one prompt, MAGNET re-runs your eval: 112/112 baseline, 111/112 hurt (-1), 112/112 helped (+1), 21 s wall clock, nothing simulated |
| 2 required | `agent-run.png` | Real Strands Agents SDK: 12 agent turns, 5 tools dispatched by the event loop, local scripted model, mode printed on screen |
| 3 required | `eval.png` | Scored against ground truth on 5 scenarios: naive 3/5, magnet 5/5, silent_null 1/5 |
| optional | `demo.png` | MAGNET refuses to trend on one reading (naive `helped` vs magnet `baseline`); week 2 labelled SIMULATED |
| optional | `history.png` | Adoption log after `magnet agent-run` |

Sidecars without a PNG: `list-probes.txt`, `check-docs.txt` (11 claims, all match), `drift-demo.txt` (fake repo 2 drifts exit 1, this repo 0 drifts exit 0), `probe-pytest-pass-rate.txt` (112/112; one test marked `slow` is deselected by the probe command), `pytest.txt` (113 passed, full suite, `python3 -m pytest -q`).

Companion text: `docs/DEVPOST-DESCRIPTION.md` (paste-ready, same numbers), `docs/VIDEO-SHOTLIST.md` (what to record, in what order), `docs/DEMO-ONE-WORKFLOW.md` (the six commands with the pasted output of an earlier run; the counts there are from 2 Sep and are superseded by `one-workflow.txt`).
