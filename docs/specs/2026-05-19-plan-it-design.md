# plan-it v0.1.0, Design Spec

- Date: 2026-05-19
- Author: OthmanAdi
- Status: APPROVED for build (decisions locked 2026-05-19)
- Repo: `github.com/OthmanAdi/plan-it`

## 1. Goal (use with Claude Code `/goal`)

Paste this into Claude Code to install the termination condition:

```
/goal plan-it v0.1.0 is shipped when all of these are true: (1) canonical skills/plan-it/SKILL.md exists with valid frontmatter, 5 lifecycle hooks declared (UserPromptSubmit, PreToolUse, PostToolUse, Stop, PreCompact), and Anti-Slop + Gotchas sections present. (2) 10 HTML plan templates ship under templates/ matching Thariq's 9 categories. (3) 17 IDE adapter mirrors exist under .codex / .cursor / .codebuddy / .factory / .mastracode / .opencode / .hermes / .continue / .gemini / .kiro / .pi / clawhub-upload, byte-identical scripts. (4) 6 language variants (en/ar/de/es/zh/zht) of SKILL.md exist. (5) scripts/ has: render-plan.sh + render-plan.ps1 (open in browser), init-plan.sh + init-plan.ps1 (scaffold), attest-plan.sh + attest-plan.ps1 (SHA-256), bump-version.py, sync-ide-folders.py, session-catchup.py. (6) ≥20 pytest tests passing under tests/. (7) Parity-locked version bumper test green across 19 files. (8) A demo plan.html renders in a real browser and proves sliders + drag-cards + copy-button + collapsibles + embedded JSON data work end-to-end. (9) README.md + CHANGELOG.md + CONTRIBUTORS.md + CITATION.cff + LICENSE (MIT) + .claude-plugin/{plugin.json,marketplace.json} ready. (10) Git initialized with main branch, single squashed initial commit by OthmanAdi only, tag v0.1.0 ready to push. (11) Adi has reviewed the demo plan.html in a browser and approved aesthetic + interactivity. (12) ClawHub upload bundle prepared. Until all 12 are green: keep building, do not declare done.
```

## 2. Mission shape

```
                          plan-it v0.1.0
                                |
        +-----------------------+-----------------------+
        |                       |                       |
   THE SKILL              THE PLAN FORMAT          DISTRIBUTION
        |                       |                       |
  SKILL.md (canonical)    plan.html              .claude-plugin/
  5 hooks                 - <script id="plan-data"     plugin.json
  10 templates              type="application/json">   marketplace.json
  scripts/                  - <style> inline CSS       17 IDE mirrors
  - render-plan          - <script> inline JS          (no lang variants v0.1.0)
  - init-plan            - Anti-slop opinion         CITATION.cff
  - attest-plan          - System fonts              README + CHANGELOG
  - bump-version           - No CDN, no network      MIT license
  - sync-ide-folders     - Single file, offline      Tests (pytest)
  - session-catchup     ready                       Smoke demo
```

## 3. Mission profile (constraints and criteria)

### Hard constraints (will NOT violate)
1. Single-file HTML output. No build step. No CDN. Offline-capable.
2. Inline `<style>`, inline `<script>`, base64 images or inline SVG only.
3. System fonts: `system-ui, sans-serif, monospace`. No web fonts.
4. Data lives in `<script type="application/json" id="plan-data">`. HTML is the renderer.
5. Hooks re-inject plan summary on UserPromptSubmit + PreToolUse just like pwf, but the source-of-truth file is `plan.html` (parse the embedded JSON).
6. SHA-256 attestation on the full `plan.html` file (same security boundary as pwf).
7. 17-IDE adapter mirror system. Byte-identical scripts.
8. English-only in v0.1.0; localized variants land in v0.2.0 with real translations.
9. Parity-locked version bumper across the 19-file set.
10. No co-authored-by trailer in commits. Author = OthmanAdi only.
11. Sachlich tone. No em-dashes. /humanizer on prose.
12. Anti-slop discipline: avoid purple gradients, excessive centered layouts, uniform rounded corners, Inter font.

