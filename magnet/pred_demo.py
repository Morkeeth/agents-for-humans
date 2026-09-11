"""pred-demo — prove prediction stems at the object (Slice 25).

Defect found by running, not reading:
  prediction_intent("pass rate improves") → unknown   (stem improv + \\b)
  prediction_intent("clean up frontmatter") → rise    (bare \\bup\\b)
  magnet adopt … "pass rate improves by 1" --demo-bonus → no-direction
    while the verdict was helped.

This demo re-derives intents, runs one adopt with "improves", and one
foreign-hurt marketing pass — cold path, no keys, no network.
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

from magnet.adopt import run_adopt
from magnet.foreign_hurt import hurt_one
from magnet.prediction import check_prediction, prediction_intent


# Cases re-derived every run — never carry a prior intent.
_STEM_CASES = (
    ("pass rate improves", "rise"),
    ("coverage increases", "rise"),
    ("coverage decreases", "fall"),
    ("pass rate rises by 1/5", "rise"),
    ("simplify skill frontmatter", "fall"),
    ("clean up frontmatter", "unknown"),  # bare "up" must NOT invent rise
    ("set up hooks", "unknown"),
    ("improve PreToolUse hooks", "rise"),
    ("optimize skill frontmatter", "unknown"),  # marketing speak — no direction
)


def run_pred_demo(*, repo_root: str | None = None) -> str:
    root = Path(repo_root or os.getcwd()).resolve()
    lines = [
        "MAGNET pred-demo — prediction stems + marketing embarrassment at the object",
        "",
        "  Defect (pre-fix, re-derived by running):",
        "    improves / increases / decreases → unknown (broken stems)",
        "    clean up / set up → rise (false \\bup\\b)",
        "    adopt 'pass rate improves' → no-direction while verdict=helped",
        "",
        "  === stem table (re-derived now) ===",
        "  intent    expected  ok   text",
        "  --------  --------  ---  ----",
    ]
    stem_ok = 0
    for text, expected in _STEM_CASES:
        got = prediction_intent(text)
        ok = got == expected
        if ok:
            stem_ok += 1
        mark = "PASS" if ok else "FAIL"
        lines.append(f"  {got:<8}  {expected:<8}  {mark}  {text}")
    lines.append(f"  stem      {stem_ok}/{len(_STEM_CASES)} match expected")
    lines.append("")

    # Adopt with the verb that used to be no-direction.
    log = tempfile.mktemp(prefix="magnet-pred-demo-", suffix=".db")
    adopt_out = run_adopt(
        "skill",
        "pred-demo-improves",
        "pass rate improves by 1/5",
        "demo-pass-rate",
        log_path=log,
        reset=True,
        apply_demo_bonus=True,
        simulate_next_week=True,
    )
    lines.append("  === adopt with 'improves' (must prediction-held) ===")
    for raw in adopt_out.splitlines():
        if raw.strip():
            lines.append(f"  {raw}" if not raw.startswith(" ") else f" {raw}")
    held = "prediction-held" in adopt_out and "intent     rise" in adopt_out
    lines.append(
        f"  adopt      {'PASS — prediction-held on improves' if held else 'FAIL — expected prediction-held'}"
    )
    lines.append("")

    # Marketing rise-speak on a real strip → prediction-missed.
    fixture = root / "fixtures" / "stack"
    if fixture.is_dir():
        result = hurt_one(str(fixture), label="pred-demo fixture")
        lines.append("  === marketing rise-speak on strip (must prediction-missed) ===")
        missed = 0
        graded = 0
        for row in result["rows"]:
            if row["hurt_label"] != "hurt":
                continue
            graded += 1
            m = row.get("market_prediction") or {}
            if m.get("outcome") == "prediction-missed":
                missed += 1
            lines.append(
                f"    {row['id']:<12} magnet=hurt  "
                f"market={m.get('outcome', '?'):<20} "
                f"intent={m.get('intent', '?'):<8}  {row['market_title']}"
            )
            honest = row.get("prediction") or {}
            lines.append(
                f"    {'':12} honest_title pred={honest.get('outcome', '?'):<20} "
                f"intent={honest.get('intent', '?'):<8}  {row['title']}"
            )
        lines.append(
            f"  market     prediction-missed {missed}/{graded} hurt rows "
            f"(naive still invents helped on {result['naive_helped_on_hurt']}/"
            f"{result['magnet_hurt']})"
        )
        if missed == graded and graded >= 1:
            lines.append(
                "  FINDING  marketing rise-speak missed while honest fall titles held "
                "— prediction grades the words, magnet grades the object."
            )
        lines.append("")
    else:
        lines.append("  (fixtures/stack missing — skip marketing strip arm)")
        lines.append("")

    # Spot-check check_prediction on the verbs themselves.
    improves = check_prediction("pass rate improves", "helped", 1)
    clean = check_prediction("clean up frontmatter", "hurt", -1)
    lines += [
        "  === check_prediction spot checks ===",
        f"  improves→helped   {improves['outcome']} (intent={improves['intent']})",
        f"  clean up→hurt     {clean['outcome']} (intent={clean['intent']})",
        "",
        "  repro      magnet pred-demo",
        "  repro      magnet foreign-hurt",
        "  repro      magnet adopt skill x 'pass rate improves by 1/5' --demo-bonus --reset",
    ]

    all_stem = stem_ok == len(_STEM_CASES)
    if not all_stem or not held:
        lines.append("  RESULT    FAIL — stem or adopt check did not hold")
    else:
        lines.append("  RESULT    PASS — stems grade; improves held; marketing can miss")
    return "\n".join(lines)
