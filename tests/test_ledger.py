"""Ledger round-trip tests."""
from datetime import datetime, timedelta

import pytest

from magnet.ledger import (
    adopt_change,
    connect,
    list_readings,
    record_reading,
    reset_demo,
)


@pytest.fixture
def conn(tmp_path):
    db = tmp_path / "ledger.db"
    c = connect(str(db))
    reset_demo(c)
    return c


def test_record_and_list_round_trip(conn):
    record_reading(
        conn,
        "demo-pass-rate",
        3,
        "magnet probe demo-pass-rate",
        population=5,
    )
    rows = list_readings(conn, "demo-pass-rate")
    assert len(rows) == 1
    assert rows[0]["value"] == 3
    assert rows[0]["population"] == 5


def test_same_week_replaces_not_appends(conn):
    now = datetime(2026, 8, 16)
    record_reading(conn, "demo-pass-rate", 1, "cmd", population=5, now=now)
    record_reading(conn, "demo-pass-rate", 4, "cmd", population=5, now=now + timedelta(hours=1))
    rows = list_readings(conn, "demo-pass-rate")
    assert len(rows) == 1
    assert rows[0]["value"] == 4


def test_adopt_change_links_to_probe(conn):
    adoption = adopt_change(
        conn,
        "skill",
        "test-skill",
        "pass rate up",
        "demo-pass-rate",
    )
    record_reading(
        conn,
        "demo-pass-rate",
        4,
        "cmd",
        population=5,
        change_id=adoption["id"],
    )
    row = list_readings(conn, "demo-pass-rate")[0]
    assert row["change_id"] == adoption["id"]
