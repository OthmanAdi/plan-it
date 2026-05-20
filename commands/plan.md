---
description: Create a new plan.html from a template, or interactively pick one.
---

# /plan

Scaffold a new `plan.html` in the current directory.

## Usage

```
/plan                              # interactive template picker
/plan implementation-plan          # use a named template
/plan ticket-triage --slug refactor-auth   # parallel-plan mode under .planning/refactor-auth/
```

## Templates

- `implementation-plan` — phases + mockups + data-flow + risks (this is the default)
- `three-approaches` — side-by-side approach comparison
- `ticket-triage` — drag-and-drop Now/Next/Later/Cut board
- `feature-flag-editor` — grouped toggles with dependency warnings
- `module-map` — boxes + arrows code architecture
- `annotated-pr` — diff with margin annotations + severity
- `living-design-system` — color/type/spacing/component variants
- `animation-sandbox` — sliders for duration + easing
- `weekly-status` — shipping/slipping/blocked + sparkline
- `incident-timeline` — minute-by-minute post-mortem

## Behavior

The skill calls `scripts/init-plan.sh` (or `.ps1` on Windows). After scaffolding, run `/plan-render` to open the result in your browser. Optionally run `/plan-attest` to lock the plan with SHA-256.

The data layer lives in `<script type="application/json" id="plan-data">` inside `plan.html`. Always update that JSON block, never the render layer below it.
