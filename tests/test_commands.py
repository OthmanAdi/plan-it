"""Slash command files must exist and have valid YAML frontmatter."""
from __future__ import annotations


EXPECTED_COMMANDS = [
    "plan.md",
    "plan-render.md",
    "plan-attest.md",
    "plan-status.md",
    "plan-export.md",
    "plan-goal.md",
    "plan-loop.md",
]


def test_all_commands_present(repo_root):
    cmd_dir = repo_root / "commands"
    for name in EXPECTED_COMMANDS:
        p = cmd_dir / name
        assert p.is_file(), f"missing command file: {p}"


def test_command_files_have_frontmatter(repo_root):
    cmd_dir = repo_root / "commands"
    for name in EXPECTED_COMMANDS:
        text = (cmd_dir / name).read_text(encoding="utf-8")
        assert text.startswith("---\n"), f"{name} missing frontmatter open"
        assert "description:" in text, f"{name} missing description in frontmatter"
        assert text.count("\n---\n") >= 1, f"{name} missing frontmatter close"
