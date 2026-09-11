"""Grade an adoption's free-text prediction against the measured verdict.

Ported spirit of helicon MAGNET S3 (prediction record): every shortlisted
candidate makes a checkable claim; check it at the next reading. Cold start
is unmeasured — never a default. A held prediction is still correlation,
not attribution: MAGNET does not claim the change caused the delta.

Slice 25: when the prediction names a fraction (`rises by 1/5`), magnet
checks magnitude (+ population when claimed). Direction-only grading is the
naive arm — it invents held when the fraction is wrong.

Slice 26: when the prediction names a stay-at level (`must stay at 5/5`),
magnet checks latest value/pop. Flat-only grading invents held when the
level is wrong.
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
    r"\b(fall|falls|falling|drop|drops|hurt|decreas|lower|down|regress|"
    r"simplify|simplifies|simplifying|streamline|relax|remove|strip|undo|revert|weaken)\b",
    re.I,
)
_FLAT = re.compile(
    r"\b(unchanged|no\s+change|same|stable|flat|must\s+NOT\s+rise|not\s+rise|"
    r"no\s+coverage\s+change|nothing\s+moves?|still\s+pass|remain(?:s|ing)?\s+green|"
    r"stay(?:s|ing)?\s+at|must\s+stay)\b",
    re.I,
)

# Absolute stay-at level: "must stay at 190/190", "stay at 4/5".
# Parsed BEFORE delta claims — this is a level, not a move.
_STAY_AT = re.compile(
    r"(?:must\s+)?(?:stay(?:s|ing)?|remain(?:s|ing)?|hold(?:s|ing)?)\s+at\s+(\d+)\s*/\s*(\d+)",
    re.I,
)

# Claimed magnitude: "rises by 1/5", "falls by 2/7", "+1/5", "by 1/5".
_CLAIM_FRAC = re.compile(
    r"(?:by\s*|[+\-]\s*|↑\s*\+?)(\d+)\s*/\s*(\d+)",
    re.I,
)
# Claimed absolute delta without population: "rises by 1", "+1", "-2" (not a date).
_CLAIM_ABS = re.compile(
    r"(?:by\s+|rises?\s+by\s+|falls?\s+by\s+|drops?\s+by\s+)(\d+)(?!\s*/)",
    re.I,
)
_CLAIM_SIGNED = re.compile(r"(?<![/\d])([+\-])(\d+)(?!\s*/)", re.I)


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


def claimed_level(prediction: str) -> dict:
    """Parse stay-at absolute value/pop. Not a delta — a required latest reading."""
    text = prediction or ""
    m = _STAY_AT.search(text)
    if not m:
        return {"value": None, "population": None, "raw": None}
    return {
        "value": int(m.group(1)),
        "population": int(m.group(2)),
        "raw": m.group(0).strip(),
    }


def claimed_magnitude(prediction: str) -> dict:
    """Parse claimed delta amount + optional population from the prediction text.

    Returns:
      amount      int | None  — absolute size of the claimed move (never signed here)
      population  int | None  — denominator when written as N/P
      raw         str | None  — matched substring for the receipt
    Sign is applied later from intent (rise → +, fall → −, flat → 0).
    Stay-at levels are NOT deltas — claimed_level owns those.
    """
    text = prediction or ""
    if claimed_level(text)["value"] is not None:
        return {"amount": None, "population": None, "raw": None}
    m = _CLAIM_FRAC.search(text)
    if m:
        return {
            "amount": int(m.group(1)),
            "population": int(m.group(2)),
            "raw": m.group(0).strip(),
        }
    m = _CLAIM_ABS.search(text)
    if m:
        return {"amount": int(m.group(1)), "population": None, "raw": m.group(0).strip()}
    m = _CLAIM_SIGNED.search(text)
    if m:
        return {"amount": int(m.group(2)), "population": None, "raw": m.group(0).strip()}
    return {"amount": None, "population": None, "raw": None}


def expected_delta_from_claim(intent: str, claim: dict) -> int | None:
    """Signed expected delta from intent + claimed amount. None if no amount."""
    amount = claim.get("amount")
    if amount is None:
        return None
    if intent == "rise":
        return int(amount)
    if intent == "fall":
        return -int(amount)
    if intent == "flat":
        return 0
    return None


def naive_direction_check(
    prediction: str,
    label: Verdict | str,
    delta: int | None = None,
    *,
    population: int | None = None,
    latest_value: int | None = None,
) -> dict:
    """Two-hour naive arm: grade direction only, ignore claimed fraction/level.

    This is what magnet did through Slice 24 — it invents prediction-held when
    the claim says rises by 2/5 and the measured delta is +1, or stay-at 5/5
    while latest is 4/5.
    """
    intent = prediction_intent(prediction)
    claim = claimed_magnitude(prediction)
    level = claimed_level(prediction)
    if label == "baseline":
        return {
            "outcome": "unmeasured",
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "grade": "direction-only",
            "claimed": claim,
            "claimed_level": level,
            "note": "unmeasured — need two readings before a prediction can be checked",
        }
    if intent == "unknown":
        return {
            "outcome": "no-direction",
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "grade": "direction-only",
            "claimed": claim,
            "claimed_level": level,
            "note": "prediction has no rise/fall/flat signal MAGNET can grade",
        }
    expected = {"rise": "helped", "fall": "hurt", "flat": "unchanged"}[intent]
    held = label == expected
    outcome = "prediction-held" if held else "prediction-missed"
    return {
        "outcome": outcome,
        "intent": intent,
        "verdict": label,
        "delta": delta,
        "population": population,
        "latest_value": latest_value,
        "expected": expected,
        "grade": "direction-only",
        "claimed": claim,
        "claimed_level": level,
        "note": (
            f"{outcome}: intent={intent} expected={expected} got={label}"
            " — direction only; claimed fraction/level ignored"
        ),
    }


def check_prediction(
    prediction: str,
    label: Verdict | str,
    delta: int | None = None,
    *,
    population: int | None = None,
    latest_value: int | None = None,
) -> dict:
    """Compare prediction intent (+ magnitude/level when claimed) to the measured verdict.

    Returns:
      outcome   prediction-held | prediction-missed | unmeasured | no-direction
      intent    rise | fall | flat | unknown
      grade     direction | direction+magnitude | direction+level
      claimed   {amount, population, raw}
      claimed_level {value, population, raw}
      note      always reminds that held ≠ attributed
    """
    intent = prediction_intent(prediction)
    claim = claimed_magnitude(prediction)
    level = claimed_level(prediction)
    if label == "baseline":
        return {
            "outcome": "unmeasured",
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "population": population,
            "latest_value": latest_value,
            "grade": "direction",
            "claimed": claim,
            "claimed_level": level,
            "note": "unmeasured — need two readings before a prediction can be checked",
        }
    if intent == "unknown":
        return {
            "outcome": "no-direction",
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "population": population,
            "latest_value": latest_value,
            "grade": "direction",
            "claimed": claim,
            "claimed_level": level,
            "note": "prediction has no rise/fall/flat signal MAGNET can grade",
        }

    expected = {"rise": "helped", "fall": "hurt", "flat": "unchanged"}[intent]
    direction_ok = label == expected
    expected_delta = expected_delta_from_claim(intent, claim)

    level_ok = True
    if level.get("value") is not None:
        if latest_value is None:
            level_ok = False
        else:
            level_ok = int(latest_value) == int(level["value"])
            if level.get("population") is not None and population is not None:
                level_ok = level_ok and int(population) == int(level["population"])

    if expected_delta is None and level.get("value") is None:
        held = direction_ok
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
            "population": population,
            "latest_value": latest_value,
            "expected": expected,
            "expected_delta": None,
            "grade": "direction",
            "claimed": claim,
            "claimed_level": level,
            "note": note,
        }

    if expected_delta is not None:
        magnitude_ok = delta is not None and int(delta) == int(expected_delta)
        pop_ok = True
        if claim.get("population") is not None and population is not None:
            pop_ok = int(claim["population"]) == int(population)
        held = direction_ok and magnitude_ok and pop_ok and level_ok
        outcome = "prediction-held" if held else "prediction-missed"
        if not direction_ok:
            why = f"direction expected={expected} got={label}"
        elif not magnitude_ok:
            why = (
                f"magnitude claimed Δ {expected_delta:+d} "
                f"got Δ {delta if delta is not None else '—'}"
            )
        elif not pop_ok:
            why = (
                f"population mismatch claimed={claim['population']} "
                f"measured={population}"
            )
        elif not level_ok:
            why = (
                f"level claimed {level['value']}/{level.get('population')} "
                f"got {latest_value}/{population}"
            )
        else:
            why = "direction+magnitude"
        grade = "direction+magnitude" + ("+level" if level.get("value") is not None else "")
        return {
            "outcome": outcome,
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "population": population,
            "latest_value": latest_value,
            "expected": expected,
            "expected_delta": expected_delta,
            "grade": grade,
            "claimed": claim,
            "claimed_level": level,
            "magnitude_ok": magnitude_ok,
            "population_ok": pop_ok,
            "level_ok": level_ok,
            "note": f"{outcome}: intent={intent} {why} — correlation, not attribution",
        }

    # Stay-at level only (no delta claim).
    held = direction_ok and level_ok
    outcome = "prediction-held" if held else "prediction-missed"
    if not direction_ok:
        why = f"direction expected={expected} got={label}"
    elif not level_ok:
        why = (
            f"level claimed {level['value']}/{level.get('population')} "
            f"got {latest_value}/{population}"
        )
    else:
        why = "direction+level"
    return {
        "outcome": outcome,
        "intent": intent,
        "verdict": label,
        "delta": delta,
        "population": population,
        "latest_value": latest_value,
        "expected": expected,
        "expected_delta": None,
        "grade": "direction+level",
        "claimed": claim,
        "claimed_level": level,
        "level_ok": level_ok,
        "note": f"{outcome}: intent={intent} {why} — correlation, not attribution",
    }


def render_prediction_check(check: dict) -> str:
    lines = [
        "MAGNET prediction check",
        "",
        f"  intent     {check['intent']}",
        f"  outcome    {check['outcome']}",
        f"  grade      {check.get('grade', 'direction')}",
    ]
    if check.get("expected"):
        lines.append(
            f"  expected   {check['expected']}  got={check['verdict']}"
        )
    claim = check.get("claimed") or {}
    if claim.get("amount") is not None:
        pop = claim.get("population")
        claim_txt = (
            f"{claim['amount']}/{pop}" if pop is not None else str(claim["amount"])
        )
        exp_d = check.get("expected_delta")
        got_d = check.get("delta")
        lines.append(
            f"  claimed Δ  {claim_txt}  expected_delta="
            f"{exp_d if exp_d is not None else '—'}  "
            f"measured_delta={got_d if got_d is not None else '—'}"
        )
        if check.get("population") is not None and pop is not None:
            lines.append(
                f"  claimed pop {pop}  measured_pop={check['population']}"
            )
    level = check.get("claimed_level") or {}
    if level.get("value") is not None:
        lines.append(
            f"  claimed lvl {level['value']}/{level.get('population')}  "
            f"latest={check.get('latest_value')}/{check.get('population')}"
        )
    lines.append(f"  note       {check['note']}")
    return "\n".join(lines)
