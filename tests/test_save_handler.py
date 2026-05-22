"""Save handler presence + size + idempotency markers (v0.1.1)."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

# Templates that mutate state and therefore must expose the Save button.
TEMPLATES_WITH_SAVE = [
    "implementation-plan",
    "annotated-pr",
    "feature-flag-editor",
    "incident-timeline",
    "animation-sandbox",
    "ticket-triage",
]

# Pure display / export templates — no Save button by design.
TEMPLATES_WITHOUT_SAVE = [
    "living-design-system",
    "module-map",
    "three-approaches",
    "weekly-status",
]


def _read(name: str) -> str:
    return (TEMPLATES_DIR / f"{name}.html").read_text(encoding="utf-8")


@pytest.mark.parametrize("name", TEMPLATES_WITH_SAVE)
def test_save_button_present(name):
    t = _read(name)
    assert 'id="btn-save"' in t, f"{name} missing Save button"
    assert 'aria-label="Save plan.html to disk"' in t, f"{name} Save button missing aria-label"


@pytest.mark.parametrize("name", TEMPLATES_WITH_SAVE)
def test_save_handler_present(name):
    t = _read(name)
    for needle in ("savePlanHtml", "showSaveFilePicker", "createObjectURL", "flashSaved"):
        assert needle in t, f"{name} missing {needle!r}"


@pytest.mark.parametrize("name", TEMPLATES_WITH_SAVE)
def test_save_handler_uses_fsa_with_download_fallback(name):
    t = _read(name)
    # FSA path must come before the download fallback so users land on the better UX.
    fsa_pos = t.find("showSaveFilePicker")
    dl_pos = t.find("createObjectURL")
    assert 0 < fsa_pos < dl_pos, f"{name} FSA path must precede download fallback"


@pytest.mark.parametrize("name", TEMPLATES_WITH_SAVE)
def test_save_handler_writes_back_into_data_block(name):
    t = _read(name)
    assert 'dataEl.textContent = JSON.stringify(plan' in t, (
        f"{name} Save must push current plan state into the embedded JSON before serializing"
    )


@pytest.mark.parametrize("name", TEMPLATES_WITH_SAVE)
def test_save_handler_escapes_script_close(name):
    """JSON.stringify does not escape '<', so a user typing '</script>' into
    any string field would terminate the embedded script block on reload AND
    open an injection surface. Save handler must escape '<' as the literal
    six-character sequence backslash-u-0-0-3-c before write-back."""
    t = _read(name)
    # File on disk should contain the JS source literal: .replace(/</g, "<")
    # which is two characters (backslash + backslash) followed by u003c in the file.
    needle = '.replace(/</g, "\\\\u003c")'
    assert needle in t, (
        f"{name} Save handler must contain {needle!r} to escape '<' "
        f"and prevent premature </script> close on reload"
    )


@pytest.mark.parametrize("name", TEMPLATES_WITHOUT_SAVE)
def test_pure_display_templates_have_no_save(name):
    t = _read(name)
    assert 'id="btn-save"' not in t, (
        f"{name} is display-only; should not advertise Save"
    )
    assert "showSaveFilePicker" not in t, (
        f"{name} is display-only; should not ship Save handler"
    )


@pytest.mark.parametrize("name", TEMPLATES_WITH_SAVE)
def test_in_memory_only_lie_removed(name):
    t = _read(name)
    assert "in-memory only" not in t, (
        f"{name} still carries the pre-0.1.1 false-affordance comment"
    )


@pytest.mark.parametrize("name", TEMPLATES_WITH_SAVE)
def test_idempotency_marker_present(name):
    """Save serializes the populated DOM. Re-opens must clear render roots
    before re-populating or the cards would double."""
    t = _read(name)
    has_clear = (
        "replaceChildren()" in t
        or 'innerHTML = ""' in t
        or 'textContent = ""' in t
    )
    assert has_clear, f"{name} render roots are not cleared before populate"


@pytest.mark.parametrize("name", TEMPLATES_WITH_SAVE + TEMPLATES_WITHOUT_SAVE)
def test_size_under_budget(name):
    """v0.1.1 raises budget from 30KB to 35KB to absorb the inline Save handler."""
    sz = (TEMPLATES_DIR / f"{name}.html").stat().st_size
    assert sz <= 35_000, f"{name} is {sz} bytes, over the 35KB single-file budget"


def test_plan_data_block_still_parseable():
    """Save handler depends on dataEl.textContent round-tripping. Confirm
    every template still has a parseable JSON block."""
    import json
    for name in TEMPLATES_WITH_SAVE + TEMPLATES_WITHOUT_SAVE:
        t = _read(name)
        m = re.search(
            r'<script type="application/json" id="plan-data">(.*?)</script>',
            t, re.DOTALL,
        )
        assert m, f"{name} plan-data block missing"
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            raise AssertionError(f"{name} plan-data not parseable: {e}")
        assert "schema_version" in data, f"{name} plan-data missing schema_version"


@pytest.mark.parametrize("name", TEMPLATES_WITH_SAVE + TEMPLATES_WITHOUT_SAVE)
def test_no_premature_script_close_in_main_body(name):
    """Regression for issue #3 (fxy413): a literal close-script substring
    inside a JS comment or string terminates the surrounding <script> block
    in HTML raw-text mode, dropping every line after it. Walk the file as the
    HTML parser would and assert each <script> opens at the same offset its
    true end-tag closes at."""
    t = _read(name)
    # Find every <script ...> opener that is NOT type="application/json".
    for opener in re.finditer(
        r'<script(?![^>]*type="application/json")[^>]*>', t
    ):
        body_start = opener.end()
        first_close = re.search(r"</script", t[body_start:], re.IGNORECASE)
        assert first_close, f"{name} <script> at offset {opener.start()} never closes"
        true_close = re.search(r"</script\s*>", t[body_start:], re.IGNORECASE)
        assert true_close, f"{name} <script> at offset {opener.start()} has no real end-tag"
        assert first_close.start() == true_close.start(), (
            f"{name}: <script> at offset {opener.start()} is terminated early "
            f"by a literal close-script substring at body offset "
            f"{first_close.start()}. Rewrite the comment/string so the "
            f"substring does not appear, or the HTML parser will drop all JS "
            f"after that point (issue #3)."
        )
