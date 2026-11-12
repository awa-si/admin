#!/usr/bin/env python3
"""Validate the experimental Admin YAML migration against checked-in owners.

Usage: python admin/validate.py
Dependency: PyYAML (python -m pip install PyYAML).
This validator does not activate the generated contract.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML is required: python -m pip install PyYAML")


class UniqueKeysLoader(yaml.SafeLoader):
    """Reject ambiguous duplicate YAML keys."""


def construct_unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=True)
    return result


UniqueKeysLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_unique_mapping
)


def load_yaml(path: Path) -> dict:
    data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeysLoader)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return data


def git_blob_sha(text: str) -> str:
    raw = text.encode("utf-8")
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def check(root: Path, *, verify_sources: bool = True) -> dict:
    directory = root / "admin"
    core = load_yaml(directory / "core.yaml")
    runtime = load_yaml(directory / "runtime.yaml")
    assert core.get("schema_version") == runtime.get("schema_version") == 1
    assert core.get("kind") == "exhaustive_source_snapshot"
    assert runtime.get("kind") == "deduplicated_runtime_inventory"
    assert core.get("status") == runtime.get("status") == "comparison_only"
    assert core.get("scope") == runtime.get("scope") == "global_and_awa_project"
    assert core.get("repository") == runtime.get("repository") == "awa-si/admin"
    assert runtime.get("encoding", {}).get("algorithm") == "exact_line_dictionary"
    assert runtime.get("encoding", {}).get("normalization") == "none"
    assert runtime.get("entrypoint", {}).get("no_implicit_activation") is True
    decision = runtime.get("decision_contract", {})
    assert decision.get("status") == "comparison_only"
    assert decision.get("decision_owner") == "gpt"
    assert decision.get("routing_owner") == "workflow.md#routing_decision_order"
    assert decision.get("admission_owner") == "current_live_provider"
    expected_gates = [
        "product_mode", "authorization", "target", "existing_workspace",
        "capability_need", "select_route", "native_admission",
    ]
    assert decision.get("ordered_gates") == expected_gates
    assert decision.get("gate_source_keys") == [
        f"{index}_{gate}" for index, gate in enumerate(expected_gates, start=1)
    ]

    originals = core.get("sources")
    documents = runtime.get("documents")
    dictionary = runtime.get("dictionary")
    if not all(isinstance(x, list) for x in (originals, documents, dictionary)):
        raise ValueError("sources/documents/dictionary must be YAML lists")
    assert len(originals) == len(documents) == core["source_count"] == runtime["source_count"]
    assert len(dictionary) == runtime["unique_line_count"]
    assert all(isinstance(line, str) for line in dictionary)
    assert len(set(dictionary)) == len(dictionary), "dictionary is not deduplicated"

    covered = set()
    line_count = 0
    seen_paths = set()
    for original, document in zip(originals, documents):
        path = original["path"]
        assert path == document["path"] and path not in seen_paths
        seen_paths.add(path)
        if Path(path).is_absolute() or ".." in Path(path).parts:
            raise ValueError("source path escapes repository")
        sha = original["git_blob_sha"]
        assert re.fullmatch(r"[0-9a-f]{40}", sha)
        assert sha == document["git_blob_sha"]
        source = original["content"]
        assert isinstance(source, str)
        line_ids = document["line_ids"]
        assert isinstance(line_ids, list)
        if not all(type(idx) is int and 0 <= idx < len(dictionary) for idx in line_ids):
            raise ValueError(f"invalid dictionary reference: {path}")
        reconstructed = "\n".join(dictionary[idx] for idx in line_ids)
        assert reconstructed == source, f"round-trip mismatch: {path}"
        assert git_blob_sha(source) == sha, f"blob SHA mismatch: {path}"
        if verify_sources:
            local = (root / path).read_text(encoding="utf-8")
            assert local == source, f"source changed; snapshots stale: {path}"
        covered.update(line_ids)
        line_count += len(line_ids)

    assert covered == set(range(len(dictionary))), "unreferenced dictionary lines"
    workflow = next(x["content"] for x in originals if x["path"] == "workflow.md")
    assert "routing_decision_order:" in workflow
    for gate in decision["gate_source_keys"]:
        assert f"- {gate}:" in workflow, f"unsupported decision gate: {gate}"
    return {
        "status": "valid",
        "sources": len(originals),
        "source_lines": line_count,
        "unique_lines": len(dictionary),
        "repeated_line_occurrences": line_count - len(dictionary),
        "verify_sources": verify_sources,
        "source_characters": sum(len(x["content"]) for x in originals),
        "core_bytes": (directory / "core.yaml").stat().st_size,
        "runtime_bytes": (directory / "runtime.yaml").stat().st_size,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--skip-source-check", action="store_true",
                        help="validate snapshot roundtrip without local source freshness")
    args = parser.parse_args()
    try:
        result = check(args.root, verify_sources=not args.skip_source_check)
    except (AssertionError, ValueError, KeyError, OSError, yaml.YAMLError) as exc:
        print(f"admin YAML validation failed: {exc}", file=sys.stderr)
        return 1
    for key, value in result.items():
        print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
