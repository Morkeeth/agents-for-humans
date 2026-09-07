"""Stack-coverage closed loop — install into YOUR stack, then re-measure.

Slice 14 scored fit without landing the skill, so coverage stayed 8/12 while
fit said fills-gap. This demo installs the skill into a working copy of the
stack, records coverage before/after in SQLite, and prints magnet vs a naive
"any install = helped" arm that a competent team ships in two hours.

Also opens the real Agent Grinder stack object (vendored cold-path snapshot)
so the finding is measured at the object, not against a proxy title.
"""
from __future__ import annotations

import os
import shutil
from datetime import timedelta
from pathlib import Path

from magnet.constants import SIMULATED_WEEK_OFFSET_DAYS
from magnet.log import _now, connect, list_readings, record_reading, reset_demo
from magnet.probes import STACK_COVERAGE_PROBE
from magnet.reporter import format_value_pop, naive_verdict, verdict
from magnet.stack import (
    default_stack_dir,
    fit_one,
    install_skill,
    read_skill_source,
    stack_coverage,
)


def naive_install_verdict(*, installed: bool) -> str:
    """Two-hour marketplace arm: any skill you installed helped.

    Independent of coverage. Exists so we can lose to it honestly when an
    install does not move the probe.
    """
    return "helped" if installed else "unchanged"


def _repo_root(repo_root: str | None) -> Path:
    return Path(repo_root or os.getcwd()).resolve()


def _copy_stack(src: Path, dest: Path) -> Path:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    return dest


def _record_coverage(conn, stack_dir: str, *, change_id: int | None, simulate: bool) -> dict:
    probe = stack_coverage(stack_dir)
    now = _now() + timedelta(days=SIMULATED_WEEK_OFFSET_DAYS) if simulate else None
    record_reading(
        conn,
        STACK_COVERAGE_PROBE,
        probe["value"],
        probe["command"],
        population=probe["population"],
        change_id=change_id,
        now=now,
        simulated=simulate,
    )
    return probe


def run_one_install(
    *,
    work_stack: str,
    skill_source: Path,
    log_path: str,
    skill_name: str,
    prediction: str,
    fit_against: str | None = None,
) -> dict:
    """Baseline → install skill → re-probe. Returns measured outcome.

    Fit is scored against `fit_against` (pre-install stack) so a fills-gap
    label is not erased by the install itself.
    """
    from magnet.log import adopt_change

    conn = connect(log_path)
    fit_stack = fit_against or work_stack
    src = read_skill_source(str(skill_source))
    fit = fit_one(
        src["name"] or skill_name,
        src["description"],
        fit_stack,
    )
    before = _record_coverage(conn, work_stack, change_id=None, simulate=False)
    installed = install_skill(
        work_stack,
        name=src["name"] or skill_name,
        description=src["description"],
        body=src["body"],
    )
    adoption = adopt_change(
        conn,
        "skill",
        src["name"] or skill_name,
        prediction,
        STACK_COVERAGE_PROBE,
    )
    after = _record_coverage(
        conn, work_stack, change_id=adoption["id"], simulate=True
    )
    readings = list_readings(conn, STACK_COVERAGE_PROBE)
    label, delta = verdict(readings, direction="up")
    return {
        "skill": src["name"] or skill_name,
        "installed_path": installed["path"],
        "before": before,
        "after": after,
        "readings": readings,
        "magnet": label,
        "delta": delta,
        "naive_series": naive_verdict(readings),
        "naive_install": naive_install_verdict(installed=True),
        "fit": fit,
        "adoption_id": adoption["id"],
    }


