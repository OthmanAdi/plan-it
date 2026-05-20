"""plan-hook.py behavior tests."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SAMPLE_PLAN = {
    "schema_version": "0.1.0",
    "plan_title": "Sample plan",
    "goal": "Verify hook output",
    "current_phase": 1,
    "template": "implementation-plan",
    "created_at": "2026-05-20T00:00:00Z",
    "updated_at": "2026-05-20T00:00:00Z",
    "phases": [
        {"id": 1, "title": "Foundation", "status": "in_progress",
         "items": [{"text": "do a thing", "done": False, "owner": None}],
         "milestones": ["a milestone"]},
        {"id": 2, "title": "Verify", "status": "pending", "items": [], "milestones": []},
    ],
    "findings": [],
    "progress_log": [{"ts": "2026-05-20T00:30:00Z", "phase": 1, "action": "kicked off", "files": []}],
    "decisions": [],
    "errors": [],
    "attestation_sha256": None,
}


def _write_plan_html(path: Path, plan: dict) -> None:
    body = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>t</title></head>
<body>
<script type="application/json" id="plan-data">{json.dumps(plan)}</script>
<script>1</script>
</body></html>
"""
    path.write_text(body, encoding="utf-8")


def _run_hook(scripts_dir: Path, cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, str(scripts_dir / "plan-hook.py"), *args]
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, encoding="utf-8")


def test_inject_summary_with_plan(tmp_path, scripts_dir):
    _write_plan_html(tmp_path / "plan.html", SAMPLE_PLAN)
    proc = _run_hook(scripts_dir, tmp_path, "inject", "--mode", "summary", "--lines", "30")
    assert proc.returncode == 0
    out = proc.stdout
    assert "===BEGIN PLAN DATA===" in out
    assert "===END PLAN DATA===" in out
    assert "plan_title: Sample plan" in out
    assert "current_phase: 1" in out


def test_inject_silent_without_plan(tmp_path, scripts_dir):
    proc = _run_hook(scripts_dir, tmp_path, "inject", "--mode", "summary", "--lines", "30")
    assert proc.returncode == 0
    # When no plan.html exists, output should be empty (silent).
    assert proc.stdout == ""


def test_inject_active_phase_mode(tmp_path, scripts_dir):
    _write_plan_html(tmp_path / "plan.html", SAMPLE_PLAN)
    proc = _run_hook(scripts_dir, tmp_path, "inject", "--mode", "active-phase", "--lines", "15")
    assert proc.returncode == 0
    assert "active phase" in proc.stdout
    assert "Foundation" in proc.stdout


def test_check_complete_warns_on_open_phase(tmp_path, scripts_dir):
    _write_plan_html(tmp_path / "plan.html", SAMPLE_PLAN)
    proc = _run_hook(scripts_dir, tmp_path, "check-complete")
    assert proc.returncode == 0
    assert "still open" in proc.stdout


def test_check_complete_silent_when_no_plan(tmp_path, scripts_dir):
    proc = _run_hook(scripts_dir, tmp_path, "check-complete")
    assert proc.returncode == 0
    assert proc.stdout == ""


def test_attestation_match(tmp_path, scripts_dir):
    plan_path = tmp_path / "plan.html"
    _write_plan_html(plan_path, SAMPLE_PLAN)
    # Manually compute and store SHA-256
    import hashlib
    h = hashlib.sha256(plan_path.read_bytes()).hexdigest()
    (tmp_path / ".plan-attestation").write_text(h, encoding="utf-8")
    proc = _run_hook(scripts_dir, tmp_path, "inject", "--mode", "summary", "--lines", "30")
    assert proc.returncode == 0
    assert "PLAN TAMPERED" not in proc.stdout
    assert f"Plan-SHA256: {h}" in proc.stdout


def test_attestation_mismatch_blocks(tmp_path, scripts_dir):
    plan_path = tmp_path / "plan.html"
    _write_plan_html(plan_path, SAMPLE_PLAN)
    (tmp_path / ".plan-attestation").write_text("0" * 64, encoding="utf-8")
    proc = _run_hook(scripts_dir, tmp_path, "inject", "--mode", "summary", "--lines", "30")
    assert proc.returncode == 0
    assert "PLAN TAMPERED" in proc.stdout
    assert "===BEGIN PLAN DATA===" not in proc.stdout


def test_parse_subcommand(tmp_path, scripts_dir):
    plan_path = tmp_path / "plan.html"
    _write_plan_html(plan_path, SAMPLE_PLAN)
    proc = _run_hook(scripts_dir, tmp_path, "parse", str(plan_path))
    assert proc.returncode == 0
    parsed = json.loads(proc.stdout)
    assert parsed["plan_title"] == "Sample plan"
    assert parsed["current_phase"] == 1
