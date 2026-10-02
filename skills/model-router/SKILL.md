---
name: "model_router"
description: "Choose and evaluate models using Sebastian's model-routing cards; use when assigning a task to a model, comparing model outcomes, or deciding whether a route is ready for regular use."
---

# Model Router

## Purpose
Choose the smallest reliable model and route for each task while treating Sebastian's model-routing cards as hypotheses that must earn calibration from recorded outcomes.

## Workflow
1. Define the task before naming a model: task type, difficulty, context size, tool needs, quality bar, latency target, cost limit, and the deterministic checks or human decision that will judge success.
2. Consult the current model-routing cards and any existing outcome records. Treat every card as `UNCALIBRATED` until repeated outcome data supports a stronger trust state.
3. Verify that each candidate model is actually callable through the intended provider, CLI, account, and route before assigning work to it. A listed, announced, or previously available model is not evidence that it can be called now. Record unavailable candidates and use a verified fallback.
4. Match the evaluation method to the claim:
   - Use deterministic code, tests, schemas, counts, and other repeatable checks for factual gates.
   - Use Jev only for semantic judgment, classification, or choice among supplied alternatives.
   - Use human review for taste, safety, account, and irreversible decisions.
5. Select the route with the least capability that can plausibly meet the quality bar. Escalate to a stronger or more expensive model when the task is architecturally demanding, visually or interaction sensitive, high risk, or recovering from repeated failure.
6. Run the work with the evaluation criteria fixed in advance. For meaningful comparisons, keep prompts, inputs, tools, and success criteria constant across candidates and record each run rather than relying on a single demonstration.
7. Log the outcome when available: task type, candidate and chosen model, provider or route, callable verification, runs attempted, cost range, latency range, quality result, deterministic gate result, semantic judgment when relevant, failures, fallback used, and human acceptance.
8. Summarize repeated results as ranges and counts, not only means. A mean without the run range hides instability. Update calibration language only when enough comparable outcomes justify it.

## Output Contract
Report the task classification, candidates considered, callable verification, chosen model and route, fallback, evaluation method, and known cost, latency, and quality outcomes. For comparisons, report the number of runs and the observed ranges alongside any average, plus a trust label such as `UNCALIBRATED`, `SINGLE_CANDIDATE`, `NO_CLEAR_WINNER`, or `CALIBRATED` when supported by the routing-card system.

## Operating Rules
- Never claim a model or card is calibrated from one successful run.
- Never route to a model solely because it was announced, listed, or worked through a different provider or account.
- Jev is a semantic judge only. Do not use it for arithmetic, exact counts, factual verification, or deterministic release gates.
- Deterministic code decides factual pass or fail conditions; model judgment may explain or prioritize a failure but cannot override the gate.
- Prefer verified moderate routes over unverified premium routes when the quality requirement allows it.
- Record failed, timed-out, unavailable, and fallback runs. Excluding them makes the routing data falsely optimistic.
- Do not include secrets or raw credentials in routing logs or evaluation artifacts.
