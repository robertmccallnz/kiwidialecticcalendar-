"""Generate events.json and events.rss from courses.json.

events.json is a flat list — one entry per lesson — for easy consumption by
the mapper, bots, and any third-party app. events.rss is RSS 2.0 for feed
readers and Substack imports.
"""
import json
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

NZ = timezone(timedelta(hours=12))  # Pacific/Auckland (NZST; ignore DST for feed simplicity)
BASE = Path(__file__).resolve().parents[1]
RAW = "https://raw.githubusercontent.com/robertmccallnz/kiwidialecticcalendar-/main"

def lesson_id(course_slug: str, idx: int) -> str:
    return f"{course_slug}-{idx + 1}"

def load() -> dict:
    return json.loads((BASE / "courses.json").read_text())

def to_iso(date: str, time: str | None) -> str:
    t = (time or "19:00").strip() or "19:00"
    dt = datetime.strptime(f"{date} {t}", "%Y-%m-%d %H:%M").replace(tzinfo=NZ)
    return dt.isoformat()

def build_events(data: dict) -> list[dict]:
    out = []
    for course in data.get("courses", []):
        if course.get("calendar_visibility", "public") == "hidden":
            continue
        for i, l in enumerate(course.get("lessons", [])):
            if l.get("calendar_visibility", "public") == "hidden":
                continue
            start = to_iso(l["date"], l.get("time"))
            start_dt = datetime.fromisoformat(start)
            end = (start_dt + timedelta(hours=1)).isoformat()
            out.append({
                "id": lesson_id(course["slug"], i),
                "course_slug": course["slug"],
                "course_title": course["title"],
                "lesson_index": i,
                "title": l["title"],
                "start": start,
                "end": end,
                "location": l.get("location", "Substack"),
                "access": l.get("access") or course.get("access", "public"),
                "teaser": l.get("teaser", ""),
                "link": l.get("link", ""),
                "chat": course.get("chat_thread", ""),
                "badge": course.get("badge_slug", ""),
            })
    out.sort(key=lambda e: e["start"])
    return out

def write_json(events: list[dict]) -> None:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": f"{RAW}/courses.json",
        "ics":    f"{RAW}/the-kiwi-dialectic-courses.ics",
        "rss":    f"{RAW}/events.rss",
        "count": len(events),
        "events": events,
    }
    (BASE / "events.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")

def write_rss(events: list[dict]) -> None:
    items = []
    for e in events:
        pub = format_datetime(datetime.fromisoformat(e["start"]))
        desc = escape(f"{e['course_title']} — {e['teaser']}".strip(" —"))
        link = escape(e["link"] or "https://www.kiwidialectic.com/s/courses")
        items.append(f"""    <item>
      <title>{escape(e['title'])}</title>
      <link>{link}</link>
      <guid isPermaLink="false">{escape(e['id'])}</guid>
      <pubDate>{pub}</pubDate>
      <category>{escape(e['course_slug'])}</category>
      <description>{desc}</description>
    </item>""")
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>The Kiwi Dialectic — Course Events</title>
<link>https://www.kiwidialectic.com/s/courses</link>
<description>Course lesson events across The Kiwi Dialectic.</description>
<language>en-NZ</language>
<lastBuildDate>{format_datetime(datetime.now(timezone.utc))}</lastBuildDate>
{chr(10).join(items)}
</channel></rss>
"""
    (BASE / "events.rss").write_text(rss)

def main():
    data = load()
    events = build_events(data)
    write_json(events)
    write_rss(events)
    print(f"wrote events.json ({len(events)} events) and events.rss")

if __name__ == "__main__":
    main()
