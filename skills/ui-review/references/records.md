# UI review records

Adapt these fields to the project's existing documents. Do not create a competing inventory or a new tracking tool.

## Review card

Keep the user-facing card short. Detailed checks and hashes belong behind links.

| Field | Content |
|---|---|
| Target | Screen/component and direct link that opens the named state |
| Start | First landing, named message beat or explicit specimen state |
| Decision | One focused question; a few choices if useful |
| Context | Already agreed, changed and still proposed |
| Comparison | Before/after or side by side, only if it helps |
| Readiness | What was exercised and limits that affect this decision |

Record the build/revision, kit version and artifact provenance with the card. If a resettable link is unavailable, supply a short reproducible path and state that limit. Do not call a mutable preview frozen.

## Decision record

| Field | Content |
|---|---|
| ID/date | Stable ID and date |
| Source | Speaker, exact relevant words and conversation/artifact reference |
| Target | Screen/state, source revision and visual evidence; unknown fields stay unknown |
| Interpretation | The accepted rule or proposal, and its reason |
| Decision status | Observed, proposed, accepted, deferred or superseded |
| Scope | Approval boundary and what remains undecided |
| Acceptance | Observable checks that establish the rule was implemented |
| Ownership | Implementation owner and linked follow-up work |
| Impact | Affected flows, components, tokens, packages and consumers |
| Evidence | Implemented revision, technical review and render/device results, each scoped |
| Rollout | Pending consumers, exclusions, rollback and completion evidence |
| History | Superseding record ID; preserve the original |

Record decisions in the repo, but keep sensitive raw evidence in its approved storage. Link or hash it as appropriate. Avoid duplicating personal feedback across public repos.

Example: a roadmap promises coach switching. That supports the capability, but does not approve a Change coach button in the header. Record placement as proposed until the product owner accepts it.

## Rollout record

Use this when a shared change affects other surfaces or package consumers.

| Consumer | Owner/work item | Current state | Target version/behaviour | Acceptance | Status |
|---|---|---|---|---|---|
| Pilot | Named owner | Observed implementation | Proposed/accepted target | Render, interaction and applicable device checks | Pending |
| Other affected screen | Named owner | Observed implementation | Same rule or justified variation | Consumer regression checks | Pending |

Statuses: pending, implemented, verified, deferred with a reason, or not affected with evidence. Do not use a global “done” while consumers remain untracked.

Also record:

- The source graph or usage review used to identify consumers.
- Whether adoption is staged or in one change, with the reason.
- Package release dependencies, pinned artifacts and compatibility constraints.
- Token/API migration, data/consent gates and accessibility effects where relevant.
- Rollback version or approach and any incompatible changes.
- Remaining native/device checks and the owner's next action.

A shared gradient fix, for example, requires checking every affected overlay's colours, layering, scrolling and input hit targets. A rendered component specimen alone does not verify each screen's composition.
