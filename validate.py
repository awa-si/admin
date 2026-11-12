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

    # The short workflow file is a routing index; every detail has one owner.
    workflow_index = _read(repo / "workflow.md")
    source_map = workflow_index.get("source_map")
    if not isinstance(source_map, list) or not source_map:
        raise ValueError("workflow index must define a nonempty source_map")
    if "routing_decision_order" not in workflow_index:
        raise ValueError("workflow index must own the ordered route decision")
    expected_details = {
        "workflow/repository.md", "workflow/routes.md",
        "workflow/github.md", "workflow/awa.md",
        "workflow/execution.md", "workflow/preflight.md",
        "workflow/verification.md", "behavior.yaml",
    }
    mapped = {}
    for entry in source_map:
        if not isinstance(entry, dict) or len(entry) != 1:
            raise ValueError("invalid workflow source_map entry")
        path, listed = next(iter(entry.items()))
        if path not in expected_details or not isinstance(listed, str):
            raise ValueError(f"invalid workflow source_map target: {path}")
        if path in mapped:
            raise ValueError(f"duplicate workflow source_map path: {path}")
        mapped[path] = listed.split("|")
    if set(mapped) != expected_details:
        raise ValueError("workflow source_map does not cover all owner modules")
    defined = {"scope", "mode", "resolution", "decision_bootstrap",
               "routing_decision_order", "source_map", "loading"}
    for path, section_names in mapped.items():
        detail = _read(repo / path)
        for name in section_names:
            if name in defined:
                raise ValueError(f"duplicate workflow owner section: {name}")
            if name not in detail:
                raise ValueError(f"workflow section missing in {path}: {name}")
            defined.add(name)
    for path in expected_details - {"behavior.yaml"}:
        detail = _read(repo / path)
        if set(detail) != set(mapped[path]):
            raise ValueError(f"unmapped or duplicated section in {path}")
    if workflow_index.get("loading", {}).get("entrypoint") != "workflow.md#routing_decision_order":
        raise ValueError("workflow entrypoint must remain the canonical router")
    if "current_AWA_MCP_instruction_resolver" in (repo / "workflow" / "awa.md").read_text(encoding="utf-8"):
        raise ValueError("MCP technical source must not be a global instruction resolver")

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
