"""Grade an adoption's free-text prediction against the measured verdict.

Ported spirit of helicon MAGNET S3 (prediction record): every shortlisted
candidate makes a checkable claim; check it at the next reading. Cold start
is unmeasured — never a default. A held prediction is still correlation,
not attribution: MAGNET does not claim the change caused the delta.

Slice 25 (found by running, not reading): stems `improv`/`increas`/`decreas`
with a trailing word-boundary never matched improve*/increase*/decrease*.
Bare `\\bup\\b` invented rise on phrasal verbs ("clean up", "set up").
"""
from __future__ import annotations

import re

from magnet.reporter import Verdict

# Lexical intent only — never ranks by the prediction's wording beauty.
# Full conjugations, not truncated stems that die on \\b.
_RISE = re.compile(
    r"\b("
    r"ris(?:e|es|ing)|"
    r"improv(?:e|es|ed|ing|ement)|"
    r"increas(?:e|es|ed|ing)|"
    r"higher|helped|gains?|gained|"
    r"\+\s*\d|"
    r"coverage rises"
    r")\b",
    re.I,
)
_FALL = re.compile(
    r"\b("
    r"fall|falls|falling|"
    r"drop|drops|dropped|dropping|"
    r"hurt|"
    r"decreas(?:e|es|ed|ing)|"
    r"lower|down|regress(?:ion|ed|es|ing)?|"
    r"simplify|simplifies|simplifying|"
    r"streamline|streamlines|streamlining|"
    r"relax|relaxes|relaxing|"
    r"remove|removes|removing|"
    r"strip|strips|stripping|"
    r"undo|revert|weaken|weakens|weakening"
    r")\b",
    re.I,
)
_FLAT = re.compile(
    r"\b(unchanged|no\s+change|same|stable|flat|must\s+NOT\s+rise|not\s+rise|"
    r"no\s+coverage\s+change|nothing\s+moves?)\b",
    re.I,
)


def prediction_intent(prediction: str) -> str:
    """rise | fall | flat | unknown — derived from the prediction text itself."""
    text = prediction or ""
    # Flat checked first: "must NOT rise" contains rise but means flat.
    if _FLAT.search(text):
        return "flat"
    if _RISE.search(text) and not _FALL.search(text):
        return "rise"
    if _FALL.search(text) and not _RISE.search(text):
        return "fall"
    if _RISE.search(text) and _FALL.search(text):
        return "unknown"
    return "unknown"


def check_prediction(
    prediction: str,
    label: Verdict | str,
    delta: int | None = None,
) -> dict:
    """Compare prediction intent to the measured verdict.

    Returns:
      outcome   prediction-held | prediction-missed | unmeasured | no-direction
      intent    rise | fall | flat | unknown
      note      always reminds that held ≠ attributed
    """
    intent = prediction_intent(prediction)
    if label == "baseline":
        return {
            "outcome": "unmeasured",
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "note": "unmeasured — need two readings before a prediction can be checked",
        }
    if intent == "unknown":
        return {
            "outcome": "no-direction",
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "note": "prediction has no rise/fall/flat signal MAGNET can grade",
        }

    expected = {"rise": "helped", "fall": "hurt", "flat": "unchanged"}[intent]
    held = label == expected
    outcome = "prediction-held" if held else "prediction-missed"
    note = (
        f"{outcome}: intent={intent} expected={expected} got={label}"
        " — correlation, not attribution"
    )
    return {
        "outcome": outcome,
        "intent": intent,
        "verdict": label,
        "delta": delta,
        "expected": expected,
        "note": note,
    }


def render_prediction_check(check: dict) -> str:
    lines = [
        "MAGNET prediction check",
        "",
        f"  intent     {check['intent']}",
        f"  outcome    {check['outcome']}",
    ]
    if check.get("expected"):
        lines.append(
            f"  expected   {check['expected']}  got={check['verdict']}"
        )
    lines.append(f"  note       {check['note']}")
    return "\n".join(lines)
