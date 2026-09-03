"""Apply a skill into a measured stack — so stack-coverage can actually move.

Found 2026-09-03 by running:
  magnet adopt skill pdb-navigator … --fit --probe stack-coverage
→ fit said fills-gap (debug); coverage stayed 8/12 unchanged.
Adopt only wrote SQLite. The stack filesystem — the object the probe opens —
was never touched. This module writes the skill into that object.
"""
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path


_SLUG = re.compile(r"[^a-z0-9-]+")


def skill_slug(name: str) -> str:
    """Filesystem-safe skill directory name. Never ranks; only names a path."""
    s = (name or "").strip().lower().replace(" ", "-").replace("_", "-")
    s = _SLUG.sub("-", s).strip("-")
    return s or "unnamed-skill"


def skill_dir(stack_dir: str, name: str) -> Path:
    return Path(os.path.expanduser(stack_dir)) / "skills" / skill_slug(name)


def apply_skill(
    stack_dir: str,
    name: str,
    description: str,
    *,
    capabilities: list[str] | None = None,
    body: str | None = None,
) -> dict:
    """Write skills/<slug>/SKILL.md into stack_dir. Returns what was written.

    Overwrites an existing skill of the same slug. Does not touch secrets,
    settings values, or anything outside skills/<slug>/.
    """
    root = Path(os.path.expanduser(stack_dir))
    dest = skill_dir(stack_dir, name)
    dest.mkdir(parents=True, exist_ok=True)
    caps = [str(c).strip().lower() for c in (capabilities or []) if str(c).strip()]
    desc = (description or "").strip() or name
    # Keep description on one frontmatter line (inventory parser is line-oriented).
    desc_line = " ".join(desc.splitlines()).replace('"', "'")[:400]
    lines = ["---", f"name: {skill_slug(name)}", f"description: {desc_line}"]
    if caps:
        lines.append(f"capabilities: [{', '.join(caps)}]")
    lines.append("---")
    lines.append(body.strip() if body else desc_line)
    lines.append("")
    path = dest / "SKILL.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return {
        "applied": True,
        "name": skill_slug(name),
        "path": str(path),
        "stack": str(root),
        "capabilities": caps,
        "description": desc_line,
    }


def remove_skill(stack_dir: str, name: str) -> dict:
    """Remove skills/<slug>/ if present. Used by demos that must not pollute fixtures."""
    dest = skill_dir(stack_dir, name)
    if not dest.exists():
        return {"removed": False, "name": skill_slug(name), "path": str(dest)}
    shutil.rmtree(dest)
    return {"removed": True, "name": skill_slug(name), "path": str(dest)}


def copy_stack(src: str, dest: str) -> str:
    """Copy a stack tree for isolated apply demos (never mutate committed fixtures)."""
    src_p = Path(os.path.expanduser(src))
    dest_p = Path(os.path.expanduser(dest))
    if dest_p.exists():
        shutil.rmtree(dest_p)
    shutil.copytree(src_p, dest_p)
    return str(dest_p)
