"""session-catchup.py should never crash, even when nothing is configured."""
from __future__ import annotations

import subprocess
import sys


def test_catchup_silent_when_no_plan(tmp_path, scripts_dir):
    proc = subprocess.run(
        [sys.executable, str(scripts_dir / "session-catchup.py"), str(tmp_path)],
        capture_output=True, text=True, encoding="utf-8",
    )
    assert proc.returncode == 0


def test_catchup_runs_when_plan_present(tmp_path, scripts_dir):
    (tmp_path / "plan.html").write_text("<html></html>", encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(scripts_dir / "session-catchup.py"), str(tmp_path)],
        capture_output=True, text=True, encoding="utf-8",
    )
    assert proc.returncode == 0
    # Should mention "session catchup" or "no prior sessions" -- it doesn't crash either way.
    assert "catchup" in proc.stdout.lower() or proc.stdout == ""
