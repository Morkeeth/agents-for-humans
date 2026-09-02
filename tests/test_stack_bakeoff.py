"""Tests for stack inventory, gap-fit ranking, and bakeoff arms."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from magnet.bakeoff import (
    arm_naive_name,
    arm_naive_stars,
    build_flood,
    render_bakeoff,
    run_bakeoff,
)
from magnet.stack import (
    _mentions,
    default_stack_dir,
    gaps,
    inventory,
    load_candidates,
    magnet_report,
    rank,
    verify_declaration,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_STACK = ROOT / "fixtures" / "stack"


def test_fixture_stack_exists():
    assert FIXTURE_STACK.is_dir()
    assert (FIXTURE_STACK / "skills" / "writing-coach" / "SKILL.md").is_file()


def test_default_stack_dir_prefers_fixture(tmp_path, monkeypatch):
    monkeypatch.chdir(ROOT)
    assert Path(default_stack_dir(str(ROOT))) == FIXTURE_STACK


def test_inventory_names_only_no_secrets():
    inv = inventory(str(FIXTURE_STACK))
    assert inv["present"] is True
    assert len(inv["skills"]) >= 3
    blob = json.dumps(inv)
    # Specific secret shapes — NOT bare "sk-" (matches task-inbox as substring)
    for banned in ("AKIA", "sk-ant-", "sk_live", "sk_test", "BEGIN RSA", "password=", "api_key="):
        assert banned.lower() not in blob.lower()


def test_agents_surface_is_empty_on_fixture():
    inv = inventory(str(FIXTURE_STACK))
    g = gaps(inv)
    assert "agents" in g["empty_surfaces"]
    assert g["counts"]["skills"] >= 3
    assert "mcp" in g["not_enumerable"] or "mcp" not in inv.get("enumerable", [])


def test_word_boundary_rejects_ui_in_guitar():
    assert _mentions("tune a guitar by ear", ("ui", "visual")) is False
    assert _mentions("design a visual palette", ("ui", "visual", "design")) is True


def test_claims_do_not_buy_score():
    inv = inventory(str(FIXTURE_STACK))
    g = gaps(inv)
    liar = {
        "name": "wine-pairing-liar",
        "surface": "skills",
        "description": "Recommend wine pairings for a menu",
        "capabilities": ["debug", "refactor", "security"],
    }
    honest = {
        "name": "pdb-navigator",
        "surface": "skills",
        "description": "Debug a failing test by driving pdb and bisecting the stack trace",
    }
    res = rank([liar, honest], inv, g, top=10)
    names = [r["name"] for r in res["ranked"]]
    assert "pdb-navigator" in names
    assert "wine-pairing-liar" not in names
    claimed = {r["name"] for r in res["claimed"]}
    assert "wine-pairing-liar" in claimed


def test_no_signal_items_are_not_ranked_by_name():
    """EXP-MAGNET-01 defect: alphabetically-early zero-score must not enter shortlist."""
    inv = inventory(str(FIXTURE_STACK))
    g = gaps(inv)
    noise = [{"name": f"aaa-noise-{i}", "surface": "skills", "description": "read a tarot spread"} for i in range(5)]
    synonym = {
        "name": "zzz-fault-localiser",
        "surface": "skills",
        "description": "Narrow a misbehaving program to the smallest failing input",
        "capabilities": ["debug"],
    }
    res = rank(noise + [synonym], inv, g, top=20)
    ranked_names = [r["name"] for r in res["ranked"]]
    assert all(not n.startswith("aaa-noise") for n in ranked_names)
    # synonym with only a claim lands in claims tier, not primary
    assert "zzz-fault-localiser" not in ranked_names
    assert any(r["name"] == "zzz-fault-localiser" for r in res["claimed"])


def test_verify_declaration_verdicts():
    text = "Debug a failing pytest with breakpoints"
    assert verify_declaration(["debug", "refactor", "made-up"], text) == {
        "debug": "verified",
        "refactor": "claimed",
        "made-up": "unknown",
    }


def test_duplicates_are_demoted():
    inv = inventory(str(FIXTURE_STACK))
    g = gaps(inv)
    dupe = {
        "name": "writing-coach-pro",
        "surface": "skills",
        "description": (
            "Writing rules for anything with a reader. Draft an email, reply, "
            "DM, LinkedIn note, connection request, cover letter, bio or post"
        ),
    }
    res = rank([dupe], inv, g, top=10)
    assert res["ranked"] == []
    assert res["demoted"] and res["demoted"][0]["score"] < 0


def test_bakeoff_flood_is_deterministic():
    a = build_flood(noise_n=50)
    b = build_flood(noise_n=50)
    assert [r["name"] for r in a] == [r["name"] for r in b]


def test_bakeoff_magnet_keeps_liar_out_and_finds_direct(tmp_path):
    result = run_bakeoff(
        stack_dir=str(FIXTURE_STACK),
        repo_root=str(tmp_path),
        noise_n=80,
        write_candidates=False,
    )
    assert result["wine_liar_in_magnet_primary"] is False
    magnet = result["arms"]["magnet"]
    silent = result["arms"]["silent_null"]
    assert magnet["recall_at_k"] >= silent["recall_at_k"]
    # direct arm uses filter vocabulary — must all surface
    assert magnet["per_kind"]["direct"]["found"] == magnet["per_kind"]["direct"]["of"]
    # duplicates must not sit in magnet primary
    assert magnet["dupes_in_top"] == 0
    assert magnet["noise_in_top"] == 0
    # synonym primary miss is the known EXP-MAGNET finding; claims tier recovers
    assert magnet["per_kind"]["synonym"]["found"] == 0
    assert len(result["synonym_in_claims_tier"]) == magnet["per_kind"]["synonym"]["of"]
    # marketplace proxy must look worse on precision or junk admission
    stars = result["arms"]["naive_stars"]
    assert stars["dupes_in_top"] >= 1 or stars["liars_in_top"] >= 1
    assert result["best_arm"] == "magnet"


def test_naive_stars_promotes_high_star_junk(tmp_path):
    flood = build_flood(noise_n=50)
    top = arm_naive_stars(flood, top_k=10)
    # writing-coach-pro has 9999 stars — marketplace elevates the duplicate
    assert "writing-coach-pro" in top


def test_naive_name_admits_alphabetical_noise():
    inv = inventory(str(FIXTURE_STACK))
    g = gaps(inv)
    flood = build_flood(noise_n=80)
    top = arm_naive_name(flood, inv, g, top_k=20)
    # With zero-score included and sorted by name, noise-* and early letters appear
    assert any(n.startswith("noise-") or n.startswith("code-") for n in top)


def test_render_bakeoff_mentions_repro(tmp_path):
    result = run_bakeoff(
        stack_dir=str(FIXTURE_STACK),
        repo_root=str(tmp_path),
        noise_n=40,
        write_candidates=False,
    )
    text = render_bakeoff(result)
    assert "magnet bakeoff" in text
    assert "naive_stars" in text


def test_cli_stack_and_bakeoff_exit_zero():
    import subprocess
    import sys

    env = {**dict(**__import__("os").environ), "PATH": str(Path.home() / ".local/bin") + ":" + __import__("os").environ.get("PATH", "")}
    stack = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "stack", "--stack", str(FIXTURE_STACK)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env=env,
    )
    assert stack.returncode == 0, stack.stdout + stack.stderr
    assert "INVENTORY" in stack.stdout

    bake = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "bakeoff", "--stack", str(FIXTURE_STACK), "--noise", "40", "--no-write"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env=env,
    )
    assert bake.returncode == 0, bake.stdout + bake.stderr
    assert "bakeoff" in bake.stdout.lower()


def test_load_candidates_jsonl(tmp_path):
    path = tmp_path / "c.jsonl"
    path.write_text(
        json.dumps({"name": "a", "description": "debug a stack trace"}) + "\n"
        + json.dumps({"name": "b", "description": "x"}) + "\n",
        encoding="utf-8",
    )
    rows = load_candidates(str(path))
    assert len(rows) == 2


def test_magnet_report_without_candidates():
    report = magnet_report(str(FIXTURE_STACK))
    assert report["candidates_read"] == 0
    assert report["ranked"] == []
