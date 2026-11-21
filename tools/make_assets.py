"""Regenerate favicons and the social share image from the brand mark.

Usage (from the repo root):  python3 tools/make_assets.py
Needs: Python 3 with Pillow, and Google Chrome (for the share image).
"""
import math, os, re, subprocess, tempfile
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK, PAPER = (24, 58, 48), (236, 237, 230)  # forest, paper


def gaussian(width, base, peak, steps=400):
    sigma, amp, cx = width * 0.15, base - peak, width / 2
    return [(x, base - amp * math.exp(-((x - cx) ** 2) / (2 * sigma ** 2)))
            for x in (width * i / steps for i in range(steps + 1))]


def icon(size):
    """Paper bell curve with three cut rules, on a forest rounded square."""
    s = 8  # supersample
    W = size * s
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, W - 1, W - 1], radius=int(W * 0.19), fill=INK)
    pad, base, peak = W * 0.08, W * 0.74, W * 0.22
    pts = [(pad + x, y) for x, y in gaussian(W - 2 * pad, base, peak)]
    d.polygon([(pad, base)] + pts + [(W - pad, base)], fill=PAPER)
    gap = max(W * 0.035, s * 1.0)
    for f in (0.75, 0.5, 0.25):
        y = base - f * (base - peak)
        d.rectangle([0, y - gap / 2, W, y + gap / 2], fill=INK)
    return im.resize((size, size), Image.LANCZOS)


def favicons():
    for size, name in [(32, "favicon-32.png"), (180, "apple-touch-icon.png"),
                       (192, "icon-192.png"), (512, "icon-512.png")]:
        img = icon(size)
        if name == "apple-touch-icon.png":  # iOS wants an opaque square
            bg = Image.new("RGB", img.size, INK)
            bg.paste(img, mask=img.split()[3])
            img = bg
        img.save(os.path.join(ROOT, "assets", name))


def og_image():
    html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    svg = re.search(r'<svg class="lockup".*?</svg>', html, re.S).group(0)
    page = f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,400&family=Schibsted+Grotesk:wght@500&display=swap">
<style>
html,body{{margin:0;width:1200px;height:630px;background:#183A30;overflow:hidden}}
.wrap{{position:relative;width:1200px;height:630px}}
.tag{{position:absolute;left:64px;top:52px;font:500 22px/1.3 "Schibsted Grotesk",sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#BFCCC5}}
.lockup{{position:absolute;left:0;right:0;bottom:44px;width:1200px;height:470px;overflow:visible}}
.lockup__rules line{{stroke:rgba(236,237,230,.62);stroke-width:3.2}}
.lockup__curve{{fill:#ECEDE6}}
.lockup__gaps line{{stroke:#183A30;stroke-width:3.6}}
.lockup__word{{fill:#ECEDE6;font-family:"Bodoni Moda",Georgia,serif;font-size:124px;font-variation-settings:"opsz" 30}}
</style></head><body><div class="wrap">
<div class="tag">Communications · Experiential · Project delivery</div>
{svg}
</div></body></html>"""
    with tempfile.TemporaryDirectory(dir=os.path.expanduser("~/.cache")) as tmp:
        path = os.path.join(tmp, "og.html")
        open(path, "w", encoding="utf-8").write(page)
        subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--no-first-run", f"--user-data-dir={tmp}/profile", "--virtual-time-budget=6000",
                        "--window-size=1200,630", f"--screenshot={ROOT}/assets/og.png", f"file://{path}"],
                       check=True, capture_output=True)


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    favicons()
    og_image()
    print("Wrote assets/: favicon-32.png apple-touch-icon.png icon-192.png icon-512.png og.png")
