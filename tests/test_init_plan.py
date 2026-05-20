"""init-plan.sh / init-plan.ps1 functional smoke tests.

Runs whichever script is appropriate for the host OS.
"""
from __future__ import annotations

import platform
import shutil
import subprocess
from pathlib import Path

import pytest


def _run_init_plan(scripts_dir: Path, cwd: Path, template: str) -> subprocess.CompletedProcess[str]:
    is_windows = platform.system() == "Windows"
    if is_windows:
        # Prefer pwsh, fall back to powershell.
        shell = shutil.which("pwsh") or shutil.which("powershell")
        if not shell:
            pytest.skip("no PowerShell found on PATH")
        script = scripts_dir / "init-plan.ps1"
        cmd = [shell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script), "-Template", template]
    else:
        bash = shutil.which("bash")
        if not bash:
            pytest.skip("no bash found on PATH")
        script = scripts_dir / "init-plan.sh"
        cmd = [bash, str(script), template]
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, encoding="utf-8")


@pytest.mark.parametrize("template", ["implementation-plan"])
def test_init_plan_creates_plan_html(tmp_path, scripts_dir, templates_dir, template):
    # Copy templates into tmp_path/templates so init-plan can resolve them.
    dst_tpl = tmp_path / "templates"
    dst_tpl.mkdir()
    src = templates_dir / f"{template}.html"
    if not src.is_file():
        pytest.skip(f"template not yet generated: {template}")
    (dst_tpl / f"{template}.html").write_bytes(src.read_bytes())
    # Also put a scripts dir so the script's relative resolution works.
    dst_scripts = tmp_path / "scripts"
    dst_scripts.mkdir()
    shutil.copy2(scripts_dir / "init-plan.sh", dst_scripts / "init-plan.sh")
    shutil.copy2(scripts_dir / "init-plan.ps1", dst_scripts / "init-plan.ps1")

    proc = _run_init_plan(dst_scripts, tmp_path, template)
    assert proc.returncode == 0, f"init-plan failed: {proc.stdout}\n{proc.stderr}"
    assert (tmp_path / "plan.html").is_file()
    body = (tmp_path / "plan.html").read_text(encoding="utf-8")
    assert "<script type=\"application/json\" id=\"plan-data\">" in body
