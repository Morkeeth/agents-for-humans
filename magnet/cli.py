"""CLI — magnet init | demo | eval | agent-run | probe | record | check-docs"""
from __future__ import annotations

import argparse
import os
import sys

from magnet.adopt import run_adopt
from magnet.constants import CHANGE_TYPES
from magnet.agent_run import MODES, run_agent_loop
from magnet.bakeoff import render_bakeoff, run_bakeoff
from magnet.demo import run_demo
from magnet.drift_demo import run_drift_demo
from magnet.eval import run_eval
from magnet.history import render_history
from magnet.log import connect, default_log_path, reset_demo
from magnet.probes import check_docs_exit_code
from magnet.registry import list_all_probes
from magnet.stack import magnet_report, render_stack, resolve_stack_dir
from magnet.stack_demo import run_stack_demo
from magnet.receipt import render_receipt_json
from magnet.redact import run_redact_scan
from magnet.external import measure_external_stack, render_external
from magnet.bind_demo import run_bind_demo
from magnet.guide_demo import run_guide_demo
from magnet.foreign_bind import run_foreign_bind
from magnet.foreign_harden import run_foreign_harden
from magnet.foreign_hurt import run_foreign_hurt
from magnet.pred_demo import run_pred_demo
from magnet.tools import tool_check_docs, tool_record_week, tool_run_probe


def cmd_init(args: argparse.Namespace) -> int:
    path = args.log or default_log_path()
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    conn = connect(path)
    if args.reset:
        reset_demo(conn)
    print(f"MAGNET log ready at {path}")
    print("  next: magnet demo")
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    print(run_demo(log_path=args.log, repo_root=args.repo))
    return 0


def cmd_stack_demo(args: argparse.Namespace) -> int:
    print(run_stack_demo(log_path=args.log, repo_root=args.repo))
    return 0


def cmd_drift_demo(args: argparse.Namespace) -> int:
    print(run_drift_demo(repo_root=args.repo))
    return 0


def cmd_pred_demo(args: argparse.Namespace) -> int:
    text = run_pred_demo()
    print(text)
    # Done-when: magnet perfect on scenarios AND naive invents held on wrong magnitude.
    if "FINDING  naive direction-only invents" not in text:
        return 1
    magnet_line = next(
        (ln for ln in text.splitlines() if ln.strip().startswith("magnet")),
        "",
    )
    parts = magnet_line.split()
    if len(parts) < 2 or "/" not in parts[1]:
        return 1
    n_s, t_s = parts[1].split("/", 1)
    if n_s != t_s:
        return 1
    return 0


def cmd_probe(args: argparse.Namespace) -> int:
    result = tool_run_probe(
        args.name, log_path=args.log, repo_root=args.repo, stack_dir=args.stack
    )
    pop = result.get("population")
    val = result.get("value")
    shown = f"{val}/{pop}" if pop is not None else val
    print(f"{result['probe_name']}: {shown}")
    print(f"  command: {result['command']}")
    return 0


def cmd_record(args: argparse.Namespace) -> int:
    out = tool_record_week(args.name, log_path=args.log, stack_dir=args.stack)
    print(f"recorded {args.name}: verdict={out['verdict']} readings={out['readings']}")
    return 0


def cmd_eval(args: argparse.Namespace) -> int:
    print(run_eval())
    return 0


def cmd_agent_run(args: argparse.Namespace) -> int:
    print(run_agent_loop(log_path=args.log, repo_root=args.repo, mode=args.model))
    return 0


def cmd_adopt(args: argparse.Namespace) -> int:
    print(
        run_adopt(
            args.change_type,
            args.description,
            args.prediction,
            args.probe,
            log_path=args.log,
            apply_demo_bonus=args.demo_bonus,
            simulate_next_week=not args.no_simulate,
            reset=args.reset,
            fit=args.fit,
            stack_dir=args.stack,
            fit_description=args.fit_text,
            install_from=args.install,
        )
    )
    return 0


def cmd_list_probes(args: argparse.Namespace) -> int:
    probes = list_all_probes(args.repo)
    print("MAGNET probes  (built-in + .magnet/probes.json)")
    print("")
    for p in probes:
        src = p.get("source", "?")
        desc = p.get("description", "")
        print(f"  {p['name']:<20} [{src}]  {p.get('command', '')}")
        if desc:
            print(f"    {desc}")
    print("")
    print(f"  total      {len(probes)}")
    print("  repro      magnet list-probes")
    return 0


