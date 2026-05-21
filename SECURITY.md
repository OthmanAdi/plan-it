# Security

Threat model, trust boundaries, and mitigations for plan-it. Reviewed against the Gen Agent Trust Hub audit (2026-05-20) findings on data exfiltration, command execution, and prompt injection.

## Scope of this document

plan-it is an agent skill that runs inside Claude Code, Cursor, Codex, and 14 other IDEs. The skill ships:

- `plan.html`: a single-file artifact in the user's project directory, owned by the user.
- `scripts/`: helper scripts the SKILL.md hooks invoke.
- `templates/`: HTML templates seeded into new `plan.html` files.
- Lifecycle hooks declared in `SKILL.md` that fire on UserPromptSubmit, PreToolUse, PostToolUse, Stop, and PreCompact.

The trust boundary is the user's machine. Nothing in plan-it makes a network call. No data leaves the host.

## Findings vs reality

### Finding: DATA_EXFILTRATION (`scripts/session-catchup.py`)

**What the audit observed.** The script touches `~/.claude/projects/`, `~/.codex/sessions/`, and `~/.local/share/opencode/opencode.db`. The audit classified this as exfiltration.

**Reality.** No network calls exist anywhere in the codebase. Access is strictly local and strictly read. Specifically:

| Source | Access | Data extracted |
|---|---|---|
| `~/.claude/projects/<slug>/*.jsonl` | `stat()` only | filename + mtime |
| `~/.local/share/opencode/opencode.db` | SQLite `mode=ro` | one SELECT for `id, time_created` from `session` rows matching the current `cwd` |
| `~/.codex/sessions/*.json` | up to 256 KB read of the 10 most recent files | only the value of the top-level `cwd` field |

Output is a small textual report printed to stdout: which IDE has a session for this directory and how many minutes ago it was last touched. No conversation content, no message bodies, no tokens, no secrets.

**Mitigations in this release.**

- Codex case capped at 256 KB per file (`CODEX_READ_CAP`) so large session files cannot bloat the agent context.
- Codex case capped at the 10 most recent files.
- Opt-out: set `PLANIT_NO_HISTORY=1` in the environment, or pass `--no-history` to the script. plan-it then exits 0 with no session reads.
- Module docstring documents every path accessed and why.

### Finding: COMMAND_EXECUTION (SKILL.md hooks)

**What the audit observed.** SKILL.md declares five lifecycle hooks (`UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `PreCompact`). Each hook body runs bash plus Python.

**Reality.** Lifecycle hooks are the contract Claude Code and the other host IDEs provide. plan-it uses them as designed:

- Every hook body begins with `if [ -f plan.html ]; then ... fi`. No `plan.html`, no execution path.
- The only Python script the hooks invoke is `scripts/plan-hook.py`. Path resolution prefers `${CLAUDE_PLUGIN_ROOT}`, falls back to two well-known install locations. No user-input-derived path construction.
- No hook composes a shell command from plan.html content or from user prompt content.
- All hooks exit 0 unconditionally.

**Trust boundary.** An attacker who can write to your SKILL.md or `~/.claude/skills/plan-it/scripts/` already has filesystem write access and the host IDE's hook execution privileges. plan-it does not widen that boundary.

**Disable plan-it hooks.** Remove or comment out the `hooks:` block from `skills/plan-it/SKILL.md`. The skill body and the `/plan` command still work; only the auto-injection on prompt submit and the active-phase reminders go quiet.

### Finding: PROMPT_INJECTION (`scripts/plan-hook.py`)

**What the audit observed.** `plan-hook.py inject` reads strings from `plan.html`'s embedded JSON block and prints them inside `===BEGIN PLAN DATA===` / `===END PLAN DATA===` markers. The agent later sees this output. SHA-256 attestation exists but is opt-in; the script "does not perform strict sanitization of the content."

**Reality.** This was a real hole. A plan author who could write `===END PLAN DATA===` into `plan_title` (or any item text, decision rationale, or progress action) could close the bracketing marker early and append fresh instructions to the agent. The current release patches this in `_sanitize()`:

- ANSI escape sequences stripped (`\x1b[...m` etc).
- Control characters dropped, except tab and newline.
- Single-line fields fold `\r` and `\n` to spaces.
- Any literal occurrence of `===BEGIN PLAN DATA===` or `===END PLAN DATA===` (case-insensitive, three-or-more equals signs) is rewritten to `___BEGIN PLAN DATA___` / `___END PLAN DATA___`. The marker can no longer match the agent-side bracket parser.
- Every emitted string passes a length cap (200 chars for titles and item text, 400 for goal, 80 for template, 11 for status, 40 for timestamps).

Defense in depth still in place:

- The leading line of the injected block explicitly tells the agent to treat the content as data, not instructions.
- SHA-256 attestation (`/plan-attest`) blocks injection on tamper if the user opts in.
- Hook injects a summary of the active phase, never the full plan.

## Capabilities the skill requests

`allowed-tools` in SKILL.md: `Read Write Edit Bash Glob Grep WebFetch`. WebFetch is included so the agent can pull referenced URLs while planning (research links in a goal description, for example). WebFetch never originates from plan-hook.py or any other plan-it script; only the agent itself can invoke it, and only if the user prompts it to.

## Reporting

Security issues: open a GitHub issue at https://github.com/OthmanAdi/plan-it/issues with the `security` label, or email the address listed in `CITATION.cff`. Please do not file public issues for actively exploitable vulnerabilities; coordinate disclosure first.
