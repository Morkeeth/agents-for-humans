"""Bakeoff — magnet fit vs naive marketplace proxies on a planted flood.

Arms measured against something we did not invent as our best case:
  magnet       gap-fit ranker (score > 0 only; no name tie-break)
  naive_stars  rank by fake star counts (the directory/marketplace proxy)
  naive_name   include zero-score items sorted by name (EXP-MAGNET-01 bug)
  silent_null  never surfaces anyone

Ground truth: planted items with kind in {direct, synonym, surface} SHOULD
appear in top-K; duplicates SHOULD be demoted; noise SHOULD stay out.

Numbers are re-derived every run from the fixture objects — never carried.
"""
from __future__ import annotations

import hashlib
import json
import os
import random
from pathlib import Path

from magnet.stack import default_stack_dir, gaps, inventory, rank

# Seeded flood — identical on every stranger machine.
SEED = 20260816
NOISE_N = 200  # smaller than EXP-MAGNET-01's 990; same structure, cold-path fast
TOP_K = 20

PLANTED = [
    # DIRECT — vocabulary the filter owns
    {
        "name": "pdb-navigator",
        "kind": "direct",
        "surface": "skills",
        "description": (
            "Debug a failing test by driving pdb, setting breakpoints and "
            "bisecting the stack trace to the first bad frame"
        ),
        "stars": 12,
    },
    {
        "name": "safe-rename",
        "kind": "direct",
        "surface": "skills",
        "description": (
            "Refactor across a repo: rename a symbol, extract a function, "
            "simplify nested conditionals, per-site review"
        ),
        "stars": 40,
    },
    {
        "name": "trace-reader",
        "kind": "direct",
        "surface": "skills",
        "description": (
            "Read a stack trace, find the repro, and bisect commits to the "
            "first failing one"
        ),
        "stars": 8,
    },
    # SYNONYM — same gaps, words the capability list does not hold (adversarial)
    {
        "name": "fault-localiser",
        "kind": "synonym",
        "surface": "skills",
        "description": (
            "Narrow a misbehaving program to the smallest failing input and "
            "the exact line responsible"
        ),
        "stars": 900,
        "capabilities": ["debug"],
    },
    {
        "name": "code-surgeon",
        "kind": "synonym",
        "surface": "skills",
        "description": (
            "Restructure a module in place without changing behaviour, moving "
            "responsibilities between units"
        ),
        "stars": 850,
        "capabilities": ["refactor"],
    },
    {
        "name": "postmortem-pilot",
        "kind": "synonym",
        "surface": "skills",
        "description": (
            "Walk backwards from a crash to the change that caused it, one "
            "hypothesis at a time"
        ),
        "stars": 800,
        "capabilities": ["debug"],
    },
    # SURFACE — targets empty agents surface
    {
        "name": "subagent-fanout",
        "kind": "surface",
        "surface": "agents",
        "description": (
            "Define reusable subagents that fan out across a repository and "
            "report structured findings"
        ),
        "stars": 55,
    },
    {
        "name": "reviewer-agent",
        "kind": "surface",
        "surface": "agents",
        "description": (
            "A standing agent definition that inspects a change set and "
            "returns ranked observations"
        ),
        "stars": 60,
    },
    # DUPLICATE — near-copies of skills already in the fixture stack
    {
        "name": "writing-coach-pro",
        "kind": "duplicate",
        "surface": "skills",
        "description": (
            "Writing rules for anything with a reader. Draft an email, reply, "
            "DM, LinkedIn note, connection request, cover letter, bio or post"
        ),
        "stars": 9999,
    },
    {
        "name": "task-inbox-plus",
        "kind": "duplicate",
        "surface": "skills",
        "description": (
            "Task capture, closing and eviction. Add to the task list, push "
            "to tasks, put it on the board, triage and prune it"
        ),
        "stars": 8888,
    },
    # LIAR — declares many gaps; text supports none (must not buy primary rank)
    {
        "name": "wine-pairing-liar",
        "kind": "liar",
        "surface": "skills",
        "description": "Recommend wine pairings for a menu",
        "stars": 5000,
        "capabilities": ["debug", "refactor", "security"],
    },
]

NOISE_DOMAINS = [
    "generate marketing headlines for a landing page",
    "convert currencies at live rates",
    "summarise a podcast episode into bullet points",
    "plan a wedding seating chart",
    "translate subtitles between languages",
    "track calories from a photo",
    "draft a real estate listing",
    "tune a guitar by ear",
    "recommend wine pairings for a menu",
    "score a fantasy football lineup",
    "book a restaurant table",
    "identify a plant from a leaf",
    "compose a birthday poem",
    "estimate shipping costs across carriers",
    "generate a colour palette from a photograph",
    "convert a recipe between units",
    "practise flashcards with spaced repetition",
    "log a workout set",
    "find a flight under a price threshold",
    "read a tarot spread",
]


