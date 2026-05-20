# Windows notes

plan-it is tested on Windows 11 with PowerShell 7 and Git Bash. Two surfaces to know about:

## PowerShell scripts

The `.ps1` scripts use modern PowerShell idioms (PSDrive paths, `Get-FileHash`, native `Set-Content -NoNewline`). Tested on:

- PowerShell 7.x (`pwsh`)
- Windows PowerShell 5.1 (`powershell`)

If `Get-Command pwsh` fails, the test suite falls back to `powershell`. To force one or the other:

```
$env:PLAN_IT_SHELL = 'pwsh'   # or 'powershell'
```

## Git Bash

The `.sh` scripts work in Git Bash and WSL. The `render-plan.sh` script auto-detects `MINGW*` / `MSYS*` / `CYGWIN*` and uses `start` to open the browser. WSL is detected via `wslview` first, then falls back to `xdg-open`.

## Known quirks

- **Long paths**: enable long-path support if your project lives deep under `Documents\projects\...`. PowerShell's `New-Item` and Python's `Path` both handle long paths since Windows 10 1607 with the registry key, but Git on Windows still imposes a 260-char limit unless `core.longpaths=true`.
- **Junction vs symlink**: `npx skills add` creates a junction on Windows (`mklink /J`). If you symlink manually use `mklink /D` from an elevated prompt or use Developer Mode (settings → For developers → Developer Mode on).
- **CRLF**: line endings normalize via `.gitattributes`. If a script fails with `bad interpreter`, check that it ends in LF, not CRLF.
- **PATH for Python**: hooks resolve Python via `command -v python3 || command -v python` (POSIX) and via the `python.exe` on PATH (Windows). If both `python3` and `python` are missing, install Python 3.10+ from python.org or the Microsoft Store.

## Recommended PowerShell profile snippet

```powershell
function plan { & pwsh scripts/init-plan.ps1 @args }
function render { & pwsh scripts/render-plan.ps1 }
function attest { & pwsh scripts/attest-plan.ps1 @args }
```

Now `plan implementation-plan`, `render`, `attest` work as one-word commands from anywhere inside your project.
