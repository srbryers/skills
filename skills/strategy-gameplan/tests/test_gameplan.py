"""Focused checks for destructive writes and misleading decision records."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "bin" / "gameplan.py"
SPEC = importlib.util.spec_from_file_location("gameplan", SCRIPT)
gameplan = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gameplan)


class GameplanTests(unittest.TestCase):
    def candidate(self):
        record = gameplan.make_record("Example strategy", "Preserve the user's exact goal.")
        record["decisions"] = [{
            "id": "D001", "question": "Build or buy the missing capability?", "status": "proposed",
            "options": [dict(id=ident, action=action, upside="Serves the next customer need.",
                             downside="Requires integration time.", commitment="One integration prototype.",
                             reversibility="Keep the current system until the prototype is accepted.")
                        for ident, action in (("build", "Build a prototype"), ("buy", "Try an existing product"))],
            "recommendation": "buy", "rationale": "Learn whether existing tools cover the need.",
            "strongest_objection": "The dependency may constrain future work.",
            "research_stop": "A failed integration would change the recommendation.",
            "gate": dict(zip(gameplan.GATE_FIELDS, (
                "Commit to integration", "Project owner", "One representative task and its failure case",
                "The task meets the current ticket's criteria", "Propose integration",
                "Investigate the missing capability", "Record what evidence is missing",
                "Carry unchanged contract evidence", "Reopen if the supplier contract changes"))),
            "next_step": dict(zip(gameplan.STEP_FIELDS, (
                "A representative task using the existing tool", "Implementation owner",
                "One integration path", "Existing project budget and permissions",
                "Meet the representative task's criteria", "Record the task result and dependency risk"))),
        }]
        return record

    def test_exploration_is_valid_without_approving_a_decision(self):
        record = gameplan.make_record("Exploration", "A user goal")
        self.assertEqual(gameplan.check_record(record), [])
        self.assertTrue(gameplan.check_record(record, "D001"))

    def test_mission_is_optional_visible_and_separates_acceptance_from_appeal(self):
        record = gameplan.make_record("Example", "Keep this North Star unchanged")
        self.assertEqual(gameplan.check_record(record), [])
        record["mission"] = {"status": "exploring", "resonance": "untested"}
        self.assertEqual(gameplan.check_record(record), [])
        record["mission"].update(status="proposed", statement="")
        self.assertTrue(gameplan.check_record(record))
        record["mission"].update(status="accepted", statement="A mission the founder chose")
        self.assertTrue(gameplan.check_record(record))
        record["mission"]["owner_receipt"] = {"by": "Owner", "source": "Fictional test receipt"}
        self.assertEqual(gameplan.check_record(record), [])
        rendered = gameplan.brief(record)
        self.assertIn("Keep this North Star unchanged", rendered)
        self.assertIn("A mission the founder chose", rendered)
        self.assertIn('"resonance": "untested"', rendered)
        record["mission"] = "A slogan without a record"
        self.assertTrue(gameplan.check_record(record))

    def test_incomplete_gate_cannot_be_presented_as_complete(self):
        record = self.candidate()
        self.assertEqual(gameplan.check_record(record, "D001"), [])
        for field in ("acceptance", "inconclusive_action", "reopen_if"):
            broken = copy.deepcopy(record)
            del broken["decisions"][0]["gate"][field]
            self.assertTrue(gameplan.check_record(broken, "D001"))

    def test_acceptance_needs_a_real_option_and_recorded_owner_source(self):
        record = self.candidate()
        decision = record["decisions"][0]
        decision.update(status="accepted", selected="buy")
        self.assertTrue(gameplan.check_record(record))
        decision["owner_receipt"] = {"by": "Owner", "source": "Example fixture, not a real approval"}
        self.assertEqual(gameplan.check_record(record), [])
        decision["selected"] = "missing"
        self.assertTrue(gameplan.check_record(record))

    def test_duplicate_ids_and_unsupported_facts_are_rejected(self):
        record = self.candidate()
        record["decisions"].append(copy.deepcopy(record["decisions"][0]))
        record["position"] = [{"claim": "The tool meets our needs", "kind": "observed", "evidence": []}]
        errors = gameplan.check_record(record)
        self.assertTrue(any("duplicate" in item for item in errors))
        self.assertTrue(any("evidence" in item for item in errors))

    def test_malformed_fields_report_errors(self):
        for bad in (None, [], {"schema": []}):
            self.assertTrue(gameplan.check_record(bad))
        record = self.candidate()
        record["decisions"][0].update(status=[], recommendation={})
        self.assertTrue(gameplan.check_record(record))

    def test_cli_preserves_existing_session_and_reports_its_limits(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "session.json"
            init = [sys.executable, str(SCRIPT), "init", str(path), "--title", "Example", "--north-star", "An exact goal"]
            first = subprocess.run(init, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            original = path.read_bytes()
            again = subprocess.run(init, capture_output=True, text=True)
            self.assertEqual(again.returncode, 2)
            self.assertEqual(path.read_bytes(), original)
            check = subprocess.run([sys.executable, str(SCRIPT), "check", str(path)], capture_output=True, text=True)
            self.assertEqual(check.returncode, 0)
            self.assertEqual(json.loads(check.stdout)["approval"], "not_evaluated")
            rendered = subprocess.run([sys.executable, str(SCRIPT), "brief", str(path)], capture_output=True, text=True)
            self.assertEqual(rendered.returncode, 0)
            self.assertIn("An exact goal", rendered.stdout)


if __name__ == "__main__":
    unittest.main()