def build_flood(*, noise_n: int = NOISE_N, seed: int = SEED) -> list[dict]:
    rng = random.Random(seed)
    flood = []
    for i in range(noise_n):
        d = NOISE_DOMAINS[i % len(NOISE_DOMAINS)]
        # Deterministic fake stars — marketplace proxy, not measured popularity
        stars = int(hashlib.sha256(f"noise-{i:03d}".encode()).hexdigest()[:4], 16) % 500
        flood.append(
            {
                "name": f"noise-{i:03d}",
                "surface": "skills",
                "description": d,
                "kind": "noise",
                "stars": stars,
            }
        )
    flood.extend(dict(p) for p in PLANTED)
    rng.shuffle(flood)
    return flood


def _should_surface() -> list[str]:
    return [p["name"] for p in PLANTED if p["kind"] in ("direct", "synonym", "surface")]


def _kind_of(name: str) -> str:
    for p in PLANTED:
        if p["name"] == name:
            return p["kind"]
    return "noise"


def arm_magnet(flood: list[dict], inv: dict, g: dict, top_k: int = TOP_K) -> list[str]:
    """Positive-signal ranking only — the product under test."""
    res = rank(flood, inv, g, top=len(flood))
    return [r["name"] for r in res["ranked"][:top_k]]


def arm_naive_stars(flood: list[dict], top_k: int = TOP_K) -> list[str]:
    """Marketplace proxy: sort by stars descending. Ignores YOUR gaps entirely."""
    ordered = sorted(
        flood,
        key=lambda r: (-int(r.get("stars") or 0), r.get("name") or ""),
    )
    return [r["name"] for r in ordered[:top_k]]


def arm_naive_name(flood: list[dict], inv: dict, g: dict, top_k: int = TOP_K) -> list[str]:
    """EXP-MAGNET-01 bug: keep zero-score rows and order the shortlist by name.

    This invents recall when alphabetically-early synonyms score identically to noise.
    """
    res = rank(flood, inv, g, top=len(flood))
    # Include everything that is not demoted, including no-signal — then sort by name
    keep = [
        r
        for r in res["all_rows"]
        if r["score"] >= 0  # drop demoted duplicates
    ]
    keep.sort(key=lambda r: r["name"] or "")
    return [r["name"] for r in keep[:top_k]]


def arm_silent_null(_flood: list[dict], top_k: int = TOP_K) -> list[str]:
    """Always-empty shortlist — correct that it surfaces no noise; useless for gaps."""
    return []


def score_arm(top: list[str], *, top_k: int = TOP_K) -> dict:
    should = _should_surface()
    found = [n for n in should if n in top[:top_k]]
    noise_in = [n for n in top[:top_k] if _kind_of(n) == "noise"]
    liars_in = [n for n in top[:top_k] if _kind_of(n) == "liar"]
    dupes_in = [n for n in top[:top_k] if _kind_of(n) == "duplicate"]
    recall = len(found) / len(should) if should else 0.0
    precision = (
        sum(1 for n in top[:3] if _kind_of(n) in ("direct", "synonym", "surface")) / 3
        if top
        else 0.0
    )
    per_kind = {}
    for k in ("direct", "synonym", "surface"):
        names = [p["name"] for p in PLANTED if p["kind"] == k]
        per_kind[k] = {
            "found": sum(1 for n in names if n in top[:top_k]),
            "of": len(names),
        }
    return {
        "recall_at_k": round(recall, 3),
        "precision_at_3": round(precision, 3),
        "found": found,
        "noise_in_top": len(noise_in),
        "liars_in_top": len(liars_in),
        "dupes_in_top": len(dupes_in),
        "per_kind": per_kind,
        "top": top[:top_k],
    }


