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

Slice 28: stay-at without `/pop` (`must stay at 5`), remain/hold/keep/
unchanged-at lexicon, and floor claims (`at least 4/5`). A parsed level
with unknown intent is treated as flat — never no-direction while a level
sits on the table.

Slice 32: recover/restore/regain/rebound are rise. DEMO-ONE-WORKFLOW's
prediction `pass rate recovers by 1` was `no-direction` while Δ +1 and
the claimed amount already parsed — the Devpost demo could not grade its
own restore step. Slice 31 papered over by rewriting the sidecar to
`rises by 1`. Open the prediction text, not the nearest synonym.

Slice 35: negation honesty — `won't fall` / `does not regress` / `should
not drop` are flat, NOT fall. Found by running the object: magnet graded
`won't fall` as fall, inventing held when the score dropped. Ceiling
claims (`at most 3/5`, dual of floor). Target-level (`falls to 2/5`,
`reaches 5/5`) grades latest — direction alone is not the object.

Slice 36: percent-of-pop — `improves by 20%` must NOT parse as absolute
20 (the `%` was stripped and inventing held on Δ=+20 / pop 5). Grades
expected Δ = round(pop · pct / 100). `exactly 4/5` is a target level.
"""
from __future__ import annotations

import re

from magnet.reporter import Verdict

# Lexical intent only — never ranks by the prediction's wording beauty.
# improv(?:e|…) — bare `improv` failed word-boundary on "improves" (Slice 35).
_RISE = re.compile(
    r"\b("
    r"ris(?:e|es|ing)|up|improv(?:e|es|ed|ing|ement)?|increas(?:e|es|ed|ing)?|"
    r"higher|helped|gain|\+\s*\d|coverage rises|"
    r"climb(?:s|ed|ing)?|"
    r"doubles?|twice|"
    r"recover(?:s|ed|ing|y)?|restor(?:e|es|ed|ing)|regain(?:s|ed|ing)?|"
    r"rebound(?:s|ed|ing)?"
    r")\b",
    re.I,
)
_FALL = re.compile(
    r"\b(fall|falls|falling|drop|drops|dropping|hurt|decreas(?:e|es|ed|ing)?|"
    r"declin(?:e|es|ed|ing)?|worsen(?:s|ed|ing)?|slip(?:s|ped|ping)?|"
    r"halves?|half|"
    r"lower|down|regress|"
    r"simplify|simplifies|simplifying|streamline|relax|remove|strip|undo|revert|weaken)\b",
    re.I,
)
# Negated fall/rise MUST win before _FALL/_RISE. THE LIE Slice 35 fixed:
# "won't fall" was fall → invents held when the score drops.
_NEGATED_MOVE = re.compile(
    r"(?:"
    r"won'?t\s+(?:fall|drop|regress|decline|worsen|slip|hurt)|"
    r"will\s+not\s+(?:fall|drop|regress|decline|worsen|slip|hurt)|"
    r"(?:must|should|does|do|did)\s+not\s+(?:fall|drop|regress|decline|worsen|slip|hurt)|"
    r"doesn'?t\s+(?:fall|drop|regress|decline|worsen|slip|hurt)|"
    r"don'?t\s+(?:fall|drop|regress|decline|worsen|slip|hurt)|"
    r"no\s+regression|"
    r"without\s+(?:falling|dropping|regressing)|"
    r"must\s+NOT\s+rise|not\s+rise|"
    r"won'?t\s+rise|will\s+not\s+rise|"
    r"(?:must|should|does|do)\s+not\s+rise"
    r")",
    re.I,
)
_FLAT = re.compile(
    r"\b(unchanged|no\s+change|same|stable|flat|"
    r"no\s+coverage\s+change|nothing\s+moves?|still\s+pass|remain(?:s|ing)?\s+green|"
    r"stay(?:s|ing)?\s+at|must\s+stay|"
    r"remain(?:s|ing)?\s+at|hold(?:s|ing)?\s+at|keep(?:s|ing)?\s+at|"
    r"must\s+(?:remain|hold|keep)|"
    r"exactly|must\s+be\s+exactly|"
    # Slice 38: below/above-bound stay phrases — "no lower than" contains "lower"
    # (fall lexicon) but is a floor claim, not a fall.
    r"no\s+lower\s+than|no\s+less\s+than|never\s+(?:fall\s+)?below|"
    r"stay(?:s|ing)?\s+above|remain(?:s|ing)?\s+above|keep(?:s|ing)?\s+above"
    r")\b",
    re.I,
)

# Absolute stay-at level: "must stay at 190/190", "stay at 4/5", "stay at 5",
# "remain at 4/5", "hold at 190", "keep at 5/5", "unchanged at 5/5".
# Population is optional — value-only claims compare latest value alone.
_STAY_AT = re.compile(
    r"(?:must\s+)?"
    r"(?:stay(?:s|ing)?|remain(?:s|ing)?|hold(?:s|ing)?|keep(?:s|ing)?|unchanged)"
    r"\s+at\s+(\d+)(?:\s*/\s*(\d+))?",
    re.I,
)

# Floor claim: "at least 4/5", "no worse than 4/5". Held when latest >= value.
_FLOOR = re.compile(
    r"(?:at\s+least|no\s+worse\s+than)\s+(\d+)(?:\s*/\s*(\d+))?",
    re.I,
)

# Slice 38: below-bound compounds. THE LIE: "won't fall below 3/5" left floor=None
# so unchanged@latest=2 invented held. Held when latest >= value.
_FLOOR_BELOW = re.compile(
    r"(?:"
    r"(?:won'?t|will\s+not|does\s+not|doesn'?t|must\s+not|should\s+not)\s+"
    r"(?:fall|drop|regress|decline|go)\s+(?:below|under)|"
    r"never\s+(?:fall\s+)?below|"
    r"no\s+lower\s+than|"
    r"no\s+less\s+than|"
    r"(?:must\s+not|should\s+not)\s+(?:drop|fall)\s+under"
    r")\s+(\d+)(?:\s*/\s*(\d+))?",
    re.I,
)

# Strict above-bound: "stays above 3/5". Held when latest > value (not ≥).
_FLOOR_ABOVE = re.compile(
    r"(?:must\s+)?"
    r"(?:stay(?:s|ing)?|remain(?:s|ing)?|keep(?:s|ing)?)\s+above\s+"
    r"(\d+)(?:\s*/\s*(\d+))?",
    re.I,
)

# Ceiling claim (dual of floor): "at most 3/5", "no better than 3/5",
# "no more than 4/5", "capped at 4/5", "must not exceed 4/5".
# Held when latest <= value.
_CEILING = re.compile(
    r"(?:at\s+most|no\s+better\s+than|no\s+more\s+than|capped\s+at|"
    r"must\s+not\s+exceed)\s+(\d+)(?:\s*/\s*(\d+))?",
    re.I,
)

# Target-level: "falls to 2/5", "reaches 5/5", "hits 5", "ends at 4/5",
# "lands at 4/5", "returns to 4/5", "climbs to 5/5", "improves to 4/5",
# "exactly 4/5", "must be exactly 4/5", "lands at exactly 4/5".
# Direction alone is not the object — latest must match the named level.
_TARGET = re.compile(
    r"(?:"
    r"(?:falls?|drops?|rises?|climbs?|improves?)\s+to|"
    r"reaches?|hits?|"
    r"(?:ends?|lands?|settles?)\s+at|"
    r"returns?\s+to|back\s+to|"
    r"(?:must\s+be\s+)?exactly"
    r")\s+(?:exactly\s+)?(\d+)(?:\s*/\s*(\d+))?",
    re.I,
)

# Percent claim: "improves by 20%", "rises by 50%", "+10%". NOT absolute points.
_CLAIM_PCT = re.compile(
    r"(?:by\s*|[+\-]\s*)(\d+)\s*%",
    re.I,
)

# Ratio claim vs prior: doubles / halves. Prior = latest − Δ (Slice 37).
_RATIO = re.compile(
    r"\b(?:doubles?|twice(?:\s+as\s+many)?|halves?|cuts?\s+in\s+half)\b",
    re.I,
)

# Claimed magnitude: "rises by 1/5", "falls by 2/7", "+1/5", "by 1/5".
_CLAIM_FRAC = re.compile(
    r"(?:by\s*|[+\-]\s*|↑\s*\+?)(\d+)\s*/\s*(\d+)",
    re.I,
)
# Claimed absolute delta without population: "rises by 1", "+1", "-2" (not a date).
# Negative lookahead refuses digits that are part of a percent (`20%`).
_CLAIM_ABS = re.compile(
    r"(?:by\s+|rises?\s+by\s+|falls?\s+by\s+|drops?\s+by\s+|"
    r"climbs?\s+by\s+|improves?\s+by\s+|declines?\s+by\s+|worsens?\s+by\s+|"
    r"slips?\s+by\s+)\s*(\d+)(?!\s*/)(?!\s*%)",
    re.I,
)
_CLAIM_SIGNED = re.compile(r"(?<![/\d])([+\-])(\d+)(?!\s*/)(?!\s*%)", re.I)


def prediction_intent(prediction: str) -> str:
    """rise | fall | flat | unknown — derived from the prediction text itself.

    A parsed stay-at / floor / ceiling level with no rise/fall signal is flat:
    naming a required bound is itself a stay claim (Slice 28/35 — never
    no-direction while a bound sits on the table).

    Negated moves (`won't fall`) are flat — checked before fall lexicon.
    """
    text = prediction or ""
    # Negation and flat first: "won't fall" contains fall but means flat.
    if _NEGATED_MOVE.search(text) or _FLAT.search(text):
        return "flat"
    if _RISE.search(text) and not _FALL.search(text):
        return "rise"
    if _FALL.search(text) and not _RISE.search(text):
        return "fall"
    if _RISE.search(text) and _FALL.search(text):
        return "unknown"
    # Level / floor / ceiling on the table ⇒ stay intent even if lexicon missed.
    if (
        claimed_level(text)["value"] is not None
        or claimed_floor(text)["value"] is not None
        or claimed_ceiling(text)["value"] is not None
    ):
        return "flat"
    # Target-only (`reaches 5/5` / `exactly 4/5`) with no rise/fall word —
    # treat as flat so check_prediction grades the target, not no-direction.
    if claimed_target(text)["value"] is not None:
        return "flat"
    return "unknown"


def claimed_level(prediction: str) -> dict:
    """Parse stay-at absolute value (+ optional pop). Not a delta — a required latest."""
    text = prediction or ""
    m = _STAY_AT.search(text)
    if not m:
        return {"value": None, "population": None, "raw": None}
    pop = m.group(2)
    return {
        "value": int(m.group(1)),
        "population": int(pop) if pop is not None else None,
        "raw": m.group(0).strip(),
    }


def claimed_floor(prediction: str) -> dict:
    """Parse floor claim value (+ optional pop).

    Classic: `at least 4/5` — held when latest >= value.
    Slice 38 below-bound: `won't fall below 3/5`, `never below 4/5`,
    `no lower than 3/5` — same ≥ semantics (THE LIE was leaving these unbound).
    Slice 38 above-bound: `stays above 3/5` — exclusive; held when latest > value.
    """
    text = prediction or ""
    # Stay-at owns "stay at N" — floor is a different object.
    if claimed_level(text)["value"] is not None:
        return {"value": None, "population": None, "raw": None, "exclusive": False}
    m = _FLOOR_ABOVE.search(text)
    if m:
        pop = m.group(2)
        return {
            "value": int(m.group(1)),
            "population": int(pop) if pop is not None else None,
            "raw": m.group(0).strip(),
            "exclusive": True,
        }
    m = _FLOOR_BELOW.search(text) or _FLOOR.search(text)
    if not m:
        return {"value": None, "population": None, "raw": None, "exclusive": False}
    pop = m.group(2)
    return {
        "value": int(m.group(1)),
        "population": int(pop) if pop is not None else None,
        "raw": m.group(0).strip(),
        "exclusive": False,
    }


def claimed_ceiling(prediction: str) -> dict:
    """Parse ceiling claim value (+ optional pop). Held when latest <= value.

    Dual of floor (Slice 35). Stay-at / floor own their phrases first.
    """
    text = prediction or ""
    if claimed_level(text)["value"] is not None:
        return {"value": None, "population": None, "raw": None}
    if claimed_floor(text)["value"] is not None:
        return {"value": None, "population": None, "raw": None}
    m = _CEILING.search(text)
    if not m:
        return {"value": None, "population": None, "raw": None}
    pop = m.group(2)
    return {
        "value": int(m.group(1)),
        "population": int(pop) if pop is not None else None,
        "raw": m.group(0).strip(),
    }


def claimed_target(prediction: str) -> dict:
    """Parse target-level (`falls to 2/5`, `reaches 5`). Held when latest == value.

    Stay-at owns `stay at N`. Floor/ceiling own their phrases. Target is the
    directed end-state — direction alone invents held when latest ≠ target.
    """
    text = prediction or ""
    if claimed_level(text)["value"] is not None:
        return {"value": None, "population": None, "raw": None}
    if claimed_floor(text)["value"] is not None:
        return {"value": None, "population": None, "raw": None}
    if claimed_ceiling(text)["value"] is not None:
        return {"value": None, "population": None, "raw": None}
    m = _TARGET.search(text)
    if not m:
        return {"value": None, "population": None, "raw": None}
    pop = m.group(2)
    return {
        "value": int(m.group(1)),
        "population": int(pop) if pop is not None else None,
        "raw": m.group(0).strip(),
    }


def claimed_ratio(prediction: str) -> dict:
    """Parse doubles/halves claim. Grades against prior = latest − Δ.

    Slice 37: direction-only invents held on any rise when the claim said doubles.
    """
    text = prediction or ""
    m = _RATIO.search(text)
    if not m:
        return {"kind": None, "raw": None}
    raw = m.group(0).strip()
    low = raw.lower()
    if "half" in low or "halves" in low:
        kind = "half"
    else:
        kind = "double"
    return {"kind": kind, "raw": raw}


def claimed_percent(prediction: str) -> dict:
    """Parse percent claim (`improves by 20%`). NOT an absolute point count.

    Slice 36: stripping `%` and treating 20 as absolute Δ was the lie —
    Δ=+20 on pop 5 invented held; true 20% of pop 5 (Δ=+1) missed.
    Returns percent int; expected Δ = round(pop · pct / 100) at check time.
    """
    text = prediction or ""
    if claimed_level(text)["value"] is not None:
        return {"percent": None, "raw": None}
    if claimed_floor(text)["value"] is not None:
        return {"percent": None, "raw": None}
    if claimed_ceiling(text)["value"] is not None:
        return {"percent": None, "raw": None}
    if claimed_target(text)["value"] is not None:
        return {"percent": None, "raw": None}
    m = _CLAIM_PCT.search(text)
    if not m:
        return {"percent": None, "raw": None}
    return {"percent": int(m.group(1)), "raw": m.group(0).strip()}


def claimed_magnitude(prediction: str) -> dict:
    """Parse claimed delta amount + optional population from the prediction text.

    Returns:
      amount      int | None  — absolute size of the claimed move (never signed here)
      population  int | None  — denominator when written as N/P
      raw         str | None  — matched substring for the receipt
    Sign is applied later from intent (rise → +, fall → −, flat → 0).
    Stay-at / floor / ceiling / target / percent are NOT absolute deltas —
    their parsers own those. Percent must not fall through to amount=N.
    """
    text = prediction or ""
    if claimed_level(text)["value"] is not None:
        return {"amount": None, "population": None, "raw": None}
    if claimed_floor(text)["value"] is not None:
        return {"amount": None, "population": None, "raw": None}
    if claimed_ceiling(text)["value"] is not None:
        return {"amount": None, "population": None, "raw": None}
    if claimed_target(text)["value"] is not None:
        return {"amount": None, "population": None, "raw": None}
    # Percent owns `by 20%` — never absolute 20 (Slice 36).
    if claimed_percent(text)["percent"] is not None:
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


def expected_delta_from_percent(intent: str, percent: int | None, population: int | None) -> int | None:
    """Signed expected Δ from percent-of-population. None if pop or pct missing."""
    if percent is None or population is None or population <= 0:
        return None
    amount = int(round(int(population) * int(percent) / 100.0))
    if intent == "rise":
        return amount
    if intent == "fall":
        return -amount
    if intent == "flat":
        return 0
    return None


def _bound_fields(prediction: str) -> dict:
    """Shared claimed_* bundle for naive + magnet checks."""
    return {
        "claimed": claimed_magnitude(prediction),
        "claimed_level": claimed_level(prediction),
        "claimed_floor": claimed_floor(prediction),
        "claimed_ceiling": claimed_ceiling(prediction),
        "claimed_target": claimed_target(prediction),
        "claimed_percent": claimed_percent(prediction),
        "claimed_ratio": claimed_ratio(prediction),
    }


def naive_direction_check(
    prediction: str,
    label: Verdict | str,
    delta: int | None = None,
    *,
    population: int | None = None,
    latest_value: int | None = None,
) -> dict:
    """Two-hour naive arm: grade direction only, ignore claimed fraction/level/bounds.

    This is what magnet did through Slice 24 — it invents prediction-held when
    the claim says rises by 2/5 and the measured delta is +1, or stay-at 5/5
    while latest is 4/5, or stay-at 5 while latest is 4, or at most 3/5 while
    latest is 4, or falls to 2/5 while latest is 3.

    Pre-Slice-35 naive also treated `won't fall` as fall (the lie). Naive here
    still uses the *fixed* intent parser so the arm is "direction only", not
    "broken lexicon" — the embarrassment is ignoring ceiling/target/magnitude.
    """
    intent = prediction_intent(prediction)
    bounds = _bound_fields(prediction)
    if label == "baseline":
        return {
            "outcome": "unmeasured",
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "grade": "direction-only",
            **bounds,
            "note": "unmeasured — need two readings before a prediction can be checked",
        }
    if intent == "unknown":
        return {
            "outcome": "no-direction",
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "grade": "direction-only",
            **bounds,
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
        **bounds,
        "note": (
            f"{outcome}: intent={intent} expected={expected} got={label}"
            " — direction only; claimed fraction/level/floor/ceiling/target ignored"
        ),
    }


def _pop_ok(claimed_pop: int | None, measured_pop: int | None) -> bool:
    if claimed_pop is None or measured_pop is None:
        return True
    return int(claimed_pop) == int(measured_pop)


def check_prediction(
    prediction: str,
    label: Verdict | str,
    delta: int | None = None,
    *,
    population: int | None = None,
    latest_value: int | None = None,
) -> dict:
    """Compare prediction intent (+ magnitude/level/floor/ceiling/target when claimed).

    Returns:
      outcome   prediction-held | prediction-missed | unmeasured | no-direction
      intent    rise | fall | flat | unknown
      grade     direction | direction+magnitude | direction+level | floor | ceiling | target
      claimed   {amount, population, raw}
      claimed_level / claimed_floor / claimed_ceiling / claimed_target
      note      always reminds that held ≠ attributed
    """
    intent = prediction_intent(prediction)
    bounds = _bound_fields(prediction)
    claim = bounds["claimed"]
    level = bounds["claimed_level"]
    floor = bounds["claimed_floor"]
    ceiling = bounds["claimed_ceiling"]
    target = bounds["claimed_target"]
    percent = bounds["claimed_percent"]
    ratio = bounds["claimed_ratio"]

    if label == "baseline":
        return {
            "outcome": "unmeasured",
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "population": population,
            "latest_value": latest_value,
            "grade": "direction",
            **bounds,
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
            **bounds,
            "note": "prediction has no rise/fall/flat signal MAGNET can grade",
        }

    # Floor claims: held when latest >= claimed floor (or > if exclusive).
    # Pop match when both present. Slice 38: below-bound compounds open here.
    if floor.get("value") is not None:
        exclusive = bool(floor.get("exclusive"))
        if latest_value is None:
            floor_ok = False
        else:
            if exclusive:
                floor_ok = int(latest_value) > int(floor["value"])
            else:
                floor_ok = int(latest_value) >= int(floor["value"])
            floor_ok = floor_ok and _pop_ok(floor.get("population"), population)
        outcome = "prediction-held" if floor_ok else "prediction-missed"
        op = ">" if exclusive else "≥"
        why = (
            f"floor claimed {op}{floor['value']}/{floor.get('population')} "
            f"got {latest_value}/{population}"
        )
        return {
            "outcome": outcome,
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "population": population,
            "latest_value": latest_value,
            "expected": None,
            "expected_delta": None,
            "grade": "floor",
            **bounds,
            "floor_ok": floor_ok,
            "note": f"{outcome}: intent={intent} {why} — correlation, not attribution",
        }

    # Ceiling claims (Slice 35): held when latest <= claimed ceiling.
    if ceiling.get("value") is not None:
        if latest_value is None:
            ceiling_ok = False
        else:
            ceiling_ok = int(latest_value) <= int(ceiling["value"])
            ceiling_ok = ceiling_ok and _pop_ok(ceiling.get("population"), population)
        outcome = "prediction-held" if ceiling_ok else "prediction-missed"
        why = (
            f"ceiling claimed ≤{ceiling['value']}/{ceiling.get('population')} "
            f"got {latest_value}/{population}"
        )
        return {
            "outcome": outcome,
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "population": population,
            "latest_value": latest_value,
            "expected": None,
            "expected_delta": None,
            "grade": "ceiling",
            **bounds,
            "ceiling_ok": ceiling_ok,
            "note": f"{outcome}: intent={intent} {why} — correlation, not attribution",
        }

    # Percent-of-pop (Slice 36): expected Δ = round(pop · pct / 100).
    # Never treat `20%` as absolute 20 — that invented held on Δ=+20 / pop 5.
    if percent.get("percent") is not None:
        expected = {"rise": "helped", "fall": "hurt", "flat": "unchanged"}[intent]
        direction_ok = label == expected
        expected_delta = expected_delta_from_percent(
            intent, percent.get("percent"), population
        )
        if expected_delta is None:
            # No population → cannot convert % to Δ; refuse absolute invent.
            return {
                "outcome": "prediction-missed" if not direction_ok else "no-direction",
                "intent": intent,
                "verdict": label,
                "delta": delta,
                "population": population,
                "latest_value": latest_value,
                "expected": expected,
                "expected_delta": None,
                "grade": "percent",
                **bounds,
                "note": (
                    f"{'prediction-missed' if not direction_ok else 'no-direction'}: "
                    f"intent={intent} percent={percent['percent']}% needs population "
                    "to grade — will not invent absolute points"
                ),
            }
        magnitude_ok = delta is not None and int(delta) == int(expected_delta)
        held = direction_ok and magnitude_ok
        outcome = "prediction-held" if held else "prediction-missed"
        if not direction_ok:
            why = f"direction expected={expected} got={label}"
        elif not magnitude_ok:
            why = (
                f"percent {percent['percent']}% of pop {population} → "
                f"claimed Δ {expected_delta:+d} got Δ "
                f"{delta if delta is not None else '—'}"
            )
        else:
            why = f"direction+percent ({percent['percent']}% of {population})"
        return {
            "outcome": outcome,
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "population": population,
            "latest_value": latest_value,
            "expected": expected,
            "expected_delta": expected_delta,
            "grade": "direction+percent",
            **bounds,
            "magnitude_ok": magnitude_ok,
            "note": f"{outcome}: intent={intent} {why} — correlation, not attribution",
        }

    # Doubles/halves vs prior (Slice 37): prior = latest − Δ.
    # Direction alone invents held on a non-double rise.
    if ratio.get("kind") is not None:
        expected = {"rise": "helped", "fall": "hurt", "flat": "unchanged"}[intent]
        direction_ok = label == expected
        if latest_value is None or delta is None:
            return {
                "outcome": "unmeasured",
                "intent": intent,
                "verdict": label,
                "delta": delta,
                "population": population,
                "latest_value": latest_value,
                "expected": expected,
                "expected_delta": None,
                "grade": "ratio",
                **bounds,
                "note": "unmeasured — doubles/halves need latest and Δ to recover prior",
            }
        prior = int(latest_value) - int(delta)
        if ratio["kind"] == "double":
            if prior <= 0:
                ratio_ok = False
                expected_delta = None
            else:
                expected_delta = prior  # latest should be 2·prior
                ratio_ok = int(latest_value) == 2 * prior and int(delta) == prior
        else:  # half
            if prior < 0:
                ratio_ok = False
                expected_delta = None
            else:
                expected_latest = prior // 2
                expected_delta = expected_latest - prior
                ratio_ok = int(latest_value) == expected_latest and int(delta) == expected_delta
        held = direction_ok and ratio_ok
        outcome = "prediction-held" if held else "prediction-missed"
        if not direction_ok:
            why = f"direction expected={expected} got={label}"
        elif not ratio_ok:
            why = (
                f"ratio={ratio['kind']} prior={prior} "
                f"latest={latest_value} Δ={delta} "
                f"expected_delta={expected_delta if expected_delta is not None else '—'}"
            )
        else:
            why = f"direction+ratio ({ratio['kind']} prior={prior})"
        return {
            "outcome": outcome,
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "population": population,
            "latest_value": latest_value,
            "expected": expected,
            "expected_delta": expected_delta,
            "grade": "direction+ratio",
            **bounds,
            "prior": prior,
            "ratio_ok": ratio_ok,
            "note": f"{outcome}: intent={intent} {why} — correlation, not attribution",
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
            level_ok = level_ok and _pop_ok(level.get("population"), population)

    target_ok = True
    if target.get("value") is not None:
        if latest_value is None:
            target_ok = False
        else:
            target_ok = int(latest_value) == int(target["value"])
            target_ok = target_ok and _pop_ok(target.get("population"), population)

    # Target-level without stay-at / magnitude (Slice 35).
    # Direction + target when intent is rise/fall; target alone when flat
    # (`reaches 5/5` with no rise word → intent flat via claimed_target).
    if target.get("value") is not None and expected_delta is None and level.get("value") is None:
        if intent == "flat":
            held = target_ok
            grade = "target"
        else:
            held = direction_ok and target_ok
            grade = "direction+target"
        outcome = "prediction-held" if held else "prediction-missed"
        if intent != "flat" and not direction_ok:
            why = f"direction expected={expected} got={label}"
        elif not target_ok:
            why = (
                f"target claimed {target['value']}/{target.get('population')} "
                f"got {latest_value}/{population}"
            )
        else:
            why = "direction+target" if intent != "flat" else "target"
        return {
            "outcome": outcome,
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "population": population,
            "latest_value": latest_value,
            "expected": expected if intent != "flat" else None,
            "expected_delta": None,
            "grade": grade,
            **bounds,
            "target_ok": target_ok,
            "direction_ok": direction_ok if intent != "flat" else None,
            "note": f"{outcome}: intent={intent} {why} — correlation, not attribution",
        }

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
            **bounds,
            "note": note,
        }

    if expected_delta is not None:
        magnitude_ok = delta is not None and int(delta) == int(expected_delta)
        pop_ok = _pop_ok(claim.get("population"), population)
        held = direction_ok and magnitude_ok and pop_ok and level_ok and target_ok
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
        elif not target_ok:
            why = (
                f"target claimed {target['value']}/{target.get('population')} "
                f"got {latest_value}/{population}"
            )
        else:
            why = "direction+magnitude"
        grade = "direction+magnitude"
        if level.get("value") is not None:
            grade += "+level"
        if target.get("value") is not None:
            grade += "+target"
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
            **bounds,
            "magnitude_ok": magnitude_ok,
            "population_ok": pop_ok,
            "level_ok": level_ok,
            "target_ok": target_ok,
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
        **bounds,
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
        pop = level.get("population")
        lvl_txt = f"{level['value']}/{pop}" if pop is not None else str(level["value"])
        lines.append(
            f"  claimed lvl {lvl_txt}  "
            f"latest={check.get('latest_value')}/{check.get('population')}"
        )
    floor = check.get("claimed_floor") or {}
    if floor.get("value") is not None:
        pop = floor.get("population")
        fl_txt = f"{floor['value']}/{pop}" if pop is not None else str(floor["value"])
        lines.append(
            f"  claimed floor ≥{fl_txt}  "
            f"latest={check.get('latest_value')}/{check.get('population')}"
        )
    ceiling = check.get("claimed_ceiling") or {}
    if ceiling.get("value") is not None:
        pop = ceiling.get("population")
        ce_txt = (
            f"{ceiling['value']}/{pop}" if pop is not None else str(ceiling["value"])
        )
        lines.append(
            f"  claimed ceiling ≤{ce_txt}  "
            f"latest={check.get('latest_value')}/{check.get('population')}"
        )
    target = check.get("claimed_target") or {}
    if target.get("value") is not None:
        pop = target.get("population")
        tg_txt = f"{target['value']}/{pop}" if pop is not None else str(target["value"])
        lines.append(
            f"  claimed target {tg_txt}  "
            f"latest={check.get('latest_value')}/{check.get('population')}"
        )
    pct = check.get("claimed_percent") or {}
    if pct.get("percent") is not None:
        lines.append(
            f"  claimed %   {pct['percent']}%  "
            f"expected_delta={check.get('expected_delta') if check.get('expected_delta') is not None else '—'}  "
            f"measured_delta={check.get('delta') if check.get('delta') is not None else '—'}  "
            f"pop={check.get('population')}"
        )
    lines.append(f"  note       {check['note']}")
    return "\n".join(lines)
