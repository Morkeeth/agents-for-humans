"""pred-demo — embarrassment arm: naive direction invents held on wrong magnitude.

Found 2026-09-11 by running:
  check_prediction("pass rate rises by 2/5", "helped", 1) → prediction-held

That was a lie. Magnet now checks the claimed fraction; the old behaviour
ships as the naive arm so a stranger can see us lose to honesty.
"""
from __future__ import annotations

from dataclasses import dataclass

from magnet.prediction import (
    check_prediction,
    claimed_magnitude,
    naive_direction_check,
    prediction_intent,
)


@dataclass(frozen=True)
class PredScenario:
    name: str
    prediction: str
    label: str
    delta: int | None
    population: int | None
    magnet_truth: str
    note: str = ""


# Ground truth is magnet's magnitude-aware grade. Naive is scored against the
# same truth so a direction-only hold on a wrong fraction counts as a naive win
# that we refuse — the embarrassment.
SCENARIOS: tuple[PredScenario, ...] = (
    PredScenario(
        "correct_fraction",
        "pass rate rises by 1/5",
        "helped",
        1,
        5,
        "prediction-held",
        note="claim matches measured Δ +1 on pop 5",
    ),
    PredScenario(
        "wrong_magnitude",
        "pass rate rises by 2/5",
        "helped",
        1,
        5,
        "prediction-missed",
        note="direction ok but claimed Δ +2 ≠ measured +1 — THE LIE Slice 24 printed held",
    ),
    PredScenario(
        "wrong_population",
        "coverage rises by 1/5",
        "helped",
        1,
        12,
        "prediction-missed",
        note="Δ matches but claimed pop 5 ≠ measured 12",
    ),
    PredScenario(
        "vague_rise",
        "coverage rises",
        "helped",
        1,
        12,
        "prediction-held",
        note="no fraction claimed — direction is the whole grade",
    ),
    PredScenario(
        "strip_fall",
        "simplify skill frontmatter",
        "hurt",
        -7,
        7,
        "prediction-held",
        note="fall intent, no fraction — foreign-hurt titles still grade",
    ),
    PredScenario(
        "still_pass_flat",
        "all tests still pass",
        "unchanged",
        0,
        190,
        "prediction-held",
        note="still pass → flat; judge-demo prediction becomes checkable",
    ),
    PredScenario(
        "still_pass_missed",
        "all tests still pass",
        "helped",
        1,
        5,
        "prediction-missed",
        note="claimed flat, measured helped",
    ),
    PredScenario(
        "fall_fraction",
        "pass rate falls by 2/5",
        "hurt",
        -2,
        5,
        "prediction-held",
        note="fall + matching magnitude",
    ),
)


def run_pred_demo() -> str:
    """Print magnet vs naive_direction on magnitude scenarios."""
    lines = [
        "MAGNET pred-demo — magnitude honesty vs naive direction-only",
        "",
        "  When a prediction names a fraction (rises by 1/5), magnet checks Δ.",
        "  Naive grades direction only — invents held when the fraction is wrong.",
        "",
        "  scenario            claim                    Δ    pop  magnet              naive",
        "  " + "-" * 90,
    ]
    magnet_ok = 0
    naive_ok = 0
    embarrass = 0
    for sc in SCENARIOS:
        m = check_prediction(
            sc.prediction, sc.label, sc.delta, population=sc.population
        )
        n = naive_direction_check(sc.prediction, sc.label, sc.delta)
        m_out = m["outcome"]
        n_out = n["outcome"]
        if m_out == sc.magnet_truth:
            magnet_ok += 1
        if n_out == sc.magnet_truth:
            naive_ok += 1
        # Embarrassment: naive invents held while magnet correctly misses.
        if (
            sc.magnet_truth == "prediction-missed"
            and m_out == "prediction-missed"
            and n_out == "prediction-held"
        ):
            embarrass += 1
        claim = claimed_magnitude(sc.prediction)
        claim_txt = (
            f"{claim['amount']}/{claim['population']}"
            if claim["amount"] is not None and claim["population"] is not None
            else (
                str(claim["amount"])
                if claim["amount"] is not None
                else prediction_intent(sc.prediction)
            )
        )
        delta_txt = "—" if sc.delta is None else f"{sc.delta:+d}"
        pop_txt = "—" if sc.population is None else str(sc.population)
        lines.append(
            f"  {sc.name:<20}{claim_txt:<24}{delta_txt:<5}{pop_txt:<5}"
            f"{m_out:<20}{n_out}"
        )

    total = len(SCENARIOS)
    lines += [
        "",
        f"  magnet       {magnet_ok}/{total}  (direction + magnitude when claimed)",
        f"  naive        {naive_ok}/{total}  (direction only — Slice 24 behaviour)",
        f"  embarrassed  {embarrass} scenario(s) where naive invents held on wrong magnitude",
        "",
    ]
    if embarrass >= 1 and magnet_ok == total:
        lines.append(
            "  FINDING  naive direction-only invents prediction-held when the "
            "claimed fraction is wrong; magnet misses. Title/direction is not "
            "the object — open the measured Δ."
        )
    elif magnet_ok < total:
        lines.append(
            f"  FINDING  magnet scored {magnet_ok}/{total} — magnitude grade drifted; "
            "re-check claimed_magnitude / check_prediction."
        )
    else:
        lines.append(
            "  note  no magnitude-embarrassment scenario fired — unexpected."
        )
    lines += [
        "",
        "  repro      magnet pred-demo",
        "  repro      magnet adopt skill x 'pass rate rises by 2/5' --probe demo-pass-rate --demo-bonus --reset",
    ]
    return "\n".join(lines)
