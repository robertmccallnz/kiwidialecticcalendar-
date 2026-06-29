"""One-shot: regenerate every artefact from courses.json.

Run after editing courses.json. Used by CI and by new_course.py.
"""
import subprocess, sys
from pathlib import Path

SCRIPTS = Path(__file__).parent
for s in ["generate_ics.py", "generate_events.py", "generate_badges.py"]:
    print(f"→ {s}")
    r = subprocess.run([sys.executable, str(SCRIPTS / s)])
    if r.returncode != 0:
        sys.exit(r.returncode)
print("all artefacts regenerated.")
