#!/usr/bin/env python3
"""Jev judge - layer 2 of the exercise-form-review skill.

Takes visual-facts JSON files (plain-text observations written by a blind
vision reviewer per references/extraction-brief.md; Jev cannot see images)
and asks Jev one battery of noul questions per asset. Verdicts:

  PASS    every question came back clean
  FLAG    a question came back bad or uncertain - the listed questions
          go to a human

All questions are strict (block on uncertainty): they cover mechanical,
checkable properties of the facts, the same posture as the visual-review
skill's strict layer. One Jev call per asset (the whole battery at once).
Auth goes through the dynamic-credential surrogate helper, same as the
typesafe skill; the raw API key never appears in this process.

Usage:
    jev_judge.py <facts.json> [<facts.json> ...]
    jev_judge.py --dir <facts-dir>
    jev_judge.py --json <facts.json> ...     # machine-readable output
    jev_judge.py --model jev-latest <facts.json> ...
    jev_judge.py --pair <start-facts.json> <end-facts.json>
        # pair-coherence check: do the two keyframes share one camera
        # viewpoint so a video morphed between them has no camera jump?
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys

sys.path.insert(0, "/home/hatch/workspace/skills/typesafe/bin")
from jev import ask  # noqa: E402  (typesafe skill: ask(state, questions, model))

NOUL_PASS = 0.7   # P(clean) at or above this -> clean
NOUL_FLAG = 0.3   # at or below this -> confidently bad


def format_state(facts: dict) -> str:
    kind = facts.get("kind", "keyframe")
    if kind == "keyframe-start":
        phase_note = (
            "This is a START keyframe: it must show the correct BEGINNING "
            "position of the movement. Program cues that describe the END of "
            "the movement or the motion itself (e.g. 'extend', 'curl toward', "
            "'push up') are satisfied by being in the right STARTING position "
            "- the frame must NOT show the end position. Only flag a cue if "
            "the start position itself contradicts it."
        )
    elif kind == "keyframe-end":
        phase_note = (
            "This is an END keyframe: it must show the correct END position "
            "of the movement. Program cues that describe the START of the "
            "movement are satisfied by having arrived at the right END "
            "position - the frame must NOT show the start position. Only flag "
            "a cue if the end position itself contradicts it."
        )
    else:
        phase_note = ""
    lines = [
        f'EXERCISE: {facts.get("exercise")}',
        f'ASSET KIND: {kind} ({"judge motion, loop, stability" if kind == "clip" else "judge the 7 keyframe axes only"})',
    ]
    if phase_note:
        lines.append(f"PHASE: {phase_note}")
    lines.append("PROGRAM CUES:")

    for c in facts.get("cues", []):
        lines.append(f"  - {c}")
    for field in ("identity", "style", "scene", "pose", "implements",
                  "anatomy", "framing", "motion", "loop", "stability"):
        val = facts.get(field)
        if val:
            lines.append(f"{field.upper()}: {val}")
    lines.append(
        "Note: the facts above are a reviewer's plain-text observations of "
        "the asset and are authoritative. Answer each question from the facts "
        "alone; do not infer beyond what is stated."
    )
    return "\n".join(lines)


def battery(is_clip: bool) -> dict:
    qs = {
        "identity_ok": {
            "type": "noul",
            "question": (
                "The IDENTITY facts describe the character's face, hair, and "
                "wardrobe. Do they match the locked identity: athletic man in "
                "his mid-30s, short dark hair, PLAIN olive-green T-shirt (no "
                "logo, graphic, or text), plain black athletic shorts, plain "
                "black sneakers, NO watch, NO wristband, NO accessories - the "
                "same character throughout? Any logo on the shirt, any "
                "accessory, or any non-plain wardrobe item is an automatic FAIL."
            ),
            "criteria": {
                "true": "Identity matches the spec on every stated element.",
                "false": "Face, hair, or wardrobe differs from the spec.",
            },
        },
        "style_ok": {
            "type": "noul",
            "question": (
                "The STYLE facts describe the render look. Is it the locked "
                "stylized 3D game-character look: slightly exaggerated "
                "proportions, smooth clean sculpted surfaces, polished "
                "game-style face - and NOT photorealistic, NOT claymation, "
                "NOT a cartoon?"
            ),
            "criteria": {
                "true": "The locked stylized 3D look; not photoreal or clay.",
                "false": "Photorealistic, claymation, or cartoon rendering.",
            },
        },
        "scene_ok": {
            "type": "noul",
            "question": (
                "The SCENE facts describe the setting and equipment. Is it a "
                "dark upscale gym with black rubber flooring, the correct "
                "equipment for the exercise, a sparse background, and NO "
                "text, logos, or brand names? If the facts mention posters, "
                "neon signs, graffiti, or any brand name (including the word "
                "Fortnite), that is an automatic FAIL."
            ),
            "criteria": {
                "true": "Dark gym, right equipment, sparse, no text/logos.",
                "false": "Wrong setting, wrong equipment, clutter, text/logos/branding present.",
            },
        },
        "pose_ok": {
            "type": "noul",
            "question": (
                "The POSE facts describe the body position against the stated "
                "phase and each program cue. Does the pose correctly show the "
                "STATED PHASE (start = beginning position, end = end position)? "
                "A start keyframe must NOT show the end of the movement, and an "
                "end keyframe must NOT show the start. Judge each cue against "
                "the phase: a cue is contradicted only if the phase position "
                "itself violates it."
            ),
            "criteria": {
                "true": "Pose correctly shows the stated phase; no cue is violated by the phase position itself.",
                "false": "Pose shows the wrong phase, or the phase position violates a cue.",
            },
        },
        "implements_ok": {
            "type": "noul",
            "question": (
                "The IMPLEMENTS facts describe the exercise implements. If the "
                "exercise is bodyweight-only (no implements in the cues), "
                "there is nothing to check and this passes. Otherwise: is "
                "every implement present in the right count, positioned per "
                "the cues, and whole? A barbell shaft MAY run past the frame "
                "edges - flag it only if a hand, plate, or collar is cut off. "
                "Dumbbells, cables, and ropes must be whole and inside the "
                "frame."
            ),
            "criteria": {
                "true": "Bodyweight (nothing to check), or implements correct in count, position, and wholeness (barbell shaft may exit frame).",
                "false": "Wrong count, mispositioned, or a cropped implement beyond the barbell carve-out.",
            },
        },
        "anatomy_ok": {
            "type": "noul",
            "question": (
                "The ANATOMY facts describe limbs, hands, and feet. Are there "
                "no glitches: correct limb count, plausible hands and feet, "
                "no warping, melting, or fusion with equipment?"
            ),
            "criteria": {
                "true": "No anatomy glitches of any kind.",
                "false": "Extra/missing/warped limbs, bad hands/feet, or fusion.",
            },
        },
        "framing_ok": {
            "type": "noul",
            "question": (
                "The FRAMING facts describe what is in frame. Is the full "
                "body in frame with clear margins - nothing important "
                "touching the edges?"
            ),
            "criteria": {
                "true": "Full body in frame with clear margins.",
                "false": "Body or something important is cut off or touches an edge.",
            },
        },
    }
    if is_clip:
        qs.update({
            "motion_ok": {
                "type": "noul",
                "question": (
                    "The MOTION facts describe the rep across the frames. "
                    "Does the clip show the full range of motion the cues "
                    "require, with no teleporting between positions?"
                ),
                "criteria": {
                    "true": "Full range of motion per the cues; continuous movement.",
                    "false": "Partial range, missing movement, or teleporting.",
                },
            },
            "loop_ok": {
                "type": "noul",
                "question": (
                    "The LOOP facts compare the last frame to the first. Does "
                    "the last frame return to the first pose with no visible "
                    "jump?"
                ),
                "criteria": {
                    "true": "Seamless loop; last frame matches the first.",
                    "false": "Visible jump between last and first frame.",
                },
            },
            "stability_ok": {
                "type": "noul",
                "question": (
                    "The STABILITY facts describe the scene across frames. Is "
                    "the equipment, background, and wardrobe stable - no "
                    "morphing equipment, no flickering background, no "
                    "wardrobe changes mid-rep?"
                ),
                "criteria": {
                    "true": "Stable across all frames.",
                    "false": "Morphing, flicker, or wardrobe change.",
                },
            },
        })
    return qs


def judge_noul(name: str, ans: dict) -> tuple[bool, str]:
    p = ans.get("noul", 0) or 0
    if p >= NOUL_PASS:
        return True, f"noul={p:.2f}"
    if p <= NOUL_FLAG:
        return False, f"noul={p:.2f} (flagged)"
    return False, f"noul={p:.2f} (uncertain)"


def pair_battery() -> dict:
    """Questions for the --pair coherence check (start facts vs end facts)."""
    return {
        "angle_match": {
            "type": "noul",
            "question": (
                "The CAMERA_ANGLE facts describe each keyframe's camera "
                "position. Do the START and END keyframes share the SAME "
                "viewpoint: the same side of the body facing the camera, the "
                "same front/side/three-quarter viewpoint, and a similar "
                "height? A video morphed between these two frames must not "
                "show a camera jump. A side view vs a three-quarter view, or "
                "a front-left vs a front-right view, is a MISMATCH even if "
                "the pose matches. A horizontally MIRRORED pair - one frame "
                "flipped left-right relative to the other, the subject facing "
                "the opposite direction - is also a MISMATCH."
            ),
            "criteria": {
                "true": "Both frames shot from the same camera position and viewpoint, same left-right orientation.",
                "false": "Different camera sides, viewpoints, heights, or a mirrored left-right flip - the video would visibly jump.",
            },
        },
    }


def format_pair_state(start: dict, end: dict) -> str:
    lines = [
        f'EXERCISE: {start.get("exercise")}',
        "PAIR-COHERENCE CHECK: compare the START keyframe's camera angle to "
        "the END keyframe's camera angle.",
        f'START CAMERA_ANGLE: {start.get("camera_angle", "(not recorded)")}',
        f'END CAMERA_ANGLE: {end.get("camera_angle", "(not recorded)")}',
        "Note: the facts above are a reviewer's plain-text observations and "
        "are authoritative. Answer from the facts alone; do not infer beyond "
        "what is stated. If either camera_angle is missing or too vague to "
        "compare, treat that as uncertain, not as a match.",
    ]
    return "\n".join(lines)


def review_pair(start_path: str, end_path: str, model: str) -> dict:
    start = json.load(open(start_path))
    end = json.load(open(end_path))
    state = format_pair_state(start, end)
    questions = pair_battery()
    try:
        raw = ask(state, questions, model)
    except Exception as e:
        return {
            "start": start.get("asset", start_path),
            "end": end.get("asset", end_path),
            "verdict": "ERROR",
            "error": str(e)[:200],
        }
    answers = raw.get("answers", {}) if isinstance(raw, dict) else {}
    findings = []
    for name in questions:
        ok, detail = judge_noul(name, answers.get(name, {}))
        if not ok:
            findings.append({"question": name, "detail": detail})
    return {
        "start": start.get("asset", start_path),
        "end": end.get("asset", end_path),
        "exercise": start.get("exercise"),
        "verdict": "PASS" if not findings else "FLAG",
        "findings": findings,
    }


def review_asset(path: str, model: str) -> dict:
    facts = json.load(open(path))
    asset = facts.get("asset", path)
    state = format_state(facts)
    questions = battery(facts.get("kind") == "clip")
    try:
        raw = ask(state, questions, model)
    except Exception as e:
        return {"asset": asset, "verdict": "ERROR", "error": str(e)[:200]}
    answers = raw.get("answers", {}) if isinstance(raw, dict) else {}
    findings = []
    for name in questions:
        ok, detail = judge_noul(name, answers.get(name, {}))
        if not ok:
            findings.append({"question": name, "detail": detail})
    return {
        "asset": asset,
        "exercise": facts.get("exercise"),
        "verdict": "PASS" if not findings else "FLAG",
        "findings": findings,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("facts", nargs="*")
    p.add_argument("--dir")
    p.add_argument("--json", action="store_true")
    p.add_argument("--model", default="jev-latest")
    p.add_argument("--pair", nargs=2, metavar=("START_FACTS", "END_FACTS"),
                   help="pair-coherence check on two facts files")
    args = p.parse_args()

    if args.pair:
        r = review_pair(args.pair[0], args.pair[1], args.model)
        if args.json:
            print(json.dumps(r, indent=2))
            return
        if r["verdict"] == "PASS":
            print(f'PAIR {r["exercise"]}: PASS (camera angles match)')
        elif r["verdict"] == "ERROR":
            print(f'PAIR {r["exercise"]}: ERROR {r.get("error", "")}')
        else:
            print(f'PAIR {r["exercise"]}: FLAG')
            for f in r["findings"]:
                print(f'  {f["question"]}: {f["detail"]}')
        return

    paths = list(args.facts)
    if args.dir:
        paths += sorted(glob.glob(os.path.join(args.dir, "*-facts.json")))
    if not paths:
        p.error("give facts JSON files or --dir")

    results = [review_asset(path, args.model) for path in paths]

    if args.json:
        print(json.dumps(results, indent=2))
        return

    for r in results:
        if r["verdict"] == "PASS":
            print(f'{r["asset"]}: PASS')
        elif r["verdict"] == "ERROR":
            print(f'{r["asset"]}: ERROR {r.get("error", "")}')
        else:
            print(f'{r["asset"]}: FLAG')
            for f in r["findings"]:
                print(f'  {f["question"]}: {f["detail"]}')


if __name__ == "__main__":
    main()
