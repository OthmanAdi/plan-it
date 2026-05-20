---
description: Compose with Claude Code's /goal primitive. Derives a termination condition from the active plan.
---

# /plan-goal

Hand the active plan's completion criterion to Claude Code's `/goal` (v2.1.139+, May 2026).

## Usage

```
/plan-goal
```

## Behavior

Reads the JSON block in `plan.html`, computes a goal condition like:

```
all phases in plan.html report status: complete (and current_phase == phases.length).
```

Then surfaces it to the user as a `/goal "..."` line they can paste, or directly invokes `/goal` if the runtime exposes the primitive to skills (Claude Code v2.1.139+).

The agent will then keep working until the plan-file is genuinely done, not just when the conversation looks done. Compose with `/plan-loop` to add a cadence on top.
