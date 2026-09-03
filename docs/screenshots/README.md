# Screenshots · captured 2026-09-03 00:27 CEST on fable/devpost-pack-2026-09-03 @ b3af7a1

Every `.png` is rendered from the `.txt` beside it by `scripts/render-screenshot.py` (Menlo 30 px on a dark ground, nothing edited). Each `.txt` opens with the command that produced it and the time, branch and interpreter it ran under. Re-derive any of them: run the first line of the `.txt`, then `python3 scripts/render-screenshot.py <txt> <png>`.

| Devpost slot | file | caption |
|---|---|---|
| 1 required | `demo.png` | MAGNET refuses to trend on one reading (naive `helped` vs magnet `baseline`) |
| 2 required | `eval.png` | We ship the baseline arm that embarrasses us (naive 3/5 · magnet 5/5 · silent_null 1/5) |
| 3 required | `agent-run.png` | Real Strands Agents SDK — 5 tools dispatched by the event loop, SQLite log |
| what to demonstrate | `one-workflow.png` | Change one prompt → MAGNET re-runs your eval → 85/85 → 84/85 hurt → 85/85 helped, 24 s |
| optional | `history.png` | Adoption log |

Sidecars without a PNG: `list-probes.txt`, `check-docs.txt` (11 claims, all match), `drift-demo.txt`, `probe-pytest-pass-rate.txt` (85/85), `pytest.txt` (86 passed).

Not done in this pass (close-down 02:4x): DEVPOST-READY.md and DEVPOST-DESCRIPTION.md still carry their pre-existing prose; their test counts already re-derive (`magnet check-docs` passes) but "What to demonstrate" still lists five commands instead of the one workflow, and the Strands proof section does not yet cite `magnet/tools.py:174-183` (`from strands import Agent` / `Agent(tools=…)`), `magnet/agent_run.py:131-132` (`create_agent` → `agent(AGENT_TASK)`), or `docs/BEDROCK-LIVE-RECEIPT-2026-09-02.md`. No bakeoff figures exist on this branch; they live on `cursor/stack-magnet-bakeoff-5608`.
