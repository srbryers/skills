---
name: "kit_curator"
description: "Run the Agentic UI Kit promotion gate on a UI PR in any kit repo (Prelude, Flora Studio, ui-kit, Wedding): contract, stories, dual-theme baselines, independent review, inventory check. Use whenever feature work adds or changes a component, primitive, or design token."
---

# Kit Curator

## Purpose
Keep the Agentic UI Kit growing in step with feature work, in whichever repo the PR lives. New primitives enter the kit in the same PR that invents them, reviewed by someone other than the author, so the repo's inventory never goes stale unnoticed.

The law is the same everywhere. Only the paths and commands differ, and they come from the repo profile below. The shared check is `kit-inventory` (`@srbryers/kit-inventory`, in srbryers/ui-kit `packages/kit-inventory`). Where a repo has not adopted it yet, run the repo's own command from its profile.

## Repo profiles

Read the repo's boot doc first; it wins over this table when they disagree.

| Repo | Boot doc | Inventory | Contracts | Review notes | Repo gate |
|---|---|---|---|---|---|
| Prelude (`prelude-social-skills-coach`) | `docs/design/screen-inventory/README.md` | `docs/design/screen-inventory/component-review.json` (`prelude` format) | `components/*.contract.ts` where the pattern applies | `docs/design/kit-review-<date>/` | `npm run ui:inventory`, `node scripts/check_screen_adoption.cjs --check` |
| Flora Studio (`flora-studio`, base branch `preview`) | `docs/design/agentic-ui-kit.md` | `gallery/src/components/kit/kit-inventory.json` (`flora` format, root `gallery`) | `gallery/src/components/kit/contracts.ts` (one file) | as `.agents/skills/review-effort/SKILL.md` says | `cd gallery && npm run ui:gate && npm run kit:inventory:check && npm run kit:screens:check` |
| ui-kit (`ui-kit`) | `AGENTS.md` | `packages/kit-rn/registry.json` (generated from contracts; never hand-edit) | `packages/kit-rn/src/**/<Name>.contract.ts` | PR body | `npm run check`, `npm run check:canfail`, `npm run visual` |
| Wedding (`wedding`) | `docs/ui-kit.md` | `docs/design/2026-09-22-component-review/review-ledger.json` | none yet | `docs/design/<date>-*/` | `npm run ui-kit:inventory`, `npm run check` |
| Pi Station (`pi-station`, base `master`) | `docs/kit-guide.md` (generated), then `scripts/kit-audit/README.md` | `web/src/ui/catalog.ts`: one entry per component, no hashes, so `kit-inventory` does not apply | The catalog entry: `useFor`, `notFor`, states, markers, `alike`, `truncates` | PR body, one block per component | `pnpm kit-guide` leaves no diff; `pnpm kit-audit --static-only`; `pw-slot pnpm kit-audit` for the PR's stories; `pnpm kit-audit:full` once at the release tip |

For a repo not in the table, ask which file is the inventory and which command is the gate before starting. Do not guess.

Pi Station has no hashed inventory. Record the review per component in the PR body (step 5, "without it"). Its light and dark baselines are generated at the release tip, not committed, so list baseline coverage as a known limit in the PR. Use pnpm, never npm or npx.

## Workflow
1. Work in the branch's own checkout or worktree. Find the repo's profile above and read its boot doc.
2. Diff the branch against its base and list every added or changed reusable primitive or token: components, contracts, story files and token files (for example `constants/motion.ts` in Prelude, `gallery/src/styles/workbench.css` in Flora, `packages/tokens/src` in ui-kit).
3. For each one, confirm the kit absorbed it in this PR: the component, its contract where the repo uses contracts, Storybook stories covering its states, and visual baselines in both light and dark themes where the repo keeps baselines. Raw native controls in feature code are a finding, not a shortcut.
4. Review motion explicitly: loading, typing, streaming, pending, message and screen transitions, height and width changes, and the reduced-motion variant of each. A state with no motion story is a gap.
5. Read each changed component and its diff. That reading is the review. Then record it in the inventory, one component at a time:
   - With the shared tool: `npx kit-inventory stamp --inventory <inventory> --component <Name> --reviewer <id>` (add `--root gallery` in Flora). It re-hashes that one entry and refuses a reviewer who is an author.
   - Without it: update that entry's source hash, story hashes, states, responsibility and evidence by hand or with the repo's generator, scoped to the entries you reviewed.
6. The reviewer is never the author. The builder is recorded in `authors`; an independent agent is the `reviewer`. Roman is the default reviewer in ui-kit and Flora; Prelude already spreads reviews across several agents. Sebastian's taste check is a separate gate and is not replaced by this review.
7. Write the review note where the profile says, then run the gate:
   - `npx kit-inventory check --inventory <inventory>` and `npx kit-inventory canfail --inventory <inventory>` (shared floor), and
   - the repo gate from its profile (repo-specific rules such as Flora's contract pairing or Prelude's route and native-control checks).

## Output Contract
Report: repo and profile used; primitives and tokens touched; for each, contract status, story coverage (including motion and reduced-motion states), baseline coverage (light and dark); reviewer per entry; inventory check and canfail result; repo gate result; and either "kit gate green" or the exact list of missing pieces blocking it.

## Operating Rules
- The gate passes only with zero inventory findings and a green repo gate. A red check means the PR is not merge-ready, whatever the code does.
- Never refresh a hash you have not reviewed. There is no bulk refresh in `kit-inventory` on purpose; do not work around it with a repo's `--generate` for entries you did not read. Paperwork without reading is how stale entries happen.
- A listed state must be a real story export. `state-not-exported` means the record drifted from the stories: fix the record or the story, and say which in the review note.
- Hash-only churn from a shared story file may be refreshed across entries, but say so in the review note.
- Known limits (web-only no-ops, single-screen adoption, baselines that only protect local runs) go in the PR description, not in a chat aside.
