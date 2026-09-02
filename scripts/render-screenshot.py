#!/usr/bin/env python3
"""Render a captured terminal transcript to a video-legible PNG.

Usage: render-screenshot.py <sidecar.txt> <out.png> [--font-size 30]

The .txt is the real output of the command (first line: the command, second
line: when and where it ran). This draws exactly that text in Menlo on a dark
terminal ground, wide enough for a 1920-wide video frame. Nothing is edited.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = (
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/SFNSMono.ttf",
    "/System/Library/Fonts/Supplemental/Courier New.ttf",
)
BG = (24, 24, 27)
FG = (229, 229, 234)
DIM = (140, 140, 150)
PROMPT = (110, 200, 140)
GOOD = (120, 210, 150)
BAD = (240, 130, 120)


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    sys.exit("no monospace font found")


def colour_for(line: str) -> tuple[int, int, int]:
    if line.startswith("$ "):
        return PROMPT
    if line.startswith("#"):
        return DIM
    low = line.lower()
    if "hurt" in low or "fail" in low or "✗" in line:
        return BAD
    if "helped" in low or "pass" in low or "✓" in line or "OK" in line:
        return GOOD
    return FG


def render(src: Path, out: Path, font_size: int) -> None:
    lines = src.read_text(encoding="utf-8").rstrip("\n").split("\n")
    font = load_font(font_size)
    pad = font_size * 2
    line_h = int(font_size * 1.45)
    widest = max(font.getlength(ln) for ln in lines) if lines else 0
    width = max(1600, int(widest) + pad * 2)
    height = pad * 2 + line_h * len(lines) + int(font_size * 1.2)
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)
    # three window dots, so it reads as a terminal at a glance
    for i, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
        x = pad // 2 + i * int(font_size * 0.9)
        draw.ellipse((x, pad // 2, x + font_size // 2, pad // 2 + font_size // 2), fill=c)
    y = pad + font_size // 2
    for ln in lines:
        draw.text((pad, y), ln, font=font, fill=colour_for(ln))
        y += line_h
    img.save(out, optimize=True)
    print(f"{out}  {width}x{height}  {len(lines)} lines  font {font_size}px")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--font-size", type=int, default=30)
    a = ap.parse_args()
    render(a.src, a.out, a.font_size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
