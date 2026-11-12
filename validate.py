#!/usr/bin/env python3
"""Validate root-level experimental Admin YAML contracts.

Requires PyYAML. This does not activate the runtime candidate.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
import sys

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required for admin YAML validation") from exc


class StrictLoader(yaml.SafeLoader):
    pass


def _unique_mapping(loader, node):
    pairs = loader.construct_pairs(node, deep=True)
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = value
    return result


StrictLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping
)


def _read_yaml(path: Path) -> dict:
    value = yaml.load(path.read_text(encoding="utf-8"), Loader=StrictLoader)
    if not isinstance(value, dict):
        raise ValueError(f"expected YAML mapping in {path}")
    return value


def _blob_sha(content: str) -> str:
    encoded = content.encode("utf-8")
    return hashlib.sha1(
        b"blob " + str(len(encoded)).encode("ascii") + b"\0" + encoded
    ).hexdigest()


def validate(repo: Path) -> dict:
    core = _read_yaml(repo / "core.yaml")
    runtime = _read_yaml(repo / "runtime.yaml")
    assert core["schema_version"] == runtime["schema_version"] == 1
    assert core["kind"] == "exhaustive_source_snapshot"
    assert runtime["kind"] == "decision_runtime_projection"
    assert core["status"] == runtime["status"] == "comparison_only"
    assert runtime["authority"]["decision_owner"] == "gpt"
    assert runtime["authority"]["route_owner"] == "workflow.md"
    assert runtime["authority"]["provider_admission_owner"] == "live_provider"
    assert runtime["limitations"]["replaces_canonical_sources"] is False
    assert runtime["limitations"]["safe_for_automatic_bootstrap"] is False

    sources = core["sources"]
    assert len(sources) == core["source_count"] == 8
    seen = set()
    total = 0
    for document in sources:
        name = document["path"]
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts or name in seen:
            raise ValueError("unsafe or duplicate source path")
        seen.add(name)
        content = document["content"]
        assert isinstance(content, str)
        assert (repo / name).read_text(encoding="utf-8") == content, name
        assert _blob_sha(content) == document["git_blob_sha"], name
        total += len(content.encode("utf-8"))

    sections = runtime["source_coverage"]
    assert len(sections) == len(seen)
    assert set(item["path"] for item in sections) == seen
    structural_sections = 0
    excluded_headers = {"scope", "mode", "repository", "level", "project", "branch"}
    for item in sections:
        name = item["path"]
        source = (repo / name).read_text(encoding="utf-8")
        if name == "instructions.txt":
            expected_sections = re.findall(r"^## ([a-z][a-z0-9_]*)", source, re.M)
        else:
            body = re.sub(r"\\A---\\n.*?\\n---\\n", "", source, count=1, flags=re.S)
            expected_sections = [
                key for key in re.findall(r"^([a-z][a-z0-9_]*):", body, re.M)
                if key not in excluded_headers
            ]
        actual = item["sections"]
        if len(actual) != len(set(actual)) or actual != expected_sections:
            raise ValueError(
                f"incomplete or out-of-order section inventory: {name}; "
                f"expected={expected_sections!r}, actual={actual!r}"
            )
        structural_sections += len(actual)
    assert runtime["limitations"]["source_inventory_complete"] is True
    assert runtime["limitations"]["semantic_projection_is_not_a_lossless_transformation"] is True
    assert runtime["limitations"]["normative_equivalence_verified"] is False

    expected = [
        "product_mode", "authorization", "target", "existing_workspace",
        "capability_need", "select_route", "native_admission",
    ]
    assert [gate["id"] for gate in runtime["decision"]["order"]] == expected
    workflow = (repo / "workflow.md").read_text(encoding="utf-8")
    for i, gate in enumerate(expected, start=1):
        assert f"- {i}_{gate}:" in workflow
    assert runtime["decision"]["source"] == "workflow.md#routing_decision_order"
    return {
        "status": "source_verified",
        "source_count": len(sources),
        "source_utf8_bytes": total,
        "runtime_utf8_bytes": (repo / "runtime.yaml").stat().st_size,
        "coverage_sections": structural_sections,
        "semantic_equivalence": "not_verified",
        "bootstrap_activation": "unchanged",
    }


if __name__ == "__main__":
    try:
        for field, value in validate(Path(__file__).resolve().parent).items():
            print(f"{field}: {value}")
    except (AssertionError, ValueError, KeyError, OSError, yaml.YAMLError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
