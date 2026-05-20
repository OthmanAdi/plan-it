# Installation

## Claude Code (recommended)

Two ways:

### Via marketplace
```
/plugin marketplace add OthmanAdi/plan-it
/plugin install plan-it@plan-it
```

After install, restart Claude Code to activate the hooks.

### Via npx skills
```
npx skills add OthmanAdi/plan-it
```

The installer places `plan-it` into `~/.claude/skills/plan-it/` (a junction on Windows, a symlink on POSIX).

## Cursor

```
npx skills add OthmanAdi/plan-it
```

Cursor reads `~/.cursor/skills/`. If your install path differs, symlink manually:
```
ln -s <repo-clone>/.cursor/skills/plan-it ~/.cursor/skills/plan-it
```

## Codex

```
npx skills add OthmanAdi/plan-it
```

Codex reads `~/.codex/skills/`. Hooks are wired via the bundled `.codex/hooks.json` (auto-loaded).

## Other IDEs

| IDE | Path | Notes |
|---|---|---|
| GitHub Copilot | `.github/copilot/skills/plan-it/` | Hooks per Copilot Hooks spec |
| Mastra Code | `~/.mastracode/skills/plan-it/` | Hooks per Mastra config |
| Gemini CLI | `~/.gemini/skills/plan-it/` | Skills + hooks |
| Kiro | `~/.kiro/skills/plan-it/` | Agent Skills layout |
| Hermes | `~/.hermes/skills/plan-it/` | Project plugin |
| Factory Droid | `~/.factory/skills/plan-it/` | Skills + hooks |
| OpenCode | `~/.opencode/skills/plan-it/` | Uses SQLite session storage |
| CodeBuddy | `~/.codebuddy/skills/plan-it/` | Skills + hooks |
| Continue | `~/.continue/skills/plan-it/` | Continue skills + .prompt |
| Pi Agent | `~/.pi/skills/plan-it/` | npm @mariozechner/pi-coding-agent |
| OpenClaw | `~/.openclaw/skills/plan-it/` | docs.openclaw.ai/tools/skills |
| Antigravity | `~/.agent/skills/plan-it/` | codelabs.developers.google.com/getting-started-with-antigravity-skills |
| Kilocode | `~/.kilocode/skills/plan-it/` | kilo.ai/docs/agent-behavior/skills |
| AdaL CLI | `~/.adal/skills/plan-it/` | docs.sylph.ai/features/plugins-and-skills |

## Manual install

```
git clone https://github.com/OthmanAdi/plan-it ~/plan-it
ln -s ~/plan-it/skills/plan-it ~/.claude/skills/plan-it
```

## Verify install

```
python -m pytest tests/ -q
```

You should see 20+ tests pass. If any fail, open an issue with the test output.

## ClawHub

After install via plugin marketplace or npx, plan-it is also reachable via the [ClawHub](https://clawhub.io) skill directory. The SSL certificate on clawhub.io is expired, click through the browser warning.
