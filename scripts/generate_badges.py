"""Generate accreditation badge SVGs (+ PNG rasters when Pillow is available)
and a badges/index.html showcase from courses.json.

Each course gets one badge per locale (mi = te reo Māori, en = English).
Adding a locale: extend LOCALES below.

Badge design:
- 1200×1200 circular black field
- Red poutama stepped chevron at the base
- Thinker glyph centred (star, gear, koru, etc.)
- Course title arc-text around the top
- "POU TOHU" + locale label on the lower rim
"""
import json, math
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BADGES = BASE / "badges"
BADGES.mkdir(exist_ok=True)

# Locale labels and rim text. Extend here to add a language.
LOCALES = {
    "mi": {"label": "TE REO MĀORI", "completion": "Kua Oti — Pou Tohu", "subline": "Kua tutuki tēnei akoranga"},
    "en": {"label": "ENGLISH",      "completion": "Completed — Course Pou", "subline": "Awarded on completion"},
}

# Glyph SVG fragments (centred, ~340px tall, drawn in white with red highlight).
GLYPHS = {
    "star": """<polygon points="600,310 660,500 860,500 700,615 760,810 600,695 440,810 500,615 340,500 540,500"
                 fill="#f5f0e6" stroke="#c41e1e" stroke-width="6"/>""",
    "gear": """<g fill="#f5f0e6" stroke="#c41e1e" stroke-width="5">
                <circle cx="600" cy="600" r="160"/>
                <circle cx="600" cy="600" r="60" fill="#0c0c0c"/>
              </g>""",
    "hands": """<g fill="none" stroke="#f5f0e6" stroke-width="14" stroke-linecap="round">
                  <path d="M460 640 Q540 540 600 600 Q660 540 740 640"/>
                  <path d="M460 690 Q540 590 600 650 Q660 590 740 690" stroke="#c41e1e"/>
                </g>""",
    "chain": """<g fill="none" stroke="#f5f0e6" stroke-width="14">
                  <ellipse cx="540" cy="600" rx="60" ry="90"/>
                  <ellipse cx="660" cy="600" rx="60" ry="90"/>
                </g>""",
    "koru": """<path d="M600 460 C 720 460 780 560 780 640 C 780 740 700 800 600 800 C 520 800 460 740 460 660 C 460 600 520 560 600 560 C 660 560 700 600 700 640"
                fill="none" stroke="#f5f0e6" stroke-width="14"/>""",
    "rhizome": """<g fill="none" stroke="#f5f0e6" stroke-width="10">
                    <circle cx="500" cy="540" r="22"/><circle cx="700" cy="540" r="22"/>
                    <circle cx="540" cy="700" r="22"/><circle cx="660" cy="700" r="22"/>
                    <circle cx="600" cy="620" r="22" fill="#c41e1e" stroke="#c41e1e"/>
                    <path d="M500 540 L600 620 L700 540 M540 700 L600 620 L660 700 M500 540 L540 700 M700 540 L660 700"/>
                  </g>""",
}

def arc_text(text: str, radius: int, top: bool = True, size: int = 54,
             color: str = "#f5f0e6", spacing: int = 6) -> str:
    """Render text along a circular arc centred on (600, 600).

    top=True   → arc across the upper half, text reads left-to-right along the top.
    top=False  → arc across the lower half, text reads left-to-right along the bottom.
    """
    pid = f"arc-{abs(hash((text, radius, top, size))) % 1_000_000}"
    if top:
        # Upper semicircle: start bottom-left of arc, sweep clockwise to bottom-right.
        d = (f"M {600 - radius} 600 "
             f"A {radius} {radius} 0 0 1 {600 + radius} 600")
    else:
        # Lower semicircle reversed so text baseline sits on the inside of the
        # arc and reads left-to-right when viewed normally.
        d = (f"M {600 - radius} 600 "
             f"A {radius} {radius} 0 0 0 {600 + radius} 600")
    return f"""<defs><path id="{pid}" d="{d}"/></defs>
<text font-family="'Bebas Neue',sans-serif" font-size="{size}" fill="{color}" letter-spacing="{spacing}">
  <textPath href="#{pid}" startOffset="50%" text-anchor="middle">{text}</textPath>
</text>"""

