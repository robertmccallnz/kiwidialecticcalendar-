import json
from pathlib import Path
from datetime import datetime, UTC
base = Path(__file__).resolve().parents[1]
courses = json.loads((base / 'courses.json').read_text())['courses']
lines = ['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//The Kiwi Dialectic//Course Calendar//EN','CALSCALE:GREGORIAN','METHOD:PUBLISH','X-WR-CALNAME:The Kiwi Dialectic Courses','X-WR-TIMEZONE:Pacific/Auckland']
stamp = datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')
for course in courses:
    for idx, lesson in enumerate(course.get('lessons', []), start=1):
        dt = datetime.strptime(f"{lesson['date']} {lesson.get('time','19:00')}", '%Y-%m-%d %H:%M')
        dtend = dt.replace(hour=min(dt.hour + 1, 23))
        uid = f"{course.get('slug','course')}-{idx}@thekiwidialectic"
        desc = f"{course['title']} — {lesson['title']}"
        if lesson.get('link'): desc += f"\\n{lesson['link']}"
        lines += ['BEGIN:VEVENT',f'UID:{uid}',f'DTSTAMP:{stamp}',f'DTSTART;TZID=Pacific/Auckland:{dt.strftime("%Y%m%dT%H%M%S")}',f'DTEND;TZID=Pacific/Auckland:{dtend.strftime("%Y%m%dT%H%M%S")}',f'SUMMARY:{course["title"]} — {lesson["title"]}',f'DESCRIPTION:{desc}',f'LOCATION:{lesson.get("location", "Substack")}','STATUS:CONFIRMED','END:VEVENT']
lines.append('END:VCALENDAR')
(base / 'the-kiwi-dialectic-courses.ics').write_text('\r\n'.join(lines) + '\r\n')
