#!/usr/bin/env python3
"""
Renders the branded 1080x1350 graphic for each slide in
social-assets/series/plan.json using headless Chromium, matching the
site's navy/gold design system (see tools/social_series_template.html).

Usage: python3 tools/social_series_generator.py [--only DAY_NUM]

Requires a Chromium binary. Set CHROME_BIN to override the default
lookup under /opt/pw-browsers.
"""
import base64
import glob
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from png_crop import crop_top_left

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN_PATH = os.path.join(REPO_ROOT, "social-assets", "series", "plan.json")
TEMPLATE_PATH = os.path.join(REPO_ROOT, "tools", "social_series_template.html")
OUT_DIR = os.path.join(REPO_ROOT, "social-assets", "series")
MARK_PATH = os.path.join(REPO_ROOT, "manzil-mark.png")


def find_chrome():
    override = os.environ.get("CHROME_BIN")
    if override and os.path.isfile(override):
        return override
    candidates = glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")
    if candidates:
        return sorted(candidates)[-1]
    candidates = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell")
    if candidates:
        return sorted(candidates)[-1]
    raise SystemExit("No Chromium binary found. Set CHROME_BIN.")


def render_slide(chrome, template, mark_b64, slide, total):
    bullets_html = "\n".join(
        f'<div class="bullet"><div class="dot"></div><p>{b}</p></div>'
        for b in slide["bullets"]
    )
    html = (
        template
        .replace("__NUM__", f'{slide["day"]:02d}')
        .replace("__TOTAL__", f"{total:02d}")
        .replace("__HEADLINE__", slide["headline"])
        .replace("__BULLETS__", bullets_html)
        .replace("__MARK_B64__", mark_b64)
    )
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
        html_path = f.name

    # Headless Chromium's viewport (window.innerHeight) in this environment
    # is consistently ~90px shorter than the requested --window-size, so the
    # bottom of the page renders as blank space if we ask for exactly
    # 1080x1350. Render taller, then crop to the exact target size.
    render_height = 1350 + 150
    out_path = os.path.join(OUT_DIR, f'day-{slide["day"]:02d}.png')
    tall_path = out_path + ".tall.png"
    subprocess.run(
        [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            "--force-color-profile=srgb",
            f"--window-size=1080,{render_height}",
            f"--screenshot={tall_path}",
            f"file://{html_path}",
        ],
        check=True,
        capture_output=True,
    )
    os.unlink(html_path)
    crop_top_left(tall_path, out_path, 1080, 1350)
    os.unlink(tall_path)
    return out_path


def main():
    only = None
    if "--only" in sys.argv:
        only = int(sys.argv[sys.argv.index("--only") + 1])

    with open(PLAN_PATH) as f:
        plan = json.load(f)
    with open(TEMPLATE_PATH) as f:
        template = f.read()
    with open(MARK_PATH, "rb") as f:
        mark_b64 = base64.b64encode(f.read()).decode("ascii")

    chrome = find_chrome()
    os.makedirs(OUT_DIR, exist_ok=True)

    total = len(plan["slides"])
    for slide in plan["slides"]:
        if only is not None and slide["day"] != only:
            continue
        out_path = render_slide(chrome, template, mark_b64, slide, total)
        print(f'day {slide["day"]:02d} -> {out_path}')


if __name__ == "__main__":
    main()
