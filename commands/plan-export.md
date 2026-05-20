---
description: Flatten plan.html embedded JSON to Markdown or JSON file for chained-agent use or version control.
---

# /plan-export

Round-trip the active plan out of HTML and into a flat format. Mitigates the "I want to hand-edit" critique.

## Usage

```
/plan-export markdown        # writes task_plan.md + findings.md + progress.md (planning-with-files compatible)
/plan-export markdown --single   # single combined plan.md
/plan-export markdown --stdout   # print to stdout
/plan-export json            # writes plan.json with just the data block
```

## Behavior

Calls `scripts/export-markdown.py`. Parses the `<script type="application/json" id="plan-data">` block out of `plan.html` and renders it into the requested format:

- **markdown** mode produces planning-with-files compatible files (task_plan.md / findings.md / progress.md) so an existing pwf workflow can pick up the plan.
- **json** mode produces a clean plan.json suitable for jq pipelines, CI artifacts, or feeding to a different agent.

## Round-trip

After hand-editing the exported Markdown, you can re-import via `/plan import task_plan.md` in v0.2.0+. For v0.1.0 the round-trip is one-way (HTML → Markdown); re-importing requires regenerating plan.html from the template and copying the JSON back manually.
