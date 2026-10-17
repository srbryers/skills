---
name: strategy-gameplan
description: "Develop a long-term vision into an executable strategy through staged decisions, research, strategic interaction and delivery gates. Use to game out alternative routes, stress-test assumptions or resume a strategy discussion."
---

# Strategy gameplan

Turn an agreed North Star into a sequence of useful commitments. Keep the vision stable while revising the route through evidence.

## Start or resume

Read the user's existing strategy, decisions and project constraints before asking for them again. Preserve their exact North Star unless they change it.

Use an existing decision record when it can hold this work. Otherwise, keep one portable JSON session beside the strategy documents. See [the record contract](references/record.md).

```sh
python <skill-directory>/bin/gameplan.py init <session.json> --title "Project strategy" --north-star "The user's exact North Star"
python <skill-directory>/bin/gameplan.py check <session.json>
python <skill-directory>/bin/gameplan.py brief <session.json>
```

The helper needs Python 3.10+ and no packages, credentials or network. It creates records without overwriting files. Checks verify structure and completeness; they never approve a strategy or certify evidence.

Keep discussion and execution distinct. Planning permission does not grant permission to spend, contact people, change a product or release work.

## Work through the next decision

Adapt the depth to the decision. Resume at the earliest unresolved point; do not repeat accepted work.

1. **Establish the position.** Separate observed facts, user reports, assumptions, unknowns and constraints. Link evidence for observed facts. Include resources, current capabilities and founder motivations.
2. **Agree what matters.** Propose decision criteria tied to the North Star and current needs. Record which criteria the user accepts. Do not replace their goals with a generic growth or revenue objective.
3. **Map plausible routes.** Show useful intermediate outcomes, dependencies, costly commitments and what remains valuable if a route ends early. Keep distant stages conditional.
4. **Examine strategic interaction.** Identify relevant participants, incentives, available moves and possible responses. Include cooperation and dependence. Treat predicted responses as hypotheses. If interaction does not affect the decision, use decision analysis without inventing opponents.
5. **Compare the next moves.** Include waiting, buying or using an existing capability where credible. Examine value, cost, downside, reversibility and future options. Stress-test important assumptions across plausible futures.
6. **Resolve decision-changing uncertainty.** Research the question whose answer could change the next commitment. Define that stopping condition first. Use current primary sources for technical claims. Separate demonstrated results, authors' claims and our inference. Preserve useful negative findings.
7. **Recommend and define the gate.** Explain the tradeoff and the strongest case against the recommendation. Name what evidence would change it. Define the next commitment, its gate and the useful work that can proceed now.

In a step-by-step discussion, present the next material decision and let the user resolve it before dependent commitments. Continue independent research already authorized. Avoid turning every response into another question.

When authorized, delegate a specific research question with a named result. Follow the host's model and spending rules. This skill adds no paid calls or standing review board.

## Define gates that unlock action

For each proposed commitment, record:

- What decision the gate unlocks, and who owns that decision.
- The smallest sufficient evidence, its source and the acceptance criteria.
- The action after success, failure or an inconclusive result.
- Evidence that carries forward, and the change that would justify reopening it.
- The next deliverable's owner, scope, limits, acceptance and finish condition.

Use measured thresholds or acceptable ranges where they answer the decision. Agree them before evaluating a candidate. For qualitative gates, name the judgment and its owner.

Keep technical evidence, customer demand, economics and human preference distinct. A combined score cannot replace a failed requirement or grant human approval.

Check the proposed decision before presenting it:

```sh
python <skill-directory>/bin/gameplan.py check <session.json> --decision D001
```

This checks whether the record is complete enough to discuss. Inspect the linked evidence yourself. Record actual owner decisions with their sources; silence and agent recommendations are not owner decisions.

## Finish with an executable handoff

The plan is ready when the next commitment has a selected route, explicit assumptions, an owner, sufficient acceptance criteria and a finish condition. Longer-term branches can remain unresolved.

Summarize the chosen route, its strongest remaining risk, the next gate and the next action. Distinguish proposed work from accepted decisions. Hand execution to the project's existing ticket and delivery process. Do not create sprints or a new tracker by default.

Further analysis must identify which live decision it could change. Reuse unchanged evidence and prior decisions. Reopen work for changed assumptions, evidence or scope, following the host's existing process.

## Method and limits

Game theory addresses strategic interaction. Decision analysis handles choices under uncertainty. Use both where useful; do not invent probabilities, payoffs or equilibria from narrative guesses.

For research on the method, start with these primary explanations:

- [Nobel Prize: strategic interaction](https://www.nobelprize.org/prizes/economic-sciences/2005/ceremony-speech/).
- [NASA: alternatives, uncertainty and the value of further analysis](https://www.nasa.gov/reference/6-8-decision-analysis/).

This skill supports strategic decisions. Ordinary edits, code review, sprint administration and specialist acceptance use their existing workflows.
