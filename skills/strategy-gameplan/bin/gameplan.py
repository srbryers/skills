#!/usr/bin/env python3
"""Create and inspect portable strategy records; never grant approval."""

import argparse
import json
from pathlib import Path
import sys

SCHEMA = "strategy-gameplan.v1"
STATUSES = {"exploring", "proposed", "accepted", "rejected", "deferred"}
GATE_FIELDS = (
    "unlocks", "owner", "evidence_needed", "acceptance", "pass_action",
    "fail_action", "inconclusive_action", "reuse", "reopen_if",
)
STEP_FIELDS = ("outcome", "owner", "scope", "limits", "acceptance", "finish")


def has_text(value):
    return isinstance(value, str) and bool(value.strip())


def text_fields(obj, fields, label, errors):
    if not isinstance(obj, dict):
        errors.append(f"{label} must be an object")
        return
    for field in fields:
        if not has_text(obj.get(field)):
            errors.append(f"{label}.{field} needs nonempty text")


def object_list(obj, field, label, errors):
    value = obj.get(field)
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        errors.append(f"{label}.{field} must be a list of objects")
        return []
    return value


def unique_ids(items, label, errors):
    seen = set()
    for item in items:
        ident = item.get("id")
        if not has_text(ident):
            errors.append(f"{label} entries need a nonempty id")
        elif ident in seen:
            errors.append(f"{label} has duplicate id: {ident}")
        else:
            seen.add(ident)
    return seen


def check_record(record, decision_id=None):
    errors = []
    if not isinstance(record, dict):
        return ["Session must be a JSON object"]
    if record.get("schema") != SCHEMA:
        errors.append(f"schema must be {SCHEMA}")
    text_fields(record, ("title", "north_star"), "session", errors)
    if "mission" in record:
        mission = record["mission"]
        if not isinstance(mission, dict):
            errors.append("mission must be an object")
        else:
            status = mission.get("status")
            if not isinstance(status, str) or status not in {"exploring", "proposed", "accepted"}:
                errors.append("mission.status must be exploring, proposed or accepted")
            if status in ("proposed", "accepted"):
                text_fields(mission, ("statement",), "mission", errors)
            if status == "accepted":
                text_fields(mission.get("owner_receipt"), ("by", "source"), "mission.owner_receipt", errors)
    for field in ("criteria", "position", "actors", "routes"):
        items = object_list(record, field, "session", errors)
        if field == "position":
            for index, item in enumerate(items):
                if item.get("kind") == "observed":
                    evidence = item.get("evidence")
                    if not isinstance(evidence, list) or not evidence or not all(map(has_text, evidence)):
                        errors.append(f"position[{index}] observed claim needs evidence references")
    decisions = object_list(record, "decisions", "session", errors)
    unique_ids(decisions, "decisions", errors)
    found = False
    for decision in decisions:
        label = f"decision[{decision.get('id', '?')}]"
        text_fields(decision, ("question", "status"), label, errors)
        status = decision.get("status")
        if not isinstance(status, str) or status not in STATUSES:
            errors.append(f"{label}.status must be one of {', '.join(sorted(STATUSES))}")
        options = object_list(decision, "options", label, errors)
        option_ids = unique_ids(options, f"{label}.options", errors)
        for option in options:
            text_fields(option, ("action",), f"{label}.option", errors)
        for field in ("recommendation", "selected"):
            value = decision.get(field)
            if value is not None and (not has_text(value) or value not in option_ids):
                errors.append(f"{label}.{field} must reference an option id")
        if status == "accepted":
            if not has_text(decision.get("selected")):
                errors.append(f"{label}.selected is required for an accepted decision")
            text_fields(decision.get("owner_receipt"), ("by", "source"), f"{label}.owner_receipt", errors)
        if decision_id is not None and decision.get("id") == decision_id:
            found = True
            if len(options) < 2 and not has_text(decision.get("alternatives_limited_because")):
                errors.append(f"{label} needs alternatives or alternatives_limited_because")
            if not options:
                errors.append(f"{label} needs at least one option")
            text_fields(decision, ("recommendation", "rationale", "strongest_objection", "research_stop"), label, errors)
            for option in options:
                text_fields(option, ("upside", "downside", "commitment", "reversibility"), f"{label}.option[{option.get('id', '?')}]", errors)
            text_fields(decision.get("gate"), GATE_FIELDS, f"{label}.gate", errors)
            text_fields(decision.get("next_step"), STEP_FIELDS, f"{label}.next_step", errors)
    if decision_id is not None and not found:
        errors.append(f"Decision not found: {decision_id}")
    return errors


def make_record(title, north_star):
    return dict(schema=SCHEMA, title=title, north_star=north_star,
                criteria=[], position=[], actors=[], routes=[], decisions=[])


def brief(record):
    lines = [f"# {record['title']}", "", "> " + record["north_star"], ""]
    if "mission" in record:
        lines.extend(["## Mission", "", "```json",
                      json.dumps(record["mission"], ensure_ascii=False, indent=2), "```", ""])
    for section in ("criteria", "position", "actors", "routes"):
        lines.extend([f"## {section.capitalize()}", ""])
        for item in record[section]:
            lines.extend(["```json", json.dumps(item, ensure_ascii=False, indent=2), "```", ""])
        if not record[section]:
            lines.extend(["Not recorded yet.", ""])
    lines.extend(["## Decisions", ""])
    for item in record["decisions"]:
        lines.extend([f"### {item['id']}: {item['question']}", "", f"Recorded status: {item['status']}", ""])
        for option in item["options"]:
            lines.append(f"- {option['id']}: {option['action']}")
        lines.extend(["", f"Recommendation: {item.get('recommendation') or 'Not recorded'}",
                      f"Selected option: {item.get('selected') or 'Not recorded'}", ""])
        for field in ("rationale", "strongest_objection", "research_stop", "owner_receipt", "gate", "next_step"):
            if field in item:
                lines.extend([f"**{field.replace('_', ' ').capitalize()}**", "",
                              "```json", json.dumps(item[field], ensure_ascii=False, indent=2), "```", ""])
    lines.append("This snapshot reports recorded decisions. It does not verify evidence or authorize execution.")
    return "\n".join(lines) + "\n"


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Create a session without overwriting files")
    init.add_argument("path", type=Path)
    init.add_argument("--title", required=True)
    init.add_argument("--north-star", required=True)
    check = commands.add_parser("check", help="Check record structure or decision completeness")
    check.add_argument("path", type=Path)
    check.add_argument("--decision")
    show = commands.add_parser("brief", help="Print a Markdown snapshot")
    show.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            record = make_record(args.title, args.north_star)
            errors = check_record(record)
            if errors:
                emit({"valid": False, "errors": errors})
                return 1
            with args.path.open("x", encoding="utf-8", newline="\n") as stream:
                json.dump(record, stream, ensure_ascii=False, indent=2)
                stream.write("\n")
            emit({"created": str(args.path), "schema": SCHEMA})
            return 0
        record = json.loads(args.path.read_text(encoding="utf-8-sig"))
        errors = check_record(record, getattr(args, "decision", None))
        if errors or args.command == "check":
            emit({"valid": not errors, "errors": errors,
                  "scope": "decision_completeness" if getattr(args, "decision", None) else "record_structure",
                  "approval": "not_evaluated", "evidence_truth": "not_evaluated"})
            return 1 if errors else 0
        print(brief(record), end="")
        return 0
    except (OSError, ValueError) as error:
        emit({"valid": False, "error": str(error)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
