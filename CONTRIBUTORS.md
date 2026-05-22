# Contributors

## Lead

- **Ahmad Othman Ammar Adi** (@OthmanAdi), Author, maintainer, and release manager.

## Lineage

- **planning-with-files** (OthmanAdi), The markdown-era predecessor. plan-it inherits its hook lifecycle, session catchup, SHA-256 attestation, parity-locked version bumper, and 17-IDE adapter distribution.

## Reporters

- **@fxy413** (issue #3, v0.1.1). Identified that a literal `</script>` substring inside a JavaScript comment was terminating the embedded script block in HTML raw-text mode, dropping all tab-switching and event-listener code in every generated `plan.html`. Provided a working repro, a correct root cause, and a usable patch.

## How to contribute

- Open an issue first to discuss; PRs from drive-by commits without prior discussion get triaged but may not merge if scope creep is unclear.
- Public-facing prose tone: sachlich, no em-dashes. Run through `/humanizer` before posting.
- Author of commits is `OthmanAdi` only. Contributors are credited here and in `CHANGELOG.md` Thanks section, not via `Co-Authored-By` trailers.
- One squashed commit per release.
- Tests must pass: `python -m pytest tests/ -q`.

Thank you for your interest.