### Soft constraints (preferences, can bend)
- Prefer keyboard-navigable templates (escape closes modal, arrow keys move through phases).
- Templates ship dark + light by `prefers-color-scheme`.
- Each template includes a "Copy as Markdown" button for chained-agent intermediate steps.
- Each template includes a "Copy as JSON" button for the data layer.
- All templates pass basic WCAG AA contrast.

### Definition of done (10x quality bar)
1. **Adi opens demo plan.html, drags a card, clicks copy-as-markdown, sees clean Markdown in clipboard. No bugs.**
2. Reinstall via `npx skills add OthmanAdi/plan-it` works on Claude Code, Cursor, Codex day 1.
3. Description field passes Anthropic's skill-discovery loader (no YAML collisions; we use `===` delimiters from pwf v2.38.1 lesson).
4. SHA-256 attestation gates injection on a tampered file.
5. Session catchup parses Claude Code / OpenCode session DBs and surfaces unsynced plan-html edits.
6. ≥20 pytest tests cover: hook bodies parse, templates render, JSON schema validates, parity locked, scripts portable on Windows+Linux+macOS shebangs, attestation match/mismatch, render-plan opens the browser, init-plan scaffolds from template, sync-ide-folders byte-identical.
7. README has demo gif of plan.html with interactive controls.
8. CHANGELOG entry sachlich, no em-dashes, Thanks line.
9. Issue tracker primed with v0.2.0 backlog (translations of templates, more IDEs, more templates).

### Reach goals (v0.2.0+ candidates, NOT this session)
- Plan-it ↔ pwf compat mode: read existing task_plan.md, render as plan.html.
- Team / multi-user editing (CRDT-lite via shared `<script>`-stored last-writer-wins).
- Auto-publishing via here.now to share URLs.

## 4. Architecture

### File layout (29 canonical + 82 mirrors + 6 lang + 3 manifests = ~120 files)

```
plan-it/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── skills/
│   └── plan-it/                          # canonical English (v0.1.0 ships en only)
│       ├── SKILL.md                      # frontmatter + body
│       ├── scripts/                      # byte-identical to top-level scripts/
│       └── templates/                    # byte-identical to top-level templates/
├── scripts/                              # top-level canonical scripts
│   ├── render-plan.sh / .ps1             # opens plan.html in browser
│   ├── init-plan.sh / .ps1               # scaffolds plan.html from template
│   ├── attest-plan.sh / .ps1             # SHA-256 of plan.html
│   ├── bump-version.py                   # parity-locked 19-file bump
│   ├── sync-ide-folders.py               # mirror canonical to .codex etc.
│   └── session-catchup.py                # parse IDE session DBs for unsynced edits
├── templates/                            # the 10 HTML templates
│   ├── implementation-plan.html
│   ├── ticket-triage.html
│   ├── feature-flag-editor.html
│   ├── module-map.html
│   ├── annotated-pr.html
│   ├── living-design-system.html
│   ├── animation-sandbox.html
│   ├── feature-explainer.html
│   ├── weekly-status.html
│   └── incident-timeline.html
├── commands/
│   ├── plan.md                           # /plan invokes init-plan
│   ├── plan-render.md                    # /plan-render opens browser
│   ├── plan-attest.md                    # /plan-attest locks SHA-256
│   ├── plan-status.md                    # /plan-status one-line summary
│   ├── plan-goal.md                      # /plan-goal composes with Claude /goal
│   └── plan-loop.md                      # /plan-loop composes with Claude /loop
├── tests/                                # pytest, 20+ tests
├── docs/
│   ├── installation.md
│   ├── quickstart.md
│   ├── windows.md
│   └── specs/2026-05-19-plan-it-design.md
├── .codex/skills/plan-it/                # 11 IDE mirrors
├── .cursor/skills/plan-it/
├── .codebuddy/skills/plan-it/
├── .factory/skills/plan-it/
├── .mastracode/skills/plan-it/
├── .opencode/skills/plan-it/
├── .hermes/skills/plan-it/
├── .continue/skills/plan-it/
├── .gemini/skills/plan-it/
├── .kiro/skills/plan-it/
├── .pi/skills/plan-it/
├── clawhub-upload/                       # manual upload bundle
├── examples/                             # filled-in demo plans (the goal-state demo)
├── media/                                # banner + demo gif
├── README.md
├── CHANGELOG.md
├── CONTRIBUTORS.md
├── CITATION.cff
├── LICENSE                               # MIT
├── AGENTS.md                             # cross-IDE manifest
├── CLAUDE.md                             # project working rules
└── .gitignore
```

