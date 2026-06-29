"""Generate six per-module Te Pā pou tohu (en + mi) as 1200x1200 SVGs.

Style locked to match badges/te-pa-tuwatawata/{en,mi}.svg:
  - Charcoal background #0c0c0c, red ring #c41e1e
  - Bebas Neue arc text (top: course title, bottom: module tag)
  - Centre motif specific to each module
  - Niho taniwha base running across the bottom

Run: python scripts/build_te_pa_badges.py
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "badges"

CHARCOAL = "#0c0c0c"
RING_BG  = "#0e0e0e"
RED      = "#c41e1e"
BONE     = "#f5f0e6"
GREY     = "#8a8a8a"
INK      = "#1a1a1a"

# ---------------------------------------------------------------------------
# Motif SVG fragments — each draws centred around (600, 600) inside 1200x1200
# ---------------------------------------------------------------------------

def motif_koru() -> str:
    """Module 1 — Whakapapa: a single unfurling koru spiral."""
    return f"""
  <g stroke="{BONE}" stroke-width="16" fill="none" stroke-linecap="round">
    <path d="M 600 820
             C 460 820 360 720 360 580
             C 360 460 460 380 580 380
             C 680 380 760 460 760 560
             C 760 640 700 700 620 700
             C 560 700 510 650 510 590
             C 510 540 550 500 600 500
             C 640 500 670 530 670 570"/>
  </g>
  <circle cx="670" cy="570" r="14" fill="{RED}"/>
"""

def motif_pa() -> str:
    """Module 2 — Te Pā Tūwatawata: stylised palisade fortification."""
    posts = []
    # outer palisade ring (truncated arc) — 11 stakes
    cx, cy = 600, 640
    import math
    for i, t in enumerate([-0.55, -0.44, -0.33, -0.22, -0.11, 0, 0.11, 0.22, 0.33, 0.44, 0.55]):
        angle = (-math.pi / 2) + t * math.pi
        r_top = 200
        r_base = 240
        x_top = cx + r_top * math.cos(angle)
        y_top = cy + r_top * math.sin(angle)
        x_base = cx + r_base * math.cos(angle)
        y_base = cy + r_base * math.sin(angle)
        posts.append(f'<line x1="{x_top:.1f}" y1="{y_top:.1f}" x2="{x_base:.1f}" y2="{y_base:.1f}" stroke="{BONE}" stroke-width="12" stroke-linecap="round"/>')
        # spear tip
        posts.append(f'<circle cx="{x_top:.1f}" cy="{y_top:.1f}" r="6" fill="{RED}"/>')
    # central whare outline (gable + base)
    whare = f"""
    <path d="M 520 700 L 600 580 L 680 700 Z" fill="none" stroke="{RED}" stroke-width="10"/>
    <rect x="540" y="700" width="120" height="80" fill="none" stroke="{BONE}" stroke-width="8"/>
    """
    return "\n  ".join(posts) + whare

def motif_niho() -> str:
    """Module 3 — Niho taniwha for AI/algorithmic encroachment: jagged teeth pattern."""
    teeth = []
    # row of nine triangular teeth, alternating red/bone, jagged baseline
    base_y = 720
    tip_y  = 480
    n = 9
    span = 540
    start_x = 600 - span / 2
    for i in range(n):
        x0 = start_x + i * (span / n)
        x1 = x0 + (span / n)
        xm = (x0 + x1) / 2
        fill = RED if i % 2 == 0 else BONE
        teeth.append(f'<path d="M {x0:.1f} {base_y} L {xm:.1f} {tip_y} L {x1:.1f} {base_y} Z" fill="{fill}"/>')
    # digital "bit" dots above teeth — algorithmic motif
    dots = []
    for i, x in enumerate(range(400, 820, 40)):
        c = RED if i % 3 == 0 else BONE
        dots.append(f'<circle cx="{x}" cy="430" r="6" fill="{c}"/>')
    return "\n  ".join(teeth + dots)

def motif_kowhaiwhai() -> str:
    """Module 4 — Kōwhaiwhai scroll pattern for tikanga/mana whakahaere."""
    return f"""
  <g fill="none" stroke="{BONE}" stroke-width="14" stroke-linecap="round">
    <path d="M 360 600
             C 360 480 460 480 520 540
             C 580 600 580 720 520 720
             C 460 720 460 600 540 600
             C 640 600 660 720 720 720
             C 800 720 820 600 760 540
             C 700 480 680 600 760 600
             C 820 600 840 540 840 480"/>
  </g>
  <g fill="{RED}">
    <circle cx="360" cy="600" r="14"/>
    <circle cx="840" cy="480" r="14"/>
    <circle cx="600" cy="660" r="10"/>
  </g>
