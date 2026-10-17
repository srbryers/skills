# Session record v1

Use one session per strategy. Keep it in the user's chosen workspace, outside the installed skill. Existing strategy records can replace this format.

`init` creates this envelope:

```json
{
  "schema": "strategy-gameplan.v1",
  "title": "Project strategy",
  "north_star": "The user's exact North Star",
  "criteria": [],
  "position": [],
  "actors": [],
  "routes": [],
  "decisions": []
}
```

The four lists before `decisions` hold objects whose details can grow with the discussion:

- `criteria`: `id`, `description`, and `status` such as proposed or accepted. Link the user's source for acceptance.
- `position`: `claim`, `kind` (observed, reported, assumption, unknown or constraint), and `evidence` references. Observed claims require evidence.
- `actors`: participant, interests, moves, and possible responses. Label response predictions as hypotheses.
- `routes`: stable `id`, path, dependencies, assumptions, risks, and value if stopped. Use conditional horizons rather than invented dates.

## Mission

Add an optional `mission` object when developing the company's purpose. Existing v1 sessions without it remain valid.

Use `status` (`exploring`, `proposed` or `accepted`) and `statement` for the current wording. Store `human_stakes`, `beneficiaries`, `frontier`, `contributor_role`, `near_term_proof`, `objections` and `candidates` as useful discussion notes. Record recruitment evidence and its source separately; `resonance` can remain `untested`.

A proposed or accepted mission needs a nonempty `statement`. Accepted means the founder chose the mission. It requires an `owner_receipt` with `by` and `source`; it does not establish recruitment appeal.

`brief` includes the mission and its recorded status. The helper checks these structural boundaries, without scoring inspiration or asserting that people will join.

## Decisions

Each decision starts with `id`, `question`, `status` and an `options` list. Status is `exploring`, `proposed`, `accepted`, `rejected` or `deferred`.

Each option has a stable `id` and an `action`. Before presenting a decision, add `upside`, `downside`, `commitment` and `reversibility` to each option. Use descriptions or sourced ranges. A single-option decision needs `alternatives_limited_because`.

For `check --decision <id>`, include these fields:

| Field | Required content |
| --- | --- |
| `recommendation` | One option ID; this is an agent recommendation until accepted |
| `rationale` | Why this option fits the agreed criteria and current evidence |
| `strongest_objection` | The strongest credible case against it |
| `research_stop` | What remaining finding could change the choice, or why current evidence is sufficient |
| `gate` | Nonempty strings: `unlocks`, `owner`, `evidence_needed`, `acceptance`, `pass_action`, `fail_action`, `inconclusive_action`, `reuse`, `reopen_if` |
| `next_step` | Nonempty strings: `outcome`, `owner`, `scope`, `limits`, `acceptance`, `finish` |

Record scenarios, sources and comparisons in additional fields as needed. Avoid filling fields with unsupported certainty just to pass a check.

Accepted decisions also require `selected` as an option ID and `owner_receipt` with nonempty `by` and `source` strings. `source` identifies an actual owner instruction or approval. An accepted option may differ from the recommendation.

The helper checks that these fields exist and agree. It cannot verify a transcript, read external sources, assess strategic merit or authorize execution. A well-formed receipt can still be false. The executing agent must inspect its source and follow project authorization rules.

`brief` produces a Markdown snapshot for discussion. It is derived from the JSON; edit the JSON rather than maintaining competing copies. It labels recommendations, selected options and recorded owner sources separately.

## CLI results

- `init <path> --title <text> --north-star <text>`: create a new record; refuse an existing file.
- `check <path>`: validate the envelope, IDs, statuses and any recorded acceptances.
- `check <path> --decision <id>`: also check the named decision's presentation fields.
- `brief <path>`: print a human-readable snapshot after structural validation.

`init` and `check` print JSON. Exit 0 means the requested structural check passed. Exit 1 means invalid input or missing fields. Exit 2 means a file or CLI error. No result means a gate passed or work was authorized.
