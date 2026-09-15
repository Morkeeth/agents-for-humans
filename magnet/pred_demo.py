"""pred-demo — embarrassment arm: naive direction invents held on wrong magnitude.

Found 2026-09-11 by running:
  check_prediction("pass rate rises by 2/5", "helped", 1) → prediction-held

That was a lie. Magnet now checks the claimed fraction; the old behaviour
ships as the naive arm so a stranger can see us lose to honesty.

Slice 28: stay-at without /pop, remain/hold lexicon, floor claims.

Slice 32: recover/restore rise lexicon — Devpost one-workflow prediction
`pass rate recovers by 1` must grade, not print no-direction.

Slice 35: negation (`won't fall` was fall — invents held on drop), ceiling
(`at most 3/5`), target-level (`falls to 2/5` grades latest).
"""
from __future__ import annotations

from dataclasses import dataclass

from magnet.prediction import (
    check_prediction,
    claimed_ceiling,
    claimed_floor,
    claimed_level,
    claimed_magnitude,
    claimed_target,
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
    PredScenario(
        "stay_at_no_slash",
        "must stay at 5",
        "unchanged",
        0,
        5,
        "prediction-missed",
        latest_value=4,
        note="no /pop — Slice 26 left unparsed → invents held; now grades value",
    ),
    PredScenario(
        "remain_at_wrong",
        "must remain at 5/5",
        "unchanged",
        0,
        5,
        "prediction-missed",
        latest_value=4,
        note="remain-at was no-direction while level sat on the table",
    ),
    PredScenario(
        "hold_at_wrong",
        "hold at 190/190",
        "unchanged",
        0,
        190,
        "prediction-missed",
        latest_value=189,
        note="hold-at lexicon; latest 189 ≠ claimed 190",
    ),
    PredScenario(
        "floor_holds",
        "pass rate at least 4/5",
        "unchanged",
        0,
        5,
        "prediction-held",
        latest_value=4,
        note="floor met: latest 4 ≥ claimed 4",
    ),
    PredScenario(
        "floor_missed",
        "pass rate at least 4/5",
        "unchanged",
        0,
        5,
        "prediction-missed",
        latest_value=3,
        note="direction flat ok but latest 3 < floor 4 — naive invents held",
    ),
    PredScenario(
        "recover_held",
        "pass rate recovers by 1",
        "helped",
        1,
        244,
        "prediction-held",
        latest_value=244,
        note="DEMO-ONE-WORKFLOW restore step — was no-direction before Slice 32",
    ),
    PredScenario(
        "recover_wrong_mag",
        "pass rate recovers by 2",
        "helped",
        1,
        244,
        "prediction-missed",
        latest_value=244,
        note="recover is rise; claimed Δ +2 ≠ measured +1 — magnitude still bites",
    ),
    PredScenario(
        "restore_held",
        "coverage restores by 1",
        "helped",
        1,
        12,
        "prediction-held",
        latest_value=9,
        note="restore lexicon grades as rise with matching magnitude",
    ),
    PredScenario(
        "wont_fall_holds",
        "pass rate won't fall",
        "unchanged",
        0,
        5,
        "prediction-held",
        latest_value=4,
        note="negation → flat; unchanged holds — THE LIE was fall→missed",
    ),
    PredScenario(
        "wont_fall_missed",
        "pass rate won't fall",
        "hurt",
        -1,
        5,
        "prediction-missed",
        latest_value=3,
        note="THE LIE: old magnet graded won't-fall as fall → invents held on drop",
    ),
    PredScenario(
        "does_not_regress_holds",
        "coverage does not regress",
        "unchanged",
        0,
        12,
        "prediction-held",
        latest_value=9,
        note="does not regress → flat, not fall",
    ),
    PredScenario(
        "ceiling_holds",
        "pass rate at most 3/5",
        "unchanged",
        0,
        5,
        "prediction-held",
        latest_value=3,
        note="ceiling met: latest 3 ≤ claimed 3",
    ),
    PredScenario(
        "ceiling_missed",
        "pass rate at most 3/5",
        "unchanged",
        0,
        5,
        "prediction-missed",
        latest_value=4,
        note="latest 4 > ceiling 3 — naive invents held on flat direction",
    ),
    PredScenario(
        "falls_to_holds",
        "pass rate falls to 2/5",
        "hurt",
        -2,
        5,
        "prediction-held",
        latest_value=2,
        note="fall + target 2/5 matches latest",
    ),
    PredScenario(
        "falls_to_missed",
        "pass rate falls to 2/5",
        "hurt",
        -1,
        5,
        "prediction-missed",
        latest_value=3,
        note="direction fall ok but latest 3 ≠ target 2 — THE LIE was held",
    ),
    PredScenario(
        "reaches_holds",
        "pass rate reaches 5/5",
        "unchanged",
        0,
        5,
        "prediction-held",
        latest_value=5,
        note="target-only reaches grades latest == 5",
    ),
    PredScenario(
        "reaches_missed",
        "pass rate reaches 5/5",
        "unchanged",
        0,
        5,
        "prediction-missed",
        latest_value=4,
        note="reaches 5 with latest 4 — was no-direction before Slice 35",
    ),
    PredScenario(
        "improves_held",
        "coverage improves by 1",
        "helped",
        1,
        12,
        "prediction-held",
        latest_value=9,
        note="improves was unknown (improv stem word-boundary fail) — now rise",
    ),
)


