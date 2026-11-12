"""python scripts/school_icon.py <school>  ->  schools/<school>.png (128 px).

The panel's mark in white on the school's colour, for the extension list.
Needs Python Playwright (host: /opt/miniconda3/bin/python)."""
import json
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

root = pathlib.Path(__file__).resolve().parents[1]
school_id = sys.argv[1]
school = json.loads((root / "schools" / f"{school_id}.json").read_text())
accent = school["accent"]
if not re.fullmatch(r"#[0-9a-fA-F]{6}", accent):
    sys.exit(f"school {school_id}: accent must be #rrggbb")
# The variant's own mark (schools/<id>.svg) or BulkHours' B; drawn in white
# on the accent, or in the accent on the variant's `tile` colour.
mark = root / "schools" / f"{school_id}.svg"
tile = school.get("tile")
ink, ground = (accent, tile) if tile else ("#ffffff", accent)
svg = (mark if mark.exists() else root / "media" / "icon.svg").read_text()
svg = svg.replace("currentColor", ink).replace("<svg", '<svg width="88" height="88"')
html = (f'<body style="margin:0;background:transparent"><div style="width:128px;height:128px;border-radius:28px;'
        f'background:{ground};display:grid;place-items:center">{svg}</div></body>')
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 128, "height": 128})
    page.set_content(html)
    out = root / "schools" / f"{school_id}.png"
    page.screenshot(path=str(out), omit_background=True)
    browser.close()
print(out.relative_to(root))
