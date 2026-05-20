# Quickstart

## In 60 seconds

```
/plan implementation-plan
/plan-render
```

That's it. You now have `plan.html` in your cwd; the browser is open; the hooks are active.

## Three minutes deeper

1. Open `plan.html` in your editor. Look at the `<script type="application/json" id="plan-data">` block. Everything is there. The HTML below it is just the renderer.
2. Edit the JSON: change `plan_title`, add a phase, mark an item done.
3. Refresh the browser. Your changes show up.
4. Run `/plan-attest`. The skill computes a SHA-256, writes it to `.plan-attestation`. From now on the skill blocks injection if `plan.html` is tampered with.
5. Run `/plan-export markdown`. You get `task_plan.md`, `findings.md`, `progress.md` — same shape as planning-with-files. Hand-edit if you want.

## Pick the right template

- **Building something new?** `/plan implementation-plan`
- **Comparing options?** `/plan three-approaches`
- **Triaging tickets?** `/plan ticket-triage`
- **Editing feature flags?** `/plan feature-flag-editor`
- **Mapping unknown code?** `/plan module-map`
- **Reviewing a PR?** `/plan annotated-pr`
- **Designing a system?** `/plan living-design-system`
- **Tuning an animation?** `/plan animation-sandbox`
- **Writing a weekly status?** `/plan weekly-status`
- **Post-morteming an incident?** `/plan incident-timeline`

## Parallel plans

Working on two things in the same project? Use slug mode:

```
/plan implementation-plan --slug auth-rewrite
/plan ticket-triage --slug release-1.2
```

This puts plans under `.planning/auth-rewrite/plan.html` and `.planning/release-1.2/plan.html`. Switch active plan with `export PLAN_ID=auth-rewrite` (POSIX) or `$env:PLAN_ID = 'auth-rewrite'` (Windows).

## Compose with /goal and /loop

```
/plan implementation-plan
/plan-goal           # installs a termination condition: agent keeps going until all phases complete
/plan-loop 10m       # tick every 10 minutes; re-read plan, run check-complete
```

Now you have a planning skill, a termination criterion, and a cadence. Walk away, come back, the plan is further done.
