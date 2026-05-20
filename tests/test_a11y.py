"""Accessibility checks. Every template must pass WCAG-AA-aligned baseline."""
from __future__ import annotations

import re
from pathlib import Path

import pytest


def _template_files() -> list[Path]:
    tdir = Path(__file__).resolve().parent.parent / "templates"
    return sorted([p for p in tdir.glob("*.html")])


@pytest.mark.parametrize("tpl_path", _template_files() or [None])
def test_template_has_skip_link(tpl_path):
    if tpl_path is None:
        pytest.skip("no templates present yet")
    text = tpl_path.read_text(encoding="utf-8")
    assert 'skip-link' in text.lower() or 'skip to main' in text.lower(), (
        f"{tpl_path.name} missing skip-to-main link"
    )


@pytest.mark.parametrize("tpl_path", _template_files() or [None])
def test_template_has_aria_labels(tpl_path):
    if tpl_path is None:
        pytest.skip("no templates present yet")
    text = tpl_path.read_text(encoding="utf-8")
    aria_count = len(re.findall(r'aria-(label|labelledby|describedby|controls|selected|expanded)', text))
    assert aria_count >= 3, f"{tpl_path.name} has too few aria attributes ({aria_count})"


@pytest.mark.parametrize("tpl_path", _template_files() or [None])
def test_template_uses_system_fonts(tpl_path):
    """No web fonts — system-ui, ui-serif, ui-monospace only."""
    if tpl_path is None:
        pytest.skip("no templates present yet")
    text = tpl_path.read_text(encoding="utf-8")
    assert "system-ui" in text or "system" in text.lower(), (
        f"{tpl_path.name} does not declare system fonts"
    )
    # No @font-face, no Google Fonts
    assert "@font-face" not in text, f"{tpl_path.name} uses @font-face"
    assert "fonts.googleapis.com" not in text, f"{tpl_path.name} uses Google Fonts"


@pytest.mark.parametrize("tpl_path", _template_files() or [None])
def test_template_has_lang_attribute(tpl_path):
    if tpl_path is None:
        pytest.skip("no templates present yet")
    text = tpl_path.read_text(encoding="utf-8")
    assert re.search(r'<html\s+lang=', text), f"{tpl_path.name} <html> missing lang attribute"
