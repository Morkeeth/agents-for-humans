"""Apply a candidate skill onto a writable copy of YOUR stack.

The ranking / fit layer answers "would this fill a gap?". Apply closes the loop:
write the skill into a working stack, then re-probe. The fixture stack under
`fixtures/stack` is never mutated — every apply materializes a copy first.

Safety model (ported in spirit from helicon.writeback):
  - dry-run is the default (adopt without --apply never writes)
  - --apply writes only into an explicit dest or `.magnet/applied-stack`
  - source fixture / ~/.claude is never the write target of --apply
"""
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

_SLUG = re.compile(r"[^a-z0-9]+")


def skill_slug(name: str) -> str:
    slug = _SLUG.sub("-", (name or "").strip().lower()).strip("-")
    return slug or "unnamed-skill"


def default_apply_dest(repo_root: str | None = None) -> str:
    root = Path(repo_root or os.getcwd())
    return str(root / ".magnet" / "applied-stack")


def materialize_working_stack(source: str, dest: str) -> str:
    """Copy `source` → `dest` (replace). Returns dest path."""
    src = Path(os.path.expanduser(source))
    dst = Path(os.path.expanduser(dest))
    if not src.is_dir():
        raise FileNotFoundError(f"stack source not found: {src}")
    if dst.resolve() == src.resolve():
        raise ValueError(
            "refuse to apply in-place onto the source stack; pass a distinct --apply-dest"
        )
    if dst.exists():
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)
    return str(dst)


def write_skill(
    stack_dir: str,
    name: str,
    description: str,
    *,
    body: str | None = None,
) -> dict:
    """Write skills/<slug>/SKILL.md into stack_dir. Returns path + slug."""
    slug = skill_slug(name)
    skill_dir = Path(stack_dir) / "skills" / slug
    skill_dir.mkdir(parents=True, exist_ok=True)
    path = skill_dir / "SKILL.md"
    desc = (description or "").strip() or slug
    text = (
        "---\n"
        f"name: {slug}\n"
        f"description: {desc}\n"
        "---\n"
        f"{body if body is not None else desc}\n"
    )
    path.write_text(text, encoding="utf-8")
    return {"path": str(path), "slug": slug, "name": name, "description": desc}


def apply_skill_to_stack(
    source_stack: str,
    name: str,
    description: str,
    *,
    dest: str | None = None,
    repo_root: str | None = None,
    body: str | None = None,
) -> dict:
    """Materialize a working copy and write one skill. Never mutates source."""
    target = dest or default_apply_dest(repo_root)
    materialize_working_stack(source_stack, target)
    written = write_skill(target, name, description, body=body)
    return {
        "written": True,
        "source": source_stack,
        "stack": target,
        "skill_path": written["path"],
        "slug": written["slug"],
        "name": written["name"],
        "description": written["description"],
    }
