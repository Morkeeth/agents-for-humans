"""Tests for MAGNET reporter — baseline / helped / hurt labels."""
from magnet.reporter import format_value_pop, naive_verdict, verdict


def test_value_pop_never_bare_integer():
    assert format_value_pop(3, 5) == "3/5"
    assert format_value_pop(3, None) == "3"


def test_unmeasured_is_not_zero():
    assert format_value_pop(None, 5) == "unmeasured"


def test_first_reading_is_baseline():
    readings = [{"value": 3, "population": 5}]
    label, delta = verdict(readings, direction="up")
    assert label == "baseline"
    assert delta is None


def test_second_reading_can_be_helped():
    readings = [
        {"value": 3, "population": 5},
        {"value": 4, "population": 5},
    ]
    label, delta = verdict(readings, direction="up")
    assert label == "helped"
    assert delta == 1


def test_second_reading_can_be_hurt():
    readings = [
        {"value": 4, "population": 5},
        {"value": 3, "population": 5},
    ]
    label, delta = verdict(readings, direction="up")
    assert label == "hurt"
    assert delta == -1


def test_gap_week_does_not_fake_delta():
    """Unmeasured middle week is skipped — compare two real readings."""
    readings = [
        {"value": 2, "population": 5},
        {"value": None, "population": 5},
        {"value": 4, "population": 5},
    ]
    label, delta = verdict(readings, direction="up")
    assert label == "helped"
    assert delta == 2


def test_naive_arm_invents_helped_on_one_reading():
    readings = [{"value": 3, "population": 5}]
    assert naive_verdict(readings) == "helped"
