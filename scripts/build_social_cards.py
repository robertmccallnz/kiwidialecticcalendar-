"""Build 1200x675 social-card PNGs for both course campaigns.

Te Pā:        6 cards (one per module) — dark, red accent, motif on right
AI Literacy:  7 cards (launch + 6 weeks) — light cream, navy accent, whare glyph

Layout uses real word-wrap so long titles/teasers don't overflow.
"""
from __future__ import annotations
import cairosvg, json
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
OUT_TP  = ROOT / "social" / "te-pa"
OUT_AIL = ROOT / "social" / "ai-literacy"
OUT_TP.mkdir(parents=True, exist_ok=True)
OUT_AIL.mkdir(parents=True, exist_ok=True)

DATA  = json.loads((ROOT / "courses.json").read_text())
TE_PA = [c for c in DATA["courses"] if c["slug"] == "te-pa-tuwatawata"][0]
AIL   = [c for c in DATA["courses"] if c["slug"] == "ai-literacy-for-families"][0]

MOTIFS_TP = ["koru", "pa", "niho", "kowhaiwhai", "unaunahi", "takarangi"]


def esc(s) -> str:
    return xml_escape(str(s or ""))

def fmt_date(iso_date: str) -> str:
    return datetime.strptime(iso_date, "%Y-%m-%d").strftime("%a %d %b %Y").upper()

def wrap(text: str, max_chars: int, max_lines: int) -> list[str]:
    words = (text or "").split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if len(test) <= max_chars:
            cur = test
        else:
            if cur:
                lines.append(cur)
                cur = w
            else:
                lines.append(w[:max_chars])
                cur = ""
            if len(lines) >= max_lines:
                cur = ""
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    return lines or [""]


# --- motif glyphs (right-hand side of card) -----------------------------------
def g_koru():
    return ('<g stroke="#f5f0e6" stroke-width="10" fill="none" stroke-linecap="round">'
            '<path d="M 980 380 C 880 380 800 300 800 200 C 800 130 870 80 950 80 '
            'C 1010 80 1050 130 1050 180 C 1050 220 1020 250 980 250 C 960 250 940 230 940 210"/>'
            '</g><circle cx="940" cy="210" r="9" fill="#c41e1e"/>')

def g_pa():
    parts, posts = [], []
    for i, x in enumerate(range(830, 1130, 30)):
        h = 80 - abs(i - 5) * 8
        posts.append(
            f'<line x1="{x}" y1="{220-h}" x2="{x}" y2="320" '
            f'stroke="#f5f0e6" stroke-width="6" stroke-linecap="round"/>'
            f'<circle cx="{x}" cy="{220-h}" r="4" fill="#c41e1e"/>'
        )
    parts.extend(posts)
    parts.append('<path d="M 880 320 L 950 240 L 1020 320 Z" fill="none" stroke="#c41e1e" stroke-width="6"/>')
    parts.append('<rect x="895" y="320" width="110" height="60" fill="none" stroke="#f5f0e6" stroke-width="5"/>')
    return "".join(parts)

def g_niho():
    return "".join(
        f'<path d="M {820+i*40} 360 L {840+i*40} 150 L {860+i*40} 360 Z" '
        f'fill="{"#c41e1e" if i%2==0 else "#f5f0e6"}"/>' for i in range(7)
    )

def g_kowhaiwhai():
    return ('<g fill="none" stroke="#f5f0e6" stroke-width="8" stroke-linecap="round">'
            '<path d="M 800 230 C 800 170 850 170 880 210 C 910 250 910 320 880 320 '
            'C 850 320 850 230 890 230 C 940 230 950 320 990 320 '
            'C 1030 320 1040 240 1010 200 C 980 170 970 230 1010 230 '
            'C 1050 230 1060 190 1060 150"/></g>'
            '<circle cx="800" cy="230" r="7" fill="#c41e1e"/>')

def g_unaunahi():
    parts = []
    for row in range(3):
        y = 170 + row * 50
        off = 25 if row % 2 else 0
        for col in range(5):
            x = 820 + off + col * 55
            stroke = "#c41e1e" if (row + col) % 3 == 0 else "#f5f0e6"
            parts.append(f'<path d="M {x-22} {y} A 22 22 0 0 1 {x+22} {y}" '
                         f'fill="none" stroke="{stroke}" stroke-width="5"/>')
    return "".join(parts)

def g_takarangi():
    return ('<g fill="none" stroke-linecap="round" stroke-width="9">'
            '<path d="M 880 230 C 880 185 910 155 950 155 C 990 155 1020 185 1020 230 '
            'C 1020 265 990 290 955 290 C 930 290 915 275 915 250 '
            'C 915 230 935 215 950 230" stroke="#f5f0e6"/>'
            '<path d="M 1020 230 C 1020 275 990 305 950 305 C 910 305 880 275 880 230 '
            'C 880 185 910 155 950 155 C 975 155 990 170 990 195 '
            'C 990 220 970 235 950 225" stroke="#c41e1e"/></g>'
            '<circle cx="950" cy="230" r="7" fill="#f5f0e6"/>')

GLYPHS = {
    "koru": g_koru, "pa": g_pa, "niho": g_niho,
    "kowhaiwhai": g_kowhaiwhai, "unaunahi": g_unaunahi, "takarangi": g_takarangi,
}

