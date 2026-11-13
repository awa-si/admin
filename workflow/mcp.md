# Conditional AWA MCP workflow: load only after a material, permitted AWA route is selected.
# Admin owns route and approval decisions; live AWA MCP owns tool schemas, admission and technical execution.
awa_mcp:
- scope: AWA_MCP_routing|provider_selection|permissions|technical_source_resolution|execution|recovery|completion
- admin_owns: user_intent|workflow.md#routing_decision_order|product_mode_gates|approval_boundaries|semantic_completion
- canonical_gateway: awa-si/awa@main:mcp/README.md
- canonical_route_reference: awa-si/awa@main:mcp/docs/routing.md
- canonical_tool_index: awa-si/awa@main:mcp/docs/TOOLS.md
- canonical_recovery_reference: awa-si/awa@main:mcp/recovery/README.md
- source_and_runtime_are_distinct: connected_GitHub_main_is_repository_revision|mcp_instructions_is_current_local_technical_source|mcp_version_is_loaded_runtime_identity
- technical_source_resolution: select_current_mcp_instructions_topic_and_matching_owner_contract|when_local_and_GitHub_versions_differ_report_revision_gap_and_use_live_provider_contract_for_running_behavior
- authority_order: higher_priority_ChatGPT_rules|Admin_routing_and_approval|live_registered_schema_for_invocation|current_local_AWA_owner_for_technical_semantics|provider_admission_and_native_receipts_for_effects
- no_second_router: mcp_model_is_read_only_discovery|AWA_bootstrap_routes_are_advisory|workflow.md_remains_sole_normative_route_selection_owner
- product_mode: obey_workflow.md#chatgpt_work_mode;AWA_MCP_disabled_in_ChatGPT_Work_without_explicit_current_user_AWA_MCP_command
- route_is_not_permission: selecting_AWA_does_not_grant_workspace_reuse|host_mutation|external_delivery|destructive_operation|retry|deployment
- connected_provider_boundary: do_not_substitute_AWA_for_a_sufficient_selected_ChatGPT_connector_or_explicit_native_provider_without_permitted_route_change
- no_automatic_provider_probe: inspect_only_material_eligible_capabilities|no_global_tool_scan_per_prompt

awa_mcp_discovery:
- entrypoint: current_client_exposed_tool_schema_and_mcp_model
- client_owner: native_tool_search|deferred_schema_loading|exposed_invocation_schema
- admin_owner: use_case_match|route_selection|authorization|evidence_requirements
- AWA_owner: live_registration|operation_catalog|provider_effects|admission|execution|receipts
- technical_topics:
  - source: mcp_instructions_compact_topic_index
  - allowed_current_topics: agent|github|host|intelligence|mcp|repository|tasks|work|workspace
  - topics_are_technical_documents_not_execution_routes: true
  - read: one_matching_topic_with_full_content_before_relevant_nontrivial_operation;read_only_relevant_subsystem_workflows_on_demand
  - repository_topic: AWA_repository_agent_for_AWA_code_changes_only;not_Admin_policy_or_default_agent_for_other_repositories
  - no_implicit_project_instruction_loading: mcp_instructions_must_not_replace_connected_GitHub_Admin_bootstrap_or_ChatGPT_Project_sources
- mcp_model_contract:
  - initial: operation=bootstrap_for_unfamiliar_AWA_capability_or_route|omit_operation_for_tool_schema_index
  - targeted: operation=bootstrap.routes|bootstrap.workflows|bootstrap.tools.NAME_when_relevant;operation=schema_or_tools_with_exact_tool_for_payload_and_effects
  - optional: operation=capability|execution|capacity|native_only_when_material_and_supported
  - unsupported: overview|routing|standalone_knowledge
  - no_inference: returned_node|registered_tool|capacity_estimate|topic_summary_does_not_grant_admission
- technical_dispatcher_discovery: prefer_current_provider_capabilities_operation_when_documented|otherwise_exact_live_registered_tool_and_owner_contract
- avoid: copying_live_parameter_catalogs_into_Admin|guessing_domain.action_operations|inventing_separate_legacy_private_handlers|using_discovery_as_execution
- stale_or_unreadable_source: inspect_current_owner_and_live_schema_or_report_exact_gap|do_not_claim_full_contract_loaded
- schema_change: rediscover_affected_tool_only|avoid_unrelated_repeat_probes

