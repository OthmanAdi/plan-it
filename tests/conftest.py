"""Shared pytest fixtures and helpers for plan-it tests."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
TEMPLATES_DIR = REPO_ROOT / "templates"
SKILL_DIR = REPO_ROOT / "skills" / "plan-it"

# Make scripts/ importable for direct module tests.
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture
def scripts_dir() -> Path:
    return SCRIPTS_DIR


@pytest.fixture
def templates_dir() -> Path:
    return TEMPLATES_DIR


@pytest.fixture
def skill_dir() -> Path:
    return SKILL_DIR


def parse_skill_frontmatter(skill_md_text: str) -> tuple[str, str]:
    """Return (frontmatter_yaml_text, body_markdown). Splits on first/second '---' lines."""
    lines = skill_md_text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md does not start with '---' frontmatter delimiter")
    end_idx = None
    for i, ln in enumerate(lines[1:], start=1):
        if ln.strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        raise ValueError("SKILL.md frontmatter has no closing '---'")
    return "\n".join(lines[1:end_idx]), "\n".join(lines[end_idx + 1 :])


PLAN_DATA_BLOCK_RE = re.compile(
    r'<script\s+type="application/json"\s+id="plan-data"\s*>\s*(\{.*?\})\s*</script>',
    re.DOTALL,
)


def extract_plan_json(html_text: str) -> dict:
    """Pull the embedded plan-data JSON out of a template's HTML."""
    m = PLAN_DATA_BLOCK_RE.search(html_text)
    if not m:
        raise AssertionError("template has no <script type='application/json' id='plan-data'> block")
    return json.loads(m.group(1))
