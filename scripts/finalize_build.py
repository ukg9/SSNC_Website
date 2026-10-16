#!/usr/bin/env python3
"""Replace CDN runtime Tailwind with compiled CSS after successful build."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
css=root/"assets/site.css"
if not css.exists() or css.stat().st_size < 1000: raise SystemExit("Compiled CSS missing or unexpectedly small")
for page in sorted(root.glob("*.html")):
 s=page.read_text(encoding="utf-8")
 s=s.replace('<script src="https://cdn.tailwindcss.com"></script>','<link rel="stylesheet" href="assets/site.css">')
 if page.name=="index.html" and "<main" not in s.lower():
  s=s.replace('<!-- Image Slider with Individual Quotes -->','<!-- Image Slider with Individual Quotes -->',1)
  start=s.find('<section',s.find('</header>'))
  end=s.find('<!-- Footer -->')
  if start>=0 and end>start:
   s=s[:start]+'<main id="main-content">\n'+s[start:end]+'</main>\n'+s[end:]
 page.write_text(s,encoding="utf-8")
print("Production stylesheet linked in HTML pages.")
