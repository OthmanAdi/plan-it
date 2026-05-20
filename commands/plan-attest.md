---
description: Compute a SHA-256 attestation of the active plan.html and lock it against tampering.
---

# /plan-attest

Cryptographically lock the active plan. After this, any byte change to `plan.html` will block injection until you re-attest.

## Usage

```
/plan-attest             # compute and store
/plan-attest --show      # print the stored hash
/plan-attest --clear     # remove the attestation (returns to pre-lock behavior)
```

## Behavior

`scripts/attest-plan.sh` (or `.ps1`) computes a SHA-256 of `plan.html` and writes it to:

- `./.plan-attestation` (legacy single-plan mode)
- `./.planning/<active-plan>/.attestation` (parallel-plan mode)

The skill's hooks recompute the hash on every UserPromptSubmit / PreToolUse fire. On mismatch they emit `[PLAN TAMPERED — injection blocked]` with expected/actual hashes and a hint to run `/plan-attest` to re-approve.

Run `/plan-attest --clear` after legitimate edits, then re-run `/plan-attest` to lock the new state.

## When to attest

- After finalizing a phase definition.
- Before handing the plan off to a teammate or to the shipping pipeline.
- After running `/plan-export markdown` if you want round-trip integrity.