### Hook semantics

| Hook | Trigger | Behavior |
|---|---|---|
| UserPromptSubmit | every prompt | If `plan.html` exists, read embedded JSON, inject 30-line summary wrapped in `===BEGIN PLAN DATA===` / `===END PLAN DATA===`. Verify SHA-256 if attested; block on tamper. |
| PreToolUse | Write\|Edit\|Bash\|Read\|Glob\|Grep | Same as UserPromptSubmit but tighter: just the active-phase JSON object. |
| PostToolUse | Write\|Edit | Nudge: "Update plan.html embedded JSON with what you just did." |
| Stop | always | Run check-complete script: if any phase status != "complete" and the user said /done, surface a warning. |
| PreCompact | * | "Compaction about to fire. Flush in-context progress into plan.html's JSON before it does. Plan-SHA256: <hash>." |

### Plan.html structure (single file)

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{plan-title}}</title>
  <style>/* inline CSS, no CDN, prefers-color-scheme aware */</style>
</head>
<body>
  <script type="application/json" id="plan-data">
  {
    "schema_version": "0.1.0",
    "plan_title": "...",
    "goal": "...",
    "current_phase": 1,
    "phases": [
      { "id": 1, "title": "...", "status": "in_progress", "items": [...], "milestones": [...] }
    ],
    "findings": [...],
    "progress_log": [...],
    "decisions": [...],
    "errors": [...]
  }
  </script>

  <header>...</header>
  <nav>tabs for Phases | Findings | Progress | Decisions | Errors</nav>
  <main id="root"></main>
  <footer>Copy-as-Markdown / Copy-as-JSON / Print / Attest</footer>

  <script>
    // vanilla JS reads JSON, renders panels
    // no framework, no build, ~200-400 lines per template
  </script>
