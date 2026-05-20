"""SKILL.md frontmatter regression tests.

Locks the v2.38.1 lesson from planning-with-files: never let `---` substrings
appear inside hook command scalars, since Claude Code's skill-discovery loader
splits on the first `---` to find the closing frontmatter fence.
"""
from __future__ import annotations

from conftest import parse_skill_frontmatter


def test_canonical_skill_has_frontmatter(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    assert skill_md.is_file(), f"missing canonical SKILL.md at {skill_md}"
    text = skill_md.read_text(encoding="utf-8")
    fm, body = parse_skill_frontmatter(text)
    assert "name: plan-it" in fm
    assert "description:" in fm
    assert "metadata:" in fm
    assert "version:" in fm
    assert body.strip(), "SKILL.md body must not be empty"


def test_description_contains_trigger_phrases(skill_dir):
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    fm, _ = parse_skill_frontmatter(text)
    # The trigger phrases live in the description field. Match a few canonical ones.
    description_line = next((ln for ln in fm.splitlines() if ln.startswith("description:")), "")
    triggers = ["plan it", "html plan", "show me the plan"]
    found = [t for t in triggers if t in description_line.lower()]
    assert len(found) >= 2, f"description should contain at least 2 trigger phrases, found {found}"


def test_no_yaml_collision_in_hooks(skill_dir):
    """Lock the v2.38.1 lesson: no `---` substrings inside hook command scalars."""
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    fm, _ = parse_skill_frontmatter(text)
    # Inside frontmatter, look for hook command strings.
    # Bare `---` lines in frontmatter would end frontmatter early.
    # Any `---` substring inside a quoted scalar is the danger.
    for line in fm.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("command:"):
            # The closing `---` of frontmatter is on its own line at column 0 only.
            assert "---" not in stripped, (
                f"hook command line contains '---' which collides with YAML doc-separator: {stripped[:120]}"
            )


def test_plan_data_delimiters_use_equals(skill_dir):
    """Plan data delimiters must use === not ---, per pwf v2.38.1."""
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    assert "===BEGIN PLAN DATA===" in text or "===BEGIN" in text, (
        "SKILL.md should reference ===BEGIN PLAN DATA=== delimiter style"
    )
    # Verify no occurrence of the old --- style.
    assert "---BEGIN PLAN DATA---" not in text, (
        "SKILL.md must not use ---BEGIN PLAN DATA--- delimiter (collides with YAML)"
    )


def test_five_hooks_declared(skill_dir):
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    fm, _ = parse_skill_frontmatter(text)
    required = ["UserPromptSubmit:", "PreToolUse:", "PostToolUse:", "Stop:", "PreCompact:"]
    for hook in required:
        assert hook in fm, f"missing hook declaration: {hook}"


def test_user_invocable_true(skill_dir):
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    fm, _ = parse_skill_frontmatter(text)
    assert "user-invocable: true" in fm
