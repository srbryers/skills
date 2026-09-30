---
name: exercise-form-review
description: Blind visual QA for exercise demo keyframes and clips, judged against the program's form cues and a locked style spec without hinting at suspected flaws. Use when gating generated fitness keyframes or clips before video rendering, or when calibrating the judge against human taste.
compatibility: The Jev judge needs the typesafe skill's credential helper and the custom.typesafe connector, which exist only on the hatch host.
---

# exercise-form-review

Blind visual QA for exercise demo keyframes and clips. A reviewer who can see
images judges each asset against the program's form cues and a locked style
guide, WITHOUT being told what anyone suspects is wrong. Built to gate
keyframes before video rendering, and to calibrate the judge against human
taste before trusting it.

## The blindness rule

This is the whole skill. The reviewer receives:

- the asset (keyframe image, or a contact sheet of frames for a clip)
- the exercise name and, for keyframes, the phase (start = bottom/rest, end = top)
- the program's form cues for that exercise
- the locked style/identity spec below

The reviewer is NEVER told: what flaws are suspected, which assets are
known-good, what a previous reviewer said, or what the human disliked. Brief
the reviewer with "evaluate only against the spec below and report every
deviation you actually see." If you catch yourself hinting at the suspected
flaw, the test is void.

## Locked style/identity spec (fitness coach series)

- Fortnite-like stylized 3D game character: slightly exaggerated proportions,
  smooth clean sculpted surfaces, polished game-style face. Not photorealistic,
  not claymation, not a cartoon.
- Identity: athletic man in his mid-30s, short dark hair, olive-green T-shirt,
  black athletic shorts, black sneakers. Same face in every asset.
- Dark upscale gym, black rubber floor, sparse real-looking equipment. The
  coach is correctly positioned on/against the equipment.
- No text, no logos, no brand names, no edge stretching, no cluttered
  background. Both implements fully inside the frame with clear margins.

## Rubric — keyframes

Score each axis PASS/FLAG, then give an overall verdict.

1. **identity** — same character as the spec (face, hair, wardrobe)?
2. **style** — the stylized 3D look, not photoreal or clay?
3. **scene** — right equipment for the exercise, dark gym, sparse background?
4. **pose** — does the body position match the phase AND the program cues?
   Quote the cue it breaks, if any.
5. **implements** — every implement visible, whole, inside the frame, and a
   sensible count (two dumbbells means two, not three)? Carve-out: a barbell
   shaft may run past the frame edges in the vertical crop — flag it only
   if a hand, plate, or collar is cut off. Dumbbells, cables, and ropes
   must be whole and inside the frame.
6. **anatomy** — no extra/missing/warped limbs, hands and feet plausible,
   equipment not melted or fused to the body?
7. **framing** — full body in frame with margin, nothing important touching
   the edges?

## Rubric — clips (judge a contact sheet of 6-8 evenly spaced frames)

All seven keyframe axes, judged across the frames, plus:

8. **motion** — the rep reads correctly: full range of motion per the cues,
   no teleporting between positions?
9. **loop** — the last frame returns to the first pose with no visible jump?
10. **stability** — equipment doesn't morph, the background doesn't flicker,
    the character doesn't change clothes mid-rep?

## Verdict format

One JSON object per asset:

```json
{
  "asset": "<filename>",
  "exercise": "<name>",
  "verdict": "PASS",
  "flags": [
    {"axis": "pose", "what": "knees cave inward at the bottom",
     "spec": "program cue: knees tracking over the toes"}
  ]
}
```

`verdict` is `PASS` only when every axis passes. Otherwise `FLAG`, with one
entry per deviation: what you see, in plain words, and which spec line it
breaks. No scores, no hedging, no praise. If an axis can't be judged from the
asset (e.g. loop from a single keyframe), mark it `n/a`, never a guess.

## Calibration procedure

To test whether the judge sees what a human sees:

1. Assemble a set mixing assets the human has flagged and hasn't flagged,
   plus at least one known-good control. Do not label them.
2. Brief reviewers with the blindness rule. Use a fresh reviewer per asset
   (or per small batch) so one verdict can't anchor the next.
3. Collect the verdict JSONs, THEN compare against the human's notes.
4. A useful judge flags the human's issues and stays quiet on the control.
   If it flags the control, the rubric is too strict. If it misses the
   human's issues, the rubric or the reviewer needs work.

## Gating keyframes before video

Once calibrated: every keyframe pair goes through the judge before any
render is launched. A FLAGged pair goes back for regeneration (reword the
prompt, up to 2 retries). Renders only launch on PASSed pairs. The judge's
verdict JSON is saved next to the keyframes as the audit trail.

## Two-layer scripted flow (mirrors the visual-review skill)

The one-shot blind review above is layer 1+2 in a single reviewer. For
repeatable gating, split it the way `visual-review` splits pixel facts from
the Jev judge — because the TypeSafe endpoint takes no image input:

**Layer 1 — visual facts extraction** (needs a vision-capable reviewer).
Brief per `references/extraction-brief.md`: the reviewer looks at the asset
and writes plain-text observations to the schema in
`references/facts-schema.json`. Facts only — no verdicts, no PASS/FLAG
language. The blindness rule still applies: the extractor is never told what
is suspected.

**Layer 2 — Jev judge** (scripted, runs on the agent host).
`bin/jev_judge.py` sends the facts plus the program cues to Jev as one
battery of `noul` questions per asset — all strict, blocking on uncertainty:

| question | what it checks |
|---|---|
| `identity_ok` | face, hair, wardrobe match the locked identity |
| `style_ok` | stylized 3D look; not photoreal, not claymation |
| `scene_ok` | dark gym, right equipment, sparse, no text/logos |
| `pose_ok` | pose matches the phase and every program cue |
| `implements_ok` | right count and position; whole (barbell shaft may exit frame) |
| `anatomy_ok` | no warped/missing/fused limbs or bad hands/feet |
| `framing_ok` | full body in frame with clear margins |
| `motion_ok` (clips) | full range of motion per cues, no teleporting |
| `loop_ok` (clips) | last frame returns to the first with no jump |
| `stability_ok` (clips) | equipment, background, wardrobe stable |

```bash
bin/jev_judge.py <facts.json> [<facts.json> ...]
bin/jev_judge.py --dir <facts-dir>
bin/jev_judge.py --json ...   # machine-readable
```

Verdict `PASS` only when every question comes back clean; otherwise `FLAG`
with the failed questions listed. Only the facts JSONs are judged — the
TypeSafe credential never leaves the agent host.

## Calibration record (2026-09-30)

Four blind reviewers, 33 verdicts over 12 exercises (11 finished + the
approved press as control). The judge independently caught the Bulgarian
split squat (step-up pattern, shallow bob) and the dead bug (opposite
arm-and-leg extension never reads), flagged a start/end label swap on the
fly keyframes, and stayed quiet on the approved press control and five other
clean exercises. The barbell carve-out above came from this round: the
strict "implements fully inside the frame" line flagged two otherwise-clean
barbell keyframes for shaft cropping that is near-unavoidable in the
vertical crop.

## Known limits

- The judge reads pixels, not biomechanics: it checks the pose against
  written cues, it doesn't measure joint angles.
- Contact sheets can hide brief mid-rep glitches; for a disputed clip, judge
  more frames.
- A PASS is not a human approval. The judge is a filter, not a verdict.