awa_mcp_route_taxonomy:
- classification: generic_execution_routes_vs_domain_providers_vs_observability_and_knowledge
- generic_routes:
  - native_task:
      intent: reviewed_short_computation|bounded_handler|admitted_isolated_python_or_node_when_engine_enabled
      tool: task_exec
      owner: awa-si/awa@main:mcp/tasks/contract.md
      topic: tasks
      evidence: native_Task_result_or_Task_protocol_receipt
      boundary: no_general_shell|no_repository_checkout|no_host_escape|no_implicit_async_durability
  - workspace:
      intent: repository_tests|development|run|build|debug|dependency_toolchains|container_jobs|local_Git
      tool: workspace_exec
      owner: awa-si/awa@main:mcp/workspace/contract.md
      topic: workspace
      evidence: admitted_workspace_slot|native_job_terminal_status_and_result|separate_Git_push_receipt_if_publishing
      boundary: explicit_workspace_permission|repository_identity|slot|image|resource_and_environment_admission
  - durable_work:
      intent: dependent_steps|checkpointed_execution|operator_approval_resume|durable_receipts|governed_recovery
      tool: work_exec
      owner: awa-si/awa@main:mcp/work/contract.md
      topic: work
      evidence: work_id|native_DBOS_state|step_receipts|underlying_provider_results
      boundary: not_a_shell|not_an_automatic_replay_mechanism|not_ChatGPT_Work_mode
- domain_provider_routes:
  - github_remote:
      intent: direct_AWA_GitHub_read|search|bounded_remote_commit|branch_operation_when_this_AWA_route_explicitly_selected_and_permitted
      tool: github_exec
      owner: awa-si/awa@main:mcp/github/contract.md
      topic: github
      boundary: independent_AWA_host_GitHub_credentials|not_ChatGPT_GitHub_connector_grants|no_Workspace_checkout
      default_for_ordinary_repository_read_patch_write: ChatGPT_GitHub_connector_and_derivatives_per_workflow/github.md
  - agent:
      intent: registered_Agent_discovery|definitions|plans|provider_delegation
      tool: agent_exec
      owner: awa-si/awa@main:mcp/agent/contract.md
      topic: agent
      boundary: agent_descriptors_and_plans_are_read_only_not_approval|provider_invocation_retains_original_domain_gates
  - intelligence:
      intent: evidence_discovery|research_attempts|claims|entities|processing|reviewed_delivery
      tool: intelligence_exec
      owner: awa-si/awa@main:mcp/intelligence/README.md
      topic: intelligence
      boundary: domain_workflow_not_fourth_generic_execution_engine|delivery_requires_its_own_review_and_provider_receipt
  - host:
      intent: bounded_host_diagnostics|service_status|approved_maintenance|isolated_host_or_Odoo_tests|recovery_preflight
      tool_family: host_exec|host_odoo_*|host_work_*|host_podman_benchmark
      owner: awa-si/awa@main:mcp/host/contract.md
      topic: host
      boundary: allowlisted_operations_only|no_general_host_shell|effect_specific_operator_approval|isolation_and_release_gates
      mcp_update: honor_command.yaml_mcp_auto_update_owner|single_authorized_mcp_diagnostic_update_executor|separate_restart_and_runtime_verification
  - external_integrations:
      intent: Apple|Microsoft|Google|AWS|Odoo|messaging|social|browser|research_data|threat_intelligence|other_registered_provider_operation
      tool_family: current_specific_registered_provider_only
      owner: awa-si/awa@main:mcp/docs/TOOLS.md|matching_mcp/tools_or_interfaces_owner|provider_specific_current_contract
      topic: mcp_when_gateway_context_material|otherwise_narrow_registered_tool_document
      boundary: prefer_selected_native_ChatGPT_plugin_when_sufficient|verify_AWA_route_is_permitted|provider_credentials_and_effects_are_independent
  - session_and_resume:
      intent: explicitly_authorized_checkpoint|restore|revoke|session_binding_when_supported
      tool: session_exec
      owner: awa-si/awa@main:mcp/docs/tools/session_exec.md
      boundary: bearer_checkpoint_not_full_chat_snapshot|no_replay_or_cross_chat_permission_inferred
- observation_and_knowledge_not_execution_routes:
  - discover: mcp_model|mcp_instructions
  - gateway_diagnostics: mcp_diagnostic|mcp_version|mcp_trace|mcp_reload
  - cross_engine_observation: lifecycle
  - evidence_search: search|fetch|check_freshness|data_core|data_oai_pmh|data_openalex|ingest_text|ingest_url
  - exact_owner: current_tool_reference_and_live_registered_provider;read_only_hints_do_not_override_effect_checks
  - boundary: discovery|diagnostic|lifecycle_projection|knowledge_record_is_not_execution_admission|external_freshness_proof|publication_permission
  - config_reload: treat_reload_as_effectful_according_to_live_provider_schema_not_a_passive_status_check

