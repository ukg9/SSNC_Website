#!/usr/bin/env python3
"""Create responsive, lightweight variants of existing local images without changing originals.
The GitHub Actions build uses these outputs and commits them to the working branch.
"""
from __future__ import annotations
import hashlib
import re
from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "images" / "optimized"
SOURCE = re.compile(r'(<img\b[^>]*\bsrc\s*=\s*)(["\'])(images/[^"\']+\.(?:jpe?g|png))\2([^>]*>)', re.I | re.S)
BACKGROUND = re.compile(r'url\((["\']?)(images/[^)"\']+\.(?:jpe?g|png))\1\)', re.I)
cache: dict[str, tuple[int, int, list[tuple[int, str]]]] = {}

def optimize(source: str):
    if source in cache:
        return cache[source]
    path = ROOT / source
    if not path.is_file():
        print(f"Skipping missing image: {source}")
        return None
    key = re.sub(r'[^a-z0-9]+', '-', path.stem.lower()).strip('-')
    short_hash = hashlib.sha1(source.encode()).hexdigest()[:7]
    name = f"{key}-{short_hash}"
    ASSET_ROOT.mkdir(parents=True, exist_ok=True)
    try:
        with Image.open(path) as opened:
            img = ImageOps.exif_transpose(opened)
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
            full_width, full_height = img.size
            if full_width < 1 or full_height < 1:
                return None
            variants = []
            for max_width in ([480, 1600] if full_width > 700 else [480]):
                actual_width = min(max_width, full_width)
                target_height = max(1, round(full_height * actual_width / full_width))
                copy = img.copy()
                if actual_width != full_width:
                    copy = copy.resize((actual_width, target_height), Image.Resampling.LANCZOS)
                dest = ASSET_ROOT / f"{name}-{actual_width}.webp"
                copy.save(dest, format="WEBP", quality=78, method=5)
                variants.append((actual_width, dest.relative_to(ROOT).as_posix()))
            cache[source] = (full_width, full_height, variants)
            return cache[source]
    except (OSError, UnidentifiedImageError, ValueError) as exc:
        print(f"Unable to optimize {source}: {exc}")
        return None

def change_img(match):
    opening, quote, original, rest = match.groups()
    details = optimize(original)
    if not details:
        return match.group(0)
    width, height, variants = details
    by_width = sorted(variants)
    default = by_width[0][1]
    rest = re.sub(r'\s+srcset\s*=\s*(["\']).*?\1', '', rest, flags=re.I|re.S)
    rest = re.sub(r'\s+sizes\s*=\s*(["\']).*?\1', '', rest, flags=re.I|re.S)
    if not re.search(r'\bwidth\s*=', rest):
        rest = f' width="{width}"' + rest
    if not re.search(r'\bheight\s*=', rest):
        rest = f' height="{height}"' + rest
    tag = opening + quote + default + quote
    if len(by_width) > 1:
        srcset = ', '.join(f'{path} {w}w' for w, path in by_width)
        sizing = "64px" if re.search(r'\bw-16\b', rest) else ("100vw" if re.search(r'h-screen|w-full', rest) else "(max-width: 640px) 100vw, 700px")
        tag += f' srcset="{srcset}" sizes="{sizing}"'
    return tag + rest

for page in sorted(ROOT.glob("*.html")):
    original = page.read_text(encoding="utf-8")
    updated = SOURCE.sub(change_img, original)
    def change_background(m):
        details = optimize(m.group(2))
        if not details:
            return m.group(0)
        return "url('" + details[2][-1][1] + "')"
    updated = BACKGROUND.sub(change_background, updated)
    if original != updated:
        page.write_text(updated, encoding="utf-8")
print(f"Optimized {len(cache)} original image references.")
