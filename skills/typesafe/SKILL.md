---
name: "typesafe"
description: "Call Jev (TypeSafe System One) to classify text with typed choice, score, and true/false questions. Use when a pipeline or review needs Jev's typed answers, such as categorizing commits and PRs in the stackdiff pipeline."
compatibility: "Needs the hatch host's dynamic-credential helper at /opt/hatch/skills/skill-creator/bin and the custom.typesafe connector. Neither exists on other hosts, so calls fail there."
---

# Typesafe

## Purpose
Use Typesafe with the user-connected `custom.typesafe` credential.

## Tooling
`bin/jev.py ask` - POST a state plus typed questions to `https://api.typesafe.ai/v1/systemone`.

- `jev.py ask --state "..." --questions '{...}' [--model jev-latest]`
- `jev.py ask --state "..." --questions-file questions.json`
- `echo '{"state": "...", "questions": {...}}' | jev.py ask --stdin`

Question types: `choice` (pick from criteria, returns choice + probabilities + confidence), `score` (rubric), `noul` (true/false 0-1). Multiple questions evaluate in parallel in one call.

Python CLIs must import `/opt/hatch/skills/skill-creator/bin/dynamic_credentials.py` and call `add_surrogate_to_request(...)`, `url_with_surrogate_query_param(...)`, or `url_with_surrogate_path_segment(...)` before authenticated requests, matching where the provider reads the key. If they use `urllib`, read JSON responses with `read_json_response(resp)` from the same helper instead of calling `resp.read()` directly. They must send only `hsurr:*` values, and only to the hosts below.

## Auth
The credential is already stored; nothing here collects one. Never ask the user to paste a raw key in chat, set a secret environment variable, pass a secret flag, or write an auth file.

A 401 or 403 is a question about the request before it is a question about the key. Check that the credential was attached at all: a request built without the helpers named under Tooling carries nothing, and that looks exactly like a wrong or under-scoped token. Only once a request that did carry the credential is still rejected, call `credentials.request_api_access` with `reconnect` to replace it. The connector is stored as `custom.typesafe`.

## Operating Rules
1. Use this skill when the user asks for Typesafe or this provider's API.
2. Restrict authenticated requests to: api.typesafe.ai.
3. Do not print, log, or persist raw credentials.
4. If auth is missing or rejected, follow the Auth section rather than asking for a key.
