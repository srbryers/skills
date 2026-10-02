---
name: "supabase_edge_ops"
description: "Operate Prelude Supabase edge functions and database safely - inspect, verify, and sequence deploys for llm-proxy and jev-extract. Use for any Supabase function, migration, routing, or model_config work."
---

# Supabase Edge Ops

## Purpose
Handle Prelude's Supabase surface (edge functions, migrations, `model_config` routing) without the known landmines: no secret handling by agents, no reapplied migrations, no unverified deploys.

## Workflow
1. Run everything from the linked repo on the Mac Studio: `cd ~/Development/prelude-social-skills-coach` (via `~/workspace/bin/macstudio` from this VM). The CLI is not on the non-interactive PATH; use the full path `/opt/homebrew/Cellar/supabase/2.101.0/bin/supabase`.
2. Inspect before changing: `supabase functions list` for deploy state, and read the function source in `supabase/functions/<name>/` plus any `model_config` rows the change touches.
3. State the deploy sequencing note before any code change: what ships, what behavior production has before and after, what the client does if the new signal or route is absent, and what rollback looks like.
4. Verify end-to-end with a synthetic test user minted through the admin API (clean up `auth.users` afterwards). Do not use fake JWT shortcuts; the sandbox JWT path 403s and proves nothing.
5. Deploy only on Sebastian's explicit go-ahead: `supabase functions deploy <name>`. After deploy, re-run the synthetic-user verification against production before claiming it works.
6. For routing changes (`llm-proxy`, OpenRouter provider settings, `model_config`), name the privacy and cost effect in the deploy note, including `data_collection` settings per row.

## Output Contract
Report: function or migration touched; current production state (version, ACTIVE or not, from the CLI); the sequencing note (before, after, client fallback, rollback); verification evidence (synthetic-user result, not a log excerpt with secrets); and the deploy status as exactly one of: inspected only, ready for Sebastian's deploy approval, deployed and verified.

## Operating Rules
- Sebastian enters secrets himself in the Supabase dashboard. Never request, receive, relay, echo, or store a secret value. Describe a credential check by result only.
- Migration 00046 was already applied to production on 2026-09-30. Never reapply it; check database state before believing any migration hypothesis.
- Deploys and production routing changes are Sebastian-gated. A merged PR is not a deployed function; say which state you are in.
- `llm-proxy` and `jev-extract` changes always ship with explicit deploy sequencing notes, because the client must behave correctly both before and after the deploy.
- There is no `supabase functions logs` in CLI v2.101.0. Verify through behavior (synthetic requests), not log tailing.
