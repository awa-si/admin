scope: project_workflow_delta
project: awa
mode: normative_machine_directives

resolution:
- parent: awa-si/admin/workflow.md
- project_instructions: awa-si/admin/projects/awa/instructions.txt
- inheritance: delta_only|explicit_override_only|parent_rules_remain_active
- source_of_truth: awa-si/awa@main
- repository_agent: awa-si/awa@main:AGENTS.md
- state_authority: current_repository_and_live_runtime

canonical_owners:
- workspace_reuse_and_consent: awa-si/admin/projects/awa/instructions.txt
- repository_ownership: awa-si/awa@main:AGENTS.md
- MCP_runtime_and_entrypoint: awa-si/awa@main:mcp/README.md
- workspace_API_and_lifecycle: awa-si/awa@main:mcp/workspace/contract.md
- workspace_implementation_map: awa-si/awa@main:mcp/workspace/README.md
- workspace_profile: awa-si/awa@main:workspace.ini
- invocation_authority: live_AWA_MCP_tool_schema
- semantics_authority: current_canonical_repository_contract
- execution_routing_authority: awa-si/admin/workflow.md#routing_decision_order
- unavailable_owner: report_exact_missing_source|do_not_invent_fallback_contract


routing:
- precedence: awa-si/admin/workflow.md#routing_decision_order
- authorization: inherited_global_and_project_policy; workspace_reuse_requires_existing_verified_consent_and_ownership
- operations_and_limits: current_AWA_MCP_contract_and_live_schema_only
- unsupported_or_retired_operation: consult_current_owner|never_infer_legacy_name

workspace:
- technical_reference: awa-si/awa@main:mcp/workspace/contract.md
- selection: inherited_global_routing_gates
- live_schema: authoritative

delivery:
- lifecycle_and_deployment_gate: awa-si/admin/workflow.md#deployment_cadence
- code_or_registration_change: process_restart_or_redeploy_per_canonical_runtime_contract
- configuration_reload_as_code_activation: prohibited
- runtime_claim: verify_process_and_live_capability_evidence
