---
name: "sim_lab"
description: "Run and interpret Prelude onboarding simulated-user sims when validating interview or sharpening changes against personas, invariants, and Jev gating verdicts."
---

# Sim Lab

## Purpose
Operate the Prelude onboarding simulated-user harness to test prompt, hook, and extractor changes before device checks. Use transcripts and deterministic failures as evidence; do not treat a clean run as device proof.

## Workflow
1. Work from the Prelude repo on the Studio: `~/Development/prelude-social-skills-coach`.
2. Confirm tooling exists under `scripts/simulate-onboarding/`. If the harness or Results DB tooling is absent, report the gap instead of improvising.
3. Ensure the shell can load `OPENROUTER_API_KEY` and `TYPESAFE_API_KEY` from `~/.zshrc` without printing values. When PATH is incomplete, use `/opt/homebrew/bin/npm`.
4. Run a focused persona first when changing one behavior: `npm run simulate:onboarding -- --persona <id>`.
5. Run the full suite before staging or ship decisions: `npm run simulate:onboarding -- --persona all`.
6. Read the exit code before reading prose:
   - `0` pass
   - `1` flag
   - `2` cannot run
   - `3` deterministic fail
7. Separate failures into product failures, invariant failures, Jev gating flags, and provider noise. Provider noise includes judge overloads, timeouts, rate limits, and 529-class errors; retry once only when the run output points to infra rather than behavior.
8. If Results DB or transcript-import tooling is present in the repo, use it to compare the new run against prior runs and note the baseline. If absent, compare against named transcript paths manually.
9. Inspect exact transcript evidence for every deterministic fail before proposing a fix. Quote the failing turn and the rule it violated.

## Output Contract
Report:
- command run and persona scope
- exit code
- run cost when the harness prints it
- transcript path for each checked run
- exact failures, grouped by deterministic fail, invariant flag, Jev gating flag, and provider noise
- whether the result blocks staging, needs a retry, or is safe to note and move on

## Operating Rules
- Start narrow, then widen. Do not run the full suite as a substitute for reading a failed transcript.
- A Jev flag is a review signal, not proof. A deterministic fail is a blocker until explained.
- Keep cost visible. If a suite run is unexpectedly expensive or loops, stop and report before repeating it.
- Never hide a failed run inside a later pass. Name both.
- "What I'll say" is the feature name. Use `flow`, never `beats`.
