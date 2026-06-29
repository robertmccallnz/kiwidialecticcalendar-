"""Generate subscriber.rss — Feed 2: AI Warrior + mapper news combined.

For people who follow the *project*, not the calendar. This feed combines:

  1. AI Warrior site updates — read from GitHub's native commits Atom feed
     for robertmccallnz/ai-warrior (no scraping required).
  2. Indigenous-news pulses from the te-pa.org rhizome mapper — read from
     the analytics Worker's /news endpoint when it exists. Currently a
     placeholder; will light up as soon as the news layer ships.

Output is a single merged RSS 2.0 feed sorted by recency.
"""
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime, parsedate_to_datetime
from pathlib import Path
from xml.sax.saxutils import escape
import re

BASE = Path(__file__).resolve().parents[1]
FEED_URL = "https://raw.githubusercontent.com/robertmccallnz/kiwidialecticcalendar-/main/subscriber.rss"
SITE_URL = "https://robertmccallnz.github.io/kiwidialecticcalendar-/"

AI_WARRIOR_ATOM = "https://github.com/robertmccallnz/ai-warrior/commits/main.atom"
MAPPER_NEWS_API = "https://te-pa-analytics.sketchschool.workers.dev/news?days=14"

MAX_AI_WARRIOR = 30
MAX_NEWS = 60
HTTP_TIMEOUT = 10  # seconds

def http_get(url: str) -> str | None:
    """Tolerant HTTP GET. Returns None on any failure so the feed still builds."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "kiwi-dialectic-feedgen/1.0"})
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, Exception) as e:
        print(f"  (skip) {url}: {type(e).__name__}: {e}")
        return None

# ──────────────────────────────────────────────────────────────────────
# AI Warrior — parse GitHub's commits Atom feed
# ──────────────────────────────────────────────────────────────────────

ATOM_ENTRY_RE = re.compile(r"<entry>(.*?)</entry>", re.DOTALL)
ATOM_FIELD_RE = {
    "title":   re.compile(r"<title>(.*?)</title>", re.DOTALL),
    "link":    re.compile(r'<link[^>]+href="([^"]+)"'),
    "updated": re.compile(r"<updated>([^<]+)</updated>"),
    "id":      re.compile(r"<id>([^<]+)</id>"),
    "content": re.compile(r"<content[^>]*>(.*?)</content>", re.DOTALL),
}

def parse_atom_entries(atom_text: str) -> list[dict]:
    """Parse GitHub commits atom feed into a normalised entry list."""
    out = []
    for m in ATOM_ENTRY_RE.finditer(atom_text):
        block = m.group(1)
        entry = {}
        for k, rx in ATOM_FIELD_RE.items():
            mm = rx.search(block)
            entry[k] = mm.group(1).strip() if mm else ""
        if not entry.get("title") or not entry.get("link"):
            continue
        try:
            entry["dt"] = datetime.fromisoformat(entry["updated"].replace("Z", "+00:00"))
        except Exception:
            entry["dt"] = datetime.now(timezone.utc)
        # strip leading commit-sha noise from titles
        entry["title"] = re.sub(r"^\s*", "", entry["title"])
        out.append(entry)
    return out

def fetch_ai_warrior_updates() -> list[dict]:
    print("→ fetching ai-warrior commits…")
    raw = http_get(AI_WARRIOR_ATOM)
    if not raw:
        return []
    entries = parse_atom_entries(raw)[:MAX_AI_WARRIOR]
    items = []
    for e in entries:
        items.append({
            "kind": "ai-warrior",
            "id":   f"aw-{e['id'].rsplit('/', 1)[-1][:12]}",
            "title": f"AI Warrior — {e['title']}",
            "link": e["link"],
            "pub":  e["dt"],
            "category": "ai-warrior",
            "description": (
                "<p><strong>Update to the AI Warrior site / course materials.</strong></p>"
                f"<p>{escape(e['title'])}</p>"
                f'<p><a href="{escape(e["link"])}">View change on GitHub →</a></p>'
            ),
        })
    print(f"   got {len(items)} ai-warrior entries")
    return items

# ──────────────────────────────────────────────────────────────────────
# Mapper news — pull from analytics Worker /news (placeholder until live)
# ──────────────────────────────────────────────────────────────────────

def fetch_mapper_news() -> list[dict]:
    print("→ fetching mapper news…")
    raw = http_get(MAPPER_NEWS_API)
    if not raw:
        print("   (news endpoint not live yet — skipping)")
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []
    events = data.get("events", data) if isinstance(data, dict) else data
    if not isinstance(events, list):
        return []
    items = []
    for e in events[:MAX_NEWS]:
        if not isinstance(e, dict):
            continue
        try:
            pub = datetime.fromtimestamp(e.get("published_at", 0) / 1000, tz=timezone.utc)
        except Exception:
            pub = datetime.now(timezone.utc)
        lang = e.get("lang", "—")
        region = e.get("region", "—")
        items.append({
            "kind": "mapper-news",
            "id":   f"news-{e.get('id', '')}",
            "title": f"[{region.upper()} · {lang}] {e.get('title', 'Untitled')}",
            "link": e.get("url", SITE_URL),
            "pub":  pub,
            "category": f"mapper-news-{region}",
            "description": (
                f"<p>{escape(e.get('summary', ''))}</p>"
                f"<p><em>Source: {escape(e.get('source_name', ''))} · Language: {escape(lang)}</em></p>"
            ),
        })
    print(f"   got {len(items)} news entries")
    return items

# ──────────────────────────────────────────────────────────────────────
# Render
# ──────────────────────────────────────────────────────────────────────

def render_rss(items: list[dict]) -> str:
    items.sort(key=lambda x: x["pub"], reverse=True)
    now = datetime.now(timezone.utc)
    head = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        '<channel>',
        '<title>The Kiwi Dialectic — Subscriber Feed (AI Warrior + Mapper)</title>',
        f'<link>{SITE_URL}</link>',
        f'<atom:link href="{FEED_URL}" rel="self" type="application/rss+xml"/>',
        '<description>For people who follow the project, not the calendar. AI Warrior site updates plus live indigenous-news pulses from the te-pa.org rhizome mapper.</description>',
        '<language>en-NZ</language>',
        f'<lastBuildDate>{format_datetime(now)}</lastBuildDate>',
    ]
    body = []
    for it in items:
        body += [
            '<item>',
            f'  <title>{escape(it["title"])}</title>',
            f'  <link>{escape(it["link"])}</link>',
            f'  <guid isPermaLink="false">{escape(it["id"])}</guid>',
            f'  <pubDate>{format_datetime(it["pub"])}</pubDate>',
            f'  <category>{escape(it["category"])}</category>',
            f'  <description><![CDATA[{it["description"]}]]></description>',
            '</item>',
        ]
    tail = ['</channel>', '</rss>', '']
    return "\n".join(head + body + tail)

def main() -> None:
    items = []
    items += fetch_ai_warrior_updates()
    items += fetch_mapper_news()
    if not items:
        # Empty-but-valid feed so subscribers don't see errors
        print("   (no items — emitting empty feed)")
    out = BASE / "subscriber.rss"
    out.write_text(render_rss(items))
    print(f"wrote {out.name} ({len(items)} total items)")

if __name__ == "__main__":
    main()
