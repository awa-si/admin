---
title: AWA Project Workflow
description: AWA-specific workflow delta delegating MCP mechanics to canonical repository contracts.
type: standard
status: active
language: en
owner: AWA
created: 2026-10-31
updated: 2026-11-03
---
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
- workspace_API_and_lifecycle: awa-si/awa@main:mcp/docs/workspace.md
- workspace_implementation_map: awa-si/awa@main:mcp/workspace/README.md
- workspace_profile: awa-si/awa@main:workspace.ini
- invocation_authority: live_AWA_MCP_tool_schema
- semantics_authority: current_canonical_repository_contract
- execution_routing_authority: awa-si/admin/workflow.md
- unavailable_owner: report_exact_missing_source|do_not_invent_fallback_contract


routing:
- GitHub_connector: repository_only_work_when_sufficient
- existing_workspace: reuse_only_under_project_consent_and_registry_policy
- AWA_MCP_Workspace: heavy_or_runtime_work_when_authorized_and_global_gate_passes
- AWA_Work: durable_orchestration_only_when_global_gate_passes
- short_native_task_or_workspace_execution: select_from_live_AWA_capabilities_and_canonical_owner_contract
- tool_registration_and_task_registry: delegate_to_awa-si/awa_MCP_owner_and_current_tool_schema
- runtime_limits|operation_names|payloads|retry_or_polling_details: do_not_define_in_admin
- unknown_or_retired_operation: consult_current_contract|never_infer_from_legacy_name

workspace:
- directive: awa-si/admin/workflow.md#awa_mcp_workspace
- technical_reference: awa-si/awa@main:mcp/docs/workspace.md
- live_schema: authoritative

delivery:
- scope: complete_coherent_change_set_before_release_boundary
- sequence: inspect -> implement_related_changes -> validate_bundle -> commit -> authorized_deploy_if_required -> verify_live_behavior
- pre_deploy: tests|versioning|compatibility|required_approval
- deploy_gate: user_request|existing_authorized_workflow
- deployment_cadence: one_per_coherent_release_boundary_when_practical
- post_deploy: verify_running_service_and_live_capabilities_when_runtime_affected
- code_or_registration_change: process_restart_or_redeploy_per_canonical_runtime_contract
- configuration_reload_as_code_activation: prohibited
- corrective_cycle: observed_failure -> focused_fix -> validation -> authorized_redeploy -> verification

verification:
- tests: focused_affected_contracts_first|broader_if_material
- repository_write: verify_remote_state
- runtime_claim: live_endpoint_evidence_required
- report: actual_changes|executed_tests|commit|deployment_status|blockers
