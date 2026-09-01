"""Probe registry — load YOUR eval commands from `.magnet/probes.json`.

Built-in probes (demo-pass-rate, check-docs, pytest-pass-rate) always exist.
The registry adds stack-specific probes without code changes.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

DEFAULT_REGISTRY = ".magnet/probes.json"

BUILTIN_PROBE_NAMES = frozenset({"demo-pass-rate", "demo", "check-docs", "pytest-pass-rate"})


def registry_path(repo_root: str | None = None) -> Path:
    root = Path(repo_root or os.getcwd())
    return root / DEFAULT_REGISTRY


def load_registry(repo_root: str | None = None) -> dict[str, dict[str, Any]]:
    """Return {probe_name: spec} from the registry file, or {} if missing."""
    path = registry_path(repo_root)
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    probes = data.get("probes", data)
    if not isinstance(probes, dict):
        raise ValueError(f"{path}: expected object at top level or under 'probes'")
    return {str(k): v for k, v in probes.items()}


def list_all_probes(repo_root: str | None = None) -> list[dict[str, Any]]:
    """Built-ins plus registry entries, re-derived at read time."""
    from magnet.probes import BUILTIN_PROBES

    out = [dict(p, source="builtin") for p in BUILTIN_PROBES]
    for name, spec in sorted(load_registry(repo_root).items()):
        if name in {p["name"] for p in out}:
            continue
        out.append(
            {
                "name": name,
                "command": spec.get("command", spec.get("shell", "")),
                "direction": spec.get("direction", "up"),
                "parser": spec.get("parser", "pytest_summary"),
                "source": "registry",
            }
        )
    return out


def run_registry_probe(name: str, spec: dict[str, Any], *, repo_root: str) -> dict:
    """Execute a registry probe's shell command and parse the output."""
    cmd = spec.get("command") or spec.get("shell")
    if not cmd:
        raise ValueError(f"registry probe {name!r} has no command")

    if isinstance(cmd, list):
        argv = [str(x) for x in cmd]
        shell = False
        shown = " ".join(argv)
    else:
        argv = cmd if isinstance(cmd, str) else str(cmd)
        shell = True
        shown = str(cmd)

    proc = subprocess.run(
        argv,
        cwd=repo_root,
        capture_output=True,
        text=True,
        shell=shell,
        timeout=spec.get("timeout", 300),
    )
    combined = (proc.stdout or "") + (proc.stderr or "")
    parser = spec.get("parser", "pytest_summary")
    value, population = _parse_output(combined, parser, proc.returncode)
    direction = spec.get("direction", "up")

    return {
        "probe_name": name,
        "value": value,
        "population": population,
        "command": shown,
        "direction": direction,
        "detail": {
            "exit_code": proc.returncode,
            "parser": parser,
            "registry": True,
        },
    }


def _parse_output(text: str, parser: str, exit_code: int) -> tuple[int | None, int | None]:
    if parser == "pytest_summary":
        return parse_pytest_summary(text)
    if parser == "value_pop":
        return parse_value_pop(text)
    if parser == "exit_code":
        # 0 -> 1/1 pass, non-zero -> 0/1
        return (1 if exit_code == 0 else 0, 1)
    if parser.startswith("regex:"):
        pattern = parser.split(":", 1)[1]
        m = re.search(pattern, text, re.M)
        if not m:
            return None, None
        if m.lastindex and m.lastindex >= 2:
            return int(m.group(1)), int(m.group(2))
        if m.lastindex == 1:
            return int(m.group(1)), None
        return None, None
    raise ValueError(f"unknown parser: {parser!r}")


def parse_pytest_summary(text: str) -> tuple[int | None, int | None]:
    """Parse pytest -q tail: '48 passed' or '45 passed, 3 failed'."""
    passed = failed = errors = 0
    tail = text.strip().splitlines()[-1] if text.strip() else ""
    for part in tail.split(","):
        part = part.strip()
        if m := re.search(r"(\d+)\s+passed", part):
            passed = int(m.group(1))
        elif m := re.search(r"(\d+)\s+failed", part):
            failed = int(m.group(1))
        elif m := re.search(r"(\d+)\s+error", part):
            errors = int(m.group(1))
    total = passed + failed + errors
    if total == 0:
        return None, None
    return passed, total


def parse_value_pop(text: str) -> tuple[int | None, int | None]:
    """Parse '4/5' or JSON {"value": 4, "population": 5}."""
    text = text.strip()
    if text.startswith("{"):
        data = json.loads(text)
        return data.get("value"), data.get("population")
    m = re.search(r"(\d+)\s*/\s*(\d+)", text)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None, None
