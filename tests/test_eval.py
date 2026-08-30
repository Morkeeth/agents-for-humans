"""Eval harness — naive vs magnet vs silent_null."""
from magnet.eval import SCENARIOS, run_eval, silent_null_verdict
from magnet.reporter import naive_verdict, verdict


def test_silent_null_always_baseline():
    for sc in SCENARIOS:
        assert silent_null_verdict(sc.readings) == "baseline"


def test_naive_wrong_on_one_reading():
    sc = next(s for s in SCENARIOS if s.name == "one_reading")
    assert naive_verdict(sc.readings) == "helped"
    assert sc.truth == "baseline"


def test_naive_wrong_on_unchanged():
    sc = next(s for s in SCENARIOS if s.name == "unchanged")
    assert naive_verdict(sc.readings) == "helped"
    assert verdict(sc.readings)[0] == "unchanged"


def test_magnet_beats_naive_on_scenarios():
    naive_correct = magnet_correct = 0
    for sc in SCENARIOS:
        n = naive_verdict(sc.readings)
        m = verdict(sc.readings, direction=sc.direction)[0]
        if n == sc.truth:
            naive_correct += 1
        if m == sc.truth:
            magnet_correct += 1
    assert magnet_correct > naive_correct


def test_eval_output_names_all_scenarios():
    out = run_eval()
    for sc in SCENARIOS:
        assert sc.name in out
    assert "arm scores" in out
    assert "repro        magnet eval" in out
