---
description: Compose with Claude Code's /loop primitive. Default 10-minute tick re-reads the plan and runs check-complete.
---

# /plan-loop

Add a cadence on top of the active plan. Re-reads `plan.html` every tick, runs check-complete, appends a `progress_log` entry if no change since the last tick.

## Usage

```
/plan-loop                 # default 10-minute tick
/plan-loop 5m              # custom interval
/plan-loop 30m "custom prompt for each tick"
```

## Behavior

Composes with Claude Code's `/loop` primitive (v2.1.72+). On every tick the skill:

1. Reads `plan.html` embedded JSON.
2. Runs `scripts/plan-hook.py check-complete` to surface incomplete phases.
3. If no progress_log entry since the last tick, nudges the agent to add one (or close the loop).
4. Re-injects active-phase summary into the context.

Compose with `/plan-goal` to add a termination condition: the loop keeps running until /goal evaluates true.

## Template

The bare `/loop` command reads `./.claude/loop.md` (project) or `~/.claude/loop.md` (user). plan-it ships a `templates/loop.md` that's planning-aware so even a naive `/loop` invocation will respect the active plan. Copy it into one of the two paths once; not auto-wired.
