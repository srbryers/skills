#!/usr/bin/env python3
"""Jev (TypeSafe System One) CLI for the stackdiff pipeline.

Sends a state plus typed questions to Jev and returns structured answers.
Auth goes through the dynamic-credential surrogate helper; the raw API key
never appears in this process.

Usage:
    jev.py ask --state "..." --questions '{"category": {"type": "choice", ...}}'
    jev.py ask --state "..." --questions-file questions.json
    echo '{"state": "...", "questions": {...}}' | jev.py ask --stdin
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
import dynamic_credentials as dc

ENDPOINT = "https://api.typesafe.ai/v1/systemone"
ALLOWED = ["api.typesafe.ai"]
CREDENTIAL = "custom.typesafe"


def ask(state, questions, model="jev-latest"):
    body = json.dumps({"state": state, "model": model,
                       "questions": questions}).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=body,
        headers={"Content-Type": "application/json",
                 "User-Agent": "stackdiff-pipeline"},
        method="POST",
    )
    dc.add_surrogate_to_request(req, CREDENTIAL, allowed_hosts=ALLOWED)
    try:
        with urllib.request.urlopen(req) as resp:
            return dc.read_json_response(resp)
    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8", "replace")[:500]
        except Exception:
            detail = ""
        raise SystemExit(f"TypeSafe API error {exc.code}: {detail}")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("ask")
    a.add_argument("--state")
    a.add_argument("--questions")
    a.add_argument("--questions-file")
    a.add_argument("--stdin", action="store_true")
    a.add_argument("--model", default="jev-latest")
    args = p.parse_args()

    if args.stdin:
        payload = json.load(sys.stdin)
        state, questions = payload["state"], payload["questions"]
        model = payload.get("model", args.model)
    else:
        state = args.state
        if args.questions_file:
            with open(args.questions_file) as f:
                questions = json.load(f)
        else:
            questions = json.loads(args.questions)
        model = args.model

    print(json.dumps(ask(state, questions, model), indent=2))


if __name__ == "__main__":
    main()
