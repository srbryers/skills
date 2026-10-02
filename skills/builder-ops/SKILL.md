---
name: "builder_ops"
description: "Launch, monitor, and finish Claude Code or Codex builder sessions on the Mac Studio; use when delegating coding work to an autonomous builder."
---

# Builder Ops

## Purpose
Run autonomous coding builders without duplicate launches, permission stalls, shared-worktree conflicts, or unfinished work being reported as complete.

## Workflow
1. Define the assignment before launch: task, repository, base branch, expected feature branch, required checks, deliverable, and any human gate. Write these into a self-contained prompt file because the builder does not inherit the conversation.
2. Check for an existing builder, branch, or worktree for the same task. Inspect active Claude and Codex processes, existing prompt files, and the intended worktree. Do not start a duplicate because an existing builder looks slow or quiet.
3. Route the model:
   - Use Sonnet by default for scripted, gate-verified, and bug-fix work.
   - Reserve Opus for demanding UI or iOS work, architecture, and recovery after repeated failures.
   - Use the established local Codex invocation for independent implementation or review only when its route has been verified for the task.
4. Give every builder its own worktree. Never run two builders in one worktree. For a fresh worktree in the Prelude repo, install dependencies before launch:
   - `~/workspace/bin/macstudio 'export PATH=/opt/homebrew/bin:$PATH && cd <worktree> && npm ci --no-audit --no-fund'`
5. Launch through the Mac Studio helper with subscription auth mapped into Claude Code. Use single quotes around the remote command and send stdin from `/dev/null`:
   - `~/workspace/bin/macstudio 'export PATH=/opt/homebrew/bin:$PATH && source ~/.zshrc >/dev/null 2>&1 && export CLAUDE_CODE_OAUTH_TOKEN="$CLAUDE_OAUTH_TOKEN" && unset ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN && cd <worktree> && timeout 2400 /opt/homebrew/bin/claude --model sonnet --dangerously-skip-permissions -p "$(cat <prompt-file>)" < /dev/null'`
   - Substitute `opus` only when the routing rule calls for it.
6. Monitor the recorded process or session. A running, queued, or quiet process proves only that work started. If output stops or the process exits, inspect the final output and worktree state before deciding whether to resume, relaunch, or finish the remaining mechanical steps directly.
7. Finish independently. Completion requires all of the following:
   - the intended branch exists and is pushed;
   - a PR exists for that branch when the assignment calls for one;
   - the relevant tests, typechecks, and task-specific gates were actually run and their results inspected;
   - failures, skipped checks, and unresolved issues are surfaced rather than hidden by a retry;
   - no merge, deploy, publish, send, or other human-gated action was taken without explicit approval.

## Output Contract
Report the task, selected model and reason, worktree, branch, PR, checks run with pass or fail results, total known cost when available, unresolved failures, and the exact next human gate if one remains. Link or name the prompt file and any investigation or evidence files produced.

## Operating Rules
- One builder per worktree; one active builder per task.
- A builder's self-report is evidence to verify, never proof of completion.
- Do not describe queued, running, or partially implemented work as done.
- If a background builder stops unexpectedly, say what it was doing, that it stopped, what state it left behind, and how it will be recovered.
- Do not place secrets, tokens, or private credentials in prompt files, logs, commits, or reports.
- Feature branches and PRs only for Sebastian's personal repositories. Never push directly to `main`, and never merge without his explicit approval.
- Stop at device checks, taste decisions, account actions, deployments, and other gates that require Sebastian.
