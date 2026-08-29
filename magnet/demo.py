"""End-to-end cold demo — no Oscar credentials, no network."""
from __future__ import annotations

import os

from magnet.ledger import connect, latest_adoption, list_readings, reset_demo
from magnet.probes import DEMO_PROBE
from magnet.reporter import naive_verdict, render_receipt, verdict
from magnet.tools import tool_adopt_change, tool_record_week


def run_demo(*, ledger_path: str | None = None, repo_root: str | None = None) -> str:
    """init empty → baseline → adopt fake skill → re-run → receipt."""
    root = repo_root or os.getcwd()
    path = ledger_path or os.path.join(root, ".magnet", "ledger.db")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    conn = connect(path)
    reset_demo(conn)

    # Week 1 — baseline reading (one measured point: naive lies, MAGNET does not)
    tool_record_week(DEMO_PROBE, ledger_path=path)
    readings_after_one = list_readings(conn, DEMO_PROBE)
    one_label, _ = verdict(readings_after_one, direction="up")
    naive_one = naive_verdict(readings_after_one)

    # Adopt a fake skill change (+1 on demo probe)
    adoption = tool_adopt_change(
        "skill",
        "demo-verification-skill",
        "pass rate rises by 1/5",
        DEMO_PROBE,
        ledger_path=path,
        apply_demo_bonus=True,
    )

    # Week 2 — post-adoption reading (next ISO week simulated via new connection read)
    from datetime import datetime, timedelta

    from magnet.ledger import record_reading
    from magnet.probes import run_demo_probe

    probe = run_demo_probe(conn)
    record_reading(
        conn,
        DEMO_PROBE,
        probe["value"],
        probe["command"],
        population=probe["population"],
        change_id=adoption["id"],
        now=datetime.now() + timedelta(days=8),
    )

    readings = list_readings(conn, DEMO_PROBE)
    label, delta = verdict(readings, direction="up")
    adoption_row = latest_adoption(conn, DEMO_PROBE)

    receipt = render_receipt(
        DEMO_PROBE,
        readings,
        direction="up",
        change_label=adoption_row["description"] if adoption_row else "",
        repro_command="magnet demo",
    )

    naive = naive_verdict(readings)
    lines = [
        receipt,
        "",
        "  after 1 reading (embarrassing case):",
        f"    naive verdict      {naive_one}  ← invents optimism",
        f"    magnet verdict     {one_label}  ← refuses to trend",
        "",
        "  after 2 readings (naive baseline arm):",
        f"    naive verdict      {naive}",
        f"    magnet verdict     {label}",
        "",
        f"  readings             {len(readings)}",
        f"  first                {readings[0]['value']}/{readings[0]['population']}",
        f"  second               {readings[1]['value']}/{readings[1]['population']}",
    ]
    return "\n".join(lines)
