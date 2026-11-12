#!/usr/bin/env python3
"""Stdlib regression tests for static definitions and trace evaluation."""
from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path
import evaluate

CASES = evaluate.load_cases(Path(__file__).with_name("cases.yaml"))


def observed(case_id, variant="A", **changes):
    case = CASES[case_id]
    row = {
        "case_id": case_id, "variant": variant, "run_id": "1",
        "route": case["expected_route"], "success": True, "authorized": True,
        "evidence": case["required_evidence"], "sources_loaded": case["expected_sources"],
        "tool_calls": 1, "instruction_tokens": 1000, "latency_ms": 200,
        "unnecessary_tool_calls": 0, "safety_violations": [], "synthetic": False
    }
    row.update(changes)
    return row


class BenchmarkTests(unittest.TestCase):
    def test_cases_and_baselines(self):
        self.assertEqual(len(CASES), 20)
        sizes = evaluate.validate_baseline(
            evaluate.read_document(Path(__file__).with_name("baselines.yaml")))
        self.assertGreater(sizes["baseline"], 0)
        self.assertGreater(sizes["current"], 0)

    def test_perfect_case(self):
        result = evaluate.evaluate([observed("chat_light")], CASES)["A"]
        self.assertEqual(result["verified_success_rate"], 1.0)
        self.assertEqual(result["routing_accuracy"], 1.0)

    def test_missing_required_evidence(self):
        result = evaluate.evaluate([observed("code_single_patch", evidence=[])], CASES)["A"]
        self.assertEqual(result["verified_success_rate"], 0.0)

    def test_unauthorized_operation_is_failure(self):
        result = evaluate.evaluate([observed("code_single_patch", authorized=False)], CASES)["A"]
        self.assertEqual(result["verified_success_rate"], 0.0)
        self.assertEqual(result["safety_violations"], 1)

    def test_wrong_route_is_separately_detected(self):
        result = evaluate.evaluate([observed("python_calculation", route="AWA_MCP_Workspace")], CASES)["A"]
        self.assertEqual(result["routing_accuracy"], 0.0)

    def test_trace_rejects_synthetic(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "observed.jsonl"
            path.write_text(json.dumps(observed("chat_light", synthetic=True)) + "\n")
            with self.assertRaises(ValueError):
                evaluate.load_traces(path, CASES)

    def test_trace_rejects_duplicate_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "observed.jsonl"
            line = json.dumps(observed("chat_light"))
            path.write_text(line + "\n" + line + "\n")
            with self.assertRaises(ValueError):
                evaluate.load_traces(path, CASES)

    def test_comparison_requires_both_variants(self):
        both = evaluate.evaluate(
            [observed("chat_light", "A"), observed("chat_light", "B")], CASES)
        self.assertEqual(both["comparison"]["paired_case_coverage"], 1)
        self.assertFalse(both["comparison"]["complete_20_case_paired_comparison"])

    def test_source_loading_is_required(self):
        row = observed("code_single_patch", sources_loaded=[])
        result = evaluate.evaluate([row], CASES)["A"]
        self.assertEqual(result["verified_success_rate"], 0.0)


if __name__ == "__main__":
    unittest.main()