"""

def motif_unaunahi() -> str:
    """Module 5 — Unaunahi (fish scales) for hoahoa tika / data sovereignty layering."""
    import math
    scales = []
    rows = 4
    for row in range(rows):
        y = 470 + row * 60
        offset = 30 if row % 2 else 0
        for col in range(7):
            x = 360 + offset + col * 70
            stroke = RED if (row + col) % 3 == 0 else BONE
            scales.append(
                f'<path d="M {x-30} {y} A 30 30 0 0 1 {x+30} {y}" fill="none" stroke="{stroke}" stroke-width="6"/>'
            )
    return "\n  ".join(scales)

def motif_takarangi() -> str:
    """Module 6 — Takarangi double spiral for anamata rangatira (sovereign future)."""
    return f"""
  <g fill="none" stroke-linecap="round">
    <path d="M 500 600
             C 500 540 540 500 600 500
             C 660 500 700 540 700 600
             C 700 660 660 700 600 700
             C 560 700 540 680 540 640
             C 540 600 580 580 600 600"
          stroke="{BONE}" stroke-width="14"/>
    <path d="M 700 600
             C 700 660 660 700 600 700
             C 540 700 500 660 500 600
             C 500 540 540 500 600 500
             C 640 500 660 520 660 560
             C 660 600 620 620 600 600"
          stroke="{RED}" stroke-width="14"/>
  </g>
  <circle cx="600" cy="600" r="10" fill="{BONE}"/>
"""

# ---------------------------------------------------------------------------

MODULES = [
    {
        "n": 1,
        "slug": "te-pa-module-1",
        "title_en": "WHAKAPAPA O TE RARAUNGA",
        "title_mi": "WHAKAPAPA O TE RARAUNGA",
        "tag_en":   "MODULE 1 · LINEAGE OF DATA",
        "tag_mi":   "WĀHANGA 1 · TE TIMATANGA",
        "motif": motif_koru,
    },
    {
        "n": 2,
        "slug": "te-pa-module-2",
        "title_en": "TE PĀ TŪWATAWATA HEI TAUIRA",
        "title_mi": "TE PĀ TŪWATAWATA HEI TAUIRA",
        "tag_en":   "MODULE 2 · THE PĀ AS PATTERN",
        "tag_mi":   "WĀHANGA 2 · HEI TAUIRA",
        "motif": motif_pa,
    },
    {
        "n": 3,
        "slug": "te-pa-module-3",
        "title_en": "AI ME TE RAUPATU MATIHIKO",
        "title_mi": "AI ME TE RAUPATU MATIHIKO",
        "tag_en":   "MODULE 3 · AI AND DIGITAL ENCROACHMENT",
        "tag_mi":   "WĀHANGA 3 · TE RAUPATU MATIHIKO",
        "motif": motif_niho,
    },
    {
        "n": 4,
        "slug": "te-pa-module-4",
        "title_en": "TIKANGA, TURE, MANA WHAKAHAERE",
        "title_mi": "TIKANGA, TURE, MANA WHAKAHAERE",
        "tag_en":   "MODULE 4 · LAW AND GOVERNANCE",
        "tag_mi":   "WĀHANGA 4 · MANA WHAKAHAERE",
        "motif": motif_kowhaiwhai,
    },
    {
        "n": 5,
        "slug": "te-pa-module-5",
        "title_en": "HOAHOA TIKA",
        "title_mi": "HOAHOA TIKA",
        "tag_en":   "MODULE 5 · DESIGNING WITH SOVEREIGNTY",
        "tag_mi":   "WĀHANGA 5 · HOAHOA RANGATIRA",
        "motif": motif_unaunahi,
    },
    {
        "n": 6,
        "slug": "te-pa-module-6",
        "title_en": "HE ANAMATA RANGATIRA",
        "title_mi": "HE ANAMATA RANGATIRA",
        "tag_en":   "MODULE 6 · A SOVEREIGN FUTURE",
        "tag_mi":   "WĀHANGA 6 · TE ANAMATA",
        "motif": motif_takarangi,
    },
]

# Niho taniwha base ornament shared by every badge (mirror of tuwatawata)
NIHO_BASE = """
  <g fill="{red}">
    <rect x="360" y="882" width="18" height="18"/>
    <rect x="378" y="864" width="18" height="36"/>
    <rect x="396" y="846" width="18" height="54"/>
    <rect x="414" y="828" width="18" height="72"/>
    <rect x="432" y="810" width="18" height="90"/>
    <rect x="740" y="882" width="18" height="18"/>
    <rect x="758" y="864" width="18" height="36"/>
    <rect x="776" y="846" width="18" height="54"/>
    <rect x="794" y="828" width="18" height="72"/>
    <rect x="812" y="810" width="18" height="90"/>
  </g>
