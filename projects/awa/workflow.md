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
- native_reviewed_task: prefer_registered_task_exec_when_suitable|verify_live_capabilities_and_scope
- task_registry_and_registration: delegate_to_current_awa-si/awa_MCP_task_contract|no_unreviewed_dynamic_handler_or_arbitrary_shell
- container_job: use_workspace_exec_per_live_schema_when_isolation_or_runtime_requirements_demand
- retired_exec_sync: prohibited
- execution_duration_and_limits: inspect_live_contract|never_hardcode_previous_15_second_limit
- task_vs_container: do_not_confuse_native_task_engine_with_workspace_container_jobs
- reload_boundary: task_handler_reload_is_not_gateway_process_restart_or_tool_schema_refresh
- latency: avoid_job_polling_when_terminal_result_is_already_available|prefer_existing_capability_to_new_handler
- measurement: distinguish_tool_overhead|admission|runtime|handler_compute

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
