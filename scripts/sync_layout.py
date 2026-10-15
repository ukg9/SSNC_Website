#!/usr/bin/env python3
"""Keep the seven static pages' common header/footer synchronized with partials."""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
pages=["index.html","about.html","services.html","gallery.html","legacy.html","Consultation.html","Education.html"]
header=(root/"partials/header.html").read_text(encoding="utf-8").strip()
footer=(root/"partials/footer.html").read_text(encoding="utf-8").strip()
for name in pages:
    file=root/name
    c=file.read_text(encoding="utf-8")
    for kind,template in (("HEADER",header),("FOOTER",footer)):
        start=f"<!-- SSNC-SHARED-{kind}:START -->"
        end=f"<!-- SSNC-SHARED-{kind}:END -->"
        if c.count(start)!=1 or c.count(end)!=1:
            raise RuntimeError(f"{name}: missing or duplicate {kind} markers")
        content=template
        content=content.replace(f'href="{name}"',f'href="{name}" aria-current="page"')
        begin=c.index(start);finish=c.index(end,begin)+len(end)
        c=c[:begin]+content+c[finish:]
    file.write_text(c,encoding="utf-8")
print(f"Synchronized {len(pages)} shared layouts.")
