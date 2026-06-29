"""Add or update a course end-to-end.

Usage:
    python3 scripts/new_course.py path/to/course.json

Where course.json is the full course block (same shape used inside courses.json).
The script:
  1. Merges the course into courses.json (replace by slug if it exists).
  2. Regenerates ICS + events.json + events.rss + badges via build_all.py.
  3. Prints the suggested mapper layout block and a commit message.
"""
import json, sys, subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

def usage():
    print(__doc__)
    sys.exit(1)

def main():
    if len(sys.argv) != 2:
        usage()
    src = Path(sys.argv[1])
    if not src.exists():
        print(f"course file not found: {src}", file=sys.stderr)
        sys.exit(2)
    course = json.loads(src.read_text())
    if "slug" not in course or "title" not in course:
        print("course JSON must have slug + title", file=sys.stderr)
        sys.exit(2)

    courses_path = REPO / "courses.json"
    data = json.loads(courses_path.read_text())
    before = len(data["courses"])
    data["courses"] = [c for c in data["courses"] if c.get("slug") != course["slug"]]
    data["courses"].append(course)
    courses_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"courses.json: {course['slug']} {'updated' if before == len(data['courses']) else 'added'}")

    subprocess.run([sys.executable, str(REPO / "scripts" / "build_all.py")], check=True)

    print("\n— Suggested thinkers-mapper layout block —")
    print(f'  LAYOUT["{course["slug"]}"] = {{x: 50, y: 50}};   // adjust')
    print(f'  SHORT["{course["slug"]}"]  = "{course["title"].split("—")[0].strip()}";')
    print(f'  QUOTES["{course["slug"]}"] = "…";')
    print("\n— Suggested commit message —")
    print(f'  Add/update course: {course["title"]}')

if __name__ == "__main__":
    main()