def cmd_history(args: argparse.Namespace) -> int:
    path = args.log or default_log_path()
    conn = connect(path, announce=False)
    print(render_history(conn, probe_name=args.probe))
    return 0


def cmd_check_docs(args: argparse.Namespace) -> int:
    out = tool_check_docs(repo_root=args.repo, log_path=args.log)
    for row in out["results"]:
        mark = "PASS" if row["ok"] else "FAIL"
        print(f"[{mark}] {row['claim']}: {row['why']}")
    if out["drifted"]:
        print(f"\n{out['drifted']} claim(s) drifted.")
        return 1
    print(f"\n{out['checked']} claims checked. All match source.")
    return 0


def cmd_stack(args: argparse.Namespace) -> int:
    stack_dir = resolve_stack_dir(args.stack, repo_root=args.repo)
    report = magnet_report(stack_dir, candidates_path=args.candidates or "", top=args.top)
    print(render_stack(report))
    return 0 if report["inventory"].get("present") else 1


def cmd_fit(args: argparse.Namespace) -> int:
    stack_dir = resolve_stack_dir(args.stack, repo_root=args.repo)
    if not args.candidates:
        print("magnet fit requires --candidates <file.jsonl>")
        return 2
    report = magnet_report(stack_dir, candidates_path=args.candidates, top=args.top)
    print(render_stack(report))
    if not report["inventory"].get("present"):
        return 1
    return 0


def cmd_bakeoff(args: argparse.Namespace) -> int:
    result = run_bakeoff(
        stack_dir=resolve_stack_dir(args.stack, repo_root=args.repo),
        repo_root=args.repo,
        noise_n=args.noise,
        write_candidates=not args.no_write,
    )
    print(render_bakeoff(result))
    # Exit 0 even when magnet loses — the finding is the product.
    # Exit 1 only if the wine-liar bought primary rank (constitution break).
    if result["wine_liar_in_magnet_primary"]:
        print("\nCONSTITUTION FAIL: liar bought primary rank")
        return 1
    return 0


def cmd_receipt(args: argparse.Namespace) -> int:
    print(
        render_receipt_json(
            log_path=args.log,
            probe_name=args.probe,
            adoption_id=args.id,
        )
    )
    return 0


def cmd_redact_scan(args: argparse.Namespace) -> int:
    text, code = run_redact_scan(repo_root=args.repo)
    print(text)
    return code


def cmd_external_stack(args: argparse.Namespace) -> int:
    if not args.stack:
        print("magnet external-stack requires --stack <path>")
        return 2
    result = measure_external_stack(args.stack)
    print(render_external(result))
    return 0 if result["inventory"].get("present") else 1


def cmd_bind_demo(args: argparse.Namespace) -> int:
    text = run_bind_demo(repo_root=args.repo, stack_dir=args.stack, log_path=args.log)
    print(text)
    if "stack-bind probes did NOT move" in text:
        return 1
    if "repo-blind check-docs stayed flat while stack-bind probes moved" not in text:
        return 1
    return 0


def cmd_guide_demo(args: argparse.Namespace) -> int:
    text = run_guide_demo(repo_root=args.repo, stack_dir=args.stack, log_path=args.log)
    print(text)
    if "guide-demo must fail loud" in text:
        return 1
    if "repo-blind check-docs stayed flat while" not in text:
        return 1
    if "Ultimate Guide stack-bind probes moved" not in text:
        return 1
    return 0


def cmd_foreign_bind(args: argparse.Namespace) -> int:
    stacks = list(args.stack or [])
    text = run_foreign_bind(repo_root=args.repo, stacks=stacks or None)
    print(text)
    if "no stacks found" in text:
        return 1
    if "no stack embarrassed naive_title" in text:
        return 1
    if "FINDING" not in text:
        return 1
    return 0


def cmd_foreign_harden(args: argparse.Namespace) -> int:
    stacks = list(args.stack or [])
    text = run_foreign_harden(repo_root=args.repo, stacks=stacks or None)
    print(text)
    if "no stacks found" in text or "no usable stack" in text:
        return 1
    if "no stack closed the foreign-harden loop" in text:
        return 1
    if "FINDING" not in text:
        return 1
    if "title→apply→helped" not in text and "title never measured" not in text:
        # Require the closed-loop finding language, not a generic FINDING.
        if "closed the title" not in text:
            return 1
    return 0


