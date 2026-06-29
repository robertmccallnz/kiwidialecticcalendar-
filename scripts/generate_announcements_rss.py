"""Generate announcements.rss — Feed 1: multi-channel calendar announcements.

Each calendar event becomes one RSS item with all platform links (Substack
post, Facebook post, TikTok video, X thread, Bluesky, LinkedIn, Instagram)
in the description body. Subscribers see "this event went live on all
these places at once".

Reads:
  - courses.json (canonical source)
  - announcements.json (optional per-event channel-link overrides)

Writes:
  - announcements.rss
"""
import json
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

NZ = timezone(timedelta(hours=12))
BASE = Path(__file__).resolve().parents[1]
FEED_URL = "https://raw.githubusercontent.com/robertmccallnz/kiwidialecticcalendar-/main/announcements.rss"
SITE_URL = "https://robertmccallnz.github.io/kiwidialecticcalendar-/"

# Default channel template — applied to every event unless overridden in
# announcements.json. Use {course_slug}, {lesson_slug}, {date} as placeholders.
DEFAULT_CHANNELS = {
    "Substack": "https://www.kiwidialectic.com",
    "Facebook": "https://www.facebook.com/kiwidialectic",
    "TikTok":   "https://www.tiktok.com/@kiwidialectic",
    "X":        "https://x.com/kiwidialectic",
    "Bluesky":  "https://bsky.app/profile/kiwidialectic.com",
    "LinkedIn": "https://www.linkedin.com/in/robertmccallnz",
    "Instagram": "https://www.instagram.com/kiwidialectic",
}

def load_courses() -> dict:
    return json.loads((BASE / "courses.json").read_text())

def load_overrides() -> dict:
    """Optional file: announcements.json maps lesson-id -> {platform: url}."""
    p = BASE / "announcements.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}

def to_dt(date: str, time: str | None) -> datetime:
    t = (time or "19:00").strip() or "19:00"
    return datetime.strptime(f"{date} {t}", "%Y-%m-%d %H:%M").replace(tzinfo=NZ)

def channels_for(event_id: str, course_slug: str, primary_link: str, overrides: dict) -> dict:
    """Return platform -> url map for a single event, merging defaults with overrides."""
    chans = dict(DEFAULT_CHANNELS)
    # The primary link (Substack post URL from courses.json) replaces the default Substack link
    if primary_link:
        chans["Substack"] = primary_link
    # Per-event overrides win
    chans.update(overrides.get(event_id, {}))
    return chans

def render_description(course: dict, lesson: dict, channels: dict, dt: datetime) -> str:
    """HTML description with channel links."""
    teaser = lesson.get("teaser", "") or ""
    nice_date = dt.strftime("%a %d %b %Y · %I:%M %p NZT")
    parts = [
        f"<p><strong>{escape(course['title'])}</strong></p>",
        f"<p>{escape(teaser)}</p>" if teaser else "",
        f"<p><em>{escape(nice_date)}</em></p>",
        "<p><strong>Where this lives:</strong></p>",
        "<ul>",
    ]
    for name, url in channels.items():
        if not url:
            continue
        parts.append(f'  <li><a href="{escape(url)}">{escape(name)}</a></li>')
    parts.append("</ul>")
    return "\n".join(p for p in parts if p)

def build_items(courses_data: dict, overrides: dict) -> list[dict]:
    items = []
    for course in courses_data.get("courses", []):
        if course.get("calendar_visibility", "public") == "hidden":
            continue
        for i, lesson in enumerate(course.get("lessons", [])):
            if lesson.get("calendar_visibility", "public") == "hidden":
                continue
            if not lesson.get("published", True):
                continue
            event_id = f"{course['slug']}-{i+1}"
            dt = to_dt(lesson["date"], lesson.get("time"))
            primary_link = lesson.get("link", "") or ""
            chans = channels_for(event_id, course["slug"], primary_link, overrides)
            items.append({
                "id": event_id,
                "title": f"{course['title']} — {lesson['title']}",
                "link": primary_link or SITE_URL,
                "pub": dt,
                "description": render_description(course, lesson, chans, dt),
                "category": course["slug"],
            })
    # Newest first
    items.sort(key=lambda x: x["pub"], reverse=True)
    return items

def render_rss(items: list[dict]) -> str:
    now = datetime.now(timezone.utc)
    head = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        '<channel>',
        '<title>The Kiwi Dialectic — Multi-Channel Announcements</title>',
        f'<link>{SITE_URL}</link>',
        f'<atom:link href="{FEED_URL}" rel="self" type="application/rss+xml"/>',
        '<description>One feed for every Kiwi Dialectic event across Substack, Facebook, TikTok, X, Bluesky, LinkedIn, and Instagram. Subscribe once, get them all.</description>',
        '<language>en-NZ</language>',
        f'<lastBuildDate>{format_datetime(now)}</lastBuildDate>',
    ]
    body = []
    for it in items:
        body += [
            '<item>',
            f'  <title>{escape(it["title"])}</title>',
            f'  <link>{escape(it["link"])}</link>',
            f'  <guid isPermaLink="false">announce-{escape(it["id"])}</guid>',
            f'  <pubDate>{format_datetime(it["pub"])}</pubDate>',
            f'  <category>{escape(it["category"])}</category>',
            f'  <description><![CDATA[{it["description"]}]]></description>',
            '</item>',
        ]
    tail = ['</channel>', '</rss>', '']
    return "\n".join(head + body + tail)

def main() -> None:
    courses = load_courses()
    overrides = load_overrides()
    items = build_items(courses, overrides)
    out = BASE / "announcements.rss"
    out.write_text(render_rss(items))
    print(f"wrote {out.name} ({len(items)} announcements)")

if __name__ == "__main__":
    main()
