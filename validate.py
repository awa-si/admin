#!/usr/bin/env python3
"""Validate the dynamic ChatGPT source index and referenced Admin owners."""
from __future__ import annotations

from pathlib import Path
import sys

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required for Admin validation") from exc


class StrictLoader(yaml.SafeLoader):
    pass


def _unique_mapping(loader, node):
    output = {}
    for key, value in loader.construct_pairs(node, deep=True):
        if key in output:
            raise ValueError(f"duplicate YAML key: {key}")
        output[key] = value
    return output


StrictLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping
)


def _read(path: Path) -> dict:
    data = yaml.load(path.read_text(encoding="utf-8"), Loader=StrictLoader)
    if not isinstance(data, dict):
        raise ValueError(f"expected YAML mapping: {path}")
    return data


def validate(repo: Path) -> dict:
    core = _read(repo / "core.yaml")
    template = _read(repo / "projects" / "template.txt")
    if (core.get("scope"), core.get("mode")) != ("chatgpt", "source_index"):
        raise ValueError("core.yaml must be a non-normative source index")
    if set(core) != {"version", "scope", "mode", "sources"}:
        raise ValueError("core.yaml contains unexpected instruction sections")
    sources = core["sources"]
    if set(sources) != {
        "behavior", "workflow", "coding", "research", "mcp",
        "project", "repository_agent"
    }:
        raise ValueError("unexpected source ownership map")
    for name, path in (
        ("behavior", "behavior.yaml"),
        ("workflow", "workflow.md"),
        ("coding", "coding.md"),
        ("research", "research.md"),
    ):
        if sources[name].get("path") != f"awa-si/admin/{path}":
            raise ValueError(f"invalid source reference: {name}")
        if not (repo / path).is_file():
            raise ValueError(f"missing canonical source file: {path}")
    if sources["behavior"].get("load") != "always":
        raise ValueError("behavior must always load")
    for name in ("workflow", "coding", "research"):
        if not str(sources[name].get("load", "")).startswith("on_"):
            raise ValueError(f"{name} must load on demand")

    if sources["mcp"].get("discovery") != "mcp_model":
        raise ValueError("MCP capability discovery must use mcp_model")
    if sources["mcp"].get("technical_sources") != "mcp_instructions":
        raise ValueError("MCP technical-source discovery must use mcp_instructions")
    if sources["project"].get("path") != "awa-si/admin/projects/<project>/*":
        raise ValueError("project wildcard source missing")
    if sources["project"].get("read") != "enumerate_all_existing_files_then_read_each_completely":
        raise ValueError("project file loading is not exhaustive")

    if template.get("authority") != "awa-si/admin/core.yaml":
        raise ValueError("project authority must point at core.yaml")
    if template.get("load", {}).get("index") != "awa-si/admin/core.yaml":
        raise ValueError("project bootstrap must load core.yaml index")
    if template.get("load", {}).get("project") != sources["project"]["path"]:
        raise ValueError("project wildcard differs between bootstrap and core")
    if template.get("load", {}).get("project_mode") != sources["project"]["read"]:
        raise ValueError("project loading mode differs between bootstrap and core")

    # Behavior is the only universal policy owner; the core index has none.
    behavior = _read(repo / "behavior.yaml")
    if behavior.get("mode") != "normative" or "communication" not in behavior:
        raise ValueError("behavior.yaml must contain the global normative rules")
    for name in ("workflow", "coding", "research"):
        if not (repo / f"{name}.md").read_text(encoding="utf-8").strip():
            raise ValueError(f"empty source: {name}.md")
    return {
        "status": "valid",
        "index": "core.yaml",
        "global_policy": "behavior.yaml",
        "conditional_sources": "workflow.md|coding.md|research.md",
        "mcp_discovery": "mcp_model|mcp_instructions",
    }


if __name__ == "__main__":
    try:
        for key, value in validate(Path(__file__).resolve().parent).items():
            print(f"{key}: {value}")
    except (ValueError, TypeError, KeyError, OSError, yaml.YAMLError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