def run_pred_demo() -> str:
    """Print magnet vs naive_direction on magnitude/level/floor/ceiling/target scenarios."""
    lines = [
        "MAGNET pred-demo — magnitude + stay-at + floor/ceiling/target honesty vs naive",
        "",
        "  When a prediction names a fraction (rises by 1/5), magnet checks Δ.",
        "  When it names a stay-at level (must stay at 5/5 or stay at 5), magnet checks latest.",
        "  When it names a floor (at least 4/5), magnet checks latest ≥ floor.",
        "  When it names a ceiling (at most 3/5), magnet checks latest ≤ ceiling.",
        "  When it names a target (falls to 2/5 / reaches 5/5), magnet checks latest.",
        "  won't fall / does not regress are flat — NOT fall (Slice 35 negation honesty).",
        "  recover/restore/regain/rebound are rise (Slice 32 — Devpost one-workflow grades).",
        "  Naive grades direction only — invents held when the claim is wrong.",
        "",
        "  scenario                 claim                    Δ    pop  latest magnet              naive",
        "  " + "-" * 104,
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
        floor = claimed_floor(sc.prediction)
        ceiling = claimed_ceiling(sc.prediction)
        target = claimed_target(sc.prediction)
        claim = claimed_magnitude(sc.prediction)
        if floor["value"] is not None:
            pop = floor["population"]
            claim_txt = (
                f"≥{floor['value']}/{pop}" if pop is not None else f"≥{floor['value']}"
            )
        elif ceiling["value"] is not None:
            pop = ceiling["population"]
            claim_txt = (
                f"≤{ceiling['value']}/{pop}"
                if pop is not None
                else f"≤{ceiling['value']}"
            )
        elif target["value"] is not None:
            pop = target["population"]
            claim_txt = (
                f"to {target['value']}/{pop}"
                if pop is not None
                else f"to {target['value']}"
            )
        elif level["value"] is not None:
            pop = level["population"]
            claim_txt = (
                f"stay {level['value']}/{pop}"
                if pop is not None
                else f"stay {level['value']}"
            )
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
            f"  {sc.name:<25}{claim_txt:<24}{delta_txt:<5}{pop_txt:<5}"
            f"{latest_txt:<7}{m_out:<20}{n_out}"
        )

    total = len(SCENARIOS)
    lines += [
        "",
        f"  magnet       {magnet_ok}/{total}  (direction + magnitude/level/floor/ceiling/target)",
        f"  naive        {naive_ok}/{total}  (direction only — pre-Slice-25 behaviour)",
        f"  embarrassed  {embarrass} scenario(s) where naive invents held on wrong claim",
        "",
    ]
    if embarrass >= 1 and magnet_ok == total:
        lines.append(
            "  FINDING  naive direction-only invents prediction-held when the "
            "claimed fraction, stay-at level, floor, ceiling, or target is wrong; "
            "magnet misses. Direction is not the object — open the measured Δ / latest. "
            "Negation (`won't fall`) is flat — inventing fall was the Slice 35 lie."
        )
    elif magnet_ok < total:
        lines.append(
            f"  FINDING  magnet scored {magnet_ok}/{total} — bound grade drifted; "
            "re-check claimed_* / check_prediction."
        )
    else:
        lines.append(
            "  note  no claim-embarrassment scenario fired — unexpected."
        )
    lines += [
        "",
        "  repro      magnet pred-demo",
        "  repro      magnet adopt skill x 'pass rate rises by 2/5' --probe demo-pass-rate --demo-bonus --reset",
        "  repro      magnet adopt skill x 'must stay at 5' --probe demo-pass-rate --reset",
        "  repro      magnet adopt skill x 'at least 4/5' --probe demo-pass-rate --reset",
        "  repro      magnet adopt skill x 'at most 3/5' --probe demo-pass-rate --reset",
        "  repro      magnet adopt skill x \"won't fall\" --probe demo-pass-rate --reset",
        "  repro      magnet adopt skill x 'falls to 2/5' --probe demo-pass-rate --reset",
    ]
    return "\n".join(lines)
