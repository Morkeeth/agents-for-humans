# Video shot list · MAGNET · 2 min 50 s

One workflow on screen, then the Strands loop, then the drift gate. Every number below was produced on 2026-09-03 on `main` @ f690fd0; the transcript is `docs/screenshots/one-workflow.txt`. Devpost allows 5 minutes; this list uses 2:50 so nothing is rushed.

The judging criteria this list serves, quoted from the Devpost rules: "Does the video clearly demonstrate the project working end-to-end? Does the pitch communicate what problem is solved, who it's for, and why it matters?" and "How thoroughly and skillfully does the project use Strands Agents?"

## Before recording (2 minutes, once)

```bash
cd ~/CODE/agents-for-humans
git status --short          # must be empty (stash hack.md if it is dirty)
git rev-parse --short HEAD  # say this hash if you want; f690fd0 or later
rm -f .magnet/demo-one.db   # clean log so the first reading is reading 1
python3 -m magnet.cli probe pytest-pass-rate   # warms the pytest cache; expect 112/112
clear
```

- Terminal: dark background, monospaced font 18 pt or larger, window about 110 columns wide so the `latest` line does not wrap.
- Define the alias once, off camera, so each command is short on screen: `M="python3 -m magnet.cli --log .magnet/demo-one.db"`.
- Each pytest run takes about 7 s. Do not cut it; say the line while it runs.
- Do not show `magnet demo` (it uses a labelled simulated week). Do not say a percentage. The numbers to say are `112 of 112`, `111 of 112`, `112 of 112`.

## Shots

| # | Time | On screen | Command | Say |
|---|---|---|---|---|
| 1 | 0:00 to 0:15 | Empty terminal, repo root | (none) | "You change a prompt, a model, or a skill in your agent stack, and the eval number that would tell you what it did scrolls away. MAGNET keeps that number, with the command that made it, next to what you predicted." |
| 2 | 0:15 to 0:35 | `magnet eval` table | `python3 -m magnet.cli eval` | "The usual rule is: score went up, so it helped. Scored against ground truth on five scenarios, that rule is wrong on 2 of 5. MAGNET gets 5 of 5. The do-nothing arm gets 1 of 5. We ship all three arms." |
| 3 | 0:35 to 0:50 | one line: `recorded pytest-pass-rate: verdict=baseline readings=1` | `$M record pytest-pass-rate` | "My eval is this repo's test suite. Baseline first: 112 of 112. One reading, so MAGNET says baseline. It will not call a trend from one number." |
| 4 | 0:50 to 1:05 | the diff, two lines | `sed -i '' 's/ — never invent a trend from one reading//' magnet/tools.py` then `git diff magnet/tools.py` | "The change: I drop one rule from MAGNET's own system prompt, the line that says never invent a trend from one reading." |
| 5 | 1:05 to 1:25 | the adopt receipt with `latest 111/112` and `verdict hurt` | `$M adopt prompt 'drop the never-invent rule from SYSTEM_PROMPT' 'pass rate unchanged' --probe pytest-pass-rate --no-simulate` | Say before pressing enter: "I predict unchanged." While pytest runs: "MAGNET re-runs the suite." When the receipt prints: "111 of 112. Hurt, minus 1 versus prior. My prediction was wrong, and the log keeps both." |
| 6 | 1:25 to 1:45 | the second receipt with `latest 112/112` and `verdict helped` | `git checkout -- magnet/tools.py` then `$M adopt prompt 'restore the never-invent rule' 'pass rate recovers by 1' --probe pytest-pass-rate --no-simulate` | "Put the rule back. Prediction: recovers by 1. 112 of 112. Helped, plus 1. Every reading shows the command that produced it and the population it is out of." |
| 7 | 1:45 to 2:00 | `magnet history`, two rows | `$M history` | "The log. Row 1: predicted unchanged, got hurt. Row 2: predicted plus 1, got helped. This is what a team lead pastes when asked why a prompt changed." |
| 8 | 2:00 to 2:25 | `MODE:` line, `agent turns 12`, `tools dispatched 5`, the five tool names | `python3 -m magnet.cli agent-run` | "The same four tools run under a real Strands Agent. The SDK builds the tool specs from the decorators, dispatches five calls, and feeds the results back. This mode uses a local scripted model: no keys, no spend, and it says so on screen." |
| 9 | 2:25 to 2:40 | the Bedrock receipt, top 30 lines | `head -30 docs/BEDROCK-LIVE-RECEIPT-2026-09-02.md` | "With AWS credentials the same loop runs on Amazon Bedrock and the model chooses the tools. We ran it once, 2 September, exit 0, five tools dispatched. The receipt is in the repo, including the one parse warning it logged." |
| 10 | 2:40 to 2:50 | `11 claims checked. All match source.` | `python3 -m magnet.cli check-docs` | "Last, the drift gate: every number the docs claim is re-derived from source, 11 claims, and the build fails when one drifts. MAGNET. github.com/Morkeeth/agents-for-humans. MIT." |

Optional shot 9b, only if AWS credentials are on the machine and spend is acceptable: replace shot 9 with a live `python3 -m magnet.cli agent-run --model bedrock` (about 15 s, costs money). If it fails, keep shot 9 as written; never imply Bedrock ran when it did not.

## What must be visible in the frame

- Shot 5 and 6: the `latest` line with the population (`111/112`), the `verdict` line, and the `repro` line. These three lines are the product.
- Shot 8: the `MODE:` line at the top. It is the honesty claim for the Strands criterion.
- Shot 10: the exit line. Say "exit 0" only if the terminal shows it (`echo $?`).

## Voiceover, optional and free

A local text-to-speech tool exists at `~/CODE/voice-generation` (Kokoro-82M, runs on CPU, no key, nothing leaves the machine). It is the checked option before any paid service. To render the say-lines above as one track:

1. Save the say-lines as a script file, one spoken line per line. Format from that repo's README: directives such as `@voice bm_george`, `@lang b`, `@speed 1.0`, `@pause 400` at the top; a blank line adds one pause.
2. Render:

```bash
cd ~/CODE/voice-generation
./kvenv/bin/python vo.py /path/to/magnet-vo.txt -o renders/magnet-vo.mp3 --preset demo
```

The `demo` preset is tuned to sit under a screen capture. Recording your own voice over the live terminal is the simpler path and reads as more real; the tool is there if a second take is faster to type than to say.

## Ready state

- Commands: run today, exit 0, transcript in `docs/screenshots/one-workflow.txt`, still frames in `docs/screenshots/one-workflow.png`, `agent-run.png`, `eval.png`, `history.png`.
- Paste text for the Devpost form: `docs/DEVPOST-DESCRIPTION.md`.
- Architecture diagram (required by the rules): `docs/architecture.md`.
