"""Adoption-log round-trip tests, plus the migration from the pre-rename database file."""
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from magnet.log import (
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


# -- the rename to log.db must not lose anyone's data ----------------------
def test_existing_pre_rename_db_is_migrated_to_log_db(tmp_path, capsys):
    """A user who ran the old build has .magnet/ledger.db. It must survive."""
    from magnet.log import connect, list_readings, record_reading

    legacy = tmp_path / "ledger.db"
    conn = connect(str(legacy))
    record_reading(conn, "p", 3, "cmd", population=5)
    conn.close()
    assert legacy.exists()

    # connecting under the new name migrates the old file in place
    new = tmp_path / "log.db"
    conn2 = connect(str(new))
    out = capsys.readouterr().out

    assert new.exists(), "log.db was not created"
    assert not legacy.exists(), "ledger.db should have been renamed, not copied"
    assert "migrated" in out, "the migration must announce itself"

    rows = list_readings(conn2, "p")
    assert len(rows) == 1 and rows[0]["value"] == 3, rows


def test_migration_never_clobbers_an_existing_log_db(tmp_path):
    """If both files exist the new one wins and the old is left for inspection."""
    from magnet.log import connect, list_readings, migrate_legacy_database, record_reading

    legacy, new = tmp_path / "ledger.db", tmp_path / "log.db"
    # create log.db FIRST, so connecting to it does not migrate anything
    c2 = connect(str(new)); record_reading(c2, "p", 9, "cmd", population=5); c2.close()
    c1 = connect(str(legacy)); record_reading(c1, "p", 1, "cmd", population=5); c1.close()
    assert legacy.exists() and new.exists()

    assert migrate_legacy_database(str(new)) is None
    assert legacy.exists(), "the old file must not be deleted"
    rows = list_readings(connect(str(new)), "p")
    assert rows[0]["value"] == 9, "existing log.db must win"


def test_old_module_name_is_gone():
    """The pre-rename module and its alias function no longer exist; magnet.log is the only name."""
    import importlib

    import pytest

    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("magnet.ledger")
    import magnet.log as log

    assert not hasattr(log, "default_ledger_path")


def test_the_word_ledger_is_gone_from_user_facing_surfaces():
    """House ruling: LOG, record or database -- never 'ledger'.

    The only survivor is the migration code, which has to name the old file.
    """
    import subprocess

    root = Path(__file__).resolve().parents[1]
    tracked = subprocess.run(
        ["git", "ls-files"], cwd=root, capture_output=True, text=True
    ).stdout.split()

    # these legitimately name the old word: the migration code, this test file,
    # and hack.md's historical LOG entry
    allowed = {"magnet/log.py", "tests/test_log.py", "hack.md"}
    offenders = {}
    for rel in tracked:
        if rel in allowed or not rel.endswith((".py", ".md", ".toml")):
            continue
        text = (root / rel).read_text(errors="ignore")
        hits = [
            ln for ln in text.splitlines()
            if "ledger" in ln.lower()
            # the word may appear ONLY where we are explaining the rename itself
            and not any(w in ln.lower() for w in ("migrat", "deprecat", "earlier build"))
        ]
        if hits:
            offenders[rel] = hits
    assert not offenders, offenders