def run_bakeoff(
    *,
    stack_dir: str | None = None,
    repo_root: str | None = None,
    noise_n: int = NOISE_N,
    top_k: int = TOP_K,
    write_candidates: bool = True,
) -> dict:
    root = repo_root or os.getcwd()
    stack = stack_dir or default_stack_dir(root)
    inv = inventory(stack)
    g = gaps(inv)
    flood = build_flood(noise_n=noise_n)

    if write_candidates:
        out_path = Path(root) / "fixtures" / "candidates-bakeoff.jsonl"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            for row in flood:
                f.write(json.dumps(row, sort_keys=True) + "\n")

    arms = {
        "magnet": arm_magnet(flood, inv, g, top_k),
        "naive_stars": arm_naive_stars(flood, top_k),
        "naive_name": arm_naive_name(flood, inv, g, top_k),
        "silent_null": arm_silent_null(flood, top_k),
    }
    scored = {name: score_arm(top, top_k=top_k) for name, top in arms.items()}

    # Best arm by recall, then by precision, then by least noise
    def key(item):
        name, s = item
        return (s["recall_at_k"], s["precision_at_3"], -s["noise_in_top"])

    best_name, best = max(scored.items(), key=key)

    # Claims tier recovery for synonyms (S1 finding) — not primary recall
    magnet_res = rank(flood, inv, g, top=len(flood))
    claimed_names = {r["name"] for r in magnet_res.get("claimed", [])}
    synonym_names = [p["name"] for p in PLANTED if p["kind"] == "synonym"]
    synonym_in_claims = [n for n in synonym_names if n in claimed_names]

    return {
        "stack": stack,
        "flood": len(flood),
        "noise": noise_n,
        "planted": len(PLANTED),
        "top_k": top_k,
        "gaps": {
            "empty_surfaces": g["empty_surfaces"],
            "uncovered": g["uncovered"],
            "counts": g["counts"],
        },
        "arms": scored,
        "best_arm": best_name,
        "synonym_in_claims_tier": synonym_in_claims,
        "wine_liar_in_magnet_primary": "wine-pairing-liar"
        in scored["magnet"]["top"],
        "token_cost": 0,
    }


def render_bakeoff(result: dict) -> str:
    lines = [
        "MAGNET bakeoff — gap-fit vs marketplace proxies on a planted flood",
        "",
        f"  stack      {result['stack']}",
        f"  flood      {result['flood']}  ({result['noise']} noise + {result['planted']} planted)",
        f"  empty      {', '.join(result['gaps']['empty_surfaces']) or '(none)'}",
        f"  uncovered  {', '.join(result['gaps']['uncovered'][:8])}"
        + ("…" if len(result["gaps"]["uncovered"]) > 8 else ""),
        f"  top_k      {result['top_k']}",
        f"  tokens     {result['token_cost']}",
        "",
        "  arm            recall@k  p@3   noise  liars  dupes",
        "  " + "-" * 58,
    ]
    for name in ("magnet", "naive_stars", "naive_name", "silent_null"):
        s = result["arms"][name]
        lines.append(
            f"  {name:<14} {s['recall_at_k']:<8} {s['precision_at_3']:<5} "
            f"{s['noise_in_top']:<6} {s['liars_in_top']:<6} {s['dupes_in_top']}"
        )

    lines += ["", "  per-kind (magnet):"]
    for k, v in result["arms"]["magnet"]["per_kind"].items():
        lines.append(f"    {k:<10} {v['found']}/{v['of']}")

    lines += [
        "",
        f"  synonym claims-tier recovery  "
        f"{len(result['synonym_in_claims_tier'])}/"
        f"{result['arms']['magnet']['per_kind']['synonym']['of']}  "
        f"{result['synonym_in_claims_tier']}",
        f"  wine-liar in magnet primary   "
        f"{result['wine_liar_in_magnet_primary']}  (must be False)",
        f"  best arm                      {result['best_arm']}",
        "",
    ]

    if result["best_arm"] != "magnet":
        lines.append(
            "  FINDING  MAGNET lost the bakeoff on this fixture — that is the "
            "result. Do not paper over it."
        )
    elif result["arms"]["magnet"]["per_kind"]["synonym"]["found"] == 0:
        lines.append(
            "  FINDING  magnet primary misses the synonym arm (deaf to paraphrase); "
            "claims tier recovers declarations without letting liars buy rank."
        )
    else:
        lines.append("  FINDING  magnet leads on recall without admitting noise/liars.")

    # Embarrass naive_stars if it elevated the duplicate with 9999 stars
    stars = result["arms"]["naive_stars"]
    if stars["dupes_in_top"] or stars["liars_in_top"]:
        lines.append(
            "  FINDING  naive_stars promoted duplicates and/or liars by star count — "
            "the marketplace failure mode."
        )
    name_arm = result["arms"]["naive_name"]
    if name_arm["noise_in_top"] > result["arms"]["magnet"]["noise_in_top"]:
        lines.append(
            "  FINDING  naive_name admitted noise via alphabetical tie-break — "
            "the EXP-MAGNET-01 defect re-derived."
        )

    lines += ["", "  repro      magnet bakeoff"]
    return "\n".join(lines)