def poutama() -> str:
    """Two small poutama chevrons flanking the centre — do not crowd the rim text."""
    out = []
    step = 18
    base_y = 900
    cols = [step * (i + 1) for i in range(5)]
    # Left poutama, ascending toward centre.
    x0 = 360
    for i, h in enumerate(cols):
        out.append(f'<rect x="{x0 + i*step}" y="{base_y - h}" width="{step}" height="{h}" fill="#c41e1e"/>')
    # Right poutama, mirrored.
    x0 = 740
    for i, h in enumerate(cols):
        out.append(f'<rect x="{x0 + i*step}" y="{base_y - h}" width="{step}" height="{h}" fill="#c41e1e"/>')
    return "\n".join(out)

def badge_svg(course: dict, locale: str) -> str:
    title = course["title"].upper()
    glyph = GLYPHS.get(course.get("badge_glyph", "star"), GLYPHS["star"])
    loc = LOCALES[locale]
    # Trim long titles so arc text fits cleanly along the top.
    short = title.split("—")[0].strip() if "—" in title else title
    if len(short) > 28:
        short = short[:26] + "…"
    # Top arc sits well inside the rim; bottom arc reads left-to-right above the poutama band.
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1200" width="1200" height="1200">
  <rect width="1200" height="1200" fill="#0c0c0c"/>
  <circle cx="600" cy="600" r="560" fill="#0e0e0e" stroke="#c41e1e" stroke-width="10"/>
  <circle cx="600" cy="600" r="500" fill="none" stroke="#1a1a1a" stroke-width="2"/>
  {arc_text(short, 480, top=True, size=54)}
  {arc_text(loc["completion"].upper(), 480, top=False, size=42, color="#c41e1e", spacing=8)}
  {glyph}
  {poutama()}
  <text x="600" y="230" font-family="'Bebas Neue',sans-serif" font-size="30" fill="#c41e1e"
        text-anchor="middle" letter-spacing="8">THE KIWI DIALECTIC</text>
  <text x="600" y="1000" font-family="'Bebas Neue',sans-serif" font-size="22" fill="#8a8a8a"
        text-anchor="middle" letter-spacing="6">POU TOHU · {loc["label"]}</text>
</svg>
"""

def maybe_png(svg_path: Path) -> None:
    """If cairosvg is available, render a PNG sibling. Otherwise skip silently."""
    try:
        import cairosvg  # type: ignore
        png = svg_path.with_suffix(".png")
        cairosvg.svg2png(url=str(svg_path), write_to=str(png), output_width=1200, output_height=1200)
    except Exception:
        pass

def write_index(data: dict) -> None:
    rows = []
    for c in data["courses"]:
        slug = c["slug"]
        access = c.get("access", "free_subscriber")
        access_label = "PAID SUBSCRIBER" if access == "paid_subscriber" else "FREE SUBSCRIBER"
        launch = next((l for l in c.get("lessons", []) if l), None)
        course_url = (launch or {}).get("link") or "https://www.kiwidialectic.com/s/courses"
        chat_url = c.get("chat_thread") or "https://substack.com/chat"
        rows.append(f"""<article class="badge" id="{slug}">
  <h3>{c['title']} <span class="pill">{access_label}</span></h3>
  <div class="status">Status: {c.get('status','')} · <a href="{course_url}">Open course on Substack</a> · <a href="{chat_url}">Chat thread</a></div>
  <p class="reqs">To claim this pou tohu you must (1) be a Kiwi Dialectic subscriber, (2) read all lessons on Substack, (3) post your completion reflection in the course chat thread. Robert awards the badge by reply with your name added below the SVG.</p>
  <div class="grid">
    <a href="{slug}/mi.svg"><img src="{slug}/mi.svg" alt="{c['title']} — te reo Māori badge"/><span>TE REO MĀORI · download SVG</span></a>
    <a href="{slug}/en.svg"><img src="{slug}/en.svg" alt="{c['title']} — English badge"/><span>ENGLISH · download SVG</span></a>
  </div>
  <div class="ctas">
    <a class="cta" href="{course_url}">Open the course →</a>
    <a class="cta alt" href="{chat_url}">Claim in chat thread →</a>
    <a class="cta alt" href="https://www.kiwidialectic.com/subscribe">Subscribe (free) →</a>
  </div>
</article>""")
    html = """<!doctype html><html lang="en"><head><meta charset="utf-8"/>
