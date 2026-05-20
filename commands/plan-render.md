---
description: Open the active plan.html in the default browser.
---

# /plan-render

Open `plan.html` (or `.planning/<active-plan>/plan.html`) in your default browser.

## Usage

```
/plan-render
```

## Behavior

The skill calls `scripts/render-plan.sh` (or `.ps1` on Windows). It resolves the active plan via:

1. `PLAN_ID` env var → `.planning/<PLAN_ID>/plan.html`
2. `.planning/.active_plan` file → `.planning/<slug>/plan.html`
3. Legacy `./plan.html`

On Linux: uses `xdg-open` or `wslview`. On macOS: `open`. On Windows: `Start-Process`.

If no plan.html is found, surfaces a hint to run `/plan` first.
