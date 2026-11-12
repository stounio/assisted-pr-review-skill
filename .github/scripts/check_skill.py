"""Validate the skills in this repository.

Checks, for every skills/<name>/SKILL.md:
- the frontmatter has a name matching the folder and a description;
- the skill is invoked by command only (disable-model-invocation: true);
- relative links in the skill's Markdown files resolve.
And, for assisted-pr-review, that the areas listed in SKILL.md match the
area headings of QUESTIONS.md.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")

errors: list[str] = []


def fail(path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {message}")


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(path, "missing frontmatter")
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return fields


def check_frontmatter(skill_md: Path) -> None:
    fields = frontmatter(skill_md)
    name = fields.get("name", "")
    if name != skill_md.parent.name:
        fail(skill_md, f"name '{name}' does not match folder '{skill_md.parent.name}'")
    if not NAME_PATTERN.match(name) or len(name) > 64:
        fail(skill_md, f"name '{name}' must be lowercase words joined by hyphens, at most 64 characters")
    description = fields.get("description", "")
    if not description:
        fail(skill_md, "description is missing")
    elif len(description) > 1024:
        fail(skill_md, "description is longer than 1024 characters")
    if fields.get("disable-model-invocation") != "true":
        fail(skill_md, "disable-model-invocation must be true: the skill is invoked by command only")


def check_links(markdown: Path) -> None:
    for target in LINK_PATTERN.findall(markdown.read_text(encoding="utf-8")):
        if re.match(r"^[a-z]+:", target):
            continue
        if not (markdown.parent / target).exists():
            fail(markdown, f"broken link to '{target}'")


def normalise(area: str) -> str:
    area = re.sub(r"\(.*?\)", "", area).strip().lower()
    return area


def check_areas(skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    questions_md = skill_dir / "QUESTIONS.md"
    listed = re.search(r"from \[`QUESTIONS\.md`\]\(QUESTIONS\.md\): (.+?)\. ", skill_md.read_text(encoding="utf-8"))
    if not listed:
        fail(skill_md, "cannot find the list of areas in step 2")
        return
    in_skill = {normalise(area) for area in listed.group(1).split(", ")}
    headings = re.findall(r"^## (.+)$", questions_md.read_text(encoding="utf-8"), re.MULTILINE)
    in_questions = {normalise(heading) for heading in headings}
    for area in sorted(in_questions - in_skill):
        fail(skill_md, f"area '{area}' is in QUESTIONS.md but not listed in step 2")
    for area in sorted(in_skill - in_questions):
        fail(skill_md, f"area '{area}' is listed in step 2 but has no heading in QUESTIONS.md")


def main() -> int:
    skill_files = sorted(ROOT.glob("skills/*/SKILL.md"))
    if not skill_files:
        errors.append("no skills/*/SKILL.md found")
    for skill_md in skill_files:
        check_frontmatter(skill_md)
        for markdown in sorted(skill_md.parent.glob("*.md")):
            check_links(markdown)
    for markdown in sorted(ROOT.glob("*.md")):
        check_links(markdown)
    check_areas(ROOT / "skills" / "assisted-pr-review")

    for error in errors:
        print(f"::error::{error}")
    if errors:
        return 1
    print(f"Checked {len(skill_files)} skill(s): OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
