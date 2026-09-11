"""Machine-readable adoption receipt — verify without inventing numbers.

A stranger (or Agent Grinder) can check value/pop/command/verdict at the object.
No network; reads the local SQLite log only.
"""
from __future__ import annotations

import json
from typing import Any

from magnet.history import list_adoptions, readings_for_adoption
from magnet.log import connect, default_log_path, list_readings
from magnet.prediction import check_prediction, claimed_magnitude
from magnet.reporter import format_value_pop, verdict


def build_receipt(
    conn,
    *,
    probe_name: str | None = None,
    adoption_id: int | None = None,
) -> dict[str, Any]:
    """Build one receipt dict from the log. Numbers come from stored readings."""
    adoptions = list_adoptions(conn, probe_name=probe_name)
    row = None
    if adoption_id is not None:
        row = next((a for a in adoptions if a["id"] == adoption_id), None)
        if row is None:
            raise ValueError(f"no adoption id={adoption_id}")
    elif adoptions:
        row = adoptions[-1]  # latest by recorded_at ascending list

    probe = (row or {}).get("probe_name") or probe_name
    if not probe:
        for name in ("demo-pass-rate", "stack-coverage", "pytest-pass-rate"):
            if list_readings(conn, name):
                probe = name
                break

    if not probe:
        return {
            "schema": "magnet.receipt/v1",
            "probe": None,
            "change": None,
            "latest": None,
            "verdict": "baseline",
            "delta": None,
            "readings": 0,
            "repro": "magnet receipt --json",
        }

    series = list_readings(conn, probe)
    if row is not None:
        series = readings_for_adoption(series, row["id"])

    label, delta = verdict(series, direction="up") if series else ("baseline", None)
    measured = [r for r in series if r.get("value") is not None]
    latest = measured[-1] if measured else None
    prediction_text = (row or {}).get("prediction")
    pred_stored = ((row or {}).get("detail") or {}).get("prediction_check")
    if pred_stored is None and prediction_text:
        pred_stored = check_prediction(
            prediction_text,
            label,
            delta,
            population=(latest or {}).get("population"),
        )
    claim = claimed_magnitude(prediction_text or "") if prediction_text else None
    return {
        "schema": "magnet.receipt/v1",
        "probe": probe,
        "tag_vocab_version": None,  # filled by caller for stack receipts if needed
        "change": None
        if row is None
        else {
            "id": row["id"],
            "type": row.get("change_type"),
            "description": row.get("description"),
            "prediction": row.get("prediction"),
            "recorded_at": row.get("recorded_at"),
        },
        "latest": None
        if latest is None
        else {
            "value": latest.get("value"),
            "population": latest.get("population"),
            "value_pop": format_value_pop(latest.get("value"), latest.get("population")),
            "command": latest.get("command"),
            "recorded_at": latest.get("recorded_at") or latest.get("read_at"),
            "simulated": bool((latest.get("detail") or {}).get("simulated")),
        },
        "verdict": label,
        "delta": delta,
        "readings": len(measured),
        "prediction_check": pred_stored,
        "claimed_magnitude": claim,
        "repro": "magnet receipt" + (f" --probe {probe}" if probe else ""),
    }


def render_receipt_json(
    *,
    log_path: str | None = None,
    probe_name: str | None = None,
    adoption_id: int | None = None,
) -> str:
    conn = connect(log_path or default_log_path(), announce=False)
    payload = build_receipt(conn, probe_name=probe_name, adoption_id=adoption_id)
    # Drop null tag_vocab unless set
    if payload.get("tag_vocab_version") is None:
        payload.pop("tag_vocab_version", None)
    return json.dumps(payload, indent=2, sort_keys=False)
