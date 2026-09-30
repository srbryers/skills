---
name: visual-review
description: Two-layer visual gate for Storybook UI work. Pixel-diff baselines per story catch regressions, then Jev judges new or changed stories from extracted layout facts. Use when checking UI changes in a Storybook corpus for overlaps, clipped content, and off-center brand marks before merge.
compatibility: Layer 1 needs Storybook, pngjs, and pixelmatch in the project. The Jev judge needs the typesafe skill's credential helper and the custom.typesafe connector, which exist only on the hatch host.
---

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

Run these with the project's package manager (`pnpm` on Shopify machines):

```bash
pnpm run ui:visual            # full gate: render + diff, exits non-zero on fail
pnpm run ui:visual:update     # re-render baselines after intentional changes
```

Requires: `pngjs`, `pixelmatch` (`pnpm add -D pngjs pixelmatch`).

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
pnpm run ui:layout-facts              # all stories (~50s for 273)
pnpm run ui:layout-facts -- --changed # only stories the pixel gate flagged
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

## End-to-end entry point

`bin/semantic_review.py` — one command that runs the whole layer-2 flow across
both machines. It drives the Storybook host through a remote-execution helper
(default `~/workspace/bin/macstudio`; override with `--studio`). `--repo` names
the project checkout on the Studio, and `--pm` names its package manager
(`npm` or `pnpm`, default `npm`):

1. `<pm> run ui:visual` on the Studio (pixel gate, writes `report.json`).
2. Reads NEW/CHANGED story ids from the report.
3. `<pm> run ui:layout-facts -- --changed` on the Studio.
4. Fetches those facts files back to the agent host.
5. Runs the Jev judge on each.

```bash
bin/semantic_review.py --repo ~/Development/<project>                # full flow; exit 1 if any story needs REVIEW
bin/semantic_review.py --repo ~/Development/<project> --skip-visual  # reuse the latest pixel-gate report
bin/semantic_review.py --repo ~/Development/<project> --pm pnpm      # project uses pnpm
```

Exit 0 means no changed stories, or every changed story PASSed. Only the facts
JSONs cross machines — the TypeSafe credential never leaves the agent host.

## Wiring a new project

1. Copy `scripts/storybook_visual.cjs` and `scripts/storybook_layout_facts.cjs`
   into the project; add the `ui:visual` / `ui:layout-facts` package scripts.
2. Install this whole repo on the agent host. `jev_review.py` imports
   `../../typesafe/bin/jev.py` from beside itself for auth (same host, no
   credential copying), so the two skills must stay together.
3. Run `bin/semantic_review.py --repo <project>` (adjust `--studio` and `--pm`
   for your Storybook host).

## Known limits

- Light mode only; animations paused; one viewport (390x844).
- The judge reads text facts, not pixels — it can't see color, imagery quality,
  or motion. A screen can PASS and still look dull.
- Residual false-positive classes: decorative overlays the extractor can't
  classify (tooltips, absolutely-positioned flourishes). When the judge flags
  something odd, look at the story before the code.
- Calibrated 2026-09-30 on 273 Prelude stories: 1 real bug found
  (`prelude-transcript-review--long-reply` — long reply text overflows its
  card, verified in a screenshot and fixed), zero false positives in the
  deterministic layer after the scrollport-clamp fix (elements inside vertical
  scrollers report their visible rect, not their full content height). Do not
  fix flagged stories from the gate — report them.
