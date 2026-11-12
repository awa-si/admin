#!/usr/bin/env python3
"""Validate the canonical Admin instruction hierarchy and global bootstrap."""
from __future__ import annotations

from pathlib import Path
import sys

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required for Admin YAML validation") from exc


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


def _count_nodes(value: dict) -> int:
    count = 0
    for item in value.values():
        count += 1
        if isinstance(item, dict):
            count += _count_nodes(item)
        elif not isinstance(item, (str, bool, int, list)):
            raise ValueError("unexpected instruction value type")
    return count


def validate(repo: Path) -> dict:
    core = _read(repo / "core.yaml")
    template = _read(repo / "projects" / "template.txt")
    if (core.get("scope"), core.get("level"), core.get("mode")) != ("global", 0, "normative"):
        raise ValueError("invalid canonical global instruction identity")

    original_sections = [
        "communication", "accuracy", "interactive_execution",
        "workspace_repository_write_boundary", "execution", "context",
        "dispute_and_escalation_strategy", "research",
        "plugin_and_skill_workflow_resolution", "connector_and_file_reading",
        "sharepoint_origin_file_workflow", "apple_icloud_workflow",
        "control_plane", "awa_mcp_information_delegation",
        "admin_plane_reload", "loading_and_resolution",
        "repository_agent_policy", "instruction_resolution_cache",
        "mcp_instruction_reload", "public_repo_safety", "openai_safety_blocks",
    ]
    for section in original_sections:
        if not isinstance(core.get(section), dict) or not core[section]:
            raise ValueError(f"missing or invalid global section: {section}")

    for name in ("workflow", "coding", "research_guidance", "repository_agent"):
        if not isinstance(core.get(name), dict) or not core[name]:
            raise ValueError(f"missing or invalid integrated domain: {name}")

    workflow = core["workflow"]
    if "routing_decision_order" not in workflow or "decision_bootstrap" not in workflow:
        raise ValueError("workflow routing decision owner missing")
    if "resolution" not in core["coding"] or "resolution" not in core["research_guidance"]:
        raise ValueError("coding/research source resolution missing")
    guide = core.get("human_guide")
    if not isinstance(guide, dict) or guide.get("normative") is not False:
        raise ValueError("README guide must remain non-normative")

    if template.get("authority") != "awa-si/admin/core.yaml":
        raise ValueError("project bootstrap must point to core.yaml")
    if template.get("load", {}).get("required") != "awa-si/admin/core.yaml":
        raise ValueError("project bootstrap must have a single global source")
    if template.get("load", {}).get("project") != "awa-si/admin/projects/<project>/*":
        raise ValueError("project bootstrap must discover all files via wildcard")
    if template.get("load", {}).get("project_mode") != "enumerate_all_existing_files_then_read_each_completely":
        raise ValueError("project bootstrap must fully read every project file")
    loading = core.get("loading_and_resolution", {})
    if loading.get("project_directory_contract") != "awa-si/admin/projects/<project>/*":
        raise ValueError("core project wildcard contract mismatch")
    if "read_every_existing_regular_file" not in loading.get("project_file_loading", ""):
        raise ValueError("core must require complete file reads")
    if template.get("execute", {}).get("routing") != "core.yaml#workflow.routing_decision_order":
        raise ValueError("routing must resolve to core.yaml")

    return {
        "status": "valid",
        "authority": "core.yaml",
        "original_global_sections": len(original_sections),
        "integrated_domains": 4,
        "instruction_nodes": _count_nodes({k: v for k, v in core.items() if isinstance(v, dict) and k != "human_guide"}),
        "bootstrap_global_sources": 1,
    }


if __name__ == "__main__":
    try:
        for key, value in validate(Path(__file__).resolve().parent).items():
            print(f"{key}: {value}")
    except (AssertionError, ValueError, KeyError, TypeError, OSError, yaml.YAMLError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
