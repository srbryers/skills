# visual-review

Two-layer visual gate for UI work: cheap pixel-diff screenshot baselines catch
regressions on every story, then Jev judges new/changed screens semantically
from extracted layout facts. Built for the Prelude Storybook corpus, designed
to port anywhere.

## Why two layers

The pixel gate is fast and catches *changed* pixels, but it can't tell a good
change from a bad one, and it never looks at a brand-new story with judgment.
The Jev layer only runs on new/changed stories and answers one question:
"does this layout look right?" — centered, no overlaps, nothing clipped,
sensible spacing and hierarchy.

## Layer 1 — pixel diff (runs on the machine hosting Storybook)

`scripts/storybook_visual.cjs` — renders every story at 390x844, light mode,
animations paused, and diffs against `baselines/`. Per-story threshold
(0.1%, min 25px) plus a global cap. Output: `.storybook/visual-diffs/report.json`
with `added` / `removed` / `changed` story lists.

```bash
npm run ui:visual            # full gate: render + diff, exits non-zero on fail
npm run ui:visual:update     # re-render baselines after intentional changes
```

Requires: `pngjs`, `pixelmatch` (`npm i -D pngjs pixelmatch`).

## Layer 2 — Jev semantic judge (runs where the TypeSafe credential lives)

Facts extraction must run next to Storybook (it drives a real browser); the
judge must run on the agent host, because the TypeSafe credential surrogate
(`custom.typesafe`) exists only there. Never copy credential material to the
Storybook machine — only the facts JSONs travel back.

### 2a. Extract layout facts (Storybook machine)

`scripts/storybook_layout_facts.cjs` — for each story, walks the rendered DOM
and writes `.storybook/layout-facts/<story-id>.json`:

- Up to 60 visible elements in reading order: kind (text/image/button/input),
  label, geometry (x/y/w/h, center), font size, bold, alignment, line count.
- Deterministic geometry: `overlaps` (pairwise, skips containment and the
  scroll-indicator pattern), `clipped` (past viewport edges, text wider than
  its box), `gaps` (vertical rhythm between consecutive elements).
- Deliberate non-issues are filtered in code, not left to the judge:
  below-fold content on scrolling screens, ellipsis truncation (`numberOfLines`),
  content past the right edge inside horizontal scrollers, badge-on-icon style
  containment.

```bash
npm run ui:layout-facts              # all stories (~50s for 273)
npm run ui:layout-facts -- --changed # only stories the pixel gate flagged
```

### 2b. Judge the facts (agent host)

`bin/jev_review.py` — one Jev call per story, five `noul` questions:

| question | framing | strict? |
|---|---|---|
| `no_overlapping_elements` | "there are NO overlapping elements" | yes — blocks on uncertainty |
| `no_clipped_content` | "NO content is clipped" | yes |
| `brand_or_logo_centered` | "the brand mark IS centered" (only when a logo/wordmark is present) | yes |
| `spacing_mistake` | "there IS a spacing mistake" | advisory — reported, never blocks |
| `hierarchy_problem` | "there IS a hierarchy problem" | advisory |

Verdicts: `PASS` (no strict question failed) or `REVIEW` with the failed
questions listed. Overlap/clip facts are stated as authoritative in the prompt
("computed exactly by code — trust them"), so the judge is decisive on
mechanical defects; spacing/hierarchy stay advisory because the text-only
judge is honest about its uncertainty on aesthetics.

```bash
bin/jev_review.py --dir .storybook/layout-facts
bin/jev_review.py --dir <dir> --json   # machine-readable
bin/jev_review.py <file>...            # specific stories
```

## Wiring a new project

1. Copy `scripts/storybook_visual.cjs` and `scripts/storybook_layout_facts.cjs`
   into the project; add the `ui:visual` / `ui:layout-facts` npm scripts.
2. Copy this skill's `bin/jev_review.py` to the agent host (it imports the
   `typesafe` skill's `bin/jev.py` for auth — see the `JEV_IMPORT` fallback
   chain at the top of the file).
3. Run layer 1, extract facts for `--changed`, fetch the JSONs, run the judge.

## Known limits

- Light mode only; animations paused; one viewport (390x844).
- The judge reads text facts, not pixels — it can't see color, imagery quality,
  or motion. A screen can PASS and still look dull.
- Residual false-positive classes: decorative overlays the extractor can't
  classify (tooltips, absolutely-positioned flourishes). When the judge flags
  something odd, look at the story before the code.
- Calibrated 2026-09-30 on 273 Prelude stories: 1 real bug found
  (`prelude-transcript-review--long-reply` — long reply text overflows its
  card, verified in a screenshot), zero false positives in the deterministic
  layer. Do not fix flagged stories from the gate — report them.
