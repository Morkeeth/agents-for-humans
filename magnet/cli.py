"""CLI — magnet init | magnet demo | magnet probe | magnet check-docs"""
from __future__ import annotations

import argparse
import os
import sys

from magnet.agent_run import MODES, run_agent_loop
from magnet.demo import run_demo
from magnet.eval import run_eval
from magnet.ledger import connect, default_ledger_path, reset_demo
from magnet.probes import check_docs_exit_code
from magnet.tools import tool_check_docs, tool_record_week, tool_run_probe


def cmd_init(args: argparse.Namespace) -> int:
    path = args.ledger or default_ledger_path()
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    conn = connect(path)
    if args.reset:
        reset_demo(conn)
    print(f"MAGNET ledger ready at {path}")
    print("  next: magnet demo")
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    print(run_demo(ledger_path=args.ledger, repo_root=args.repo))
    return 0


def cmd_probe(args: argparse.Namespace) -> int:
    result = tool_run_probe(args.name, ledger_path=args.ledger)
    pop = result.get("population")
    val = result.get("value")
    shown = f"{val}/{pop}" if pop is not None else val
    print(f"{result['probe_name']}: {shown}")
    print(f"  command: {result['command']}")
    return 0


def cmd_record(args: argparse.Namespace) -> int:
    out = tool_record_week(args.name, ledger_path=args.ledger)
    print(f"recorded {args.name}: verdict={out['verdict']} readings={out['readings']}")
    return 0


def cmd_eval(args: argparse.Namespace) -> int:
    print(run_eval())
    return 0


def cmd_agent_run(args: argparse.Namespace) -> int:
    print(run_agent_loop(ledger_path=args.ledger, repo_root=args.repo, mode=args.model))
    return 0


def cmd_check_docs(args: argparse.Namespace) -> int:
    out = tool_check_docs(repo_root=args.repo, ledger_path=args.ledger)
    for row in out["results"]:
        mark = "PASS" if row["ok"] else "FAIL"
        print(f"[{mark}] {row['claim']}: {row['why']}")
    if out["drifted"]:
        print(f"\n{out['drifted']} claim(s) drifted.")
        return 1
    print(f"\n{out['checked']} claims checked. All match source.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="magnet",
        description="MAGNET — adoption ledger + eval runner for your agent stack",
    )
    parser.add_argument("--ledger", help="Path to SQLite ledger (default: .magnet/ledger.db)")
    parser.add_argument("--repo", default=".", help="Repo root for check-docs")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Create empty in-repo ledger")
    p_init.add_argument("--reset", action="store_true", help="Clear existing ledger")
    p_init.set_defaults(func=cmd_init)

    p_demo = sub.add_parser("demo", help="Cold demo: baseline → adopt → receipt")
    p_demo.set_defaults(func=cmd_demo)

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
    p_probe.set_defaults(func=cmd_probe)

    p_record = sub.add_parser("record", help="Run probe and store this week")
    p_record.add_argument("name", help="Probe name")
    p_record.set_defaults(func=cmd_record)

    p_docs = sub.add_parser("check-docs", help="Re-derive README numbers; exit 1 on drift")
    p_docs.set_defaults(func=cmd_check_docs)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
