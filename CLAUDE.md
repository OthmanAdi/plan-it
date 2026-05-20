# plan-it: Claude working rules

## Core preservation (locked 2026-05-20)
- `plan.html` is user-owned. NEVER edit it directly. All updates go through the embedded JSON data layer via `scripts/init-plan` or in-browser controls.
- The `<script type="application/json" id="plan-data">` block is the single source of truth. The render layer is derived.
- Plan-injection delimiter is `===BEGIN PLAN DATA===` / `===END PLAN DATA===`. NEVER `---` (collides with YAML doc-separator and breaks Claude Code's skill-discovery loader, per planning-with-files v2.38.1 incident).
- SHA-256 attestation lives at `./.plan-attestation` (legacy) or `.planning/<slug>/.attestation` (parallel-plan mode).
- Hooks must be silent (exit 0) when `plan.html` is absent. Skill must compose, not collide.

## Release discipline
- Every release: update 14 SKILL.md variants + `plugin.json` + `marketplace.json` + `CITATION.cff` via `scripts/bump-version.py`. Parity test gates the build.
- One squashed commit per release, Conventional Commits format.
- Author: OthmanAdi only. NEVER add Co-Authored-By trailers. Contributors credited in CHANGELOG Thanks + CONTRIBUTORS.md.
- Run public-facing prose through `/humanizer`. No em-dashes. Sachlich tone.

## File modification rules
- `plan.html` — DO NOT EDIT directly, ever.
- `task_plan.md` (when running plan-it on plan-it itself) — DO NOT EDIT directly.
- `findings.md` — append only, under appropriate `## ` section.
- `progress.md` — append at end with timestamp.
- `docs/specs/*.md` — write once, update only on explicit user approval.

## Test discipline
- `python -m pytest tests/ -q` is the gate. All v0.1.0 work must land green.
- Accessibility tests are non-optional. Every template must pass WCAG AA + ARIA + keyboard-nav assertions.
- Parity test fails the build on any version drift across the 19-file parity set.

## Skill design rules (per Thariq's 9 tips)
1. Description field is for the model, not for users. Optimize for trigger.
2. Build a Gotchas section. Highest-signal content.
3. Don't railroad Claude. Goals + constraints, not step-by-step prescriptions.
4. Scripts ship pre-written. Claude composes, doesn't reinvent.
5. Hooks only fire when active plan exists. No collisions.

## Aesthetic stance (anti-slop, baked in)
- Editorial dashboard, not SaaS dashboard.
- Strong typographic hierarchy.
- One accent color, never gradients.
- Sharp corners (≤4px radius) or no radius.
- Mono for data, serif optional for headings, sans for body.
- Information density over whitespace inflation.
- Tables before cards.
- Sliders: 32px thumb, no shadow.
- Drag cards: 1px border, not box-shadow.

## Token-cost honesty
plan-it HTML output is roughly 2-3× the token cost of equivalent Markdown. With Opus 4.7's 1M context, this is negligible in practice. If you need lower-cost output for chained agents or git-committed specs, run `/plan-export markdown`.

## References
- Industry-shift thesis: research/01-anthropic-blog-html-thesis.md (mirror in `Documents/html-planning-skill/research/`)
- Community sentiment: research/07-bg-agent-community-sentiment.md
- Anthropic official patterns: research/08-bg-agent-anthropic-official-skills.md
- Markdown predecessor: OthmanAdi/planning-with-files.
