"""Wire the two parallel campaigns into courses.json.

Te Pā Tūwatawata — Wednesdays 18:00 NZT, 1 Jul → 5 Aug 2026
AI Literacy for Families — Saturdays 10:00 NZT, 4 Jul → 15 Aug 2026

Also: attach per-module badge slugs for Te Pā so the calendar/mapper
links to te-pa-module-1 … te-pa-module-6 instead of one shared badge.

Idempotent — safe to re-run.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "courses.json"

d = json.loads(DATA.read_text())

# --- Te Pā: Wednesdays starting 1 Jul 2026 -----------------------------------
TE_PA_DATES = [
    ("2026-07-01", "te-pa-module-1"),
    ("2026-07-08", "te-pa-module-2"),
    ("2026-07-15", "te-pa-module-3"),
    ("2026-07-22", "te-pa-module-4"),
    ("2026-07-29", "te-pa-module-5"),
    ("2026-08-05", "te-pa-module-6"),
]

# --- AI Literacy: Saturdays starting 4 Jul 2026 (intro + 6 weeks) ------------
AIL_DATES = [
    "2026-07-04",  # course launch
    "2026-07-11",  # week 1
    "2026-07-18",  # week 2
    "2026-07-25",  # week 3
    "2026-08-01",  # week 4
    "2026-08-08",  # week 5
    "2026-08-15",  # week 6 / wrap-up
]

for course in d["courses"]:
    if course["slug"] == "te-pa-tuwatawata":
        for lesson, (date, badge_slug) in zip(course["lessons"], TE_PA_DATES):
            lesson["date"] = date
            lesson["time"] = "18:00"
            lesson["badge_slug"] = badge_slug
            lesson["claim_url"] = (
                f"https://robertmccallnz.github.io/kiwidialecticcalendar-/badges/{badge_slug}/"
            )
        course["badge_glyph"] = None  # we ship bespoke per-module badges
        course["campaign"] = {
            "cadence": "weekly",
            "day_of_week": "Wednesday",
            "post_time": "07:00",
            "auto_post_platforms": ["x", "facebook_pages", "bluesky"],
            "draft_notify_platforms": ["linkedin", "instagram", "tiktok", "substack"],
            "starts": TE_PA_DATES[0][0],
            "ends": TE_PA_DATES[-1][0],
        }
    elif course["slug"] == "ai-literacy-for-families":
        for lesson, date in zip(course["lessons"], AIL_DATES):
            lesson["date"] = date
            lesson["time"] = "10:00"
        course["campaign"] = {
            "cadence": "weekly",
            "day_of_week": "Saturday",
            "post_time": "08:00",
            "auto_post_platforms": ["x", "facebook_pages", "bluesky"],
            "draft_notify_platforms": ["linkedin", "instagram", "tiktok", "substack"],
            "starts": AIL_DATES[0],
            "ends": AIL_DATES[-1],
        }

DATA.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
print("courses.json updated:")
print(f"  Te Pā:        {TE_PA_DATES[0][0]} → {TE_PA_DATES[-1][0]} (Wednesdays 18:00)")
print(f"  AI Literacy:  {AIL_DATES[0]} → {AIL_DATES[-1]} (Saturdays 10:00)")