# Whare/house glyph for AI Literacy cards
AIL_GLYPH = (
    '<g transform="translate(880,140)" stroke="#1a3a6c" fill="none" '
    'stroke-width="6" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M 0 140 L 130 20 L 260 140"/>'
    '<rect x="20" y="140" width="220" height="130"/>'
    '<rect x="100" y="180" width="60" height="90" fill="#c41e1e" stroke="none"/>'
    '<rect x="40" y="160" width="40" height="40"/>'
    '<rect x="180" y="160" width="40" height="40"/>'
    '<path d="M 195 60 Q 215 45 200 30 Q 185 15 205 0" stroke-width="4"/>'
    '</g>'
)


def card_te_pa(idx: int, lesson: dict) -> str:
    glyph = GLYPHS[MOTIFS_TP[idx]]()
    raw_title = lesson["title"].split("—")[-1].strip()
    t_lines  = wrap(raw_title, max_chars=24, max_lines=2)
    te_lines = wrap(lesson["teaser"], max_chars=58, max_lines=2)
    t_y      = 210 if len(t_lines) > 1 else 250
    te_y     = t_y + (68 * len(t_lines)) + 28
    t_tspans = "".join(
        f'<tspan x="80" dy="{0 if i==0 else 68}">{esc(l)}</tspan>'
        for i, l in enumerate(t_lines)
    )
    te_tspans = "".join(
        f'<tspan x="80" dy="{0 if i==0 else 32}">{esc(l)}</tspan>'
        for i, l in enumerate(te_lines)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" width="1200" height="675">
  <rect width="1200" height="675" fill="#0c0c0c"/>
  <rect x="0" y="0" width="14" height="675" fill="#c41e1e"/>
  <text x="80" y="100" font-family="'Bebas Neue',sans-serif" font-size="30" fill="#c41e1e" letter-spacing="5">TE PĀ TŪWATAWATA · MODULE {idx+1}</text>
  <text y="{t_y}" font-family="'Bebas Neue',sans-serif" font-size="60" fill="#f5f0e6" letter-spacing="2">{t_tspans}</text>
  <text y="{te_y}" font-family="-apple-system,sans-serif" font-size="22" fill="#bfb9aa">{te_tspans}</text>
  {glyph}
  <line x1="80" y1="560" x2="1120" y2="560" stroke="#262626" stroke-width="2"/>
  <text x="80" y="612" font-family="'Bebas Neue',sans-serif" font-size="28" fill="#f5f0e6" letter-spacing="4">{fmt_date(lesson['date'])} · 6PM NZT</text>
  <text x="1120" y="612" text-anchor="end" font-family="'Bebas Neue',sans-serif" font-size="22" fill="#c41e1e" letter-spacing="2">TE-PA.ORG · MODULE {idx+1}</text>
</svg>"""


def card_ail(idx: int, lesson: dict) -> str:
    t_lines  = wrap(lesson["title"], max_chars=26, max_lines=2)
    te_lines = wrap(lesson["teaser"], max_chars=58, max_lines=2)
    t_y      = 210 if len(t_lines) > 1 else 250
    te_y     = t_y + (72 * len(t_lines)) + 28
    t_tspans = "".join(
        f'<tspan x="80" dy="{0 if i==0 else 72}">{esc(l)}</tspan>'
        for i, l in enumerate(t_lines)
    )
    te_tspans = "".join(
        f'<tspan x="80" dy="{0 if i==0 else 32}">{esc(l)}</tspan>'
        for i, l in enumerate(te_lines)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" width="1200" height="675">
  <rect width="1200" height="675" fill="#fffaf0"/>
  <rect x="0" y="0" width="14" height="675" fill="#1a3a6c"/>
  <text x="80" y="100" font-family="-apple-system,sans-serif" font-weight="700" font-size="24" fill="#1a3a6c" letter-spacing="3">AI LITERACY FOR FAMILIES · WEEK {idx}</text>
  <text y="{t_y}" font-family="-apple-system,sans-serif" font-weight="700" font-size="62" fill="#1a1a1a" letter-spacing="-1">{t_tspans}</text>
  <text y="{te_y}" font-family="-apple-system,sans-serif" font-size="22" fill="#4a4a4a">{te_tspans}</text>
  {AIL_GLYPH}
  <line x1="80" y1="560" x2="1120" y2="560" stroke="#e8e0cf" stroke-width="2"/>
  <text x="80" y="612" font-family="-apple-system,sans-serif" font-weight="700" font-size="22" fill="#1a3a6c" letter-spacing="2">{fmt_date(lesson['date'])} · 10AM NZT</text>
  <text x="1120" y="612" text-anchor="end" font-family="-apple-system,sans-serif" font-weight="700" font-size="22" fill="#c41e1e" letter-spacing="2">AI-LITERACY-FOR-FAMILIES.VERCEL.APP</text>
</svg>"""


def main():
    for idx, lesson in enumerate(TE_PA["lessons"]):
        svg = card_te_pa(idx, lesson)
        (OUT_TP / f"module-{idx+1}.svg").write_text(svg)
        cairosvg.svg2png(
            bytestring=svg.encode(),
            write_to=str(OUT_TP / f"module-{idx+1}.png"),
            output_width=1200, output_height=675,
        )
        print(f"  te-pa  module-{idx+1}.png")
    for idx, lesson in enumerate(AIL["lessons"]):
        svg = card_ail(idx, lesson)
        (OUT_AIL / f"week-{idx}.svg").write_text(svg)
        cairosvg.svg2png(
            bytestring=svg.encode(),
            write_to=str(OUT_AIL / f"week-{idx}.png"),
            output_width=1200, output_height=675,
        )
        print(f"  ail    week-{idx}.png")


if __name__ == "__main__":
    main()
