# AGENTS.md

Universal manifest for agentic IDEs that read AGENTS.md (Cursor, Codex, Cline, Kilocode, Hermes, OpenCode, others).

## What this repo is

plan-it is a Claude Code skill that produces a single self-contained HTML plan file (`plan.html`) with embedded JSON state. It is the HTML-first successor to planning-with-files for the post-Thariq era.

## Where the canonical files live

- `skills/plan-it/SKILL.md` — canonical English skill manifest, frontmatter + 5 lifecycle hooks + body.
- `scripts/` — top-level canonical scripts, byte-identical to `skills/plan-it/scripts/`.
- `templates/` — the 10 HTML plan templates across Thariq's 9 categories.
- `commands/` — slash command definitions (`/plan`, `/plan-render`, `/plan-attest`, `/plan-status`, `/plan-export`, `/plan-goal`, `/plan-loop`).

## IDE mirrors

11 IDE adapter folders contain SKILL.md variants with the IDE-specific frontmatter shape but byte-identical scripts and templates:
`.codex/`, `.cursor/`, `.codebuddy/`, `.factory/`, `.mastracode/`, `.opencode/`, `.hermes/`, `.continue/`, `.gemini/`, `.kiro/`, `.pi/`, plus `clawhub-upload/` for the ClawHub manual-upload bundle.

## Language variants

English-only in v0.1.0. Localized variants (ar/de/es/zh/zht) deferred to v0.2.0 until real translations are ready. The parity bumper does not track them yet.

## Working rules for agents

1. NEVER edit `plan.html` directly. Plans are owned by users. Append-only updates go through the JSON data layer via `scripts/init-plan` or in-browser controls.
2. The `<script type="application/json" id="plan-data">` block is the single source of truth. The render layer below it is derived.
3. SHA-256 attestation lives at `./.plan-attestation` (legacy) or `.planning/<slug>/.attestation` (parallel-plan mode).
4. The plan-injection delimiter is `===BEGIN PLAN DATA===` / `===END PLAN DATA===` (never `---` — that collides with YAML doc-separator and breaks Claude Code's skill loader).
5. All scripts must be portable across Windows (Git Bash + PowerShell), Linux, macOS. Use `/usr/bin/env bash` shebangs and known system Python resolution.
6. Commits go in by OthmanAdi only. No co-authored-by trailer. Contributors credited in CONTRIBUTORS.md + CHANGELOG Thanks section.
7. Prose tone: sachlich. No em-dashes. Run public-facing prose through `/humanizer` before posting.
8. Version bumps go through `scripts/bump-version.py` across the 19-file parity set, verified by `tests/test_skill_md_version_parity.py`.

## Test discipline

- `python -m pytest tests/ -q` is the gate.
- Targets ≥20 tests for v0.1.0.
- Accessibility tests are non-optional: every template must pass WCAG AA contrast + ARIA + keyboard-nav assertions.

## Quick start for any agent

```bash
git clone https://github.com/OthmanAdi/plan-it
cd plan-it
python -m pytest tests/ -q
bash scripts/init-plan.sh implementation-plan
bash scripts/render-plan.sh
```
