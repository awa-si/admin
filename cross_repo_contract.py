#!/usr/bin/env python3
"""Validate Admin↔AWA MCP ownership against two explicitly pinned local checkouts.

Never fetch repositories or infer the other checkout from the current directory.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
from pathlib import Path

from validate import _read, validate


class ContractError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def _module(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _class(tree: ast.Module, name: str) -> ast.ClassDef:
    return next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == name)


def _function(nodes: list[ast.stmt], name: str) -> ast.AsyncFunctionDef:
    return next(node for node in nodes if isinstance(node, ast.AsyncFunctionDef) and node.name == name)


def _topics(tree: ast.Module) -> dict[str, str]:
    """Read the declarative SOURCE_REGISTRY without importing MCP runtime code."""
    registry = next(
        node.value for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "SOURCE_REGISTRY"
                for target in node.targets)
    )
    try:
        entries = ast.literal_eval(registry)
    except (ValueError, TypeError, SyntaxError, RecursionError) as exc:
        raise ContractError("SOURCE_REGISTRY must be literal data") from exc
    _require(isinstance(entries, dict) and "mcp" in entries,
             "SOURCE_REGISTRY is missing required source")
    _require(len(set(entries)) == len(entries), "duplicate source topic")
    found = {}
    registered_tools = []
    for topic, spec in entries.items():
        _require(isinstance(topic, str) and isinstance(spec, dict),
                 "invalid technical source entry")
        _require(set(spec).issubset({"path", "tool"}) and isinstance(spec.get("path"), str),
                 f"invalid technical source fields: {topic}")
        found[topic] = spec["path"]
        if "tool" in spec:
            _require(isinstance(spec["tool"], str) and spec["tool"],
                     f"invalid technical tool: {topic}")
            registered_tools.append(spec["tool"])
    _require(len(set(found.values())) == len(found),
             "duplicate technical source path")
    _require(len(set(registered_tools)) == len(registered_tools),
             "duplicate tool owner mapping")
    return found

def check_contract(admin: Path, awa: Path) -> dict[str, object]:
    admin, awa = admin.resolve(), awa.resolve()
    validate(admin)
    core = _read(admin / "core.yaml")
    cases = {item["id"]: item for item in core["registry"][1]["cases"]}
    _require(cases["mcp"]["discovery"] == "mcp_model", "Admin capability owner drift")
    _require(cases["mcp"]["technical_sources"] == "mcp_instructions",
             "Admin technical source owner drift")
    _require(core["resolution"]["route_authority"] == "awa-si/admin/workflow.md#routing_decision_order",
             "Admin routing authority drift")

    routing = _read(admin / "workflow" / "mcp.md")["awa_mcp"]
    directions = {key: value for directive in routing for key, value in directive.items()}
    _require("route_selection" in directions["admin_owns"],
             "Admin no longer owns route selection")
    _require("live_tool_schema" in directions["authority_order"],
             "Live invocation schema boundary missing")

    topics = _topics(_module(awa / "mcp" / "tools" / "model.py"))
    resolver_code = (awa / "mcp" / "instructions.py").read_text(encoding="utf-8")
    _require("SOURCE_REGISTRY" in resolver_code and "source_registry_fingerprint" in resolver_code,
             "instruction resolver is not bound to model source registry")
    for name, relative in topics.items():
        parts = Path(relative)
        _require(not parts.is_absolute() and ".." not in parts.parts,
                 f"invalid technical source path: {name}")
        _require((awa / parts).is_file(), f"technical source missing: {relative}")

    tool = _function(_module(awa / "mcp" / "tools" / "instruction_tools.py").body,
                     "mcp_instructions")
    args = [arg.arg for arg in tool.args.args]
    _require(args == ["topic", "compact"], f"obsolete or altered instruction API: {args}")
    _require(not tool.args.kwarg and not tool.args.vararg,
             "instruction tool must reject unknown parameters")

    model = _module(awa / "mcp" / "tools" / "model_tools.py")
    _function(model.body, "mcp_model")
    model_code = (awa / "mcp" / "tools" / "model_tools.py").read_text(encoding="utf-8")
    _require("source_registry_fingerprint" in model_code and "technical_source_for_tool" in model_code,
             "mcp_model does not consume the shared source registry")
    _require("ChatGPT_loads_Admin_and_project_rules_outside_MCP" in model_code,
             "MCP discovery boundary missing")
    gateway = (awa / "mcp" / "README.md").read_text(encoding="utf-8")
    _require("AWA MCP never" in gateway and "awa-si/admin/core.yaml" in gateway,
             "MCP gateway has lost Admin ownership declaration")

    docs = (awa / "mcp" / "docs" / "tools" / "mcp_instructions.md").read_text(
        encoding="utf-8")
    for name in args:
        _require(re.search(r"^\|\s*" + re.escape(name) + r"\s*\|", docs, re.M) is not None,
                 f"MCP tool docs omit argument {name}")
    for obsolete in ("project", "ref"):
        _require(re.search(r"^\|\s*" + obsolete + r"\s*\|", docs, re.M) is None,
                 f"MCP tool docs retain obsolete argument {obsolete}")
    return {"status": "valid", "admin_owner": "awa-si/admin",
            "mcp_owner": "awa-si/awa", "technical_topics": sorted(topics),
            "tool_arguments": args}


def _head(path: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--verify", "HEAD"],
        check=True, capture_output=True, text=True, timeout=15)
    return result.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--admin-root", type=Path, required=True)
    parser.add_argument("--awa-root", type=Path, required=True)
    parser.add_argument("--expected-admin-sha", required=True)
    parser.add_argument("--expected-awa-sha", required=True)
    args = parser.parse_args()
    for label, value in (("admin", args.expected_admin_sha), ("awa", args.expected_awa_sha)):
        _require(re.fullmatch(r"[0-9a-f]{40}", value) is not None,
                 f"{label} SHA must be an exact 40-character commit hash")
    actual_admin, actual_awa = _head(args.admin_root), _head(args.awa_root)
    _require(actual_admin == args.expected_admin_sha, "Admin checkout SHA mismatch")
    _require(actual_awa == args.expected_awa_sha, "AWA checkout SHA mismatch")
    result = check_contract(args.admin_root, args.awa_root)
    print(json.dumps({**result, "admin_sha": actual_admin, "awa_sha": actual_awa},
                     sort_keys=True))


if __name__ == "__main__":
    main()
