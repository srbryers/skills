---
name: ui-review
description: Run stepwise product-owner UI design review, record their feedback and decisions, and track downstream flow, component, token, kit and consumer rollout. Use when preparing an interactive or Storybook design review for the product owner, recording their UI feedback, or carrying their agreed change through adoption. Ordinary Storybook render, regression or visual QA uses the existing technical review workflow.
---

# UI review

Keep the product owner's context burden small. Agents own testing, decision records and impact tracking. The product owner judges the experience and makes product and visual choices.

Use the project's existing design contracts, inventory and component library. Read the relevant prior decisions before presenting or changing a screen. Preserve the user's scope and existing authorisation. This skill grants no authority to edit another repository, send messages, publish packages, change accounts or release an app.

## Choose the review surface

| Need | Surface |
|---|---|
| Flow, wording, pacing or transitions | Interactive app or prototype, starting at the named entry |
| A component's variants, states or motion | Storybook or the project's existing component catalogue |
| Shared change in context | The component specimen plus affected app screens |

Use the same implementation in the app and its stories. A native-app browser preview should render the reusable native components through the existing web adapter. Do not recreate the product with separate DOM controls or CSS motion. Document platform adapters and limits.

For first-run review, start at the actual landing screen. Advance through user actions, one screen or message beat at a time. Do not default to completed history, inject learner answers or skip consent. Returning and failure fixtures are explicit, separate states. Follow an explicit request for a whole-flow review instead when that is the user's intent.

## Prepare before asking for feedback

Exercise the requested path yourself. Check reset, back, retry and draft preservation where relevant. Render the relevant loading, empty, error, disabled, permission and consent states. Check themes, supported widths, larger text, reduced motion, labels, focus and touch targets appropriate to the change.

Fix broken wiring before the handoff. Show only a usable review slice. Keep unfinished paths labelled outside the product UI. If checks are unavailable, state the limit and offer a verified specimen when available. Never turn a design review into an assignment to debug the prototype.

Browser evidence proves browser behaviour. Native keyboard, gestures, safe areas, screen readers, haptics and platform effects need native checks. Record mocks, source-built packages and failed checks. A screenshot cannot prove a transition, and an initial render cannot prove an interaction.

## Give a small review card

Use [the review-card template](references/records.md#review-card). Include a direct resettable state link, the starting state, what is already agreed, the proposed change and one focused decision. Offer a small comparison only when it helps. Keep build and fixture controls outside the product UI.

Keep the reviewed build stable during feedback. Record its source revision and visual evidence before changing it. If a live preview changes, name the change and supply the new version. Do not make the user scroll backwards or repeat earlier decisions to establish context.

For stepwise reviews, finish or explicitly defer the current decision before moving to the next. Routine checks continue independently; do not delay authorised fixes for review ceremony. The user can give feedback naturally, without completing a form.

## Record and carry the decision

During the same turn, write feedback into the project's existing decision log, or create one in its maintained design documentation. Use [the decision-record fields](references/records.md#decision-record). Preserve the speaker's exact relevant words and context. Do not store private account data, credentials or personal machine paths in published records.

Keep observed, proposed, accepted, deferred and superseded decisions distinct. A suggestion or capability in a roadmap does not approve a particular control, placement or flow. Accept only what the reply and its context support. Clarify an ambiguous choice before dependent work; continue unrelated authorised work.

Record implementation, independent verification, adoption, native acceptance and release separately. Link later evidence instead of rewriting earlier decisions. If the source version was not captured, say so; feedback can guide a fix without approving frozen code.

Update the owning flow, component, token or product contract after agreement. The log preserves provenance; the owning contract supplies the rule. Show the changed slice and a brief readback of what was agreed, what changed and what remains open.

## Track downstream effects

Before implementation, use the inventory and source graph to identify affected consumers. Read actual usage; an import count alone does not prove behaviour. Create linked work with owners and acceptance criteria for effects outside the current scope.

| Change | Follow-through |
|---|---|
| Flow or copy | State contract, entry points, recovery, accessibility and behaviour checks |
| Shared component | API, real stories, meaningful states and affected consumer regressions |
| Token or motion | Semantic authority, themes, reduced motion and affected consumers |
| Shared package | Minimal reproduction, kit feedback ledger, contract/stories, reviewed release and pinned consumer artifact |
| Persisted behaviour | Schema, sync, consent, deletion and server gates owned by the relevant work |

Read [the rollout record](references/records.md#rollout-record) when a change affects other screens or packages. Decide whether to update all consumers together or stage adoption. Name the pilot, remaining consumers, exclusions, owners, dependencies, acceptance and rollback. No silent drift across screens.

A prototype patch or vendored package change is not completed kit adoption. Respect the kit repository's rules, coordinate authorised handoffs and verify the consuming app against the accepted artifact. Use the existing technical checks and independent review process. If installed, `kit-curator` covers promotion and `visual-review` covers visual QA; neither supplies product-owner acceptance. Do not invoke a paid service merely because another skill describes it.

## Completion and handoff

Report the accepted decision, implemented scope, remaining consumer work and evidence limits briefly. Update the project's inventory, stories and reviewed source records using its existing workflow.

Never infer a later milestone from an earlier one:

| Milestone | Evidence |
|---|---|
| Design accepted | Product owner's scoped decision |
| Implemented | Source, stories and owning contracts match |
| Technically verified | Required checks and distinct review on that version |
| Adopted | Named consumers use the accepted implementation/artifact |
| Native accepted | Required device evidence for affected behaviour |
| Released | Normal release checks and existing release authority |
