# Anti-slop rules

plan-it templates ship with an explicit aesthetic stance. The goal is editorial dashboards, not SaaS dashboards. Frontend-design (Anthropic, 277k installs) earned its lead because it forces an opinion before any CSS gets written; plan-it carries the same discipline.

## Don't

- **Centered everything.** Anchor content to a left rail when there is structural hierarchy. Centering implies equal weight. Plans have unequal weight.
- **Purple gradients.** No `linear-gradient(135deg, #6366f1, #8b5cf6)`. Use a single accent color or none.
- **Uniform rounded corners.** `border-radius: 8px` on every element is the look of generated UI. Use 0px or ≤4px and stay consistent within a region.
- **Inter font.** It is the default of "I did not pick a font." Use `system-ui` for body, `ui-serif` for headings if you want serif contrast, `ui-monospace` for data. That is the entire palette.
- **Excess whitespace.** Information density first. Vertical rhythm is achieved with 1.5× line-height, not with 64px gaps.
- **Card-everything.** A card is a box with a shadow that obscures the table inside it. Use tables when you have rows of structured data. Use cards only when items are heterogeneous.
- **Drop-shadow as the only depth signal.** Use borders. Use color. Reserve shadows for popovers and modals.
- **Animated counters and progress rings as decoration.** Animate when the change is informative (a state transition the user caused). Do not animate for charm.
- **Emoji bullets in agent outputs.** Templates avoid them. Use `•` or `—` or a typeset bullet.

## Do

- **One accent color.** Used sparingly. For severity, status, and selection states.
- **Sharp corners.** 0px or 2px or 4px. Never 16px on a primary surface.
- **Mono for data, sans for body, serif optional for headings.** That is the whole type system.
- **Strong typographic hierarchy.** `h1` is bigger than `h2` is bigger than `h3` is bigger than body. Do not collapse all headings to "12px bold uppercase".
- **Tables before cards.** Tables are dense, scannable, sortable. Cards are sparse, picturesque, slow.
- **Density over whitespace inflation.** 1.5× line-height, 12-16px between sections, tables get internal padding not external margins.
- **Inline SVG for diagrams.** No `<img src="diagram.png">`. Inline SVG is text, version-controllable, accessible, themeable via `currentColor`.
- **prefers-color-scheme aware.** Dark + light without a theme picker. Browsers know.
- **Keyboard-first.** Tab order, focus-visible outlines, ARIA labels. Templates should be usable without a mouse.
- **prefers-reduced-motion respected.** If the user opts out of motion, sliders still work but transitions are instant.

## When you are tempted

- "It feels empty" → add a sentence of editorial context, not a card.
- "It looks like a table" → that's the point.
- "It needs a hero image" → it does not.
- "I want to use a Google Font" → no.
- "Let me add an accent color or two" → one.

The aesthetic is **deliberately spare**. It is recognisable. It reads as plan-it.
