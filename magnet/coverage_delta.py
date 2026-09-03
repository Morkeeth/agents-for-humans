"""Coverage-delta — check an adopt prediction against stack coverage before/after.

Helicon BUILD-PLAN S3 (prediction record): every shortlisted candidate claims
*this fills gap X*. Install it into a temp copy of the stack and re-derive
coverage. If the predicted caps appear in newly-covered, verdict is `attributed`;
if coverage moved on other caps only, `coincident`; if nothing moved, `nothing-moved`.
"""
from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path

from magnet.stack import (
    CAPABILITIES,
    default_stack_dir,
    fit_one,
    inventory,
    stack_coverage,
)


def _write_skill(stack_dir: str, name: str, description: str) -> str:
    skill_dir = Path(stack_dir) / "skills" / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    path = skill_dir / "SKILL.md"
    # Escape description for YAML double quotes
    safe = description.replace("\\", "\\\\").replace('"', '\\"')
    path.write_text(
        f'---\nname: {name}\ndescription: "{safe}"\n---\n\n# {name}\n',
        encoding="utf-8",
    )
    return str(path)


def run_coverage_delta(
    name: str,
    description: str,
    *,
    stack_dir: str | None = None,
    repo_root: str | None = None,
    predicted_caps: list[str] | None = None,
) -> dict:
    root = repo_root or os.getcwd()
    stack = stack_dir or default_stack_dir(root)
    before = stack_coverage(stack)
    fit = fit_one(name, description, stack)
    predicted = predicted_caps or list(fit["fills"])

    with tempfile.TemporaryDirectory(prefix="magnet-cov-") as tmp:
        dest = Path(tmp) / "stack"
        shutil.copytree(stack, dest)
        _write_skill(str(dest), name, description)
        after = stack_coverage(str(dest))
        after_inv = inventory(str(dest))

    before_set = set(before["detail"]["covered_caps"])
    after_set = set(after["detail"]["covered_caps"])
    newly = sorted(after_set - before_set)
    predicted_hit = [c for c in predicted if c in newly]
    predicted_miss = [c for c in predicted if c not in newly]

    if predicted and predicted_hit and not predicted_miss:
        verdict = "attributed"
    elif predicted and predicted_hit:
        verdict = "partial"
    elif newly and predicted and not predicted_hit:
        verdict = "coincident"
    elif newly and not predicted:
        verdict = "coincident"
    else:
        verdict = "nothing-moved"

    return {
        "name": name,
        "description": description[:160],
        "stack": stack,
        "fit_label": fit["label"],
        "fit_score": fit["score"],
        "predicted_caps": predicted,
        "before": {"value": before["value"], "population": before["population"]},
        "after": {"value": after["value"], "population": after["population"]},
        "newly_covered": newly,
        "predicted_hit": predicted_hit,
        "predicted_miss": predicted_miss,
        "verdict": verdict,
        "skills_after": len(after_inv.get("skills") or []),
        "command": (
            f"magnet coverage-delta --name {name!r} "
            f"--text {description[:40]!r} --stack {stack}"
        ),
    }


def render_coverage_delta(result: dict) -> str:
    b, a = result["before"], result["after"]
    lines = [
        "MAGNET coverage-delta — prediction checked against stack coverage",
        "",
        f"  candidate  {result['name']}",
        f"  fit        {result['fit_label']}  (score {result['fit_score']})",
        f"  predict    {', '.join(result['predicted_caps']) or '(none — no positive fills)'}",
        f"  before     {b['value']}/{b['population']}  covered capabilities",
        f"  after      {a['value']}/{a['population']}  (temp install into stack copy)",
        f"  newly      {', '.join(result['newly_covered']) or '(none)'}",
        f"  hit        {', '.join(result['predicted_hit']) or '(none)'}",
        f"  miss       {', '.join(result['predicted_miss']) or '(none)'}",
        f"  verdict    {result['verdict']}",
        "",
    ]
    notes = {
        "attributed": "predicted caps appear in newly-covered — displacement measured",
        "partial": "some predicted caps covered; some missed",
        "coincident": "coverage moved, but not on the predicted caps — coincident, not attributed",
        "nothing-moved": "installing this text did not cover any new capability",
    }
    lines.append(f"  note       {notes.get(result['verdict'], '')}")
    lines.append(f"  repro      {result['command']}")
    # Unknown predicted tags called out
    unknown = [c for c in result["predicted_caps"] if c not in CAPABILITIES]
    if unknown:
        lines.append(f"  unknown    {', '.join(unknown)} not in CAPABILITIES vocab")
    return "\n".join(lines)