<title>Pou Tohu — Course Accreditation Badges · The Kiwi Dialectic</title>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600&display=swap" rel="stylesheet"/>
<style>
body{margin:0;background:#0c0c0c;color:#f5f0e6;font-family:Inter,system-ui,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:32px 22px}
h1{font-family:'Bebas Neue',sans-serif;font-size:72px;letter-spacing:.02em;margin:0 0 6px}
h1 .r{color:#c41e1e}
p.lede{max-width:62ch;line-height:1.6;color:#cfc8b9}
.gate{background:#120e0e;border:1px solid #3a2222;padding:14px 16px;margin:18px 0 8px;font-size:14px;line-height:1.55;color:#cfc8b9;max-width:62ch}
.gate strong{color:#c41e1e;font-family:'Bebas Neue',sans-serif;letter-spacing:.08em;display:block;margin-bottom:4px}
.gate a{color:#fff;border-bottom:1px solid #c41e1e;text-decoration:none}
.badge{border-top:1px solid #1a1a1a;padding:28px 0;scroll-margin-top:24px}
.badge h3{font-family:'Bebas Neue',sans-serif;font-size:28px;margin:0 0 4px;letter-spacing:.02em}
.badge h3 .pill{display:inline-block;background:#c41e1e;color:#fff;font-size:12px;letter-spacing:.08em;padding:2px 8px;margin-left:8px;vertical-align:3px;font-family:'Bebas Neue',sans-serif}
.status{color:#8a8a8a;font-size:13px;margin-bottom:10px;letter-spacing:.04em}
.status a{color:#cfc8b9;border-bottom:1px solid #2a2a2a;text-decoration:none}
.status a:hover{border-color:#c41e1e}
.reqs{font-size:13px;line-height:1.6;color:#cfc8b9;margin:0 0 14px;max-width:62ch}
.ctas{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}
.cta{display:inline-block;padding:10px 16px;background:#c41e1e;color:#fff;font-family:'Bebas Neue',sans-serif;letter-spacing:.12em;font-size:13px;text-decoration:none}
.cta.alt{background:#000;color:#f5f0e6;border:1px solid #1a1a1a}
.cta:hover{filter:brightness(1.1)}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}
.grid a{display:block;background:#101010;border:1px solid #1a1a1a;padding:14px;text-align:center;color:inherit;text-decoration:none;transition:border-color .15s}
.grid a:hover{border-color:#c41e1e}
.grid img{width:100%;height:auto;display:block;margin-bottom:10px}
.grid span{font-family:'Bebas Neue',sans-serif;letter-spacing:.14em;font-size:13px;color:#c41e1e}
footer{border-top:1px solid #1a1a1a;margin-top:48px;padding:18px 0;color:#8a8a8a;font-size:13px}
</style></head><body><div class="wrap">
<h1>POU TOHU <span class="r">·</span> ACCREDITATION</h1>
<p class="lede">A <em>pou tohu</em> — post, marker, badge — is awarded after completing each course. Free to use; please credit The Kiwi Dialectic. Every badge ships in te reo Māori and English; more locales on request.</p>
<div class="gate"><strong>SUBSCRIBER ACCESS</strong>Every course — free or paid — requires a Kiwi Dialectic subscription. Free subscribers get every lesson, every chat thread, and every pou tohu. Paid subscribers also get the workbooks and live Q&amp;A. <a href="https://www.kiwidialectic.com/subscribe">Subscribe (free) →</a></div>
""" + "\n".join(rows) + """
<footer>The Kiwi Dialectic · Ōtepoti / Dunedin · <a href="https://www.kiwidialectic.com" style="color:#c41e1e">kiwidialectic.com</a></footer>
</div></body></html>"""
    (BADGES / "index.html").write_text(html)

def main():
    data = json.loads((BASE / "courses.json").read_text())
    for course in data["courses"]:
        d = BADGES / course["slug"]
        d.mkdir(exist_ok=True)
        for locale in LOCALES:
            svg_path = d / f"{locale}.svg"
            svg_path.write_text(badge_svg(course, locale))
            maybe_png(svg_path)
    write_index(data)
    print(f"wrote badges for {len(data['courses'])} courses ({len(LOCALES)} locales each)")

if __name__ == "__main__":
    main()
