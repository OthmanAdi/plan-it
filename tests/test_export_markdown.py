"""export-markdown.py round-trip tests."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _write_plan(tmp_path: Path) -> None:
    plan = {
        "schema_version": "0.1.0",
        "plan_title": "RoundTrip Test",
        "goal": "Verify HTML → Markdown export.",
        "current_phase": 1,
        "template": "implementation-plan",
        "created_at": "2026-05-20T00:00:00Z",
        "updated_at": "2026-05-20T00:00:00Z",
        "phases": [
            {"id": 1, "title": "Phase 1", "status": "in_progress",
             "items": [{"text": "Item A", "done": True, "owner": "alice"}, {"text": "Item B", "done": False, "owner": None}],
             "milestones": ["m1"]},
            {"id": 2, "title": "Phase 2", "status": "pending", "items": [], "milestones": []},
        ],
        "findings": [{"id": "f1", "topic": "Discovery", "body": "Found something."}],
        "progress_log": [{"ts": "2026-05-20T00:01:00Z", "phase": 1, "action": "started", "files": ["a.py"]}],
        "decisions": [{"id": "d1", "decision": "Use HTML", "rationale": "Engagement."}],
        "errors": [],
    }
    html = f"""<!doctype html>
<html><body>
<script type="application/json" id="plan-data">{json.dumps(plan)}</script>
</body></html>
"""
    (tmp_path / "plan.html").write_text(html, encoding="utf-8")


def _run(scripts_dir: Path, cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(scripts_dir / "export-markdown.py"), *args],
        capture_output=True, text=True, cwd=cwd, encoding="utf-8",
    )


def test_export_writes_three_files(tmp_path, scripts_dir):
    _write_plan(tmp_path)
    proc = _run(scripts_dir, tmp_path)
    assert proc.returncode == 0
    assert (tmp_path / "task_plan.md").is_file()
    assert (tmp_path / "findings.md").is_file()
    assert (tmp_path / "progress.md").is_file()


def test_task_plan_md_contains_phase_titles(tmp_path, scripts_dir):
    _write_plan(tmp_path)
    _run(scripts_dir, tmp_path)
    text = (tmp_path / "task_plan.md").read_text(encoding="utf-8")
    assert "RoundTrip Test" in text
    assert "Phase 1: Phase 1" in text
    assert "[x] Item A" in text
    assert "[ ] Item B" in text
    assert "**Status:** in_progress" in text


def test_findings_md_has_topics(tmp_path, scripts_dir):
    _write_plan(tmp_path)
    _run(scripts_dir, tmp_path)
    text = (tmp_path / "findings.md").read_text(encoding="utf-8")
    assert "## Discovery" in text
    assert "Found something." in text


def test_progress_md_has_entries(tmp_path, scripts_dir):
    _write_plan(tmp_path)
    _run(scripts_dir, tmp_path)
    text = (tmp_path / "progress.md").read_text(encoding="utf-8")
    assert "started" in text
    assert "a.py" in text


def test_single_combined_mode(tmp_path, scripts_dir):
    _write_plan(tmp_path)
    proc = _run(scripts_dir, tmp_path, "--single")
    assert proc.returncode == 0
    assert (tmp_path / "plan.md").is_file()
    text = (tmp_path / "plan.md").read_text(encoding="utf-8")
    assert "# Task Plan" in text
    assert "# Findings" in text
    assert "# Progress Log" in text


def test_no_plan_returns_error(tmp_path, scripts_dir):
    proc = _run(scripts_dir, tmp_path)
    assert proc.returncode == 1
