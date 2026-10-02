---
name: "decision_board"
description: "Run an independent Claude plus Codex review board with Jev as judge when a Prelude product, prompt, or architecture decision needs a defensible call before implementation."
---

# Decision Board

## Purpose
Make contested decisions with independent review instead of quick consensus. Use this when two plausible options both have real tradeoffs, when a prompt or flow rule is changing, or when Sebastian asks for a judged call.

## Workflow
1. State the decision in one sentence, plus the constraints that cannot move.
2. Prepare the same evidence packet for both reviewers: goal, options, relevant files or transcripts, known risks, and the exact question to answer.
3. Ask Claude Code and Codex to review independently. Neither reviewer sees the other answer before submitting.
4. Require each reviewer to return: recommended option, strongest reason, biggest risk, and what evidence would change their mind.
5. If the reviewers agree and the stakes are low, proceed with that option and still log the decision.
6. If they disagree, or the stakes are high, send the anonymized cases to Jev as judge. Ask for a typed verdict, confidence, and deciding factors.
7. Implement the winning option unless Sebastian approval is required for the action itself.
8. Append a DEC entry to `~/workspace/prelude-testing-system/DECISION_LOG.md` with date, decision, evidence, residual risk, and what would change the decision.

## Output Contract
Report:
- decision question
- options considered
- reviewer positions, kept separate
- Jev verdict and confidence when used
- chosen option and implementation owner
- residual risk
- what would change the decision
- decision log entry id

## Operating Rules
- Independence is the point. Do not seed one reviewer with the other reviewer's conclusion.
- Deterministic code decides factual gates. Jev judges semantics, tone, and tradeoff quality.
- A low-confidence Jev verdict is a flag, not a mandate. Surface it plainly.
- No outbound sends, public posts, purchases, merges to `main`, or production deploys without Sebastian approval.
- Sebastian taste calls stay Sebastian taste calls. Bring clean options, not a buried recommendation.