awa_mcp_workspace_flow:
- apply_when: selected_authorized_AWA_MCP_Workspace_for_repository_execution_or_local_Git
- before_material_action: load_mcp_instructions(topic=workspace,full)|current_workspace_contract|matching_workflow/reuse_and_session_and_repository_and_execution_docs|live_workspace_exec_schema
- discovery: workspace_exec_capabilities_read_only_before_nontrivial_use|mcp_model_targeted_tool_detail
- identify: exact_repository|ref|slot|current_chat_binding|workspace_ownership|job_and_dirty_state
- cross_chat_reuse: enumerate_complete_relevant_registry_when_creation_or_import_considered|require_explicit_reuse_or_separate_or_none_choice_and_provider_authorization
- create: never_automatically_from_discovery_or_existing_registry_record|only_when_explicitly_selected_and_authorized_by_applicable_contract
- execution_preflight: repository_agent|workspace_profile|dependency_manifest|toolchain|image_allowlist|network|resource_limits|slot_and_environment_locks
- repository_acquisition: approved_session.prepare_or_repository_import_to_owning_slot;do_not_assume_import_means_compute_ready
- execution: workspace_exec_exec_start_or_current_supported_job_form_with_validated_payload|prefer_read_only_worktree_for_tests|send_runtime_outputs_and_caches_outside_repository
- publish: preserve_unrelated_dirty_edits|commit_intended_changes|workspace_exec_repository_push_with_expected_remote_head|verify_GitHub_remote_revision
- receipt: accepted_or_queued_is_not_terminal|retain_native_job_id|exec_status_and_exec_result_or_verified_inline_terminal_result
- unknown_effect: inspect_native_exec_reconcile_and_current_Git_state_before_retry|never_blind_replay
- recovery: follow_current_workspace_recovery_owner|never_unilaterally_recycle_or_replace_shared_workspace

awa_mcp_native_task_flow:
- load: mcp_instructions(topic=tasks,full)|current_Task_contract_and_matching_workflow
- discover: task_exec_capabilities|mcp_model_targeted_task_schema
- use_when: already_reviewed_bounded_handler|enabled_independently_sandboxed_TaskEngine
- enforce: reviewed_handler_permissions|explicit_runtime_profile|isolation|bounded_input_output|session_identity
- not_for: generic_host_shell|repository_test_container_jobs|Workspace_file_access_without_explicit_bridge
- completion: native_Task_receipt_or_direct_result|no_inferred_durable_Work_or_Workspace_job

awa_mcp_durable_work_flow:
- load: mcp_instructions(topic=work,full)|current_Work_contract_and_matching_workflow
- discover: work_exec_capabilities|current_operation_schema
- execution: plan_is_advisory|start_requires_current_admission_and_user_approval_where_relevant|preserve_work_id_and_step_ids
- dependency: provider_effects_execute_only_through_underlying_governed_capabilities
- completion: require_DBOS_result_plus_underlying_native_provider_receipts|do_not_treat_cancel_as_rollback
- recovery: reconcile_ambiguous_effects_first|no_automatic_start_retry_or_new_work_id

awa_mcp_host_flow:
- load: mcp_instructions(topic=host,full)|current_host_contract_and_matching_workflow
- discover: host_exec_capabilities_or_registered_specific_host_tool
- enforce: fixed_operations|provider_effect_gate|operator_approval|no_shell|protected_service_and_test_DB_boundaries
- update: use_command.yaml#governed_mcp_update_command_for_authorized_self_update|do_not_duplicate_git_pull_or_restart
- verify: host_checkout_state_and_loaded_process_identity_separately|native_action_receipts

awa_mcp_provider_flow:
- load: current_mcp_instructions_topic_if_matching|provider_owned_tool_reference|live_provider_operation_catalog
- selection: domain_intent_does_not_implicitly_choose_AWA_over_existing_ChatGPT_connector_or_plugin
- agent: agent_exec_can_delegate_only_registered_provider_operations|no_permission_inheritance_from_agent_card
- intelligence: system.capabilities_before_dispatch|separate_attempt|evidence|review|delivery|receipt
- external_effects: authenticate|scope|consent|policy|idempotency|recipient_or_target|provider_receipt
- observation: lifecycle_can_correlate_native_Task|Workspace_Job|DBOS_Work_but_never_replaces_their_native_result
- failed_capability: report_exact_missing_tool|operation|credential|admission_or_contract|fallback_only_to_separately_permitted_route

awa_mcp_completion:
- no_invented_success: discovery|plan|accepted|queued|runtime_ready|commit|deployment_are_distinct_stages
- verification: provider_native_result_for_each_effect|remote_revision_for_Git_changes|process_identity_for_runtime_activation|recipient_receipt_for_delivery_when_available
- uncertainty: keep_original_task_id|workspace_id_and_job_id|work_id|operation_reference;reconcile_before_any_side_effect_retry
- scope: reflect_only_verified_current_task_results|avoid_full_cross_provider_reinspection_without_new_evidence
- technical_change: AWA_repository_commit_does_not_activate_host_Runtime|separate_authorized_deploy_or_restart_and_live_verification
