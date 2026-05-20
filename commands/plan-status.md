---
description: Print a one-line status of the active plan to the terminal.
---

# /plan-status

Print a compact status line. Useful inside `/loop` or as a cheap pre-decision check.

## Usage

```
/plan-status
```

## Output shape

```
plan-it: <plan-title> · template=<name> · phase=<current_phase>/<total> · status=<active-phase-status> · sha=<short-hash-or-unattested>
```

Example:

```
plan-it: Replace auth middleware · template=implementation-plan · phase=2/4 · status=in_progress · sha=8f4a..
```

## Behavior

Calls `scripts/plan-hook.py status` (subcommand reads the JSON, prints one line). Designed to be cheap (no full injection); does not run SHA-256 unless an attestation is present.