""".format(red=RED)


def build_svg(module: dict, lang: str) -> str:
    title = module[f"title_{lang}"]
    tag   = module[f"tag_{lang}"]
    arc_top_id = f"arc-top-{module['n']}-{lang}"
    arc_bot_id = f"arc-bot-{module['n']}-{lang}"
    foot = "POU TOHU · ENGLISH" if lang == "en" else "POU TOHU · TE REO MĀORI"
    motif_svg = module["motif"]()
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1200" width="1200" height="1200">
  <rect width="1200" height="1200" fill="{CHARCOAL}"/>
  <circle cx="600" cy="600" r="560" fill="{RING_BG}" stroke="{RED}" stroke-width="10"/>
  <circle cx="600" cy="600" r="500" fill="none" stroke="{INK}" stroke-width="2"/>

  <defs><path id="{arc_top_id}" d="M 120 600 A 480 480 0 0 1 1080 600"/></defs>
  <text font-family="'Bebas Neue',sans-serif" font-size="50" fill="{BONE}" letter-spacing="6">
    <textPath href="#{arc_top_id}" startOffset="50%" text-anchor="middle">{title}</textPath>
  </text>

  <defs><path id="{arc_bot_id}" d="M 120 600 A 480 480 0 0 0 1080 600"/></defs>
  <text font-family="'Bebas Neue',sans-serif" font-size="38" fill="{RED}" letter-spacing="8">
    <textPath href="#{arc_bot_id}" startOffset="50%" text-anchor="middle">{tag}</textPath>
  </text>

  {motif_svg}

  {NIHO_BASE}

  <text x="600" y="230" font-family="'Bebas Neue',sans-serif" font-size="30" fill="{RED}"
        text-anchor="middle" letter-spacing="8">THE KIWI DIALECTIC</text>
  <text x="600" y="1000" font-family="'Bebas Neue',sans-serif" font-size="22" fill="{GREY}"
        text-anchor="middle" letter-spacing="6">{foot}</text>
</svg>
"""


def main() -> None:
    written = []
    for m in MODULES:
        d = OUT / m["slug"]
        d.mkdir(parents=True, exist_ok=True)
        for lang in ("en", "mi"):
            f = d / f"{lang}.svg"
            f.write_text(build_svg(m, lang))
            written.append(str(f.relative_to(ROOT)))
    print("Wrote:")
    for w in written:
        print("  ", w)


if __name__ == "__main__":
    main()
