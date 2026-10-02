---
name: "studio_ops"
description: "Diagnose Mac Studio infrastructure, local GitHub Actions runners, processes, and disk pressure; use when CI, builder, or Studio-hosted tooling appears stuck."
---

# Studio Ops

## Purpose
Determine whether a problem is on Sebastian's Mac Studio, in a local runner queue, in a repository configuration, or upstream, using direct evidence from the machine before suggesting dashboard actions or blaming GitHub.

## Workflow
1. Reach the Studio through `~/workspace/bin/macstudio`. Wrap the remote command in single quotes so `$?`, `$PIPESTATUS`, environment variables, and command substitutions expand on the Studio rather than in the local shell. Avoid piping a status check through `tail` when its exit code matters.
2. State the symptom precisely: repository, workflow, branch, run or job, how long it has been queued or busy, and what changed most recently.
3. Check the self-hosted runner fleet for `srbryers/prelude-social-skills-coach`:
   - `~/workspace/bin/macstudio 'export PATH=/opt/homebrew/bin:$PATH && gh api repos/srbryers/prelude-social-skills-coach/actions/runners'`
   - Record each runner name, online or offline state, busy state, operating system, and labels.
   - The expected fleet is `mac-studio-prelude`, `mac-studio-prelude-2`, and `mac-studio-prelude-3`.
4. Check queued and in-progress runs and their job labels:
   - `~/workspace/bin/macstudio 'export PATH=/opt/homebrew/bin:$PATH && gh api "repos/srbryers/prelude-social-skills-coach/actions/runs?per_page=20"'`
   - Compare workflow demand with available runners. One runner executes serially, so a burst of pull requests can create a long queue even when every runner is healthy.
5. Verify the local runner processes and services when the API state is unclear:
   - Runner directories: `~/actions-runners/prelude-social-skills-coach`, `~/actions-runners/prelude-social-skills-coach-2`, and `~/actions-runners/prelude-social-skills-coach-3`.
   - Services: `actions.runner.srbryers-prelude-social-skills-coach.mac-studio-prelude-*`.
   - Use `launchctl list`, process inspection for `Runner.Listener`, and each directory's `svc.sh status` as appropriate.
6. Check machine pressure when jobs or builders stall:
   - Inspect long-running Claude, Codex, Node, test, and render processes without killing unknown work.
   - Check free disk and obvious worktree or log growth with `df -h` and targeted `du` commands.
   - Identify a process by command, working directory, age, and output before treating it as stale.
7. Interpret the evidence before acting:
   - Online and busy runners plus many queued jobs means local saturation, not a GitHub outage.
   - An offline runner points to its local service or process.
   - An idle eligible runner plus a queued job points to label, run, or dispatch investigation.
   - A superseded queued run should be identified by branch and head commit before cancellation is proposed.
8. Use the narrowest recovery supported by the evidence. Recheck runner state, queue movement, or the affected job after any restart, cancellation, or configuration change. Registering another runner, changing repository settings, or killing an unknown process requires a clear operational need and appropriate approval.

## Output Contract
Report the observed runner states, queue depth, relevant processes or disk pressure, the most likely cause, the action taken, and verification after the action. Separate confirmed facts from hypotheses and name anything that remains upstream or unresolved.

## Operating Rules
- Queued CI may mean the local runners are saturated. Check the Studio fleet before attributing delay to GitHub.
- Do not send Sebastian to a dashboard for something the GitHub API or Studio shell can inspect directly.
- Never expose tokens or other secret values while checking auth, services, or process environments.
- Do not stop a Claude, Codex, test, or render process until its command and working directory show what it owns.
- Do not delete worktrees, logs, caches, or runner directories as a speculative fix.
- A service being installed is not evidence that it is running; verify its live state after starting it.
