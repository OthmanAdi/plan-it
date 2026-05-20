# Examples

This directory contains plan-it demonstration artifacts.

## demo-plan.html

A real plan-it plan that captures plan-it's own build journey. Open it in your browser to see the skill in action.

```bash
# from repo root
bash scripts/render-plan.sh           # if you scaffold a new plan first
# OR open the demo directly:
xdg-open examples/demo-plan.html        # Linux
open examples/demo-plan.html            # macOS
start examples/demo-plan.html           # Windows (cmd)
Invoke-Item examples/demo-plan.html     # Windows (PowerShell)
```

Things to try:
- Click the **Phases** tab. Toggle a checkbox. Notice the line strikes through.
- Click **Copy as Markdown** -- check your clipboard, paste somewhere.
- Click **Copy as JSON** -- the full plan-data object is on your clipboard.
- Switch tabs with `ArrowLeft` / `ArrowRight`.
- Try the page in dark mode (OS-level dark theme). The whole template re-themes via `prefers-color-scheme`.
- Read the JSON in your text editor (view-source the file, scroll to the `<script type="application/json" id="plan-data">` block). That JSON is the canonical state.

## Building your own

```
/plan implementation-plan         # scaffold a fresh plan.html from template
/plan-render                       # open in browser
/plan-attest                       # lock it with SHA-256
/plan-export markdown              # round-trip to task_plan.md + findings.md + progress.md
```
