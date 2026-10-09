# Development and delivery

Read this guide before changing a skill or sharing an update.
Each skill and consumer project keeps its current rules and approval gates.

## Sources and scope

- Verified on **2026-10-09**, against `origin/main` at `6159df6efaf65279b028afc4fb324bb202b4ef1d`.
- Source branch: `main`. Use an isolated feature branch and PR for this rollout.
- [README.md](../README.md) owns library layout, Pi installation and credential conventions.
- Each `skills/<name>/SKILL.md` owns its own workflow and acceptance rules.
- Its `bin/` scripts and `references/` files own executable behavior and input formats where present.
- No root AGENTS.md or CLAUDE.md exists at this base. Applicable ancestor instructions still apply.
- No GitHub workflow, root package manifest, lockfile or repository test runner is tracked at this base.
- Prompt source: [shared template at e938d054825d4b20b7d3fb63a4629e97b97a4142](https://github.com/srbryers/ci/blob/e938d054825d4b20b7d3fb63a4629e97b97a4142/templates/CI-CD.md).
- Template PR [ci#1](https://github.com/srbryers/ci/pull/1) remains **pending**, not an adopted universal policy.

This repo shares Markdown playbooks and four Python scripts.
It does not build or deploy an app or publish an npm package.
README's possible future catalog site is a roadmap idea. It has no delivery process yet.
This guide grants no approval to run specialist skills, paid judges or remote builders to check prose.

## Checks by change

Run source checks in this isolated worktree.
Run consumer checks in that project's own isolated workspace. Use its runtime and required approvals.
Do not install packages or run browser, native, 3D or full consumer suites for prose alone.

| Change | Focused development evidence | Stable candidate evidence |
| --- | --- | --- |
| Guide and README prose | Readback, links, `git diff --check`, compare claims with source | Independent review; no existing repository Markdown check |
| Skill instructions or frontmatter | Check name, description, trigger and referenced paths; compare consumer policy | Review a representative affected use case without granting new permissions |
| Python script | Syntax check plus review of inputs, imports, outputs and credentials | Authorized affected consumer check; retain negative/failure evidence where relevant |
| Shared typesafe client | Inspect both visual-review and exercise-form-review imports | Verify affected judges on the credential host; local syntax is not API evidence |
| Visual rules or baselines | Use that skill's documented source and evidence rules | Consumer gates, independent reviewer and human taste/device decisions remain separate |
| Install/update behavior | Check source revision and discovered skill files | Verify the installed revision, frontmatter discovery and affected consumer workflow |

There is no repository `npm test`, build, lint or typecheck command.
For future Python edits, a syntax-only check is `python3 -m py_compile skills/<name>/bin/<script>.py`.
It requires Python and writes `__pycache__`; remove only the output created by your run.
Syntax checks do not import the host credential helper or prove API behavior.
The scripts need modern Python for their type syntax. No version is pinned here.
This repo has no unit-test suite or frontmatter checker.
Report that coverage gap. Do not run unrelated project suites to fill it.

## Automation, access and live settings

| Setting | Verified state |
| --- | --- |
| Workflow triggers | None in this repository; no push, PR, schedule, tag or release workflow |
| Runner, cache, concurrency | None configured by repository workflows |
| Workflow permissions/secrets | No workflow declaration; this does not prove that consumers need no access |
| Live Actions defaults | Read-only workflow token; Actions cannot approve PR reviews |
| Protected environments | Live environment list was empty |
| Branch settings | `main` protection returned **404: Branch not protected**; rulesets were empty |
| Required checks/reviewers | No configured names found through those settings; manual gates remain |
| Human owner | **Sebastian** for merge, installation/adoption and external actions in this task's context |
| External app checks | The live PR runs GitGuardian Security Checks; its service settings and gate owner remain **unresolved** |
| CodeQL | Live default setup is not configured |

This source runs no Actions workflow on a docs PR. The external GitGuardian check still runs.
Keep exact local receipts and get independent review. Do not invent a green CI gate.
Account settings and consumer environment gate owners are **unresolved** beyond the repo settings checked here.

[Typesafe](../skills/typesafe/SKILL.md) needs the hatch host's dynamic-credential helper and `custom.typesafe` connector.
[Its client](../skills/typesafe/bin/jev.py) imports the helper from `/opt/hatch/skills/skill-creator/bin` before requests.
Jev steps fail on hosts without the helper/connector even when the skills load.
Do not print, copy, persist or request raw credentials. Keep allowed-host and surrogate rules intact.
[Visual review](../skills/visual-review/SKILL.md) needs consumer Storybook, pngjs and pixelmatch for its pixel layer.
Its semantic layer runs where the credential exists; layout facts can cross machines, credential material cannot.
[Exercise review](../skills/exercise-form-review/SKILL.md) keeps its blind extraction and locked form/style rules.
Judge PASS is a filter result, not Sebastian's human approval.

## Manual distribution and update

1. Read the changed skill and any affected consumer policy before editing.
2. Keep the change generic under README's conventions; credentials stay outside the repository.
3. Record the exact source SHA, local checks, limits and affected consumers in the PR.
4. Obtain independent review and Sebastian's merge approval. This task stops at PRs.
5. For approved Pi adoption, the maintained install command is `pi install git:github.com/srbryers/skills`.
6. Record the installer result, resolved repository revision and discovered skill frontmatter on the intended host.
7. Check the affected consumer journey there under its own access, review and device gates.

Pi loads `skills/<name>/SKILL.md` from frontmatter, as README documents.
README also describes the format as usable by Muse, but provides no separate Muse install command.
This repo gives no update command, install-path list, version pin format or automatic update schedule.
Those details are **unresolved**. Sebastian must confirm the host's package-manager steps before an update.
Do not assume a merge refreshes an existing local copy or every agent's loaded instructions.
For copied/symlinked installs, record their actual source and revision before changing them; this repo defines no sync command.
Library delivery and consumer adoption need their own proof.
Finding a skill does not prove that its scripts, APIs or consumer gates work.

## Preserve specialist gates

| Source | Gates that stay separate |
| --- | --- |
| [Kit curator](../skills/kit-curator/SKILL.md) | Consumer profile, contracts/stories, theme evidence, independent reviewer, inventory/repo gates and Sebastian's taste check |
| [PR ship gate](../skills/pr-ship-gate/SKILL.md) | Prelude checks, staging/EAS identity, merge approval and Sebastian's device confirmation |
| [Supabase operations](../skills/supabase-edge-ops/SKILL.md) | Secret handling, migration sequence, synthetic-user verification and Sebastian's production approval |
| [Builder operations](../skills/builder-ops/SKILL.md) | Own worktrees, verified checks, approval before merge/deploy/publish/send; device and taste gates |
| [Studio operations](../skills/studio-ops/SKILL.md) | Verify process ownership and runner state; appropriate approval for host/account changes |
| [Decision board](../skills/decision-board/SKILL.md) | Independent decisions; no sends, public posts, purchases, main merges or production deploys without approval |
| [Stackdiff producer](../skills/stackdiff-producer/SKILL.md) | Draft review and explicit approval before publishing, posting, scheduling or sending |
| [Plain language](../skills/plain-language/SKILL.md) | Adopted copy rules and long-form readability review |

Consumer commands and branch names in these skills are local to their named projects.
Do not copy Flora's preview branch or Prelude's native/device acceptance into this library's release process.
Source review, browser/visual evidence, native checks, device acceptance and consumer adoption remain distinct.
Never refresh hashes or baselines to conceal defects or record the author as the independent reviewer.

## Failure, rollback and cleanup

- Keep original failures, source revisions, consumer receipts and reasons for later reruns.
- Separate missing host helpers, access failures, paid-service behavior and source defects.
- Batch known repairs before a stable push. This rollout starts no manual retries or cancellations.
- Do not skip checks, change thresholds or refresh hashes to make a result appear accepted.
- Do not run remote builders, judges or outbound actions as a substitute for reviewing this guide.
- If a consumer starts a server, reserve a free port and record its PID, worktree, source SHA and build identity.
- Verify the response belongs to that build. Stop only owned processes; remove only owned outputs.
- No global `pkill`, shared cleanup or CPU burners. Keep receipts needed for review.

Automated rollback is **none**. A source revert uses a separately approved PR.
Installed-package downgrade, saved versions and local-copy restore are **unresolved** until the host's install steps are known.
A source revert does not undo database changes, device updates, posts or other effects of an executed skill.
Those actions use the consumer project's restore and approval rules.
Update this guide in the same PR as future install or check changes. Keep each SKILL.md as its policy source.
