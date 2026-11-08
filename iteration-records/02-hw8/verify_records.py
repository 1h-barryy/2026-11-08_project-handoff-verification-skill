"""Check saved review boundaries and report vocabularies without modifying evidence."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parent
for label in ("checker1", "iteration"):
    before = json.loads((root / (label + "-before.hashes.json")).read_text())
    after = json.loads((root / (label + "-after.hashes.json")).read_text())
    changes = [name for name in sorted(before.keys() | after.keys()) if before.get(name) != after.get(name)]
    print(label, "changed project files:", changes)
    assert not changes

for label in ("checker1", "skill-rerun"):
    report = (root / (label + ".result.md")).read_text(encoding="utf-8")
    cells = [line.split("|")[2].strip() for line in report.splitlines()
             if line.startswith(("| Scope |", "| Design |", "| Verification |"))]
    print(label, "status cells:", cells)
    assert len(cells) >= 3 and all(cell in {"PASS", "ISSUE", "UNVERIFIED"} for cell in cells)

before = json.loads((root / "doer2-before.hashes.json").read_text())
after = json.loads((root / "doer2-paused.hashes.json").read_text())
changes = [name for name in sorted(before.keys() | after.keys()) if before.get(name) != after.get(name)]
print("doer2 changed project files while waiting for host approval:", changes)
assert changes == []
print("Evidence checks passed. Hash scope excludes .git, .venv, __pycache__, and this coordinator evidence directory.")

project = root.parents[1]
for source, snapshot in (("server.py", "demo1-server.after.snapshot"),
                         ("tests/test_server.py", "demo1-tests.after.snapshot"),
                         ("README.md", "demo2-readme.before.snapshot"),
                         (".agents/skills/delivery-integrity-check/SKILL.md", "skill.after.snapshot")):
    assert (project / source).read_bytes() == (root / snapshot).read_bytes(), source
print("Implementation, README, and skill match their recorded snapshots.")

for path in (project / "DEMONSTRATION.md", project / "ITERATION.md", root / "INDEX.md"):
    text = path.read_text(encoding="utf-8")
    assert all(line == line.rstrip() for line in text.splitlines()), path
    for link in re.findall(r"\]\(([^)]+)\)", text):
        assert (path.parent / link).exists(), (path, link)
print("Updated documentation has no trailing whitespace or missing local link targets.")
