#!/usr/bin/env python3
"""Validate the ordered ChatGPT use-case resolver and referenced owners."""
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
    if (core.get("scope"), core.get("mode"), core.get("version")) != ("chatgpt", "use_case_resolver", 3):
        raise ValueError("core.yaml must be a version-3 use-case resolver")
    if set(core) != {"version", "scope", "mode", "registry", "resolution"}:
        raise ValueError("core.yaml contains unexpected keys")
    registry = core["registry"]
    if not isinstance(registry, list) or len(registry) != 4:
        raise ValueError("core.registry must contain four ordered top-level entries")
    if any(not isinstance(entry, dict) for entry in registry):
        raise ValueError("core.registry entries must be mappings")
    top_ids = tuple(entry.get("id") for entry in registry)
    if top_ids != ("behavior", "workflow", "project", "repository_agent"):
        raise ValueError("core top-level registry order is invalid")
    workflow_cases = registry[1].get("cases")
    if not isinstance(workflow_cases, list) or len(workflow_cases) != 5:
        raise ValueError("workflow registry must contain five cases")
    if any(not isinstance(case, dict) for case in workflow_cases):
        raise ValueError("workflow registry cases must be mappings")
    case_ids = tuple(case.get("id") for case in workflow_cases)
    if case_ids != ("coding", "research", "github", "mcp", "unknown"):
        raise ValueError("workflow cases order is invalid")
    sources = {entry["id"]: entry for entry in registry + workflow_cases}
    if len(sources) != 9:
        raise ValueError("duplicate use-case identifier in registry")
    expected_paths = {
        "behavior": "behavior.yaml",
        "workflow": "workflow.md",
        "coding": "workflow/coding.md",
        "research": "workflow/research.md",
        "github": "workflow/github.md",
        "mcp": "workflow/mcp.md",
        "unknown": "workflow.md",
    }
    for name, relative in expected_paths.items():
        if sources[name].get("path") != f"awa-si/admin/{relative}":
            raise ValueError(f"invalid source reference: {name}")
        if not (repo / relative).is_file():
            raise ValueError(f"missing canonical source file: {relative}")
    if sources["behavior"].get("load") != "always":
        raise ValueError("behavior must always load")
    for name in ("workflow", "coding", "research", "github", "mcp", "unknown"):
        if not str(sources[name].get("load", "")).startswith("on_"):
            raise ValueError(f"{name} must load on demand")
    for name in ("github", "mcp"):
        if sources[name].get("requires") != "workflow":
            raise ValueError(f"{name} must depend on workflow routing")
    if core["resolution"].get("registry_semantics") != "ordered_parent_case_source_graph_not_instruction_priority":
        raise ValueError("registry must not override instruction precedence")
    if core["resolution"].get("case_loading") != "evaluate_each_case_condition_independently;parent_not_implicitly_loaded":
        raise ValueError("registry cases must retain independent loading")
    if sources["unknown"].get("section") != "unknown_case_handling" or sources["unknown"].get("reuse_loaded_source") is not True:
        raise ValueError("unknown case must reuse the canonical workflow fallback")
    if core["resolution"].get("unknown_case") != "workflow.md#unknown_case_handling;never_bypass_authorization_or_live_provider_admission":
        raise ValueError("unknown case cannot bypass authorization or admission")
    if sources["mcp"].get("discovery") != "mcp_model":
        raise ValueError("MCP capability discovery must use mcp_model")
    if sources["mcp"].get("technical_sources") != "mcp_instructions":
        raise ValueError("MCP technical-source discovery must use mcp_instructions")
    if sources["project"].get("path") != "awa-si/admin/projects/<project>/*":
        raise ValueError("project wildcard source missing")
    if sources["project"].get("read") != "enumerate_all_existing_files_then_read_each_completely":
        raise ValueError("project file loading is not exhaustive")
    if sources["repository_agent"].get("path") != "<resolved_repository>/AGENTS.md":
        raise ValueError("repository agent path missing")
    resolution = core["resolution"]
    if resolution.get("route_authority") != "awa-si/admin/workflow.md#routing_decision_order":
        raise ValueError("workflow.md must remain the route authority")
    if template.get("authority") != "awa-si/admin/core.yaml":
        raise ValueError("project authority must point at core.yaml")
    if template.get("load", {}).get("index") != "awa-si/admin/core.yaml":
        raise ValueError("project bootstrap must load core.yaml")
    if template.get("load", {}).get("project") != sources["project"]["path"]:
        raise ValueError("project wildcard differs between bootstrap and core")
    if template.get("load", {}).get("project_mode") != sources["project"]["read"]:
        raise ValueError("project loading mode differs between bootstrap and core")

    def directive_map(items: object, owner: str) -> dict:
        if not isinstance(items, list) or any(not isinstance(item, dict) or len(item) != 1 for item in items):
            raise ValueError(f"invalid directive list in {owner}")
        return {key: value for item in items for key, value in item.items()}


    # Common workflow rules load together; only route-specific details are conditional.
    workflow_index = _read(repo / "workflow.md")
    source_map = workflow_index.get("source_map")
    if not isinstance(source_map, list) or not source_map:
        raise ValueError("workflow index must define a nonempty source_map")
    for required in ("routing_decision_order", "github_routing_gate", "known_use_cases"):
        if required not in workflow_index:
            raise ValueError(f"workflow.md must own routing section: {required}")
    use_cases = directive_map(workflow_index["known_use_cases"], "known_use_cases")
    cases = use_cases.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("known use cases must be a nonempty list")
    case_ids = [case.get("id") for case in cases if isinstance(case, dict)]
    if len(case_ids) != len(cases) or len(set(case_ids)) != len(cases):
        raise ValueError("known use cases require unique identifiers")
    for case in cases:
        if not all(case.get(field) for field in ("id", "category", "given", "expected")):
            raise ValueError("known use case missing an essential field")
    if use_cases.get("route_decision") != "routing_decision_order_remains_sole_normative_route_precedence":
        raise ValueError("known cases must not override routing decision order")
    expected_details = {"workflow/github.md", "workflow/mcp.md"}
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
    defined = set(workflow_index)
    required_common = {
        "branch_resolution", "task_scope_resolution", "repository_state_resolution",
        "repository_discovery", "cross_repository_execution", "operation_classification",
        "chatgpt_work_mode", "deployment_cadence", "change_set_lifecycle",
        "edit_and_writeback", "dependency_preflight", "rights_preflight",
        "environment_preflight", "long_running_execution", "mcp_versioning",
        "tool_discovery_boundary", "mixed_case_handling", "unknown_case_handling",
        "verification", "failure_and_recovery",
    }
    if not required_common.issubset(defined):
        raise ValueError("general workflow sections must stay in workflow.md")
    for path, section_names in mapped.items():
        detail = _read(repo / path)
        for name in section_names:
            if name in defined:
                raise ValueError(f"duplicate workflow owner section: {name}")
            if name not in detail:
                raise ValueError(f"workflow section missing in {path}: {name}")
            defined.add(name)
    for path in expected_details:
        detail = _read(repo / path)
        if set(detail) != set(mapped[path]):
            raise ValueError(f"unmapped or duplicated section in {path}")

    mixed = directive_map(workflow_index["mixed_case_handling"], "mixed_case_handling")
    unknown = directive_map(workflow_index["unknown_case_handling"], "unknown_case_handling")
    if "all_applicable" not in str(mixed.get("case_detection", "")):
        raise ValueError("mixed-case routing must preserve all applicable cases")
    if "routing_decision_order" not in str(mixed.get("authority", "")):
        raise ValueError("mixed cases must preserve route authority")
    if "authorization" not in str(unknown.get("preserve", "")):
        raise ValueError("unknown cases must preserve authorization gates")
    boundary = directive_map(workflow_index["tool_discovery_boundary"], "tool_discovery_boundary")
    if boundary.get("owner") != "awa-si/admin/workflow.md":
        raise ValueError("workflow must own general tool-discovery boundary")
    if "Code_Interpreter" not in str(boundary.get("native_execution_first", "")):
        raise ValueError("native execution must consider available Code Interpreter")
    if "client" not in str(boundary.get("discovery", "")):
        raise ValueError("tool discovery must remain client delegated")
    gate = directive_map(workflow_index["github_routing_gate"], "github_routing_gate")
    if "Native_Sandbox" not in str(gate.get("candidate_routes_after_routing_decision_order_gates", "")):
        raise ValueError("native sandbox route missing")
    mcp_detail = directive_map(_read(repo / "workflow/mcp.md")["awa_mcp"], "awa_mcp")
    discovery_entries = mcp_detail.get("discovery_boundary")
    if not isinstance(discovery_entries, list):
        raise ValueError("AWA MCP route must declare the provider-discovery boundary")
    discovery = directive_map(discovery_entries, "awa_mcp.discovery_boundary")
    if "global_tool_search" not in str(discovery.get("client_owner", "")):
        raise ValueError("global tool search must remain client-owned")
    if directive_map(workflow_index["loading"], "loading").get("entrypoint") != "workflow.md#routing_decision_order":
        raise ValueError("workflow entrypoint must remain the canonical router")
    if "current_AWA_MCP_instruction_resolver" in (repo / "workflow" / "mcp.md").read_text(encoding="utf-8"):
        raise ValueError("MCP technical source must not be a global instruction resolver")

    # Behavior is the only universal policy owner; the core index has none.
    behavior = _read(repo / "behavior.yaml")
    if behavior.get("mode") != "normative" or "communication" not in behavior:
        raise ValueError("behavior.yaml must contain the global normative rules")
    for path in ("workflow.md", "workflow/coding.md", "workflow/research.md"):
        if not (repo / path).read_text(encoding="utf-8").strip():
            raise ValueError(f"empty source: {path}")
    return {
        "status": "valid",
        "index": "core.yaml",
        "global_policy": "behavior.yaml",
        "conditional_sources": "workflow.md|workflow/coding.md|workflow/research.md",
        "mcp_discovery": "mcp_model|mcp_instructions",
    }


if __name__ == "__main__":
    try:
        for key, value in validate(Path(__file__).resolve().parent).items():
            print(f"{key}: {value}")
    except (ValueError, TypeError, KeyError, OSError, yaml.YAMLError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
