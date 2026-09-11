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
    claimed_level,
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
    latest_value: int | None = None
    note: str = ""


# Ground truth is magnet's magnitude/level-aware grade. Naive is scored against the
# same truth so a direction-only hold on a wrong fraction/level counts as a naive win
# that we refuse — the embarrassment.
SCENARIOS: tuple[PredScenario, ...] = (
    PredScenario(
        "correct_fraction",
        "pass rate rises by 1/5",
        "helped",
        1,
        5,
        "prediction-held",
        latest_value=4,
        note="claim matches measured Δ +1 on pop 5",
    ),
    PredScenario(
        "wrong_magnitude",
        "pass rate rises by 2/5",
        "helped",
        1,
        5,
        "prediction-missed",
        latest_value=4,
        note="direction ok but claimed Δ +2 ≠ measured +1 — THE LIE Slice 24 printed held",
    ),
    PredScenario(
        "wrong_population",
        "coverage rises by 1/5",
        "helped",
        1,
        12,
        "prediction-missed",
        latest_value=9,
        note="Δ matches but claimed pop 5 ≠ measured 12",
    ),
    PredScenario(
        "vague_rise",
        "coverage rises",
        "helped",
        1,
        12,
        "prediction-held",
        latest_value=9,
        note="no fraction claimed — direction is the whole grade",
    ),
    PredScenario(
        "strip_fall",
        "simplify skill frontmatter",
        "hurt",
        -7,
        7,
        "prediction-held",
        latest_value=0,
        note="fall intent, no fraction — foreign-hurt titles still grade",
    ),
    PredScenario(
        "still_pass_flat",
        "all tests still pass",
        "unchanged",
        0,
        190,
        "prediction-held",
        latest_value=190,
        note="still pass → flat; judge-demo prediction becomes checkable",
    ),
    PredScenario(
        "still_pass_missed",
        "all tests still pass",
        "helped",
        1,
        5,
        "prediction-missed",
        latest_value=4,
        note="claimed flat, measured helped",
    ),
    PredScenario(
        "fall_fraction",
        "pass rate falls by 2/5",
        "hurt",
        -2,
        5,
        "prediction-held",
        latest_value=2,
        note="fall + matching magnitude",
    ),
    PredScenario(
        "stay_at_holds",
        "must stay at 4/5",
        "unchanged",
        0,
        5,
        "prediction-held",
        latest_value=4,
        note="stay-at level matches latest 4/5",
    ),
    PredScenario(
        "stay_at_wrong_level",
        "must stay at 5/5",
        "unchanged",
        0,
        5,
        "prediction-missed",
        latest_value=4,
        note="flat ok but latest 4 ≠ claimed 5 — THE LIE Slice 25 left open",
    ),
)


def run_pred_demo() -> str:
    """Print magnet vs naive_direction on magnitude/level scenarios."""
    lines = [
        "MAGNET pred-demo — magnitude + stay-at honesty vs naive direction-only",
        "",
        "  When a prediction names a fraction (rises by 1/5), magnet checks Δ.",
        "  When it names a stay-at level (must stay at 5/5), magnet checks latest.",
        "  Naive grades direction only — invents held when the claim is wrong.",
        "",
        "  scenario            claim                    Δ    pop  latest magnet              naive",
        "  " + "-" * 100,
    ]
    magnet_ok = 0
    naive_ok = 0
    embarrass = 0
    for sc in SCENARIOS:
        m = check_prediction(
            sc.prediction,
            sc.label,
            sc.delta,
            population=sc.population,
            latest_value=sc.latest_value,
        )
        n = naive_direction_check(
            sc.prediction,
            sc.label,
            sc.delta,
            population=sc.population,
            latest_value=sc.latest_value,
        )
        m_out = m["outcome"]
        n_out = n["outcome"]
        if m_out == sc.magnet_truth:
            magnet_ok += 1
        if n_out == sc.magnet_truth:
            naive_ok += 1
        if (
            sc.magnet_truth == "prediction-missed"
            and m_out == "prediction-missed"
            and n_out == "prediction-held"
        ):
            embarrass += 1
        level = claimed_level(sc.prediction)
        claim = claimed_magnitude(sc.prediction)
        if level["value"] is not None:
            claim_txt = f"stay {level['value']}/{level['population']}"
        elif claim["amount"] is not None and claim["population"] is not None:
            claim_txt = f"{claim['amount']}/{claim['population']}"
        elif claim["amount"] is not None:
            claim_txt = str(claim["amount"])
        else:
            claim_txt = prediction_intent(sc.prediction)
        delta_txt = "—" if sc.delta is None else f"{sc.delta:+d}"
        pop_txt = "—" if sc.population is None else str(sc.population)
        latest_txt = "—" if sc.latest_value is None else str(sc.latest_value)
        lines.append(
            f"  {sc.name:<20}{claim_txt:<24}{delta_txt:<5}{pop_txt:<5}"
            f"{latest_txt:<7}{m_out:<20}{n_out}"
        )

    total = len(SCENARIOS)
    lines += [
        "",
        f"  magnet       {magnet_ok}/{total}  (direction + magnitude/level when claimed)",
        f"  naive        {naive_ok}/{total}  (direction only — pre-Slice-25 behaviour)",
        f"  embarrassed  {embarrass} scenario(s) where naive invents held on wrong claim",
        "",
    ]
    if embarrass >= 1 and magnet_ok == total:
        lines.append(
            "  FINDING  naive direction-only invents prediction-held when the "
            "claimed fraction or stay-at level is wrong; magnet misses. "
            "Direction is not the object — open the measured Δ / latest value."
        )
    elif magnet_ok < total:
        lines.append(
            f"  FINDING  magnet scored {magnet_ok}/{total} — magnitude/level grade drifted; "
            "re-check claimed_magnitude / claimed_level / check_prediction."
        )
    else:
        lines.append(
            "  note  no claim-embarrassment scenario fired — unexpected."
        )
    lines += [
        "",
        "  repro      magnet pred-demo",
        "  repro      magnet adopt skill x 'pass rate rises by 2/5' --probe demo-pass-rate --demo-bonus --reset",
        "  repro      magnet adopt skill x 'must stay at 5/5' --probe demo-pass-rate --reset",
    ]
    return "\n".join(lines)
