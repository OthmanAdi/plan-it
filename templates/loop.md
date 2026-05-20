You are running inside Claude Code's /loop primitive. A plan-it `plan.html` may exist in this directory.

On every tick:

1. Check if `plan.html` exists (or `.planning/<active>/plan.html`).
2. If yes: read the embedded JSON, identify the active phase, check whether anything new has happened since the last tick.
3. If new work happened: append a `progress_log` entry with timestamp, phase id, action summary, and files touched.
4. If no work happened: surface a single-line nudge identifying what the active phase is waiting on.
5. If the active phase is complete: bump `current_phase`, set status, move on.
6. If all phases are complete: exit the loop cleanly.

Do not write code without a phase context. Do not modify `plan.html` directly — only the JSON block inside it.

Token-honest: keep tick output ≤ 200 tokens.
