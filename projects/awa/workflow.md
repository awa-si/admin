---
title: AWA Project Workflow
description: AWA-specific workflow delta delegating MCP mechanics to canonical repository contracts.
type: standard
status: active
language: en
owner: AWA
created: 2026-10-31
updated: 2026-10-31
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
- fast_reviewed_tasks: prefer_task_exec_for_short_bounded_operations_when_registered_and_authorized
- missing_fast_task: create_reviewed_TaskContract_module_in_awa-si/awa:mcp/tasks/registry/ -> validate -> approved_host_sync -> task_exec_reload -> capabilities -> invoke
- task_reload_call: task_exec(operation="reload",payload={})
- task_reload_scope: file_backed_handler_registry_only|not_MCP_tool_registrations_or_gateway_infrastructure
- task_route_boundary: no_arbitrary_shell_or_privileged_mutation|workspace_exec_for_container_commands|work_exec_for_durable_work
- task_preference_limit: do_not_create_handler_if_suitable_existing_native_provider_tool_is_available
- short_workspace_execution: prefer_workspace_exec(operation="exec_sync")_when_isolation_required_and_known_bounded_runtime_fits_deployed_sync_limit
- sync_limit: inspect_deployed_schema|current_host_limit_15_seconds|do_not_use_sync_for_uncertain_duration
- long_workspace_execution: use_exec_start_then_exec_result_for_long_or_uncertain_jobs
- latency_optimization: avoid_unnecessary_exec_start_result_polling_for_short_jobs|avoid_handler_creation_for_one_off_calls_when_setup_exceeds_execution_cost
- measurement: separate_GPT_orchestration|tool_wall_time|provider_admission|container_execution|handler_compute

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
