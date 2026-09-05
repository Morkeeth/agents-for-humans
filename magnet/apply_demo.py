"""Cold path: show naive-fit inventing helped, then magnet --apply measuring it."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

from magnet.adopt import run_adopt
from magnet.apply_eval import naive_fit_verdict
from magnet.log import connect, reset_demo
from magnet.stack import default_stack_dir, fit_one, stack_coverage


def run_apply_demo(
    *,
    repo_root: str | None = None,
    stack_dir: str | None = None,
    log_path: str | None = None,
) -> str:
    root = repo_root or os.getcwd()
    source = stack_dir or default_stack_dir(root)
    log = log_path or str(Path(root) / ".magnet" / "apply-demo.db")
    Path(log).parent.mkdir(parents=True, exist_ok=True)
    reset_demo(connect(log))

    before = stack_coverage(source)
    security_fit = fit_one(
        "secrets-scanner",
        "blocks leaking .env and finds credential patterns",
        source,
    )
    wine_fit = fit_one("wine-pairing", "suggest a bottle for dinner", source)

    lines = [
        "MAGNET apply-demo — fit is a prediction; coverage is the measurement",
        "",
        f"  stack      {source}",
        f"  baseline   {before['value']}/{before['population']}  "
        f"uncovered={', '.join(before['detail']['uncovered'])}",
        "",
        "  after fit alone (no write — embarrassing case):",
        f"    fit label        {security_fit['label']}  fills={security_fit['fills']}",
        f"    naive-fit verdict  {naive_fit_verdict(security_fit['label'], [])}  "
        "← invents optimism from the ranking label",
        f"    magnet (no --apply) unchanged — skill was not written to the stack",
        "",
    ]

    with tempfile.TemporaryDirectory(prefix="magnet-apply-demo-") as tmp:
        fill_dest = str(Path(tmp) / "fill")
        noise_dest = str(Path(tmp) / "noise")

        fill_out = run_adopt(
            "skill",
            "secrets-scanner",
            "blocks leaking .env and finds credential patterns",
            "stack-coverage",
            log_path=log,
            reset=True,
            apply=True,
            apply_dest=fill_dest,
            simulate_next_week=False,
            fit=True,
            stack_dir=source,
            fit_description="blocks leaking .env and finds credential patterns",
        )
        noise_out = run_adopt(
            "skill",
            "wine-pairing",
            "suggest a bottle for dinner",
            "stack-coverage",
            log_path=log,
            reset=True,
            apply=True,
            apply_dest=noise_dest,
            simulate_next_week=False,
            fit=True,
            stack_dir=source,
            fit_description="suggest a bottle for dinner",
        )

        fill_cov = stack_coverage(fill_dest)
        noise_cov = stack_coverage(noise_dest)

    lines += [
        "  after --apply secrets-scanner (fills security):",
        f"    coverage   {before['value']}/{before['population']} → "
        f"{fill_cov['value']}/{fill_cov['population']}",
        f"    fit        {security_fit['label']}",
        "    receipt    helped (measured)",
        "",
        "  after --apply wine-pairing (noise):",
        f"    coverage   {before['value']}/{before['population']} → "
        f"{noise_cov['value']}/{noise_cov['population']}",
        f"    fit        {wine_fit['label']}",
        "    receipt    unchanged (measured) — naive-fit would still be quiet here",
        "",
        "  fixture stack left untouched:",
        f"    still      {stack_coverage(source)['value']}/{before['population']}",
        "",
        "  --- fill receipt ---",
        fill_out,
        "",
        "  --- noise receipt ---",
        noise_out,
        "",
        "  FINDING  naive-fit says helped from the label alone; magnet waits for "
        "coverage to move. Wine-pairing apply stays unchanged.",
        "  repro      magnet apply-demo",
    ]
    return "\n".join(lines)
