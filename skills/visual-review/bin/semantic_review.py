#!/usr/bin/env python3
"""End-to-end semantic layout review (layer 2 of the visual-review skill).

Runs on the agent host. Drives the machine that runs Storybook through a
remote-execution helper (default: ~/workspace/bin/macstudio):

  1. <pm> run ui:visual                 pixel gate, writes report.json
  2. read NEW/CHANGED story ids from the report
  3. <pm> run ui:layout-facts -- --changed
  4. fetch those facts files locally
  5. run the Jev judge (jev_review.py) on each

Exit 0: no changed stories, or every changed story PASSes.
Exit 1: any story needs human REVIEW, or a step failed.

Usage:
    semantic_review.py --repo ~/Development/<project> [--pm npm|pnpm]
                       [--skip-visual] [--studio ~/workspace/bin/macstudio]

--repo is the project checkout on the Studio. --pm is its package manager.
--skip-visual reuses the latest report.json instead of re-running screenshots.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

SKILL_BIN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_BIN)
from jev_review import review_story  # noqa: E402

ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def studio(cmd: str, args) -> str:
    """Run a shell command on the Studio; return stdout. Raises on failure."""
    full = f"export PATH=/opt/homebrew/bin:/usr/bin:/bin && cd {args.repo} && {cmd}"
    p = subprocess.run([args.studio, full], capture_output=True, text=True,
                       timeout=1800)
    if p.returncode != 0:
        raise RuntimeError(f"studio command failed: {cmd}\n{p.stderr[-2000:]}")
    return p.stdout


def changed_story_ids(args) -> list[str]:
    out = studio(
        "python3 -c \"import json; r=json.load(open('.storybook/visual-diffs/report.json')); "
        "print(chr(10).join(x['id'] for x in r['results'] "
        "if x['status'] in ('NEW','CHANGED')))\"",
        args,
    )
    ids = [i.strip() for i in out.splitlines() if i.strip()]
    bad = [i for i in ids if not ID_RE.match(i)]
    if bad:
        raise RuntimeError(f"unexpected story ids from report: {bad}")
    return ids


def fetch_facts(args, ids: list[str], dest: str) -> list[str]:
    paths = []
    for sid in ids:
        out = studio(f"cat .storybook/layout-facts/{sid}.json", args)
        # sanity: must be JSON with the right story id
        facts = json.loads(out)
        if facts.get("story") != sid:
            raise RuntimeError(f"facts file mismatch for {sid}")
        path = os.path.join(dest, f"{sid}.json")
        with open(path, "w") as f:
            f.write(out)
        paths.append(path)
    return paths


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-visual", action="store_true",
                    help="reuse the latest pixel-gate report instead of re-running it")
    ap.add_argument("--repo", required=True,
                    help="project checkout on the Studio, e.g. ~/Development/<project>")
    ap.add_argument("--pm", choices=("npm", "pnpm"), default="npm",
                    help="the project's package manager on the Studio")
    ap.add_argument("--studio", default=os.path.expanduser("~/workspace/bin/macstudio"))
    ap.add_argument("--model", default="jev-latest")
    args = ap.parse_args()

    if not args.skip_visual:
        print("layer 1: pixel gate on the Studio...", flush=True)
        # ui:visual exits 1 when stories changed - that is expected, not fatal.
        full = (f"export PATH=/opt/homebrew/bin:/usr/bin:/bin && cd {args.repo} "
                f"&& {args.pm} run ui:visual; echo VISUAL_EXIT=$?")
        p = subprocess.run([args.studio, full], capture_output=True, text=True,
                           timeout=1800)
        m = re.search(r"VISUAL_EXIT=(\d+)", p.stdout)
        if not m:
            print("pixel gate produced no exit marker; output was:")
            print(p.stdout[-2000:])
            print(p.stderr[-2000:])
            return 1
        tail = "\n".join(p.stdout.splitlines()[-12:])
        print(tail)

    ids = changed_story_ids(args)
    if not ids:
        print("no NEW or CHANGED stories - semantic review skipped.")
        return 0
    print(f"{len(ids)} new/changed stories: extracting layout facts...", flush=True)
    studio(f"{args.pm} run ui:layout-facts -- --changed >/dev/null 2>&1", args)

    with tempfile.TemporaryDirectory(prefix="layout-facts-") as tmp:
        paths = fetch_facts(args, ids, tmp)
        print(f"judging {len(paths)} stories with Jev...", flush=True)
        results = [review_story(path, args.model) for path in paths]

    failed = 0
    for r in results:
        if r["verdict"] == "PASS":
            print(f'{r["story"]}: PASS')
        elif r["verdict"] == "ERROR":
            failed += 1
            print(f'{r["story"]}: ERROR {r.get("error", "")}')
        else:
            failed += 1
            print(f'{r["story"]}: REVIEW')
            for f in r["findings"]:
                print(f'  {f["question"]}: {f["detail"]}')
        for n in r.get("notes", []):
            print(f'  note {n["question"]}: {n["detail"]}')

    if failed:
        print(f"\n{failed} of {len(results)} stories need human review.")
        return 1
    print(f"\nall {len(results)} changed stories PASS.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
