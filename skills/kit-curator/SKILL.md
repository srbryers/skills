---
name: "kit_curator"
description: "Run the Agentic UI Kit promotion gate on a Prelude UI PR - contract, stories, dual-theme baselines, independent review, adoption check. Use whenever feature work adds or changes a component, primitive, or design token."
---

# Kit Curator

## Purpose
Keep the Agentic UI Kit growing in step with feature work. New primitives enter the kit in the same PR that invents them, reviewed by someone other than the author, so `component-review.json` never goes stale unnoticed.

## Workflow
1. Work in the branch's worktree on the Mac Studio (`~/Development/prelude-social-skills-coach` or its `~/Development/wt-*` worktrees).
2. Diff the branch and list every added or changed reusable primitive or token: components in `components/`, contracts (`*.contract.ts`), and token files such as `constants/motion.ts`.
3. For each one, confirm the kit absorbed it in this PR: component, `.contract.ts` where the pattern applies, Storybook stories covering its states, and visual baselines in both light and dark themes. Raw native controls in feature code are a finding, not a shortcut.
4. Review motion explicitly: loading, typing, streaming, pending, message and screen transitions, height and width changes, and the reduced-motion variant of each. A state with no motion story is a gap.
5. Refresh the review entries in `docs/design/screen-inventory/component-review.json`: current `sourceSha256`, story file hashes and states, a one-line responsibility, and an `evidence` list pointing at the test, stories, and review note.
6. The reviewer is never the author. The builder writes `authors`; Roman (or another independent agent) is the `reviewer`. Sebastian's taste check is a separate gate and is not replaced by this review.
7. Write the review note under `docs/design/kit-review-<date>/` in the branch, then run `npm run ui:inventory` if inventory may drift and `node scripts/check_screen_adoption.cjs --check`.

## Output Contract
Report: primitives and tokens touched; for each, contract status, story coverage (including motion and reduced-motion states), baseline coverage (light and dark); reviewer assigned per entry; adoption check result; and either "kit gate green" or the exact list of missing pieces blocking it.

## Operating Rules
- Gate passes only at zero adoption errors and zero stale entries. A red check means the PR is not merge-ready, whatever the code does.
- Never refresh a hash you have not reviewed. Reading the component and its diff is the review; paperwork without reading is how stale entries happen.
- Hash-only churn from a shared story file may be refreshed across entries, but say so in the review note.
- Known limits (web-only no-ops, single-screen adoption, baselines that only protect local runs) go in the PR description, not in a chat aside.
