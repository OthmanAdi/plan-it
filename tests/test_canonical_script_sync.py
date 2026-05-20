"""Top-level scripts/ and skills/plan-it/scripts/ must stay byte-identical after sync."""
from __future__ import annotations

import subprocess
import sys

SHARED_SCRIPTS = [
    "plan-hook.py",
    "init-plan.sh",
    "init-plan.ps1",
    "render-plan.sh",
    "render-plan.ps1",
    "attest-plan.sh",
    "attest-plan.ps1",
    "bump-version.py",
    "sync-ide-folders.py",
    "session-catchup.py",
    "export-markdown.py",
]


def test_top_level_scripts_exist(repo_root):
    for script in SHARED_SCRIPTS:
        assert (repo_root / "scripts" / script).is_file(), f"missing {script}"


def test_sync_verify_after_sync(repo_root, scripts_dir):
    """Run sync, then verify, expect green."""
    sync_path = scripts_dir / "sync-ide-folders.py"
    if not sync_path.is_file():
        return  # not yet present
    # Run sync
    proc = subprocess.run([sys.executable, str(sync_path)], capture_output=True, text=True, cwd=repo_root, encoding="utf-8")
    assert proc.returncode == 0, f"sync failed: {proc.stderr}"
    # Verify
    proc = subprocess.run([sys.executable, str(sync_path), "--verify"], capture_output=True, text=True, cwd=repo_root, encoding="utf-8")
    assert proc.returncode == 0, f"verify failed after sync: {proc.stdout}\n{proc.stderr}"
