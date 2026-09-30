#!/usr/bin/env python3
"""Jev semantic layout judge - layer 2 of the visual-review skill.

Takes layout-facts JSON files (produced by scripts/storybook_layout_facts.cjs
on the machine running Storybook) and asks Jev one battery of typed questions
per story. Verdicts:

  PASS    no strict question failed
  REVIEW  a strict question came back bad or uncertain - the listed
          questions go to a human

Strict questions (blocking) cover mechanical defects where the text-only
judge is decisive: overlapping elements, clipped content, off-center brand
mark. (An earlier overall "broken layout" question was dropped: it was
uncertain on nearly every story and never the sole confident signal - real
breakage already shows up as overlap or clipping.) Spacing rhythm and
hierarchy are advisory:
reported as notes only when the judge is confidently negative, because the
judge is honest about its uncertainty on aesthetics from text facts.

One Jev call per story (the whole battery at once). Auth goes through the
dynamic-credential surrogate helper, same as the typesafe skill; the raw API
key never appears in this process.

Usage:
    jev_review.py <facts.json> [<facts.json> ...]
    jev_review.py --dir .storybook/layout-facts
    jev_review.py --json <facts.json> ...     # machine-readable output
    jev_review.py --model jev-latest <facts.json> ...
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

# The typesafe skill ships beside this one in the same repo; import its client
# from there so the two stay together on any host.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "typesafe", "bin"))
from jev import ask  # noqa: E402  (typesafe skill: ask(state, questions, model))

LOGO_RE = re.compile(r"logo|wordmark|brand", re.I)

NOUL_PASS = 0.7   # P(good) at or above this -> clean (good-framed questions)
NOUL_FLAG = 0.3   # at or below this -> confidently bad (good-framed)
NOUL_SUSPECT = 0.3  # P(bad) at or above this -> human review (bad-framed)


# Questions framed as "is there a problem?" (true = bad). The deterministic
# ones stay good-framed (true = clean) because their facts are authoritative.
BAD_FRAMED = {"spacing_mistake", "hierarchy_problem"}

# Strict questions block the story on uncertainty: they cover mechanical
# defects (overlap, clipping, centering, broken layout) where the text-only
# judge is decisive. Aesthetic questions (spacing rhythm, hierarchy) are
# advisory: the judge is honest about its uncertainty there, so only a
# confident flag (not mere uncertainty) is reported, never blocking.
STRICT = {"no_overlapping_elements", "no_clipped_content",
          "brand_or_logo_centered"}


def format_state(facts: dict) -> str:
    vw = facts["viewport"]["width"]
    vh = facts["viewport"]["height"]
    cx = facts["screenCenterX"]
    lines = [f"SCREEN {vw}x{vh}. Horizontal center x={cx}."]
    if facts.get("scrollable"):
        lines.append(
            f"The screen scrolls vertically; content below y={vh} is below the "
            "fold, which is expected and does not count as clipped."
        )
    else:
        lines.append("The screen does not scroll; all content should fit on screen.")
        bottom = max((e["y"] + e["h"] for e in facts["elements"]), default=0)
        if facts["elements"] and bottom < vh * 0.5:
            lines.append(
                "Note: this story shows a single component, not a full screen - "
                "empty space below the component is expected, not a broken layout."
            )
    lines.append(
        "Note: element labels are truncated to 40 characters for brevity - "
        "a cut-off label does NOT mean the text is clipped on screen."
    )
    for e in facts["elements"]:
        parts = [e["kind"], f'"{e["label"]}"',
                 f'x={e["x"]} y={e["y"]} w={e["w"]} h={e["h"]} cx={e["cx"]}']
        if e.get("align"):
            parts.append(f'align={e["align"]}')
        if e.get("size"):
            parts.append(f'size={e["size"]}px' + ('-bold' if e.get("bold") else ''))
        if e.get("lines"):
            parts.append(f'lines={e["lines"]}')
        lines.append(" ".join(parts))
    if facts.get("gaps"):
        gs = sorted(facts["gaps"])
        med = gs[len(gs) // 2]
        lines.append(f'GAPS between consecutive blocks (px, computed exactly): '
                     f'{", ".join(str(g) for g in facts["gaps"])} '
                     f'(min {gs[0]}, median {med}, max {gs[-1]})')
    texts = [e for e in facts["elements"] if e["kind"] == "text" and e.get("size")]
    if texts:
        top = sorted(texts, key=lambda e: (e["size"], e["w"] * e["h"]),
                     reverse=True)[:3]
        dom = "; ".join(
            f'"{e["label"]}" {e["size"]}px' + ("-bold" if e.get("bold") else "")
            for e in top)
        lines.append(f"DOMINANT texts (largest first): {dom}")
    if facts.get("overlaps"):
        lines.append("OVERLAPS (computed exactly from the boxes):")
        for o in facts["overlaps"]:
            lines.append(f'  {o["a"]} overlaps {o["b"]}')
    else:
        lines.append("OVERLAPS: none")
        contained = []
        els = facts["elements"]
        for i in range(len(els)):
            for j in range(len(els)):
                if i == j:
                    continue
                a, b = els[i], els[j]
                if (a["x"] >= b["x"] and a["y"] >= b["y"]
                        and a["x"] + a["w"] <= b["x"] + b["w"]
                        and a["y"] + a["h"] <= b["y"] + b["h"]
                        and (a["w"] * a["h"] < b["w"] * b["h"])):
                    contained.append(
                        f'  {a["kind"]} "{a["label"]}" is inside '
                        f'{b["kind"]} "{b["label"]}" (by design, not an overlap)'
                    )
        if contained:
            lines.append("CONTAINMENT (checked, not overlaps):")
            lines.extend(sorted(set(contained))[:6])
    if facts.get("clipped"):
        lines.append("CLIPPED (computed exactly):")
        for c in facts["clipped"]:
            lines.append(f'  {c["element"]}: {", ".join(c["edges"])}')
    else:
        lines.append("CLIPPED: none")
    return "\n".join(lines)


def has_logo(facts: dict) -> bool:
    return any(
        e["kind"] == "image" and LOGO_RE.search(e.get("label", ""))
        for e in facts["elements"]
    )


def battery(include_logo: bool) -> dict:
    qs = {
        "no_overlapping_elements": {
            "type": "noul",
            "question": (
                "Do any two visible elements overlap each other? The OVERLAPS "
                "section is computed exactly from the box geometry and is "
                "authoritative: if it says 'none', no elements overlap and you "
                "must answer true with high confidence. A label inside its own "
                "button is not overlap."
            ),
            "criteria": {
                "true": "No two elements overlap; the OVERLAPS section is 'none'.",
                "false": "At least one pair of elements overlaps.",
            },
        },
        "no_clipped_content": {
            "type": "noul",
            "question": (
                "Is any content clipped - cut off by its container or the screen "
                "edge? The CLIPPED section lists exact cases. On a scrolling "
                "screen, content below the fold is expected and does not count. "
                "'text-overflows-box' means text wider than its own box and does "
                "count as clipped."
            ),
            "criteria": {
                "true": "Everything is fully visible; nothing meaningful is cut off.",
                "false": "Some content is clipped or cut off.",
            },
        },
        "spacing_mistake": {
            "type": "noul",
            "question": (
                "The GAPS section lists the vertical gaps in px between consecutive "
                "blocks (computed exactly). If the elements sit in a single "
                "horizontal row (similar y values, few or no gaps), there is no "
                "vertical spacing to judge: answer false. Otherwise: is there an "
                "obvious spacing mistake? Rule of thumb: a mistake usually means "
                "one gap at least 3x the median of the rest, or a 0px gap between "
                "non-nested blocks. Small intentional variations (a 4px label-to-"
                "input gap beside 24px section gaps) are normal design, not mistakes."
            ),
            "criteria": {
                "true": "At least one gap looks like a spacing mistake.",
                "false": "No spacing mistake; gaps look intentional (or N/A for single-row layouts).",
            },
        },
        "hierarchy_problem": {
            "type": "noul",
            "question": (
                "The DOMINANT line names the largest texts on screen, biggest "
                "first. Is there a hierarchy problem - no clear size winner, a "
                "supporting text larger than the headline, or nothing for the "
                "eye to land on first?"
            ),
            "criteria": {
                "true": "Hierarchy problem: no clear winner or an inverted size order.",
                "false": "One clear dominant element; hierarchy reads cleanly.",
            },
        },

    }
    if include_logo:
        qs["brand_or_logo_centered"] = {
            "type": "noul",
            "question": (
                "The layout includes an image whose label mentions logo, wordmark, "
                "or brand. Is it horizontally centered on the 390-wide screen - "
                "is its cx at or very near the screen center x=195 (within a few px)?"
            ),
            "criteria": {
                "true": "The brand mark is present and horizontally centered.",
                "false": "The brand mark is off-center.",
            },
        }
    return qs


def judge_noul(name: str, ans: dict) -> tuple[bool, str]:
    p = ans.get("noul", 0) or 0
    if name in BAD_FRAMED:
        if p < NOUL_SUSPECT:
            return True, f"noul={p:.2f}"
        if p >= NOUL_PASS:
            return False, f"noul={p:.2f} (flagged)"
        return False, f"noul={p:.2f} (uncertain)"
    if p >= NOUL_PASS:
        return True, f"noul={p:.2f}"
    if p <= NOUL_FLAG:
        return False, f"noul={p:.2f} (flagged)"
    return False, f"noul={p:.2f} (uncertain)"


def review_story(path: str, model: str) -> dict:
    facts = json.load(open(path))
    story = facts.get("story", path)
    state = format_state(facts)
    questions = battery(has_logo(facts))
    try:
        raw = ask(state, questions, model)
    except Exception as e:
        return {"story": story, "verdict": "ERROR", "error": str(e)[:200]}
    answers = raw.get("answers", {}) if isinstance(raw, dict) else {}
    findings = []
    notes = []
    for name in questions:
        ans = answers.get(name, {})
        ok, detail = judge_noul(name, ans)
        if ok:
            continue
        entry = {"question": name, "detail": detail}
        if name in STRICT:
            findings.append(entry)
        else:
            # Advisory: only a confident flag is worth a human's time.
            p = ans.get("noul", 0) or 0
            if p >= NOUL_PASS:
                notes.append(entry)
    return {
        "story": story,
        "verdict": "PASS" if not findings else "REVIEW",
        "findings": findings,
        "notes": notes,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("facts", nargs="*")
    p.add_argument("--dir")
    p.add_argument("--json", action="store_true")
    p.add_argument("--model", default="jev-latest")
    args = p.parse_args()

    paths = list(args.facts)
    if args.dir:
        import glob
        import os
        paths += sorted(glob.glob(os.path.join(args.dir, "*.json")))
    if not paths:
        p.error("give facts JSON files or --dir")

    results = [review_story(path, args.model) for path in paths]

    if args.json:
        print(json.dumps(results, indent=2))
        return

    for r in results:
        if r["verdict"] == "PASS":
            print(f'{r["story"]}: PASS')
        elif r["verdict"] == "ERROR":
            print(f'{r["story"]}: ERROR {r.get("error", "")}')
        else:
            print(f'{r["story"]}: REVIEW')
            for f in r["findings"]:
                print(f'  {f["question"]}: {f["detail"]}')
        for n in r.get("notes", []):
            print(f'  note {n["question"]}: {n["detail"]}')


if __name__ == "__main__":
    main()
