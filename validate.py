#!/usr/bin/env python3
"""Validate the comparison-only Admin source snapshot against canonical files.

Requires PyYAML. This validator does not activate the snapshot.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required for Admin snapshot validation") from exc


class StrictLoader(yaml.SafeLoader):
    pass


def _unique_mapping(loader, node):
    result = {}
    for key, value in loader.construct_pairs(node, deep=True):
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = value
    return result


StrictLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping
)


def _blob_sha(content: str) -> str:
    data = content.encode("utf-8")
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()


def validate(repo: Path) -> dict:
    core = yaml.load((repo / "core.yaml").read_text(encoding="utf-8"), Loader=StrictLoader)
    if not isinstance(core, dict):
        raise ValueError("expected YAML mapping in core.yaml")
    assert core["schema_version"] == 1
    assert core["kind"] == "exhaustive_source_snapshot"
    assert core["status"] == "comparison_only"
    sources = core["sources"]
    assert len(sources) == core["source_count"] == 7

    seen = set()
    total = 0
    for item in sources:
        path = item["path"]
        relative = Path(path)
        if relative.is_absolute() or ".." in relative.parts or path in seen:
            raise ValueError(f"unsafe or duplicate source path: {path}")
        seen.add(path)
        content = item["content"]
        if not isinstance(content, str):
            raise ValueError(f"invalid content: {path}")
        assert (repo / path).read_text(encoding="utf-8") == content, path
        assert _blob_sha(content) == item["git_blob_sha"], path
        total += len(content.encode("utf-8"))

    return {
        "status": "source_verified",
        "source_count": len(seen),
        "source_utf8_bytes": total,
        "bootstrap_activation": "unchanged",
        "semantic_equivalence": "not_verified",
    }


if __name__ == "__main__":
    try:
        for key, value in validate(Path(__file__).resolve().parent).items():
            print(f"{key}: {value}")
    except (AssertionError, ValueError, KeyError, OSError, yaml.YAMLError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
