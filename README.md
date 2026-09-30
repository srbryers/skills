# skills

Sebastian's reusable skills library. Each skill is a folder with a `SKILL.md`
(playbook) plus its scripts — the same format Muse reads natively, so anything
here works across all his projects with no conversion.

## Layout

```
skills/<name>/
  SKILL.md        # what it does, how to use it
  bin/            # scripts the skill runs
  references/     # schemas, docs (optional)
```

## Skills

- **typesafe** — call Jev (TypeSafe System One) to classify text with typed
  questions. `bin/jev.py ask` posts a state plus `choice`/`score`/`noul`
  questions to `https://api.typesafe.ai/v1/systemone`.
- **visual-review** — two-layer visual gate for UI work: cheap pixel-diff
  screenshot baselines per story catch regressions, then Jev judges new/changed
  screens semantically from extracted layout facts. Born from the Prelude
  paywall wordmark incident.
- **exercise-form-review**: blind visual QA for exercise demo keyframes and
  clips against the program's form cues and a locked style spec. The judge is
  never told what flaws are suspected.

## Install in Pi

```bash
pi install git:github.com/srbryers/skills
```

Pi loads each `skills/<name>/SKILL.md` from its frontmatter. The Jev calls
still need the hatch host's credential helper and the `custom.typesafe`
connector, so on other hosts the skills load but their Jev steps fail.

## Roadmap

- Migrate working skills here as they prove out (visual-review first).
- One day: publish the catalog as an area on showerthoughts.dev. Skills are
  markdown + scripts, so the site render is a static build over this repo.

## Conventions

- Skills stay generic: no hard-coded personal paths. Project-specific config
  goes in environment or arguments.
- Credentials never live in this repo. Skills reference connector names
  (e.g. `custom.typesafe`); the host injects them at runtime.
