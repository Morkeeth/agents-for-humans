"""Stack-bind probes — open YOUR stack object, not the repo proxy.

The Ultimate Guide audit (docs/ULTIMATE-GUIDE-MAGNET-2026-09-02.md) found that
repo probes (pytest-pass-rate, check-docs, demo-pass-rate) cannot see hook /
setting / skill-frontmatter changes. These probes open the stack directory
itself and re-derive value/pop from the files on disk.

Sensitive patterns and frontmatter keys are named here — never ranked by
skill title.
"""
from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path

# Patterns the Ultimate Guide says a hardened stack should deny.
# Re-derived at probe time from settings.json — never carried as a score.
SENSITIVE_DENY_PATTERNS = (".env", ".pem", ".key", "credentials")

EFFORT_PROBE = "effort-coverage"
DENY_PROBE = "deny-coverage"

STACK_BIND_PROBES = frozenset({EFFORT_PROBE, DENY_PROBE, "stack-coverage"})

_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n?", re.S)
_EFFORT_KEY = re.compile(r"^effort\s*:", re.M | re.I)


def list_skill_paths(stack_dir: str) -> list[Path]:
    """SKILL.md paths under stack/skills/*/ — same layout inventory() uses."""
    root = Path(os.path.expanduser(stack_dir))
    skills = root / "skills"
    if not skills.is_dir():
        return []
    out: list[Path] = []
    for child in sorted(skills.iterdir()):
        path = child / "SKILL.md"
        if path.is_file():
            out.append(path)
    return out


def skill_has_effort(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = _FRONTMATTER.match(text)
    if not m:
        return False
    return bool(_EFFORT_KEY.search(m.group(1)))


def effort_coverage(stack_dir: str) -> dict:
    """skills with effort: frontmatter / total skills — re-derived from disk."""
    paths = list_skill_paths(stack_dir)
    total = len(paths)
    with_effort = [p for p in paths if skill_has_effort(p)]
    value = len(with_effort)
    missing = [p.parent.name for p in paths if not skill_has_effort(p)]
    return {
        "probe_name": EFFORT_PROBE,
        "value": value,
        "population": total,
        "command": f"magnet probe {EFFORT_PROBE} --stack {stack_dir}",
        "direction": "up",
        "detail": {
            "stack": stack_dir,
            "with_effort": [p.parent.name for p in with_effort],
            "missing_effort": missing,
            "object": "SKILL.md frontmatter",
        },
    }


def _settings_blob(stack_dir: str) -> str:
    settings = Path(os.path.expanduser(stack_dir)) / "settings.json"
    if not settings.is_file():
        return ""
    try:
        return settings.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def deny_coverage(stack_dir: str) -> dict:
    """Sensitive patterns present in settings deny rules / expected set.

    Opens settings.json (or returns 0/N if missing). Looks for each pattern
    as a literal substring in the settings text — the object, not a title.
    """
    blob = _settings_blob(stack_dir)
    present = [p for p in SENSITIVE_DENY_PATTERNS if p in blob]
    missing = [p for p in SENSITIVE_DENY_PATTERNS if p not in blob]
    return {
        "probe_name": DENY_PROBE,
        "value": len(present),
        "population": len(SENSITIVE_DENY_PATTERNS),
        "command": f"magnet probe {DENY_PROBE} --stack {stack_dir}",
        "direction": "up",
        "detail": {
            "stack": stack_dir,
            "present": present,
            "missing": missing,
            "settings_present": bool(blob),
            "object": "settings.json deny patterns",
        },
    }


def apply_effort_frontmatter(stack_dir: str, *, value: str = "medium") -> list[str]:
    """Write effort: into every SKILL.md missing it. Returns names touched."""
    touched: list[str] = []
    for path in list_skill_paths(stack_dir):
        if skill_has_effort(path):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        m = _FRONTMATTER.match(text)
        if not m:
            # No frontmatter — wrap the file.
            new = f"---\neffort: {value}\n---\n{text}"
        else:
            body = m.group(1).rstrip() + f"\neffort: {value}\n"
            new = f"---\n{body}---\n" + text[m.end() :]
        path.write_text(new, encoding="utf-8")
        touched.append(path.parent.name)
    return touched


def apply_deny_patterns(stack_dir: str) -> list[str]:
    """Add permissions.deny entries for missing sensitive patterns."""
    root = Path(os.path.expanduser(stack_dir))
    settings_path = root / "settings.json"
    if settings_path.is_file():
        try:
            data = json.loads(settings_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            data = {}
    else:
        data = {}
    perms = data.setdefault("permissions", {})
    deny = list(perms.get("deny") or [])
    added: list[str] = []
    blob = json.dumps(data)
    for pattern in SENSITIVE_DENY_PATTERNS:
        if pattern in blob or any(pattern in str(d) for d in deny):
            continue
        entry = f"Read(**/{pattern})"
        deny.append(entry)
        added.append(pattern)
    perms["deny"] = deny
    data["permissions"] = perms
    settings_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return added


def copy_stack(src: str, dest: str) -> str:
    """Deep-copy a stack directory for bind-demo mutation (never touch source)."""
    dest_path = Path(dest)
    if dest_path.exists():
        shutil.rmtree(dest_path)
    shutil.copytree(src, dest_path)
    return str(dest_path)
