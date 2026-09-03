"""Grade an adoption's free-text prediction against the measured verdict.

Ported spirit of helicon MAGNET S3 (prediction record): every shortlisted
candidate makes a checkable claim; check it at the next reading. Cold start
is unmeasured — never a default. A held prediction is still correlation,
not attribution: MAGNET does not claim the change caused the delta.
"""
from __future__ import annotations

import re

from magnet.reporter import Verdict

# Lexical intent only — never ranks by the prediction's wording beauty.
_RISE = re.compile(
    r"\b(ris(?:e|es|ing)|up|improv|increas|higher|helped|gain|\+\s*\d|coverage rises)\b",
    re.I,
)
_FALL = re.compile(
    r"\b(fall|falls|falling|drop|drops|hurt|decreas|lower|down|regress)\b",
    re.I,
)
_FLAT = re.compile(
    r"\b(unchanged|no\s+change|same|stable|flat|must\s+NOT\s+rise|not\s+rise|"
    r"no\s+coverage\s+change|nothing\s+moves?)\b",
    re.I,
)

Outcome = str  # prediction-held | prediction-missed | unmeasured | no-direction


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
    # Special case: predicting flat and getting baseline-equivalent unchanged.
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