def cmd_foreign_hurt(args: argparse.Namespace) -> int:
    stacks = list(args.stack or [])
    text = run_foreign_hurt(repo_root=args.repo, stacks=stacks or None)
    print(text)
    if "no stacks found" in text or "no usable stack" in text:
        return 1
    if "no stack embarrassed naive-on-hurt" in text:
        return 1
    if "FINDING" not in text:
        return 1
    if "naive invented helped" not in text and "magnet-hurt" not in text:
        if "naive invented helped" not in text:
            return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="magnet",
        description="MAGNET — adoption log + eval runner for your agent stack",
    )
    parser.add_argument(
        "--log",
        dest="log",
        help="Path to the SQLite log (default: .magnet/log.db)",
    )
    parser.add_argument("--repo", default=".", help="Repo root for check-docs")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Create empty in-repo log")
    p_init.add_argument("--reset", action="store_true", help="Clear existing log")
    p_init.set_defaults(func=cmd_init)

    p_demo = sub.add_parser("demo", help="Cold demo: baseline → adopt → receipt")
    p_demo.set_defaults(func=cmd_demo)

    p_stack_demo = sub.add_parser(
        "stack-demo",
        help="Closed loop: install skill into stack → coverage delta + naive arm",
    )
    p_stack_demo.set_defaults(func=cmd_stack_demo)

    p_drift = sub.add_parser(
        "drift-demo",
        help="Show check_docs catching fabricated numbers (Qwen lesson)",
    )
    p_drift.set_defaults(func=cmd_drift_demo)

    p_pred = sub.add_parser(
        "pred-demo",
        help="Magnitude honesty: naive direction invents held on wrong fraction",
    )
    p_pred.set_defaults(func=cmd_pred_demo)

    p_adopt = sub.add_parser("adopt", help="Adopt a change, re-probe, print receipt")
    p_adopt.add_argument("change_type", choices=list(CHANGE_TYPES))
    p_adopt.add_argument("description", help="Short label for the change")
    p_adopt.add_argument("prediction", help="Testable prediction (e.g. 'pass rate rises by 1/5')")
    p_adopt.add_argument("--probe", default="demo-pass-rate", help="Probe to measure")
    p_adopt.add_argument("--demo-bonus", action="store_true", help="Apply demo skill bonus (+1/5)")
    p_adopt.add_argument("--no-simulate", action="store_true", help="Do not simulate next week")
    p_adopt.add_argument("--reset", action="store_true", help="Clear log before adopt")
    p_adopt.add_argument(
        "--fit",
        action="store_true",
        help="Also score this change against YOUR stack gaps (magnet stack science)",
    )
    p_adopt.add_argument(
        "--fit-text",
        help="Prose description used for fit matching (default: prediction)",
    )
    p_adopt.add_argument(
        "--stack",
        help="Stack directory for --fit/--install (default: fixtures/stack)",
    )
    p_adopt.add_argument(
        "--install",
        metavar="SKILL_PATH",
        help=(
            "Install a local skill directory/SKILL.md into a working copy of "
            "--stack, then re-probe (closes the coverage loop)"
        ),
    )
    p_adopt.set_defaults(func=cmd_adopt)

    p_eval = sub.add_parser("eval", help="Score naive vs magnet vs silent_null on scenarios")
    p_eval.set_defaults(func=cmd_eval)

    p_agent = sub.add_parser(
        "agent-run",
        help="Drive the 4 tools with a real Strands agent loop (default: local, no spend)",
    )
    p_agent.add_argument(
        "--model",
        choices=MODES,
        default="local",
        help=(
            "local = real Strands agent loop with a local scripted model "
            "(no network, no spend; the default). "
            "bedrock = real Strands agent loop with Amazon Bedrock "
            "(REQUIRES AWS CREDENTIALS AND COSTS MONEY). "
            "none = deterministic chain, no agent."
        ),
    )
    p_agent.set_defaults(func=cmd_agent_run)

    p_probe = sub.add_parser("probe", help="Run one probe")
    p_probe.add_argument("name", help="Probe name (e.g. demo-pass-rate)")
    p_probe.add_argument(
        "--stack",
        help="Stack directory for stack-coverage (also: MAGNET_STACK env)",
    )
    p_probe.set_defaults(func=cmd_probe)

    p_record = sub.add_parser("record", help="Run probe and store this week")
    p_record.add_argument("name", help="Probe name")
    p_record.add_argument("--stack", help="Stack directory for stack-coverage")
    p_record.set_defaults(func=cmd_record)

    p_docs = sub.add_parser("check-docs", help="Re-derive README numbers; exit 1 on drift")
    p_docs.set_defaults(func=cmd_check_docs)

    p_list = sub.add_parser("list-probes", help="List built-in and registry probes")
    p_list.set_defaults(func=cmd_list_probes)

    p_hist = sub.add_parser("history", help="Show adoption timeline from the log")
    p_hist.add_argument("--probe", help="Filter to one probe name")
    p_hist.set_defaults(func=cmd_history)

    p_stack = sub.add_parser(
        "stack",
        help="Inventory YOUR agent surfaces + gaps (fixture cold path)",
    )
    p_stack.add_argument(
        "--stack",
        help="Stack directory (default: fixtures/stack or ~/.claude)",
    )
    p_stack.add_argument(
        "--candidates",
        help="Optional local candidates JSON/JSONL to rank against YOUR gaps",
    )
    p_stack.add_argument("--top", type=int, default=10)
    p_stack.set_defaults(func=cmd_stack)

    p_fit = sub.add_parser(
        "fit",
        help="Rank a local candidates file against YOUR stack gaps (no crawl)",
    )
    p_fit.add_argument("--candidates", required=True, help="JSON or JSONL candidates")
    p_fit.add_argument("--stack", help="Stack directory")
    p_fit.add_argument("--top", type=int, default=10)
    p_fit.set_defaults(func=cmd_fit)

    p_bake = sub.add_parser(
        "bakeoff",
        help="Score magnet vs naive-stars vs naive-name vs silent_null on fixtures",
    )
    p_bake.add_argument("--stack", help="Stack directory (default: fixtures/stack)")
    p_bake.add_argument("--noise", type=int, default=200, help="Noise candidates")
    p_bake.add_argument(
        "--no-write",
        action="store_true",
        help="Do not write fixtures/candidates-bakeoff.jsonl",
    )
    p_bake.set_defaults(func=cmd_bakeoff)

    p_receipt = sub.add_parser(
        "receipt",
        help="Print latest adoption receipt as JSON (Grinder-ready, no invent)",
    )
    p_receipt.add_argument("--probe", help="Filter to one probe")
    p_receipt.add_argument("--id", type=int, help="Specific adoption id")
    p_receipt.set_defaults(func=cmd_receipt)

    p_redact = sub.add_parser(
        "redact-scan",
        help="Scan repo for live secret patterns (must go RED on plant, GREEN here)",
    )
    p_redact.set_defaults(func=cmd_redact_scan)

    p_ext = sub.add_parser(
        "external-stack",
        help="Measure a stack you did not build (inventory + coverage + naive title arm)",
    )
    p_ext.add_argument(
        "--stack",
        required=True,
        help="Path to an external stack directory (clone first)",
    )
    p_ext.set_defaults(func=cmd_external_stack)

    p_bind = sub.add_parser(
        "bind-demo",
        help="Embarrassment arm: repo-blind check-docs flat while stack-bind probes move",
    )
    p_bind.add_argument("--stack", help="Source stack to copy (default: fixtures/stack)")
    p_bind.set_defaults(func=cmd_bind_demo)

    p_guide = sub.add_parser(
        "guide-demo",
        help="Ultimate Guide closed loop: 5 recommendations measured vs naive title",
    )
    p_guide.add_argument("--stack", help="Source stack to copy (default: fixtures/stack)")
    p_guide.set_defaults(func=cmd_guide_demo)

    p_fb = sub.add_parser(
        "foreign-bind",
        help="Run bind probes on stacks we did not build (offline fixtures + optional clones)",
    )
    p_fb.add_argument(
        "--stack",
        action="append",
        help="Stack path (repeatable). Default: offline fixtures. Or set MAGNET_FOREIGN_BIND",
    )
    p_fb.set_defaults(func=cmd_foreign_bind)

    p_fh = sub.add_parser(
        "foreign-harden",
        help="Apply UG hardening to foreign stacks: title-complete → apply → helped",
    )
    p_fh.add_argument(
        "--stack",
        action="append",
        help="Stack path (repeatable). Default: offline fixtures. Or set MAGNET_FOREIGN_BIND",
    )
    p_fh.set_defaults(func=cmd_foreign_harden)

    p_hurt = sub.add_parser(
        "foreign-hurt",
        help="Strip hardening on foreign stacks: magnet hurt while naive invents helped",
    )
    p_hurt.add_argument(
        "--stack",
        action="append",
        help="Stack path (repeatable). Default: offline fixtures with skills",
    )
    p_hurt.set_defaults(func=cmd_foreign_hurt)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
