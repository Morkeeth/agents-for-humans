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
TOOLS_PROBE = "tools-coverage"
HOOK_PROBE = "hook-coverage"
PROMPT_PROBE = "prompt-consistency"

STACK_BIND_PROBES = frozenset(
    {
        EFFORT_PROBE,
        DENY_PROBE,
        TOOLS_PROBE,
        HOOK_PROBE,
        PROMPT_PROBE,
        "stack-coverage",
    }
)

_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n?", re.S)
_EFFORT_KEY = re.compile(r"^effort\s*:", re.M | re.I)
_ALLOWED_TOOLS_KEY = re.compile(r"^allowed-tools\s*:", re.M | re.I)
_MUST_LINE = re.compile(r"^MUST:\s*.+$", re.M)

# Hook hardening signals — open settings.json + hooks/, never a title.
HOOK_SIGNALS = (
    "dangerous-actions-blocker",
    "no-rm-rf-star-allow",
)

DANGEROUS_ALLOW = "Bash(rm -rf *)"
BLOCKER_SCRIPT = "dangerous-actions-blocker.sh"


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


def skill_has_allowed_tools(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = _FRONTMATTER.match(text)
    if not m:
        return False
    return bool(_ALLOWED_TOOLS_KEY.search(m.group(1)))


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


def tools_coverage(stack_dir: str) -> dict:
    """skills with allowed-tools: frontmatter / total skills — UG item 3."""
    paths = list_skill_paths(stack_dir)
    total = len(paths)
    with_tools = [p for p in paths if skill_has_allowed_tools(p)]
    missing = [p.parent.name for p in paths if not skill_has_allowed_tools(p)]
    return {
        "probe_name": TOOLS_PROBE,
        "value": len(with_tools),
        "population": total,
        "command": f"magnet probe {TOOLS_PROBE} --stack {stack_dir}",
        "direction": "up",
        "detail": {
            "stack": stack_dir,
            "with_allowed_tools": [p.parent.name for p in with_tools],
            "missing_allowed_tools": missing,
            "object": "SKILL.md allowed-tools frontmatter",
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


def _load_settings(stack_dir: str) -> dict:
    settings_path = Path(os.path.expanduser(stack_dir)) / "settings.json"
    if not settings_path.is_file():
        return {}
    try:
        return json.loads(settings_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


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


def _hook_signal_present(stack_dir: str, signal: str) -> bool:
    root = Path(os.path.expanduser(stack_dir))
    blob = _settings_blob(stack_dir)
    if signal == "dangerous-actions-blocker":
        script = root / "hooks" / BLOCKER_SCRIPT
        return BLOCKER_SCRIPT in blob or script.is_file()
    if signal == "no-rm-rf-star-allow":
        data = _load_settings(stack_dir)
        allow = [str(a) for a in ((data.get("permissions") or {}).get("allow") or [])]
        # Open the allow list itself — title "hardened" does not count.
        return DANGEROUS_ALLOW not in allow and not any(
            "rm -rf *" in a for a in allow
        )
    return False


def hook_coverage(stack_dir: str) -> dict:
    """UG item 5 — blocker hook present + Bash(rm -rf *) absent from allow."""
    present = [s for s in HOOK_SIGNALS if _hook_signal_present(stack_dir, s)]
    missing = [s for s in HOOK_SIGNALS if s not in present]
    return {
        "probe_name": HOOK_PROBE,
        "value": len(present),
        "population": len(HOOK_SIGNALS),
        "command": f"magnet probe {HOOK_PROBE} --stack {stack_dir}",
        "direction": "up",
        "detail": {
            "stack": stack_dir,
            "present": present,
            "missing": missing,
            "object": "settings.json hooks + permissions.allow",
        },
    }


def _claude_must_lines(stack_dir: str) -> list[str]:
    path = Path(os.path.expanduser(stack_dir)) / "CLAUDE.md"
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    return [m.group(0).strip() for m in _MUST_LINE.finditer(text)]


def _post_compact_text(stack_dir: str) -> str:
    path = Path(os.path.expanduser(stack_dir)) / "post-compact-reinject.txt"
    if not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def prompt_consistency(stack_dir: str) -> dict:
    """UG item 4 — CLAUDE.md MUST lines that also appear in post-compact-reinject.

    Opens both files. A title claiming 'aligned prompts' does not score.
    """
    musts = _claude_must_lines(stack_dir)
    blob = _post_compact_text(stack_dir)
    present = [m for m in musts if m in blob]
    missing = [m for m in musts if m not in blob]
    return {
        "probe_name": PROMPT_PROBE,
        "value": len(present),
        "population": len(musts),
        "command": f"magnet probe {PROMPT_PROBE} --stack {stack_dir}",
        "direction": "up",
        "detail": {
            "stack": stack_dir,
            "present": present,
            "missing": missing,
            "claude_present": bool(musts),
            "post_compact_present": bool(blob),
            "object": "CLAUDE.md vs post-compact-reinject.txt",
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


def apply_allowed_tools_frontmatter(
    stack_dir: str, *, tools: str = "Read, Grep, Glob"
) -> list[str]:
    """Write allowed-tools: into every SKILL.md missing it (UG item 3)."""
    touched: list[str] = []
    for path in list_skill_paths(stack_dir):
        if skill_has_allowed_tools(path):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        m = _FRONTMATTER.match(text)
        if not m:
            new = f"---\nallowed-tools: {tools}\n---\n{text}"
        else:
            body = m.group(1).rstrip() + f"\nallowed-tools: {tools}\n"
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


def apply_hook_hardening(stack_dir: str) -> list[str]:
    """UG item 5 — drop Bash(rm -rf *) allow; add dangerous-actions-blocker hook."""
    root = Path(os.path.expanduser(stack_dir))
    applied: list[str] = []
    hooks_dir = root / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    blocker = hooks_dir / BLOCKER_SCRIPT
    if not blocker.is_file():
        blocker.write_text(
            "#!/usr/bin/env bash\n"
            "# Blocks destructive bash patterns — Ultimate Guide security-hardening.\n"
            "exit 0\n",
            encoding="utf-8",
        )
        applied.append("wrote-blocker-script")

    data = _load_settings(stack_dir)
    perms = data.setdefault("permissions", {})
    allow = [a for a in (perms.get("allow") or []) if str(a) != DANGEROUS_ALLOW]
    if allow != list(perms.get("allow") or []):
        applied.append("removed-rm-rf-star-allow")
    perms["allow"] = allow
    data["permissions"] = perms

    hooks = data.setdefault("hooks", {})
    pre = list(hooks.get("PreToolUse") or [])
    blob = json.dumps(data)
    if BLOCKER_SCRIPT not in blob:
        pre.append(
            {
                "matcher": "Bash",
                "hooks": [
                    {
                        "type": "command",
                        "command": f"hooks/{BLOCKER_SCRIPT}",
                    }
                ],
            }
        )
        applied.append("wired-blocker-hook")
    hooks["PreToolUse"] = pre
    data["hooks"] = hooks

    settings_path = root / "settings.json"
    settings_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return applied


def apply_prompt_consistency(stack_dir: str) -> list[str]:
    """UG item 4 — rewrite post-compact-reinject.txt from CLAUDE.md MUST lines."""
    musts = _claude_must_lines(stack_dir)
    if not musts:
        return []
    path = Path(os.path.expanduser(stack_dir)) / "post-compact-reinject.txt"
    body = (
        "# Reinjected after compact — aligned to CLAUDE.md MUST lines\n"
        + "\n".join(musts)
        + "\n"
    )
    path.write_text(body, encoding="utf-8")
    return list(musts)


def copy_stack(src: str, dest: str) -> str:
    """Deep-copy a stack directory for bind-demo mutation (never touch source)."""
    dest_path = Path(dest)
    if dest_path.exists():
        shutil.rmtree(dest_path)
    shutil.copytree(src, dest_path)
    return str(dest_path)
