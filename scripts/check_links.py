"""Audit every URL referenced in courses.json.

Reports broken Substack post links (those that return 404 or redirect
silently to the publication root) and broken badge-claim URLs.

Used by CI to keep the courses + badges + mapper graph honest. Run after
build_all.py whenever courses.json changes.

Exit code 0 if all links resolve cleanly, 1 otherwise. The Bakunin
lessons are exempt until their `published` flag is True in courses.json
(see optional `published` field per lesson).
"""
from __future__ import annotations
import json, sys, subprocess
import concurrent.futures as cf
import urllib.parse
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def head(url: str) -> tuple[str, str]:
    """Return (status_code, effective_url) using curl. Empty status on error."""
    try:
        out = subprocess.run(
            ["curl", "-sL", "-A", "KDLinkAuditor/1.0", "--max-time", "20",
             "-o", "/dev/null", "-w", "%{http_code}|%{url_effective}", url],
            capture_output=True, text=True, timeout=25,
        )
        status, eff = out.stdout.split("|", 1)
        return status, eff
    except Exception:
        return "", url


def is_substack_post(url: str) -> bool:
    p = urllib.parse.urlparse(url)
    return p.netloc.endswith("kiwidialectic.com") and p.path.startswith("/p/")


def collect(courses: list[dict]) -> list[tuple[str, str, str, bool]]:
    """Return (course_slug, kind, url, exempt) for every URL we care about."""
    items: list[tuple[str, str, str, bool]] = []
    for c in courses:
        slug = c["slug"]
        for i, l in enumerate(c.get("lessons", [])):
            if not l.get("link"):
                continue
            kind = "launch" if i == 0 else f"lesson-{i}"
            # Lessons may carry a `published` boolean. Unpublished lessons
            # are expected to 404 until Robert publishes them.
            exempt = not l.get("published", False)
            items.append((slug, kind, l["link"], exempt))
        if c.get("chat_thread"):
            items.append((slug, "chat_thread", c["chat_thread"], False))
        if c.get("badge_claim_url"):
            items.append((slug, "badge_claim", c["badge_claim_url"], False))
    return items


def main() -> int:
    data = json.loads((BASE / "courses.json").read_text())
    items = collect(data["courses"])

    def probe(item):
        slug, kind, url, exempt = item
        status, eff = head(url)
        ok = status.startswith("2")
        # Substack 404s reveal themselves either as a literal 404 or by
        # rewriting /p/<slug> -> /<slug> at the root.
        if is_substack_post(url):
            want = urllib.parse.urlparse(url).path
            got = urllib.parse.urlparse(eff).path
            if got != want and not got.startswith(want):
                ok = False
        return slug, kind, url, status, eff, ok, exempt

    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(probe, items))

    failed = [r for r in results if not r[5] and not r[6]]
    pending = [r for r in results if not r[5] and r[6]]

    print(f"Audited {len(results)} URLs from courses.json")
    print(f"  OK:      {sum(1 for r in results if r[5])}")
    print(f"  PENDING: {len(pending)}  (lessons not yet published)")
    print(f"  FAILED:  {len(failed)}")
    if pending:
        print("\nPending (expected — set `published: true` on the lesson once it lands):")
        for slug, kind, url, status, eff, _, _ in pending:
            print(f"  - {slug:48s} {kind:12s} [{status}] {url}")
    if failed:
        print("\nFailed:")
        for slug, kind, url, status, eff, _, _ in failed:
            print(f"  - {slug:48s} {kind:12s} [{status}] {url}")
            if eff != url:
                print(f"      redirected to {eff}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
