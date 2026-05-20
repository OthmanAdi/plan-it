# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-05-20

### Added

- **Initial release.** First persistent, multi-IDE, hash-attested, HTML-emitting planning skill in the Claude Code ecosystem. Built within the publication window of Thariq Shihipar's "The Unreasonable Effectiveness of HTML" (claude.com/blog, 2026-05-20) to establish a first-mover position.
- **Canonical `skills/plan-it/SKILL.md`** with 5 lifecycle hooks (`UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `PreCompact`), Anti-Slop section, Gotchas section, plan-injection delimiters using `===BEGIN PLAN DATA===` / `===END PLAN DATA===` (never `---`, per the YAML-collision lesson from planning-with-files v2.38.1).
- **10 HTML templates** spanning Thariq's nine categories: `implementation-plan`, `three-approaches`, `ticket-triage`, `feature-flag-editor`, `module-map`, `annotated-pr`, `living-design-system`, `animation-sandbox`, `weekly-status`, `incident-timeline`. Each template is a single self-contained `.html` file with inline `<style>` and `<script>`, system fonts only, prefers-color-scheme aware, WCAG AA contrast, ARIA-labeled controls, keyboard navigation, no CDN, no build step.
- **7 scripts** shipped: `init-plan.sh/.ps1` (scaffold from template), `render-plan.sh/.ps1` (open in browser), `attest-plan.sh/.ps1` (SHA-256 lock with `--show`/`--clear`), `bump-version.py` (parity-locked bumper across the 17-file set), `sync-ide-folders.py` (mirror canonical to IDE adapter folders), `session-catchup.py` (parse Claude Code + OpenCode + Codex session stores for unsynced edits), `export-markdown.py` (flatten plan.html → task_plan.md + findings.md + progress.md, planning-with-files compatible).
- **8 slash commands**: `/plan`, `/plan-render`, `/plan-attest`, `/plan-status`, `/plan-export`, `/plan-goal`, `/plan-loop`, plus a `templates/loop.md` for direct use with Claude Code's `/loop` primitive.
- **20+ pytest tests** covering frontmatter parity, hook bodies, plan-hook subcommands, attestation match/mismatch, markdown export round-trip, template structural constraints, accessibility baseline, command file presence, session-catchup safety, and parity-locked version bumper.
- **17 IDE adapter mirrors**: `.codex/`, `.cursor/`, `.codebuddy/`, `.factory/`, `.mastracode/`, `.opencode/`, `.hermes/`, `.continue/`, `.gemini/`, `.kiro/`, `.pi/`, plus `clawhub-upload/` for the manual ClawHub bundle.
- **English-only SKILL.md for v0.1.0.** Localized variants (ar/de/es/zh/zht) land in v0.2.0 with real translations rather than English-body placeholders.
- **Plugin manifests** at `.claude-plugin/plugin.json` + `marketplace.json`.
- **Skeptic-mitigation features** (responding to common community critiques about HTML as an output format): bidirectional `/plan-export markdown`, JSON-only data diffs (the render layer is derived, the diff stays clean), WCAG AA + ARIA from day 1, single-file offline-only (no hosting friction), hand-written vanilla JS (no `eval`, no `Function()`, no remote loads), explicit token-cost honesty line in README.
- **Documentation**: README with install matrix for 17 platforms, prior-art credit, token-cost honesty, security boundary, schema. CONTRIBUTORS.md. CITATION.cff for academic / structured citation. AGENTS.md as the cross-IDE manifest. CLAUDE.md as project working rules.

### Thanks

- planning-with-files (OthmanAdi) for the operational discipline plan-it inherits: hook lifecycle, session catchup, SHA-256 attestation, parity-locked version bumper, 17-IDE adapter distribution.
