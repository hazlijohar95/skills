"""Fail if the shipped skill list, the commands, and the README disagree (see CLAUDE.md)."""
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
plugin = json.loads((root / ".claude-plugin/plugin.json").read_text())
readme = (root / "README.md").read_text()

listed = {s.removeprefix("./") for s in plugin["skills"]}
on_disk = {str(p.parent.relative_to(root)) for p in root.glob("skills/*/*/SKILL.md")}

errors = [f"{s}: SKILL.md on disk but not in plugin.json" for s in sorted(on_disk - listed)]
errors += [f"{s}: in plugin.json but has no SKILL.md" for s in sorted(listed - on_disk)]
for s in sorted(on_disk):
    name = Path(s).name
    if not (root / f"commands/{name}.md").exists():
        errors.append(f"{s}: no commands/{name}.md")
    if f"(./{s}/SKILL.md)" not in readme:
        errors.append(f"{s}: not linked from README.md")
    if f"\nname: {name}\n" not in (root / s / "SKILL.md").read_text().split("\n---", 1)[0]:
        errors.append(f"{s}: frontmatter name is not {name}")
if json.loads((root / "plugin.json").read_text())["version"] != plugin["version"]:
    errors.append("plugin.json and .claude-plugin/plugin.json versions differ")

print("\n".join(errors) or f"OK: {len(on_disk)} skills; manifests, commands and README agree")
sys.exit(1 if errors else 0)
