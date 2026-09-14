"""Machine-readable adoption receipt — verify without inventing numbers.

A stranger (or Agent Grinder) can check value/pop/command/verdict at the object.
No network for the JSON print; `--verify` re-runs the probe at the object and
compares. A receipt that only reads SQLite can lie forever after the world moves.
"""
from __future__ import annotations

import json
import os
from typing import Any

from magnet.history import list_adoptions, readings_for_adoption
from magnet.log import connect, default_log_path, list_readings
from magnet.prediction import check_prediction, claimed_level, claimed_magnitude
from magnet.probes import run_probe
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
            "repro": "magnet receipt",
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
            latest_value=(latest or {}).get("value"),
        )
    claim = claimed_magnitude(prediction_text or "") if prediction_text else None
    level = claimed_level(prediction_text or "") if prediction_text else None
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
        "claimed_level": level,
        "repro": "magnet receipt" + (f" --probe {probe}" if probe else ""),
    }


def verify_receipt(
    conn,
    *,
    probe_name: str | None = None,
    adoption_id: int | None = None,
    repo_root: str | None = None,
    stack_dir: str | None = None,
    receipt: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Re-run the probe at the object; compare value/pop to the stored receipt.

    Returns:
      ok            bool — True only when stored value+pop match the live probe
      mismatches    list[str]
      stored        {value, population, command}
      live          {value, population, command}
      note          always names the probe command that was re-run
    """
    payload = receipt or build_receipt(
        conn, probe_name=probe_name, adoption_id=adoption_id
    )
    probe = payload.get("probe")
    latest = payload.get("latest") or {}
    if not probe or latest.get("value") is None:
        return {
            "ok": False,
            "mismatches": ["no stored reading to verify"],
            "stored": latest or None,
            "live": None,
            "probe": probe,
            "note": "verify needs a stored value/pop — run magnet adopt or magnet record first",
        }

    live = run_probe(
        conn,
        probe,
        repo_root=repo_root or os.getcwd(),
        stack_dir=stack_dir,
    )
    mismatches: list[str] = []
    if live.get("value") != latest.get("value"):
        mismatches.append(
            f"value stored={latest.get('value')} live={live.get('value')}"
        )
    if live.get("population") != latest.get("population"):
        mismatches.append(
            f"population stored={latest.get('population')} live={live.get('population')}"
        )

    ok = not mismatches
    live_vp = format_value_pop(live.get("value"), live.get("population"))
    stored_vp = latest.get("value_pop") or format_value_pop(
        latest.get("value"), latest.get("population")
    )
    return {
        "ok": ok,
        "mismatches": mismatches,
        "stored": {
            "value": latest.get("value"),
            "population": latest.get("population"),
            "value_pop": stored_vp,
            "command": latest.get("command"),
        },
        "live": {
            "value": live.get("value"),
            "population": live.get("population"),
            "value_pop": live_vp,
            "command": live.get("command"),
        },
        "probe": probe,
        "note": (
            f"verify GREEN: live {live_vp} matches stored {stored_vp}"
            if ok
            else (
                "verify RED: live probe disagrees with stored receipt — "
                + "; ".join(mismatches)
                + f" (command: {live.get('command')})"
            )
        ),
    }


def render_receipt_json(
    *,
    log_path: str | None = None,
    probe_name: str | None = None,
    adoption_id: int | None = None,
    verify: bool = False,
    repo_root: str | None = None,
    stack_dir: str | None = None,
) -> tuple[str, int]:
    """Return (json_text, exit_code). exit_code 1 when --verify finds drift."""
    conn = connect(log_path or default_log_path(), announce=False)
    payload = build_receipt(conn, probe_name=probe_name, adoption_id=adoption_id)
    if payload.get("tag_vocab_version") is None:
        payload.pop("tag_vocab_version", None)
    exit_code = 0
    if verify:
        check = verify_receipt(
            conn,
            probe_name=probe_name,
            adoption_id=adoption_id,
            repo_root=repo_root,
            stack_dir=stack_dir,
            receipt=payload,
        )
        payload["verify"] = check
        if not check["ok"]:
            exit_code = 1
    return json.dumps(payload, indent=2, sort_keys=False), exit_code


# Grinder COUNT_FIELDS we must NEVER invent (opened at Agent Grinder contract.py).
_GRINDER_COUNT_FIELDS = (
    "turns_typed",
    "tool_calls",
    "files_touched",
    "commits",
    "claims",
    "claims_verified",
    "artifacts_produced",
)


def build_grinder_evidence(
    conn,
    *,
    probe_name: str | None = None,
    adoption_id: int | None = None,
    repo_root: str | None = None,
    stack_dir: str | None = None,
    require_verify: bool = True,
) -> dict[str, Any]:
    """Evidence sidecar for Agent Grinder — magnet numbers only, no grind counts.

    Opens the probe via verify. Never sets turns_typed / claims_verified / etc.
    A prediction-held is correlation, not attribution — the note says so.
    """
    receipt = build_receipt(conn, probe_name=probe_name, adoption_id=adoption_id)
    if receipt.get("tag_vocab_version") is None:
        receipt.pop("tag_vocab_version", None)
    check = verify_receipt(
        conn,
        probe_name=probe_name,
        adoption_id=adoption_id,
        repo_root=repo_root,
        stack_dir=stack_dir,
        receipt=receipt,
    )
    receipt["verify"] = check
    pred = receipt.get("prediction_check") or {}
    change = receipt.get("change") or {}
    latest = receipt.get("latest") or {}
    evidence = {
        "schema": "magnet.grinder-evidence/v1",
        "magnet_receipt": receipt,
        "prediction": change.get("prediction"),
        "prediction_outcome": pred.get("outcome"),
        "prediction_intent": pred.get("intent"),
        "verdict": receipt.get("verdict"),
        "value_pop": latest.get("value_pop"),
        "command": (check.get("live") or {}).get("command") or latest.get("command"),
        "verify_ok": check.get("ok"),
        "note": (
            "MAGNET grades correlation, not attribution. "
            "Do not invent Agent Grinder COUNT_FIELDS from this file. "
            "Re-run: magnet receipt --grinder"
        ),
        "repro": "magnet receipt --grinder",
    }
    # Explicit refusal: never copy grind count keys even as null (avoids
    # validate_run inventing a partial grind).
    for banned in _GRINDER_COUNT_FIELDS:
        if banned in evidence:
            raise RuntimeError(f"grinder evidence must not carry {banned}")
    if require_verify and not check.get("ok"):
        evidence["exportable"] = False
        evidence["note"] = (
            "verify RED — refuse export to Grinder until live probe matches stored. "
            + str(check.get("note"))
        )
    else:
        evidence["exportable"] = bool(check.get("ok"))
    return evidence


def render_grinder_evidence_json(
    *,
    log_path: str | None = None,
    probe_name: str | None = None,
    adoption_id: int | None = None,
    repo_root: str | None = None,
    stack_dir: str | None = None,
) -> tuple[str, int]:
    conn = connect(log_path or default_log_path(), announce=False)
    evidence = build_grinder_evidence(
        conn,
        probe_name=probe_name,
        adoption_id=adoption_id,
        repo_root=repo_root,
        stack_dir=stack_dir,
        require_verify=True,
    )
    code = 0 if evidence.get("exportable") else 1
    return json.dumps(evidence, indent=2, sort_keys=False), code


def render_verify_human(check: dict[str, Any]) -> str:
    lines = [
        "MAGNET receipt verify",
        "",
        f"  probe      {check.get('probe')}",
        f"  stored     {(check.get('stored') or {}).get('value_pop', '—')}",
        f"  live       {(check.get('live') or {}).get('value_pop', '—')}",
        f"  result     {'GREEN' if check.get('ok') else 'RED'}",
        f"  note       {check.get('note')}",
    ]
    if check.get("live") and check["live"].get("command"):
        lines.append(f"  command    {check['live']['command']}")
    lines.append("  repro      magnet receipt --verify")
    return "\n".join(lines)


def run_receipt_demo(
    *,
    log_path: str | None = None,
    repo_root: str | None = None,
) -> str:
    """Embarrassment arm: verify GREEN on live receipt, RED after planted drift."""
    from magnet.adopt import run_adopt
    from magnet.log import connect as log_connect

    path = log_path or os.path.join(os.getcwd(), ".magnet", "receipt-demo.db")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    lines = [
        "MAGNET receipt-demo — Grinder bridge: re-probe vs stored receipt",
        "",
        "  A JSON receipt that only reads SQLite can lie after the world moves.",
        "  --verify re-runs the probe at the object. Planted drift must go RED.",
        "",
    ]

    run_adopt(
        "skill",
        "receipt-demo-skill",
        "pass rate recovers by 1",
        "demo-pass-rate",
        log_path=path,
        apply_demo_bonus=True,
        reset=True,
    )
    conn = log_connect(path, announce=False)
    green = verify_receipt(conn, repo_root=repo_root or os.getcwd())
    lines.append(
        f"  arm GREEN  stored={green['stored']['value_pop']}  "
        f"live={green['live']['value_pop']}  ok={green['ok']}"
    )

    # Plant drift: corrupt the latest reading value in SQLite (not the live probe).
    cur = conn.execute(
        "SELECT id, value FROM probe_readings ORDER BY id DESC LIMIT 1"
    )
    row = cur.fetchone()
    if row is None:
        lines.append("  FINDING  no reading to corrupt — unexpected")
        return "\n".join(lines)
    rid, old_val = row[0], row[1]
    planted = int(old_val) + 99 if old_val is not None else 99
    conn.execute("UPDATE probe_readings SET value = ? WHERE id = ?", (planted, rid))
    conn.commit()

    red = verify_receipt(conn, repo_root=repo_root or os.getcwd())
    lines.append(
        f"  arm RED    stored={red['stored']['value_pop']}  "
        f"live={red['live']['value_pop']}  ok={red['ok']}"
    )
    lines.append("")
    if green["ok"] and (not red["ok"]):
        lines.append(
            "  FINDING  verify goes GREEN on a live receipt and RED when the "
            "stored value is planted wrong — Grinder can refuse a stale receipt."
        )
    else:
        lines.append(
            f"  FINDING  verify arms drifted green_ok={green['ok']} red_ok={red['ok']} "
            "— open verify_receipt / probe_readings."
        )
    lines += [
        "",
        "  repro      magnet receipt-demo",
        "  repro      magnet receipt --verify",
    ]
    return "\n".join(lines)
