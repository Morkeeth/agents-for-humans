"""Slice 16 — redact-scan control that can go RED + MAGNET_STACK."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from magnet.redact import run_redact_scan, scan_tree
from magnet.stack import default_stack_dir

ROOT = Path(__file__).resolve().parents[1]

# Build PEM header at runtime so this source file itself is not a finding.
_PEM_BEGIN = "-----BEGIN " + "RSA PRIVATE KEY-----"
_PEM_END = "-----END " + "RSA PRIVATE KEY-----"


def test_redact_scan_goes_red_on_planted_secret(tmp_path):
    """A control that has never gone RED is not a control."""
    plant = tmp_path / "leak.txt"
    # Assemble at runtime so this test file is not itself a finding.
    key_name = "aws_" + "secret_access_key"
    body = "wJalrXUtnFEMI/K7MDENG/bPxRfiCY" + "TESTSECRET01"
    plant.write_text(f"{key_name} = {body}\n", encoding="utf-8")
    findings = scan_tree(tmp_path)
    assert findings, "planted secret must be found"
    assert findings[0]["kind"] == "aws_secret_assign"
    text, code = run_redact_scan(repo_root=str(tmp_path))
    assert code == 1
    assert "FINDINGS" in text


def test_redact_scan_goes_red_on_private_key_block(tmp_path):
    (tmp_path / "id_rsa").write_text(
        f"{_PEM_BEGIN}\nMIIEowIBAAKCAQEA0Z3VS5JJcds3xfn/ygWyF\n{_PEM_END}\n",
        encoding="utf-8",
    )
    text, code = run_redact_scan(repo_root=str(tmp_path))
    assert code == 1
    assert "private_key_block" in text


def test_redact_scan_ignores_example_marker(tmp_path):
    key = "api_" + "key"
    (tmp_path / "docs.md").write_text(
        f'{key} = "abcdefghijklmnopqrstuvwxyz12"  # example placeholder only\n',
        encoding="utf-8",
    )
    findings = scan_tree(tmp_path)
    assert findings == []


def test_this_repo_redact_scan_is_clean():
    """If this goes RED, we published a live secret — the finding is the product."""
    text, code = run_redact_scan(repo_root=str(ROOT))
    assert code == 0, text
    assert "clean" in text


def test_cli_redact_scan_exits_zero_on_this_repo():
    proc = subprocess.run(
        [sys.executable, "-m", "magnet.cli", "redact-scan"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "findings   0" in proc.stdout


def test_magnet_stack_env_overrides_fixture(tmp_path, monkeypatch):
    fake = tmp_path / "other-stack"
    (fake / "skills" / "x").mkdir(parents=True)
    (fake / "skills" / "x" / "SKILL.md").write_text(
        "---\nname: x\ndescription: debug a failing test\n---\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("MAGNET_STACK", str(fake))
    assert default_stack_dir(str(ROOT)) == str(fake)
