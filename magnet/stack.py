"""Stack inventory + gap-fit ranking — ported from helicon.magnet science.

Source object: Morkeeth/mountain-of-helicon helicon/magnet.py (opened 2026-09-02).
Not a skill marketplace: MAGNET does not crawl feeds. Ranking answers whether a
candidate YOU already have fills a hole in YOUR stack.

Rules carried forward from EXP-MAGNET-01 / S1:
  - Names and descriptions only — never secrets, env values, or connection strings
  - Word-boundary matching (substring "ui" in "guitar" is a false positive)
  - Items with score <= 0 are UNRANKED — never tie-break by name into a shortlist
  - Declared capabilities that text does not support are CLAIMED, not scored
  - Claims never buy rank; author-claims tier ordered by name, never claim count
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

SURFACES = ("skills", "commands", "agents", "hooks", "mcp")

CAPABILITIES = {
    "test-gate": ("test", "pytest", "jest", "suite", "green", "ci"),
    "review": ("review", "critique", "audit", "lint"),
    "security": ("secret", "credential", "vulnerab", "injection", "sandbox"),
    "docs": ("documentation", "docstring", "readme", "changelog"),
    "verification": ("verify", "probe", "receipt", "evidence", "reproduce"),
    "planning": ("plan", "decompose", "roadmap", "slice"),
    "research": ("research", "search", "literature", "source"),
    "design": ("design", "ui", "visual", "typography", "palette"),
    "writing": ("writing", "draft", "prose", "copy", "email"),
    "data": ("sql", "dataframe", "etl", "schema", "migration"),
    "debug": ("debug", "trace", "stack trace", "repro", "bisect"),
    "refactor": ("refactor", "rename", "extract method", "simplify"),
}

TAG_VOCABULARY = tuple(sorted(CAPABILITIES))
TAG_VOCAB_VERSION = "1.0"

_WORD = re.compile(r"[a-z][a-z0-9-]{2,}")
_STOP = {
    "the", "and", "for", "use", "when", "with", "this", "that", "his", "her",
    "you", "your", "not", "any", "all", "from", "into", "onto", "have", "has",
    "was", "are", "will", "can", "should", "must", "before", "after", "every",
    "one", "two", "three", "skill", "claude", "agent", "agents", "user", "code",
    "file", "files", "run", "runs", "running", "make", "makes", "get", "gets",
    "new", "old", "more", "most", "than", "then", "also", "just", "only",
}


def _words(text: str) -> set[str]:
    return {w for w in _WORD.findall((text or "").lower()) if w not in _STOP}


def _mentions(text: str, terms: tuple[str, ...]) -> bool:
    """Word-boundary match — substring false positives (ui in guitar) are forbidden."""
    words = _words(text)
    low = (text or "").lower()
    for t in terms:
        if " " in t:
            if t in low:
                return True
        elif any(w == t or (w.startswith(t) and len(t) >= 5) for w in words):
            return True
    return False


def _content_hash(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()[:12]


def verify_declaration(declared: list, text: str) -> dict:
    """Grade declared capabilities: verified / claimed / unknown."""
    out = {}
    for raw in declared or []:
        tag = str(raw).strip().lower()
        if tag not in CAPABILITIES:
            out[tag] = "unknown"
        elif _mentions(text, CAPABILITIES[tag]):
            out[tag] = "verified"
        else:
            out[tag] = "claimed"
    return out


def default_stack_dir(repo_root: str | None = None) -> str:
    """Cold-path fixture first, then ~/.claude if present."""
    root = Path(repo_root or os.getcwd())
    fixture = root / "fixtures" / "stack"
    if fixture.is_dir():
        return str(fixture)
    claude = Path(os.path.expanduser("~/.claude"))
    if claude.is_dir():
        return str(claude)
    return str(fixture)


def inventory(stack_dir: str) -> dict:
    """What this stack carries, by surface. Names and descriptions only."""
    root = os.path.expanduser(stack_dir)
    inv: dict = {s: [] for s in SURFACES}
    visible = set(SURFACES)
    if not os.path.isdir(root):
        return {"root": root, "present": False, "enumerable": [], **inv}

    skills_dir = os.path.join(root, "skills")
    if os.path.isdir(skills_dir):
        for name in sorted(os.listdir(skills_dir)):
            path = os.path.join(skills_dir, name, "SKILL.md")
            if os.path.isfile(path):
                meta = _frontmatter(path)
                inv["skills"].append(
                    {
                        "name": name,
                        "description": meta["description"],
                        "capabilities": meta["capabilities"],
                        "capability_verdicts": verify_declaration(
                            meta["capabilities"],
                            f"{name} {meta['description']}",
                        ),
                    }
                )

    cmd_dir = os.path.join(root, "commands")
    if os.path.isdir(cmd_dir):
        for fn in sorted(os.listdir(cmd_dir)):
            if not fn.endswith(".md") or ".bak" in fn:
                continue
            path = os.path.join(cmd_dir, fn)
            inv["commands"].append(
                {"name": fn[:-3], "description": _frontmatter_desc(path)}
            )

    agent_dir = os.path.join(root, "agents")
    if os.path.isdir(agent_dir):
        for fn in sorted(os.listdir(agent_dir)):
            if fn.endswith(".md") and ".bak" not in fn:
                inv["agents"].append(
                    {
                        "name": fn[:-3],
                        "description": _frontmatter_desc(os.path.join(agent_dir, fn)),
                    }
                )

    settings = os.path.join(root, "settings.json")
    if os.path.isfile(settings):
        try:
            with open(settings, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            data = {}
        for event, matchers in (data.get("hooks") or {}).items():
            for m in matchers:
                for h in m.get("hooks", []):
                    cmd = h.get("command", "")
                    inv["hooks"].append(
                        {
                            "name": (
                                os.path.basename(cmd.split()[0])
                                if cmd
                                else h.get("type", "?")
                            ),
                            "description": f"{event} on {m.get('matcher') or '*'}",
                            "event": event,
                        }
                    )
        if "mcpServers" in data:
            for server in sorted((data.get("mcpServers") or {}).keys()):
                inv["mcp"].append({"name": server, "description": ""})
        else:
            visible.discard("mcp")
    else:
        # Fixture stacks without settings.json: mcp is not enumerable.
        visible.discard("mcp")

    return {
        "root": root,
        "present": True,
        "enumerable": sorted(visible),
        **inv,
    }


def _frontmatter_desc(path: str) -> str:
    return _frontmatter(path)["description"]


def _frontmatter(path: str) -> dict:
    """Parse description + capabilities from SKILL.md / command frontmatter.

    Capabilities are the S1 declared-tag list. Coverage and ranking VERIFY them
    against the skill's own text — claimed (unsupported) never buys coverage.
    """
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            head = f.read(4000)
    except OSError:
        return {"description": "", "capabilities": []}
    desc_m = re.search(r"^description:\s*(.+?)\s*$", head, re.M)
    desc = (desc_m.group(1).strip().strip("\"'") if desc_m else "")[:400]
    caps: list[str] = []
    caps_m = re.search(r"^capabilities:\s*(.+?)\s*$", head, re.M | re.I)
    if caps_m:
        raw = caps_m.group(1).strip()
        if raw.startswith("["):
            raw = raw.strip("[]")
        for part in raw.split(","):
            tag = part.strip().strip("\"'").lower()
            if tag:
                caps.append(tag)
    return {"description": desc, "capabilities": caps}


def gaps(inv: dict) -> dict:
    """Holes as facts about this machine — never recommendations.

    A capability is covered when YOUR stack's text mentions it OR an owned skill
    declares it and the declaration VERIFYIES against that skill's text.
    CLAIMED (declared, text does not support) never buys coverage — same honesty
    rule as rank(). Found necessary when apply writes a synonym skill: without
    verified declarations, coverage stays deaf to paraphrase forever.
    """
    enumerable = set(inv.get("enumerable") or SURFACES)
    empty = [s for s in SURFACES if s in enumerable and not inv.get(s)]
    unseen = [s for s in SURFACES if s not in enumerable]
    owned: set[str] = set()
    verified_caps: set[str] = set()
    claimed_only: set[str] = set()
    for s in SURFACES:
        for item in inv.get(s) or []:
            owned |= _words(item.get("name", "")) | _words(item.get("description", ""))
            verdicts = item.get("capability_verdicts") or {}
            if not verdicts and item.get("capabilities"):
                verdicts = verify_declaration(
                    item.get("capabilities") or [],
                    f"{item.get('name', '')} {item.get('description', '')}",
                )
            for tag, verdict in verdicts.items():
                if verdict == "verified":
                    verified_caps.add(tag)
                elif verdict == "claimed":
                    claimed_only.add(tag)
    owned_blob = " ".join(sorted(owned))
    uncovered = sorted(
        cap
        for cap, terms in CAPABILITIES.items()
        if not _mentions(owned_blob, terms) and cap not in verified_caps
    )
    return {
        "empty_surfaces": empty,
        "uncovered": uncovered,
        "not_enumerable": unseen,
        "owned_terms": len(owned),
        "verified_caps": sorted(verified_caps),
        "claimed_only": sorted(claimed_only - verified_caps),
        "counts": {s: len(inv.get(s) or []) for s in SURFACES},
    }


def load_candidates(path: str) -> list[dict]:
    """Local candidates file only — MAGNET does not crawl."""
    path = os.path.expanduser(path or "")
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read().strip()
    rows: list = []
    if text.startswith("["):
        try:
            rows = json.loads(text)
        except json.JSONDecodeError:
            rows = []
    else:
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return [r for r in rows if isinstance(r, dict) and r.get("name")]


def rank(candidates: list, inv: dict, g: dict, top: int = 10) -> dict:
    """Score candidates by YOUR gaps. Score <= 0 → unranked (no name tie-break)."""
    owned_sets = [
        (
            item.get("name", ""),
            _words(item.get("name", "")) | _words(item.get("description", "")),
        )
        for s in SURFACES
        for item in (inv.get(s) or [])
    ]
    out = []
    for c in candidates:
        text = f"{c.get('name', '')} {c.get('description', '')}"
        words = _words(text)
        declared_verdicts = verify_declaration(c.get("capabilities"), text)
        fills, claims = [], []
        for cap in g["uncovered"]:
            if _mentions(text, CAPABILITIES[cap]):
                fills.append({"cap": cap, "by": "text"})
            elif declared_verdicts.get(cap) == "verified":
                fills.append({"cap": cap, "by": "declared+verified"})
            elif declared_verdicts.get(cap) == "claimed":
                claims.append({"cap": cap, "by": "claimed-unverified"})
        score = 3 * len(fills)
        unknown_tags = [t for t, v in declared_verdicts.items() if v == "unknown"]

        surface = (c.get("surface") or "").lower()
        empty_hit = surface in g["empty_surfaces"]
        if empty_hit:
            score += 2

        dupes = []
        for owned_name, owned_words in owned_sets:
            if not words or not owned_words:
                continue
            overlap = len(words & owned_words) / len(words)
            if overlap >= 0.34:
                dupes.append({"name": owned_name, "overlap": round(overlap, 2)})
        dupes.sort(key=lambda d: -d["overlap"])
        if dupes:
            score -= 4

        out.append(
            {
                "name": c.get("name"),
                "score": score,
                "fills": [f["cap"] for f in fills],
                "fills_detail": fills,
                "claims": claims,
                "unknown_tags": unknown_tags,
                "content_hash": _content_hash(text),
                "empty_surface": surface if empty_hit else "",
                "duplicates": dupes[:2],
                "description": (c.get("description") or "")[:160],
                "source": c.get("source", ""),
                "kind": c.get("kind", ""),
                "stars": c.get("stars"),
            }
        )

    scored = [r for r in out if r["score"] > 0]
    unranked = [r for r in out if r["score"] <= 0]
    scored.sort(key=lambda r: (-r["score"], r["name"]))
    demoted = sorted(
        [r for r in unranked if r["score"] < 0],
        key=lambda r: (r["score"], r["name"]),
    )
    claimed = sorted(
        [
            r
            for r in unranked
            if r["score"] == 0 and r["claims"] and not r["duplicates"]
        ],
        key=lambda r: r["name"],
    )
    claimed_names = {r["name"] for r in claimed}
    no_signal = [
        r
        for r in unranked
        if r["score"] == 0 and r["name"] not in claimed_names and r not in demoted
    ]
    for r in no_signal:
        r["no_signal"] = True
    return {
        "ranked": scored[:top],
        "demoted": demoted[:top],
        "claimed": claimed[:top],
        "claimed_total": len(claimed),
        "no_signal": len(no_signal),
        "considered": len(out),
        "all_scored": scored,
        "all_rows": out,
    }


def magnet_report(
    stack_dir: str,
    candidates_path: str = "",
    top: int = 10,
) -> dict:
    inv = inventory(stack_dir)
    g = gaps(inv)
    cands = load_candidates(candidates_path) if candidates_path else []
    base = {
        "inventory": inv,
        "gaps": g,
        "candidates_read": len(cands),
        "candidates_path": candidates_path,
        "tag_vocab_version": TAG_VOCAB_VERSION,
    }
    if not cands:
        return {
            **base,
            "ranked": [],
            "demoted": [],
            "claimed": [],
            "claimed_total": 0,
            "no_signal": 0,
            "considered": 0,
        }
    return {**base, **rank(cands, inv, g, top)}


def fit_one(
    name: str,
    description: str,
    stack_dir: str,
    *,
    surface: str = "skills",
    capabilities: list | None = None,
) -> dict:
    """Score a single candidate against YOUR stack. Used by adopt --fit."""
    inv = inventory(stack_dir)
    g = gaps(inv)
    cand = {
        "name": name,
        "description": description,
        "surface": surface,
        "capabilities": capabilities or [],
    }
    res = rank([cand], inv, g, top=1)
    row = (res["all_rows"] or [None])[0]
    if row is None:
        return {
            "name": name,
            "score": 0,
            "label": "no-signal",
            "fills": [],
            "duplicates": [],
            "claims": [],
            "empty_surface": "",
            "gaps": g,
        }
    if row["score"] > 0:
        label = "fills-gap"
    elif row["score"] < 0:
        label = "duplicate"
    elif row.get("claims"):
        label = "claimed-unverified"
    else:
        label = "no-signal"
    return {
        "name": name,
        "score": row["score"],
        "label": label,
        "fills": row["fills"],
        "duplicates": row["duplicates"],
        "claims": [c["cap"] for c in row["claims"]],
        "empty_surface": row.get("empty_surface") or "",
        "gaps": g,
    }


def stack_coverage(stack_dir: str) -> dict:
    """covered/total capabilities — re-derived from the live inventory."""
    inv = inventory(stack_dir)
    g = gaps(inv)
    total = len(CAPABILITIES)
    uncovered = set(g["uncovered"])
    covered = total - len(uncovered)
    return {
        "probe_name": "stack-coverage",
        "value": covered,
        "population": total,
        "command": f"magnet probe stack-coverage --stack {stack_dir}",
        "direction": "up",
        "detail": {
            "covered_caps": sorted(set(CAPABILITIES) - uncovered),
            "uncovered": g["uncovered"],
            "verified_caps": g.get("verified_caps") or [],
            "claimed_only": g.get("claimed_only") or [],
            "empty_surfaces": g["empty_surfaces"],
            "counts": g["counts"],
            "stack": stack_dir,
        },
    }


def render_fit(fit: dict) -> str:
    lines = [
        "MAGNET fit (against YOUR stack)",
        "",
        f"  candidate  {fit['name']}",
        f"  label      {fit['label']}  (score {fit['score']})",
    ]
    if fit["fills"]:
        lines.append(f"  fills      {', '.join(fit['fills'])}")
    if fit["empty_surface"]:
        lines.append(f"  empty      targets {fit['empty_surface']}")
    if fit["duplicates"]:
        d = fit["duplicates"][0]
        lines.append(
            f"  overlaps   {d['name']} ({int(d['overlap'] * 100)}% of candidate words)"
        )
    if fit["claims"]:
        lines.append(
            f"  claims     {', '.join(fit['claims'])}  (unverified — text does not support)"
        )
    if fit["label"] == "no-signal":
        lines.append("  note       no positive signal against current gaps")
    lines.append("  repro      magnet stack")
    return "\n".join(lines)


def render_stack(report: dict) -> str:
    """Human-readable inventory + gaps (+ optional ranked fit)."""
    inv, g = report["inventory"], report["gaps"]
    out = ["MAGNET stack — what YOUR agent surfaces carry", ""]
    if not inv.get("present"):
        return f"MAGNET stack — no stack found at {inv.get('root')}\n  tip: use fixtures/stack or pass --stack <dir>"

    unseen = set(g.get("not_enumerable") or [])
    counts = " · ".join(
        f"{'?' if s in unseen else g['counts'][s]} {s}" for s in SURFACES
    )
    out += [f"  INVENTORY   {counts}", f"  {'':11}{inv['root']}", ""]

    if g["empty_surfaces"]:
        out.append(f"  EMPTY       {', '.join(g['empty_surfaces'])}")
    if unseen:
        out.append(
            f"  NOT VISIBLE {', '.join(sorted(unseen))} — not counted as a gap"
        )
    if g["uncovered"]:
        out.append(f"  UNCOVERED   {', '.join(g['uncovered'])}")
    if not g["empty_surfaces"] and not g["uncovered"]:
        out.append("  NO GAPS     every enumerable surface populated; caps mentioned")
    out.append("")

    path = report.get("candidates_path") or ""
    if path:
        out.append(
            f"  FIT         {report['candidates_read']} read · "
            f"{len(report['ranked'])} positive signal · "
            f"{report['no_signal']} no signal (not ranked)"
        )
        if not report["ranked"]:
            out.append("              nothing in this file names a gap you have")
        for r in report["ranked"]:
            out.append(f"     {r['score']:>3}  {r['name']}")
            if r["fills"]:
                out.append(f"          fills: {', '.join(r['fills'])}")
            if r["empty_surface"]:
                out.append(f"          empty surface: {r['empty_surface']}")
            for d in r["duplicates"]:
                out.append(
                    f"          OVERLAPS owned: {d['name']} "
                    f"({int(d['overlap'] * 100)}%)"
                )
        if report.get("demoted"):
            out.append("")
            out.append("  DEMOTED — you already have something like these:")
            for r in report["demoted"][:5]:
                d = r["duplicates"][0] if r["duplicates"] else {"name": "?", "overlap": 0}
                out.append(
                    f"     {r['score']:>3}  {r['name']}  ->  {d['name']} "
                    f"({int(d['overlap'] * 100)}%)"
                )
        if report.get("claimed"):
            out.append("")
            out.append(
                f"  AUTHOR CLAIMS — {report['claimed_total']} declare a gap "
                "their text does not support (unverified, ordered by name)"
            )
            for r in report["claimed"][:5]:
                caps = ", ".join(c["cap"] for c in r["claims"])
                out.append(f"     claims [{caps}]  {r['name']}")
        out.append("")
        out.append("  These are CANDIDATES. Matching is lexical. The ruling is yours.")
        out.append("")

    out.append(f"  repro      magnet stack --stack {inv['root']}")
    return "\n".join(out)
