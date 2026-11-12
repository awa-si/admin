#!/usr/bin/env python3
"""Validate the canonical Admin global-instruction hierarchy."""
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


def _count_directives(value: dict) -> int:
    total = 0
    for item in value.values():
        total += 1
        if isinstance(item, dict):
            total += _count_directives(item)
        elif not isinstance(item, (str, bool, int)):
            raise ValueError("invalid directive type")
    return total


def validate(repo: Path) -> dict:
    core = yaml.load((repo / "core.yaml").read_text(encoding="utf-8"), Loader=StrictLoader)
    if not isinstance(core, dict):
        raise ValueError("core.yaml must contain a YAML mapping")
    if core.get("scope") != "global" or core.get("level") != 0 or core.get("mode") != "normative":
        raise ValueError("invalid global instruction identity")

    expected_sections = [
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
    actual_sections = [key for key in core if key not in {"scope", "level", "mode"}]
    if actual_sections != expected_sections:
        raise ValueError("global section hierarchy changed; review ownership and order")
    for section in expected_sections:
        if not isinstance(core[section], dict) or not core[section]:
            raise ValueError(f"empty or invalid section: {section}")
    count = _count_directives({section: core[section] for section in expected_sections})
    if count != 298:
        raise ValueError(f"directive count changed: {count}; expected 298")

    return {
        "status": "valid",
        "source": "core.yaml",
        "sections": len(expected_sections),
        "directives": count,
        "authority": "normative",
    }


if __name__ == "__main__":
    try:
        for key, value in validate(Path(__file__).resolve().parent).items():
            print(f"{key}: {value}")
    except (AssertionError, ValueError, KeyError, OSError, yaml.YAMLError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
