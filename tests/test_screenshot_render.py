"""Slice 27 — screenshot renderer finds a monospace font on Linux."""
from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RENDER = ROOT / "scripts" / "render-screenshot.py"


def test_render_screenshot_font_candidates_include_linux_paths():
    text = RENDER.read_text(encoding="utf-8")
    assert "DejaVuSansMono.ttf" in text
    assert "/System/Library/Fonts/Menlo.ttc" in text  # macOS kept


def test_render_screenshot_loads_a_font_on_this_host():
    pytest.importorskip("PIL")
    import importlib.util

    spec = importlib.util.spec_from_file_location("render_screenshot", RENDER)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    font = mod.load_font(20)
    assert font is not None


def test_pred_demo_sidecar_exists_and_mentions_finding():
    side = ROOT / "docs" / "screenshots" / "pred-demo.txt"
    assert side.is_file()
    text = side.read_text(encoding="utf-8")
    assert "magnet pred-demo" in text or "pred-demo" in text
    assert "FINDING" in text
    assert "stay_at_wrong_level" in text
    png = ROOT / "docs" / "screenshots" / "pred-demo.png"
    assert png.is_file()
    assert png.stat().st_size > 1000
