"""bump-version.py end-to-end tests."""
from __future__ import annotations

import json
import re
import subprocess
import sys


def test_dry_run_does_not_modify(repo_root, scripts_dir):
    """--dry-run shouldn't touch any file."""
    skill_md = repo_root / "skills" / "plan-it" / "SKILL.md"
    before = skill_md.read_text(encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(scripts_dir / "bump-version.py"), "9.9.9", "--dry-run"],
        capture_output=True, text=True, encoding="utf-8",
    )
    assert proc.returncode == 0
    after = skill_md.read_text(encoding="utf-8")
    assert before == after, "dry run modified a file"


def test_rejects_invalid_semver(scripts_dir):
    proc = subprocess.run(
        [sys.executable, str(scripts_dir / "bump-version.py"), "not-a-version"],
        capture_output=True, text=True, encoding="utf-8",
    )
    assert proc.returncode == 2


def test_plugin_json_version_matches_skill_md(repo_root):
    """plugin.json version must match the canonical SKILL.md version."""
    plugin_json = json.loads((repo_root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    skill_md = (repo_root / "skills" / "plan-it" / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r'version:\s*"(\d+\.\d+\.\d+)"', skill_md)
    assert m, "canonical SKILL.md has no version field"
    assert plugin_json["version"] == m.group(1), (
        f"plugin.json version {plugin_json['version']} != SKILL.md {m.group(1)}"
    )