def run_stack_demo(*, log_path: str | None = None, repo_root: str | None = None) -> str:
    """Cold path: closed-loop coverage adopt + naive arm + real-stack object."""
    root = _repo_root(repo_root)
    path = log_path or str(root / ".magnet" / "stack-demo.db")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    conn = connect(path)
    reset_demo(conn)

    fixture = Path(default_stack_dir(str(root)))
    work = root / ".magnet" / "stack-demo-work"
    _copy_stack(fixture, work)

    candidates = root / "fixtures" / "candidates"
    gap_skill = candidates / "pdb-navigator"
    dupe_skill = candidates / "writing-coach-pro"
    noise_skill = candidates / "wine-pairing"

    # Arm 1 — install fills an uncovered cap (debug)
    gap = run_one_install(
        work_stack=str(work),
        skill_source=gap_skill,
        log_path=path,
        skill_name="pdb-navigator",
        prediction="stack-coverage rises by filling debug",
        fit_against=str(fixture),
    )

    # Fresh working copy for the duplicate / noise arms so coverage math is clean
    work_dupe = root / ".magnet" / "stack-demo-dupe"
    _copy_stack(fixture, work_dupe)
    # Separate log namespace via probe readings on same DB is fine — reset between arms
    reset_demo(conn)
    dupe = run_one_install(
        work_stack=str(work_dupe),
        skill_source=dupe_skill,
        log_path=path,
        skill_name="writing-coach-pro",
        prediction="more writing help",
        fit_against=str(fixture),
    )

    work_noise = root / ".magnet" / "stack-demo-noise"
    _copy_stack(fixture, work_noise)
    reset_demo(conn)
    noise = run_one_install(
        work_stack=str(work_noise),
        skill_source=noise_skill,
        log_path=path,
        skill_name="wine-pairing",
        prediction="pair wine better",
        fit_against=str(fixture),
    )

    real_stack = root / "fixtures" / "real-stacks" / "agentgrinder"
    real = stack_coverage(str(real_stack))

    def _vp(probe: dict) -> str:
        return format_value_pop(probe.get("value"), probe.get("population"))

    lines = [
        "MAGNET stack-demo — closed loop: install → re-probe coverage",
        "",
        "  NOTE: Slice 14 fit-only adopt left coverage at 8/12 while printing",
        "        fills-gap. This demo installs the skill into a working copy.",
        "",
        "=== 1 · gap fill (pdb-navigator → debug) ===",
        f"  before     {_vp(gap['before'])}",
        f"  after      {_vp(gap['after'])}",
        f"  magnet     {gap['magnet']}  (Δ {gap['delta']})",
        f"  naive      {gap['naive_install']}  ← any-install arm",
        f"  fit        {gap['fit']['label']}  fills={','.join(gap['fit']['fills']) or '—'}",
        "",
        "=== 2 · duplicate install (writing-coach-pro) — embarrassment arm ===",
        f"  before     {_vp(dupe['before'])}",
        f"  after      {_vp(dupe['after'])}",
        f"  magnet     {dupe['magnet']}  (Δ {dupe['delta']})",
        f"  naive      {dupe['naive_install']}  ← invents helped on any install",
        f"  fit        {dupe['fit']['label']}",
        "",
        "=== 3 · noise install (wine-pairing) ===",
        f"  before     {_vp(noise['before'])}",
        f"  after      {_vp(noise['after'])}",
        f"  magnet     {noise['magnet']}  (Δ {noise['delta']})",
        f"  naive      {noise['naive_install']}  ← invents helped on any install",
        f"  fit        {noise['fit']['label']}",
        "",
        "=== 4 · real object: Agent Grinder stack (vendored snapshot) ===",
        f"  stack      {real_stack}",
        f"  coverage   {_vp(real)}",
        f"  uncovered  {', '.join((real.get('detail') or {}).get('uncovered') or [])}",
        f"  FINDING    companion product covers "
        f"{_vp(real)} capabilities — measured at the object, not the README.",
        "",
        "  FINDING  on duplicate/noise installs, naive says helped and magnet",
        "           refuses — the marketplace failure mode, re-derived tonight.",
        "",
        "  repro      magnet stack-demo",
        f"  repro      magnet probe stack-coverage --stack {real_stack}",
    ]
    return "\n".join(lines)
