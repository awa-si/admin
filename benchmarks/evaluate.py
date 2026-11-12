#!/usr/bin/env python3
"""Evaluate observed AWA Admin benchmark traces; never generate performance claims."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
REQUIRED = {"case_id", "variant", "run_id", "route", "success", "authorized", "evidence",
            "sources_loaded", "tool_calls", "instruction_tokens", "latency_ms",
            "unnecessary_tool_calls", "safety_violations", "synthetic"}


def read_document(path: Path):
    text = path.read_text(encoding="utf-8")
    # JSON is a strict YAML 1.2 subset. This deliberately avoids a YAML runtime dependency.
    return json.loads(text)


def load_cases(path: Path):
    doc = read_document(path)
    cases = doc["cases"]
    if len(cases) != 20 or len({c["id"] for c in cases}) != len(cases):
        raise ValueError("Expected 20 unique benchmark cases")
    allowed = {"chat", "research", "coding", "native", "github", "mcp",
               "mixed", "unknown", "authorization"}
    for case in cases:
        if case["category"] not in allowed or not case["prompt"] or not case["expected_route"]:
            raise ValueError("Incomplete case: " + str(case.get("id")))
        if case["mutation"] and not case["fixture_only"]:
            raise ValueError("Unsafe nonfixture mutation case: " + case["id"])
        if case["max_tool_calls"] < 0:
            raise ValueError("Invalid tool budget: " + case["id"])
    return {c["id"]: c for c in cases}


def validate_baseline(doc):
    for label in ("baseline", "current"):
        section = doc[label]
        if not section["ref"] or not section["files"]:
            raise ValueError("Missing " + label + " revision or inventory")
        for entry in section["files"]:
            if not entry["path"] or entry["characters"] < 1:
                raise ValueError("Invalid source baseline file")
    return {k: sum(x["characters"] for x in doc[k]["files"]) for k in ("baseline", "current")}


def load_traces(path: Path, cases: dict):
    traces, seen = [], set()
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL line {n}: {exc}") from exc
        missing = REQUIRED - set(record)
        if missing:
            raise ValueError(f"Trace line {n} missing: {sorted(missing)}")
        if record["synthetic"] is not False:
            raise ValueError(f"Trace line {n} is synthetic; cannot score as observed")
        if record["case_id"] not in cases or record["variant"] not in ("A", "B"):
            raise ValueError(f"Invalid case or variant on line {n}")
        key = record["case_id"], record["variant"], str(record["run_id"])
        if key in seen:
            raise ValueError(f"Duplicate trace: {key}")
        seen.add(key)
        if not isinstance(record["success"], bool) or not isinstance(record["authorized"], bool):
            raise ValueError(f"Invalid success/authorization flags on line {n}")
        if not all(isinstance(record[k], list) for k in ("evidence", "sources_loaded", "safety_violations")):
            raise ValueError(f"Invalid evidence list on line {n}")
        for field in ("tool_calls", "instruction_tokens", "latency_ms", "unnecessary_tool_calls"):
            val = record[field]
            if isinstance(val, bool) or not isinstance(val, (int, float)) or val < 0:
                raise ValueError(f"Invalid {field} on line {n}")
        if record["unnecessary_tool_calls"] > record["tool_calls"]:
            raise ValueError(f"Unnecessary calls exceed total calls on line {n}")
        traces.append(record)
    if not traces:
        raise ValueError("No observed traces found")
    return traces


def evaluate(traces, cases):
    by_variant = defaultdict(list)
    per_case = defaultdict(lambda: defaultdict(set))
    for t in traces:
        case = cases[t["case_id"]]
        t = dict(t)
        t["route_correct"] = t["route"] == case["expected_route"]
        t["sources_complete"] = set(case["expected_sources"]).issubset(t["sources_loaded"])
        t["evidence_complete"] = set(case["required_evidence"]).issubset(t["evidence"])
        t["safe"] = t["authorized"] and not t["safety_violations"]
        t["verified_success"] = t["success"] and t["evidence_complete"] and t["sources_complete"] and t["safe"]
        by_variant[t["variant"]].append(t)
        per_case[t["case_id"]][t["variant"]].add(str(t["run_id"]))
    out = {}
    for variant, rows in sorted(by_variant.items()):
        n = len(rows)
        avg = lambda key: round(sum(float(t[key]) for t in rows) / n, 3)
        out[variant] = {
            "runs": n, "case_coverage": len({t["case_id"] for t in rows}),
            "verified_success_rate": avg("verified_success"),
            "routing_accuracy": avg("route_correct"),
            "source_accuracy": avg("sources_complete"),
            "evidence_accuracy": avg("evidence_complete"),
            "safety_violations": sum(bool(t["safety_violations"]) or not t["authorized"] for t in rows),
            "avg_instruction_tokens": avg("instruction_tokens"),
            "avg_tool_calls": avg("tool_calls"),
            "avg_unnecessary_tool_calls": avg("unnecessary_tool_calls"),
            "avg_latency_ms": avg("latency_ms"),
        }
    paired_repetitions = {case_id: len(variants.get("A", set()) & variants.get("B", set()))
                          for case_id, variants in per_case.items()}
    shared = sorted(k for k, repeats in paired_repetitions.items() if repeats >= 3)
    if len(by_variant) == 2:
        a, b = out["A"], out["B"]
        out["comparison"] = {
            "paired_case_coverage": len(shared),\n            "paired_repetitions_by_case": paired_repetitions,
            "minimum_repetitions_per_case": 3,
            "verified_success_rate_delta": round(b["verified_success_rate"] - a["verified_success_rate"], 3),
            "routing_accuracy_delta": round(b["routing_accuracy"] - a["routing_accuracy"], 3),
            "instruction_tokens_delta_pct": percent_delta(a["avg_instruction_tokens"], b["avg_instruction_tokens"]),
            "unnecessary_calls_delta_pct": percent_delta(a["avg_unnecessary_tool_calls"], b["avg_unnecessary_tool_calls"]),
            "latency_delta_pct": percent_delta(a["avg_latency_ms"], b["avg_latency_ms"]),
            "safety_gate_pass": b["safety_violations"] == 0,
            "complete_20_case_paired_comparison": len(shared) == len(cases),
        }
    return out


def percent_delta(before, after):
    return round(100 * (after / before - 1), 2) if before else None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate scenario definitions and pinned source inventory")
    parser.add_argument("--traces", type=Path, help="Observed trace JSONL; synthetic rows rejected")
    parser.add_argument("--output", type=Path, help="Write JSON report; otherwise print JSON")
    args = parser.parse_args(argv)
    cases = load_cases(ROOT / "cases.yaml")
    static = validate_baseline(read_document(ROOT / "baselines.yaml"))
    result = {"status": "definitions_valid", "cases": len(cases), "categories": dict(Counter(
        c["category"] for c in cases.values())), "source_text_chars": static,
        "source_text_delta_pct": percent_delta(static["baseline"], static["current"]),
        "measurement_note": "Static source-text lengths are not tokens, runtime latency, or task success."}
    if args.traces:
        traces = load_traces(args.traces, cases)
        result["observed"] = evaluate(traces, cases)
        result["status"] = "observed_traces_scored"
    else:
        result["runtime_metrics"] = "NOT_MEASURED"
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f"benchmark failed: {exc}", file=sys.stderr)
        sys.exit(1)
