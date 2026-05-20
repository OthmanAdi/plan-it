# Launch comms — drafts for the v0.1.0 push (paste-ready)

Sachlich tone, no em-dashes, no hype. Run each through `/humanizer` before posting if you want the extra layer.

---

## 1. Reply to Thariq's launch tweet

Tweet ID: 2052811606032269638 ("HTML is the new markdown. I've stopped writing markdown files for almost everything...")

Draft reply:

```
Built plan-it on top of your essay. Single plan.html, embedded JSON, survives /clear, SHA-256 attested, 10 templates across the 9 categories from your gallery, mirrors to 17 IDEs day 1.

https://github.com/OthmanAdi/plan-it

Thank you for the format.
```

Why this works:
- Names the build concretely
- Cites his gallery (signals you actually read it)
- One link, no hype
- Sachlich gratitude line, no fawning

---

## 2. Hacker News submission

Title (under 80 chars):

```
Plan-it: an HTML-first persistent planning skill for Claude Code
```

If the HN thread on Thariq's essay is still active (item 48071940), post there instead as a reply, not a new submission. Lower-noise discoverability.

If posting as new submission, leave the body empty (HN convention for project links). The README does the work.

---

## 3. X / LinkedIn post (your own profile)

```
plan-it v0.1.0 is out.

HTML-first planning. Single self-contained plan.html with phases, drag-cards, sliders, mockups, embedded JSON state. Survives /clear. Tamper-protected by SHA-256. Mirrors across 17 IDEs.

Built in the publication window of Thariq Shihipar's "Unreasonable Effectiveness of HTML." Operationalises his 9-category gallery as a persistent toolkit.

10 templates. 120 tests. MIT.

https://github.com/OthmanAdi/plan-it
```

---

## 4. ClawHub manual upload (the only manual step left)

1. Open https://clawhub.io (SSL cert is expired, click through the warning).
2. Sign in.
3. Find the plan-it skill listing (or create it if first time).
4. Upload the contents of `clawhub-upload/SKILL.md` plus the scripts and templates in that folder.
5. Set version to `0.1.0`.
6. Publish.

The directory `clawhub-upload/` is byte-identical to the canonical, already at 0.1.0.

---

## 5. Cross-promotion thread for your existing pwf community

Inside `OthmanAdi/planning-with-files`:

- Open a Discussion in the "Announcements" category.
- Title: "plan-it v0.1.0 is out — the HTML-first sibling for the post-Thariq era"
- Body: link the new repo. Note explicitly that pwf v2.38.1 continues to ship, no breaking changes, and `/plan-export markdown` makes plan-it round-trip with pwf's exact file shape. Invite users who want the markdown experience to stay on pwf; users who want the HTML experience to try plan-it.

This is the "no orphans" move. Your 21k pwf users feel acknowledged, not abandoned.

---

## 6. CHANGELOG note on planning-with-files

In the next pwf release (whenever it happens), add a one-line entry:

```
- HTML-first sibling skill released: plan-it (github.com/OthmanAdi/plan-it). Use /plan-export markdown to round-trip plan.html into the pwf three-file shape.
```

Sets the relationship in the canonical pwf history.

---

## Sequence

If you only do one thing: post the Thariq reply. That's the single highest-signal move (you ride the wave he started, in-thread, in the same publication window).

If you do three: Thariq reply, then HN comment in the existing thread, then ClawHub upload.

If you do all six: Thariq, HN, your X post, your LinkedIn post (same copy as X), ClawHub, pwf discussion. Spread over 24 hours, not all at once.
