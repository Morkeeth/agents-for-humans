"""Redact-scan — find live secrets that should never be in a public repo.

Embarrassment hunt: a scan that can fail this repo. Patterns are conservative
(precision over recall). A planted secret in a temp tree must go RED; the
clean tree must go GREEN. `grep -qv` on empty input is not a control — every
finding opens the file at the line.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

# Patterns that mean "this should not be committed". Deliberately narrow.
SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("aws_secret_assign", re.compile(r"(?i)aws_secret_access_key\s*[:=]\s*['\"]?[A-Za-z0-9/+=]{40}")),
    ("generic_api_key_assign", re.compile(r"(?i)(?:api[_-]?key|secret[_-]?key)\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]")),
    ("postgres_url", re.compile(r"postgres(?:ql)?://[^\s:'\"]+:[^\s:'\"]+@[^\s'\"]+")),
    ("private_key_block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)

SKIP_DIR_NAMES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".magnet",
    ".pytest_cache",
    "dist",
    "build",
}

# Docs that intentionally quote fake secrets as examples — still scanned, but
# these substrings are allowlisted only when the line also contains the marker.
EXAMPLE_MARKERS = ("example", "fake", "placeholder", "not a real", "REDACTED")


def _iter_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES and not d.startswith(".")]
        for name in filenames:
            path = Path(dirpath) / name
            # Text / binary-ish skip
            if path.suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pyc", ".db", ".sqlite"}:
                continue
            if path.stat().st_size > 1_000_000:
                continue
            out.append(path)
    return out


def _line_is_example(line: str) -> bool:
    """Allowlist only when an example marker is a clear word/phrase, not a substring of a key."""
    low = line.lower()
    for m in EXAMPLE_MARKERS:
        if " " in m:
            if m in low:
                return True
        elif re.search(rf"\b{re.escape(m)}\b", low):
            return True
    return False



def scan_tree(root: str | Path) -> list[dict]:
    """Return findings: {path, line, kind, snippet}. Empty list = clean."""
    base = Path(root)
    findings: list[dict] = []
    for path in _iter_files(base):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            if _line_is_example(line):
                continue
            for kind, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    findings.append(
                        {
                            "path": str(path.relative_to(base)),
                            "line": i,
                            "kind": kind,
                            "snippet": line.strip()[:160],
                        }
                    )
    return findings


def render_scan(findings: list[dict], *, root: str) -> str:
    lines = [
        "MAGNET redact-scan — live secrets in a public tree",
        "",
        f"  root       {root}",
        f"  findings   {len(findings)}",
        "",
    ]
    if not findings:
        lines += [
            "  clean      no matched secret patterns",
            "  repro      magnet redact-scan",
        ]
        return "\n".join(lines)
    lines.append("  FINDINGS (open the file — do not trust this summary alone)")
    for f in findings:
        lines.append(f"    {f['path']}:{f['line']}  [{f['kind']}]  {f['snippet']}")
    lines += ["", "  repro      magnet redact-scan", "  exit       1"]
    return "\n".join(lines)


def run_redact_scan(*, repo_root: str | None = None) -> tuple[str, int]:
    root = repo_root or os.getcwd()
    findings = scan_tree(root)
    return render_scan(findings, root=root), (1 if findings else 0)
