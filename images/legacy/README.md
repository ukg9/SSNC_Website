# SSNC Legacy redesign — full replacement code

**Target:** GitHub development branch `improve/mobile-seo-performance-20261015` (not `main`).

## What's included
- `legacy.html` — fully replaced page, embedded CSS and lightbox JS, recent highlights and composite photo timeline, gallery folded into page, year order 2026 → 2012.
- `gallery.html` — legacy URL fallback redirects to `legacy.html#photo-stories`.
- `_redirects` — preferred Netlify 301 redirects (preserves links; replaces old Gallery endpoint).
- `partials/header.html` — full shared header without Gallery in desktop or mobile menus.
- `images/legacy/recent-camp-2026-{1,2,3,4}.webp` — web-optimized versions of four user-uploaded 2026 photographs.
- `scripts/apply_to_repo.py` — optional script to apply the package to a local GitHub checkout; updates other five pages' shared header, removes old Gallery sitemap link, updates existing shared-header synchronization script.

## Fastest local application (recommended)
1. Download/unzip this bundle.
2. Check out the DEVELOPMENT branch of `SSNC_Website` locally. Do not use main.
3. In your repo root, run `python path/to/SSNC_Legacy_Replacement/scripts/apply_to_repo.py`. If the bundle is located elsewhere, use its actual path.
4. Review `git diff` and confirm images present under `images/legacy/`.
5. Commit on the development branch and push; check Netlify Deploy Preview.

## Applying through GitHub web editor
Replace `legacy.html`, `gallery.html`, and `partials/header.html` with the supplied complete files. Upload four WebP files into `images/legacy/`. Add/replace `_redirects` at the repo root. In `index.html`, `about.html`, `services.html`, `Education.html`, `Consultation.html`, remove both Gallery navigation `<a>` entries from the shared header, update any remaining `href="gallery.html"` calls to action to `href="legacy.html#photo-stories"`, or replace their entire `<!-- SSNC-SHARED-HEADER -->` marked blocks from `partials/header.html` and set `aria-current="page"` on each respective page's own nav link. Remove `gallery.html` from scripts/sync_layout.py and sitemap.xml.

## Updating Recent Highlights later
In `legacy.html`, search `UPDATEABLE RECENT HIGHLIGHTS`. Replace `src` and `href` values in the four `.recent-card` anchors with your new photos (and update their descriptive captions). Use unique photos; don't repeat them in other timelines or montage cards.

## Important
All 4 recent photos are displayed once in the Recent section. Other gallery and dated legacy photo paths refer to files already present in the current development branch. Date claims are based on dated filenames, not independently verified event records. The archive does not assign unverified dates.

**Not yet deployed** — These are ready-to-apply replacement files. Test in Netlify Deploy Preview before merging into main.