</body>
</html>
```

### Description field (frontmatter, optimized for skill picker)

```yaml
name: plan-it
description: HTML-first persistent planning skill. Generates a single self-contained plan.html with interactive phases, drag-and-drop tickets, sliders, mockups, and embedded JSON state, survives /clear via session catchup, tamper-protected by SHA-256, mirrors across 17 IDEs. Use when asked to "plan it", "make me an HTML plan", "show me the plan", or when starting any multi-step task that needs a navigable artifact instead of a markdown wall.
user-invocable: true
allowed-tools: "Read Write Edit Bash Glob Grep WebFetch"
```

### Memetic trigger phrases (multiple, all valid)
- "plan it" / "plan-it" / "/plan"
- "make me an html plan"
- "show me the plan"
- "render plan"
- "open the plan in my browser"

## 5. Risks and mitigations

| Risk | Mitigation |
|---|---|
| HTML plan files become unwieldy (>2000 lines) | Hard rule: data layer ≤ 50KB JSON, render layer ≤ 400 lines JS. Reach state via multi-file mode (v0.2.0). |
| YAML frontmatter loader collision (pwf v2.38.1 bug) | Use `===` delimiters from day 1. Add YAML-load test in tests/ as a CI gate. |
| Skill description gets garbled in Claude Code skill picker | Lint description field against the `---` collision in pre-commit hook. |
| Templates look like AI slop | Anti-slop rules in skill body. Demo plan.html reviewed in browser before ship. Tasteful typography commitment (system serif headers + sans-serif body where appropriate). |
| Session catchup fails on Windows | Test matrix: Windows 11 PowerShell + Git Bash, Linux, macOS. Use known system Python paths (carry @xiaolai's PR #139 fix from pwf). |
| Markdown-loving users churn | Add `/plan-export markdown` command that flattens plan.html → task_plan.md. Optional compat layer with pwf. |
| Distribution: ClawHub still requires manual upload | Carry the protocol from pwf. Track v0.1.0 upload as a separate post-ship task. |
| 17 IDE mirrors drift | Parity-bumper + parity test from day 1 (pwf v2.37.0 lesson). |

## 6. Aesthetic stance (anti-slop opinion baked in)

The skill description forces an aesthetic stance BEFORE rendering. plan-it's stance:

> "plan-it plans look like an editorial dashboard, not a SaaS dashboard. Strong typographic hierarchy. One accent color, never gradients. Sharp corners (≤4px radius) or no radius. Mono for data, serif for headings, sans for body. Information density over whitespace inflation. Tables before cards. Sliders are 32px thumb, no shadow. Drag cards have 1px border, not box-shadow."

This stance ships INSIDE the SKILL.md so every rendered plan reflects it.

## 7. Open follow-ups (deferred to v0.2.0+)

- Translation of the 10 templates into ar/de/es/zh/zht (canonical EN ships first).
- Compose-mode with pwf: `/plan-it import task_plan.md`.
- here.now publish integration: `/plan-publish` → public URL.
- Team mode (multi-user CRDT-lite).
- Cline / Antigravity / Kilocode IDE adapters.
- MDX output mode.

## 8. Community-informed mitigations (from BG agent #2 sentiment scan)

The skeptic camp (~25% of community reaction) raised six concrete critiques. plan-it ships with explicit mitigations baked into v0.1.0 to neutralize each:

| Skeptic concern | plan-it mitigation |
|---|---|
| HTML 2-4× more tokens than Markdown | Token-accounting line in README. Templates target ≤30KB HTML + ≤50KB JSON. `/plan-export markdown` flattens at any moment. |
| "I want to hand-edit the source" (HN top critique) | **Bidirectional Markdown export** day 1. Plan-it round-trips: HTML ↔ Markdown. The JSON-in-script-tag data model means the edits happen on JSON, not on tags. |
| HTML diffs are noisy → "can't review = toy" | **JSON-only data diffs.** The plan state lives in `<script type="application/json" id="plan-data">`. Git diffs the JSON, not the rendering layer. PR reviewers see clean key-value changes. |
| Accessibility lapses in AI-generated HTML | **WCAG AA by default.** Every template ships ARIA labels, semantic landmarks (`<nav>`, `<main>`, `<aside>`), alt text on every SVG, focus order, prefers-reduced-motion respect, keyboard navigation. Accessibility tests in pytest enforce this. |
| Hosting friction for sharing HTML | Single-file offline. No CDN. No build step. Share via filesystem, email attachment, or `npx here.now publish plan.html` for instant URL. |
| AI-generated JS is over-engineering / security risk | Templates ship hand-written vanilla JS (no `eval`, no `Function()`, no remote loads). Total JS per template ≤ 400 lines, auditable by a human. |

## 9. Lineage

The only inherited project that materially shaped plan-it's architecture is **planning-with-files** (OthmanAdi). All credit consolidates there: hook lifecycle, session catchup, SHA-256 attestation, parity-locked version bumper, 17-IDE adapter distribution.

## 10. Approvals

- [x] Adi: New repo, plan-it, full MVP, single plan.html w/ embedded JSON (2026-05-19)
- [ ] Adi: Reviews this written spec (next step)
- [ ] Adi: Reviews demo plan.html in browser (definition-of-done item 1)
- [ ] Adi: Approves git initial commit
