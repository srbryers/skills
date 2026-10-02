---
name: "pr_ship_gate"
description: "Run the Prelude PR merge and ship gate - checks, kit status, staging, EAS, and device state. Use before calling any Prelude PR merge-ready, merged, shipped, or ready for Sebastian's phone."
---

# PR Ship Gate

## Purpose
Keep Prelude PRs honest through four separate states: merge-ready, merged, shipped, and verified on Sebastian's device. A PR is not done when code looks right; it is done when the gates say so and the ship state is named correctly.

## Workflow
1. Work from the Mac Studio repo at `~/Development/prelude-social-skills-coach` (via `~/workspace/bin/macstudio` from this VM). Use feature branches and PRs only. Never push to `main` directly; merge to `main` only with Sebastian's explicit in-chat approval.
2. Identify the PR: number, head branch, base, changed files, and whether it touches UI, prompts, edge functions, or migrations.
3. Check GitHub checks for the PR head. If checks sit queued, inspect the self-hosted runners (`mac-studio-prelude`, `-2`, `-3`, labels `self-hosted` + `prelude`) before blaming GitHub; cancel only superseded duplicate runs, never another builder's active work.
4. Run the local gates that CI will run: typecheck, targeted jest for touched areas, `npm run ui:inventory` if inventory may drift, and `node scripts/check_screen_adoption.cjs --check` for any UI change.
5. Confirm the three review passes for UI PRs: design pass, animation pass (loading, typing, streaming, pending, transitions, reduced motion), and kit pass via the `kit_curator` skill.
6. Merge decision: feature branch into `staging` is allowed for approved work so EAS updates do not wait on `main`. Merge to `main` waits for Sebastian's explicit approval.
7. Ship from a `staging` checkout: `eas update --branch staging --environment development --message "..." --non-interactive`. Record the update group ID. Production builds on runtime 1.0.0 use build number 101 or higher; dev-client builds use `distribution: internal`.
8. Close the loop: re-run the relevant sim suite on staging after the merge, and log the new product state. Ask Sebastian for the device check; only he can confirm what his phone shows.

## Output Contract
Report, in this order: PR number and branch; checks (pass, fail, or queued with reason); gate results (typecheck, jest, inventory, adoption); review passes (design, animation, kit); merge recommendation and target (`staging` or `main`); ship state using exactly one of: not merged, merged to staging, EAS update published (with group ID), on device (only with Sebastian's confirmation).

## Operating Rules
- Merged is not shipped. Shipped is not on his phone. On his phone is not physically verified. Say which one you mean.
- Never call a PR merge-ready with a red adoption check, stale inventory, or unrun local gates. Name the failing gate instead.
- Do not send Sebastian to a dashboard or app screen on a guess. Verify through the CLI or API first.
- A failing test or dead background process gets reported with what failed, why, and what happens next. Never bury it in a retry.
