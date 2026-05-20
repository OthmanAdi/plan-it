"""Each of the 10 templates must parse and meet single-file constraints."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from conftest import extract_plan_json


EXPECTED_TEMPLATES = {
    "implementation-plan",
    "three-approaches",
    "ticket-triage",
    "feature-flag-editor",
    "module-map",
    "annotated-pr",
    "living-design-system",
    "animation-sandbox",
    "weekly-status",
    "incident-timeline",
}


REMOTE_URL_RE = re.compile(r'(src|href)\s*=\s*"https?://')
LINK_STYLESHEET_RE = re.compile(r'<link[^>]+rel\s*=\s*"stylesheet"')
SCRIPT_SRC_RE = re.compile(r'<script[^>]+src\s*=\s*"')
# Match real eval/Function constructor calls, NOT method calls like `redis.eval(`
EVAL_OR_FUNCTION_RE = re.compile(r'(?<![.\w])(eval\s*\(|new\s+Function\s*\()')
BASE_FIELDS = {
    "schema_version",
    "plan_title",
    "goal",
    "current_phase",
    "template",
    "phases",
}


def _template_files() -> list[Path]:
    tdir = Path(__file__).resolve().parent.parent / "templates"
    return sorted([p for p in tdir.glob("*.html")])


@pytest.mark.parametrize("tpl_name", sorted(EXPECTED_TEMPLATES))
def test_template_exists(tpl_name, templates_dir):
    path = templates_dir / f"{tpl_name}.html"
    assert path.is_file(), f"template missing: {path}"


@pytest.mark.parametrize("tpl_path", _template_files() or [None])
def test_template_html_basic_structure(tpl_path):
    if tpl_path is None:
        pytest.skip("no templates present yet")
    text = tpl_path.read_text(encoding="utf-8")
    assert text.lower().startswith("<!doctype html"), f"{tpl_path.name} missing DOCTYPE"
    assert '<html lang="en"' in text or "<html lang='en'" in text, f"{tpl_path.name} missing lang attribute"
    assert '<meta name="viewport"' in text, f"{tpl_path.name} missing viewport meta"


@pytest.mark.parametrize("tpl_path", _template_files() or [None])
def test_template_has_plan_data_block(tpl_path):
    if tpl_path is None:
        pytest.skip("no templates present yet")
    text = tpl_path.read_text(encoding="utf-8")
    plan = extract_plan_json(text)
    for field in BASE_FIELDS:
        assert field in plan, f"{tpl_path.name} plan-data missing field: {field}"
    assert plan["schema_version"] == "0.1.0", f"{tpl_path.name} schema_version != 0.1.0"


@pytest.mark.parametrize("tpl_path", _template_files() or [None])
def test_template_offline_only(tpl_path):
    """No remote URLs, no external stylesheets, no script src=, no eval."""
    if tpl_path is None:
        pytest.skip("no templates present yet")
    text = tpl_path.read_text(encoding="utf-8")
    assert not LINK_STYLESHEET_RE.search(text), f"{tpl_path.name} uses <link rel=stylesheet>"
    assert not SCRIPT_SRC_RE.search(text), f"{tpl_path.name} uses <script src=...>"
    # remote URLs: only allow href to local anchors (#...) — block https://
    assert not REMOTE_URL_RE.search(text), f"{tpl_path.name} references remote URL"
    assert not EVAL_OR_FUNCTION_RE.search(text), f"{tpl_path.name} uses eval or new Function()"


@pytest.mark.parametrize("tpl_path", _template_files() or [None])
def test_template_size_budget(tpl_path):
    """Template file should be under 100KB total per the spec."""
    if tpl_path is None:
        pytest.skip("no templates present yet")
    size = tpl_path.stat().st_size
    assert size < 100_000, f"{tpl_path.name} exceeds 100KB budget ({size} bytes)"
