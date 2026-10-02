---
name: "stackdiff_producer"
description: "Produce Sebastian's weekly stackdiff drafts from GitHub work when turning shipped code changes into X, Threads, Instagram carousel, and newsletter copy for approval."
---

# Stackdiff Producer

## Purpose
Turn the week's real GitHub work into a stackdiff: what changed in the stack, why it matters, and what is different since last week. Drafts only. Sebastian approves before anything publishes or sends.

## Workflow
1. Determine the week window and the repos in scope. Default to the active Prelude repo plus any repo Sebastian names for that week.
2. Use the github skill to pull merged PRs, notable commits, releases, and closed issues for the window.
3. Read the actual PR descriptions, diffs, and commit messages. Do not write from titles alone.
4. Classify each item with typesafe/Jev: product change, infrastructure, testing system, design system, content or growth, and housekeeping.
5. Pick the few changes that form a coherent story. For every tool, model, or process pick mentioned, write one line for why it was chosen and one line for the diff since last week.
6. Draft four outputs:
   - X post: one tight post, concrete nouns, no hype padding
   - Threads version: same story, slightly more room, conversational
   - Instagram carousel outline: slide-by-slide text with the visual idea per slide
   - Newsletter digest: short sectioned summary with links to PRs or artifacts when useful
7. Mark every claim that depends on shipped versus merged versus planned state. Merged is not shipped, shipped is not on device, and planned is not done.
8. Present drafts for Sebastian approval. Revise in place when he gives notes.

## Output Contract
Deliver:
- source list of PRs and commits used
- classification summary
- X draft
- Threads draft
- Instagram carousel outline
- newsletter digest draft
- explicit list of claims needing Sebastian verification before publish

## Operating Rules
- Nothing publishes, posts, schedules, or sends without Sebastian explicit approval.
- Each tool pick gets a one-line why and a diff since last week. No silent tool swaps.
- Use exact identifiers from GitHub output. Do not invent PR numbers, dates, metrics, or outcomes.
- Plain language. Name the feature, the fix, and the user-visible change.
- Keep drafts scannable. Sebastian should be able to approve, tweak, or cut in one pass.
