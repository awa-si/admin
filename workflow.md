scope: global_workflow
mode: normative_machine_directives

resolution:
- owner: awa-si/admin/workflow.md
- project_extension: awa-si/admin/projects/<project>/workflow.md_if_present
- project_extension_semantics: extend_parent_and_explicit_override_only
- parent_rules_remain_active_unless_overridden: true

branch_resolution:
- priority: explicit_user_branch_in_current_task > clear_active_branch_from_current_chat > explicit_project_or_repository_branch > main
- do_not_infer_non_main_branch_from_stale_or_unrelated_context: true
- ask_user_instead_of_guessing_when: main_missing|multiple_materially_plausible_branches_change_task_semantics|branch_context_conflicts
- once_selected_for_task: keep_stable_until_user_or_material_repository_evidence_changes_it
- make_explicit_when: selected_branch_is_not_main|context_could_be_ambiguous

github_routing_gate:
- classify_before_repository_read_write_or_execution: Chat_Light|GitHub_Patch|GitHub_Workspace|AWA_MCP_Workspace|GitHub_Actions
- Chat_Light: use_for_non_coding_or_light_chat_work_without_repository_execution_or_workspace_need
- GitHub_Patch: default_for_known_small_deterministic_low_coupling_repository_change
- GitHub_Workspace: use_for_repository_coding_or_inspection_when_GitHub_access_is_needed_and_no_custom_system_packages_or_heavy_runtime_requirements_are_material
- GitHub_Workspace_runtime_posture: light_to_medium_repository_work
- GitHub_Workspace_dependency_posture: existing_environment_only
- GitHub_Workspace_dependency_installation: prohibited
- GitHub_Workspace_pip_or_language_package_install: prohibited
- GitHub_Workspace_runtime_modification: prohibited
- AWA_MCP_Workspace: use_for_heavy_lifting|long_running_processes|large_tests|builds|benchmarks|replays|data_processing|custom_system_packages|special_runtime_profiles|resource_intensive_execution
- AWA_MCP_Workspace_select_when: dependency_installation_or_runtime_modification_is_required|heavy_or_long_execution_is_material|custom_system_packages_or_repository_workspace_profile_is_required|GitHub_Workspace_runtime_is_insufficient|explicit_user_selection
- default_workspace_route_for_light_to_medium_repo_work: GitHub_Workspace
- default_workspace_route_for_heavy_or_long_work: AWA_MCP_Workspace
- GitHub_Actions_select_when: hosted_runner_or_durable_integration_evidence_material
- reclassify_when_scope_or_runtime_requirements_change_materially: required
- completion_requires_route_compliance: true

github_patch:
- role: connected_GitHub_connector_fast_path
- remote_transport: connected_GitHub_connector
- use_for: small_deterministic_edit|small_docs_edit|known_file_known_change|focused_low_coupling_fix|small_coherent_known_multi_file_edit_without_local_execution
- existing_file_flow: fetch_current_content_and_blob_sha -> smallest_coherent_edit -> guarded_update_with_observed_sha -> single_sufficient_remote_verification
- new_file_flow: create_file -> single_sufficient_remote_verification
- delete_file_flow: fetch_current_blob_sha -> guarded_delete -> single_sufficient_remote_verification
- avoid_unnecessary: repository_search|plugin_discovery|workspace_materialization|tree_reconstruction|redundant_head_reads_when_target_is_known
- same_path_writes: serialize
- stale_or_ambiguous_write: inspect_actual_remote_state_before_retry
- CI_or_status_polling: only_when_material
- route_to_workspace_if: local_execution|test_or_build|dependency_discovery|broad_search|uncertain_coupling

awa_mcp_workspace:
- role: heavy_or_explicit_workspace_route
- independent_from_GitHub_Workspace_contract: true
- selection_owner: github_routing_gate
- availability_gate: required_before_selection
- native_instruction_source: mcp_instructions(topic="workspace")
- load_current_native_workspace_instructions_before_use: required
- native_workspace_contract: authoritative_for_AWA_workspace_mechanics
- current_AWA_MCP_tool_schema: authoritative_for_exposed_workspace_capabilities
- chat_workspace_lifecycle:
  - workspace_identity_exposed_to_chat_and_handoff: workspace_id
  - creator_key:
    - native_parameter: workspace_create.id
    - admin_name: creator_id
    - purpose: opaque_stable_client_key_for_create_and_resolve_only
    - do_not_conflate_with_workspace_id: true
    - do_not_expose_as_primary_workspace_identity: true
  - first_AWA_workspace_use:
    - generate_stable_opaque_creator_id: required
    - first_workspace_action: workspace_create(id=creator_id)
    - capture_from_create_result: workspace_id|effective_resources|parallelism
    - first_AWA_workspace_use_chat_output: workspace_id|effective_resources|parallelism
    - retain_for_lifecycle: creator_id|workspace_id|effective_resources|parallelism|repository_binding|branch
  - resource_output_fields: cpu|memory_mb|storage_mb|pids|tmp_mb
  - retained_workspace_id_is_authoritative: true
  - do_not_scan_for_alternative_workspace: true
  - do_not_call_workspace_create_again_while_retained_workspace_exists: true
  - do_not_switch_workspace_id_silently: true
  - do_not_replace_missing_or_unhealthy_workspace_automatically: true
  - missing_or_unhealthy_retained_workspace: surface_blocker_and_keep_identity
  - workspace_resolve_role: diagnostic_by_creator_id_only_not_workspace_selection
  - replacement_allowed_only_after: explicit_user_approved_workspace_delete_then_workspace_create_with_same_creator_id
  - after_replacement_create: capture_and_report_workspace_id|effective_resources|parallelism
  - other_chat_workspace: distinct_unless_initialized_from_explicit_handoff
  - handoff_initialized_chat:
    - default_behavior: inherit_handoff_workspace
    - required_handoff_fields: workspace_id
    - preserve_when_available: creator_id|effective_resources|parallelism|repository_binding|branch|active_jobs|artifacts|checkpoint|resume_point
    - first_AWA_workspace_action: workspace_context(workspace_id=handoff_workspace_id)
    - require_context_workspace_id: handoff_workspace_id
    - do_not_call_workspace_create_when_inherited_workspace_context_is_valid: true
    - do_not_generate_new_workspace_id_when_inherited_workspace_context_is_valid: true
    - inherited_workspace_becomes_authoritative_for_new_chat: true
    - inherited_workspace_missing_or_mismatch: surface_blocker_do_not_replace_automatically
    - replacement_after_handoff:
      - requires_explicit_user_approved_workspace_delete: true
      - requires_original_creator_id: true
      - missing_creator_id: surface_blocker_for_replacement_not_for_existing_workspace_use
      - recreate_with: workspace_create(id=creator_id)
    - repository_and_branch_from_handoff: working_context_only_until_current_remote_state_verified_when_material
    - job_or_artifact_from_handoff: verify_current_workspace_state_before_resume
  - parallel_chat:
    - default_behavior: independent_workspace
    - workspace_sharing_between_simultaneously_active_chats: prohibited_unless_explicit_user_instruction
    - same_repository_concurrent_work: separate_workspace_and_separate_working_branch
    - working_branch_per_chat_or_workstream: required_for_independent_concurrent_changes
    - handoff_branch_inheritance_does_not_apply_to_independent_parallel_chat: true
    - shared_integration_point: GitHub_remote
    - same_remote_branch_concurrent_push_if_explicitly_used: require_expected_remote_head_and_non_force_push
    - remote_head_changed: fetch_integrate_reverify_before_push
    - automatic_force_push_or_silent_branch_overwrite: prohibited
    - integration_to_shared_branch: explicit_merge|rebase|cherry_pick|pull_request_as_task_requires
- execution_orchestration:
  - default_workspace_create_parallelism: 1
  - expand_slots_only_when_real_parallel_work_requires_it: workspace_expand_slots
  - speculative_slot_allocation: prohibited
  - slot_expansion_is_monotonic_for_workspace_lifetime: true
  - dependency_sensitive_execution:
    - repository_import_does_not_imply_compute_ready: true
    - before_first_compute: resolve_repository_instructions_and_workload_manifests
    - install_only_required_dependencies: true
    - dependency_setup_job: workspace_exec_start(shared_env_access="write",network=true)_when_external_retrieval_required
    - subsequent_compute_default: shared_env_access="read"
    - network_after_setup: false_unless_workload_itself_requires_network
    - dependency_source_changed: re_evaluate_shared_environment_before_compute
  - asynchronous_jobs:
    - use_start_status_result_flow: required
    - timeout_remaining_seconds_is_not_ETA: true
    - extend_running_job_when_more_budget_is_justified: workspace_exec_extend
    - extension_requires_process_local_running_job: true
    - completed_status_and_result_history_survives_MCP_restart: true
    - detached_after_restart: inspect_then_terminate_or_restart_not_extend
    - do_not_classify_restart_recovered_terminal_result_as_lost_without_checking_persisted_result: true
- repository_remote_transport:
  - applies_when: AWA_MCP_Workspace_with_GitHub_bound_repository
  - workspace_exec_git_scope: local_only
  - allowed_local_git: status|diff|add|commit|checkout|switch|merge|rebase|cherry_pick|reset|restore|stash|tag|log|show
  - prohibited_from_workspace_exec: git_fetch|git_pull|git_push|git_clone|other_GitHub_remote_transport
  - reason: workspace_exec_containers_do_not_receive_GitHub_credentials
  - authenticated_remote_read: workspace_repository_fetch
  - authenticated_remote_write: workspace_repository_push
  - initial_materialization: workspace_repository_import
  - credential_failure_from_direct_workspace_git_remote: classify_as_wrong_transport_path_not_missing_user_credentials
  - on_direct_git_remote_failure: retry_via_corresponding_workspace_repository_boundary_tool
  - do_not_ask_user_for_GitHub_username_or_token_when_bound_repository_tool_is_available: true
- repository_temp_data_boundary:
  - apply_when: AWA_workspace_contains_or_imports_GitHub_repository
  - temporary_runtime_data_must_not_be_repository_content_or_commit_candidate: true
  - prefer_workspace_data_or_work_state_for: logs|replay_outputs|benchmarks|downloads|large_datasets|scratch_files|runtime_state|generated_intermediate_data
  - native_workspace_internal_paths_allowed_when_contract_defined: .venv|.awa-mcp
  - native_internal_paths_must_remain_git_excluded: true
  - do_not_stage_or_commit_temporary_data: true
  - repository_artifact_exception: only_when_artifact_is_explicitly_part_of_repository_contract_or_user_requests_commit
  - before_commit: verify_temporary_runtime_data_is_not_in_git_status
- admin_local_workspace_mechanics: fallback_only_if_native_workspace_instruction_source_is_unavailable
- admin_owns_only: route_selection|chat_lifecycle_policy|fallback_policy|cross_route_precedence|completion_requirement
- unavailable_or_unhealthy: surface_actual_blocker
- remote_completion_claim_requires: verification_required_by_current_native_workspace_contract

github_workspace:
- role: route_to_installed_GitHub_Workspace_skill
- skill: skills://plugins/github-workspace-web/github-workspace/skill.md
- load_current_skill_before_use: required
- skill_execution_contract: authoritative_for_workspace_mechanics
- repository_remote_reads_and_writes: connected_GitHub_connector_only
- repository_acquisition: connector_mediated_materialization
- repository_remote_transport_from_shell: prohibited
- local_git_scope: offline_diff|status|hash_mechanics_only
- local_workspace: temporary_connector_materialized_snapshot
- external_runtime_substitution: prohibited_unless_explicitly_selected_by_route_or_user
- dependency_resolution_before_materialization: required_once_per_scope_version
- dependency_closure_freeze_before_file_fetch: required
- parallel_connector_fetch_after_dependency_join: preferred_and_bounded
- fetch_lanes_consume_frozen_scope: required
- dependency_scope_reopen_only_on_new_material_evidence_or_scope_change: required
- incomplete_dependency_coverage_must_limit_completion_claim: true
- detached_or_background_jobs: prohibited
- long_or_resource_heavy_local_jobs_default_concurrency: 1
- reread_skill_if: plugin_changed|skill_changed|explicitly_requested|workspace_capability_changed

github_actions:
- use_when: hosted_runner_behavior|workflow_integration|platform_difference|artifact_contract|matrix_execution|long_reproducible_experiment|remote_sha_tied_evidence|durable_long_execution_required
- do_not_use_merely_because_code_changed: true
- old_run_rerun_after_code_change: prohibited
- start_new_run_on_new_head: required

edit_and_writeback:
- smallest_coherent_change: required
- unrelated_refactor_in_same_change: prohibited
- docs_only_ci: avoid_unless_executable_examples_or_machine_checked_contracts_changed
- one_coherent_change: one_coherent_commit_when_supported
- commit_message: user_supplied_else_concise_factual
- split_commits_only_if: user_requests|repo_requires|independent_rollback_boundary
- pull_request: only_if_explicitly_requested|required_by_repo|direct_write_blocked_and_authorized_fallback
- merge_pull_request: only_if_explicitly_requested
- force_push_or_force_overwrite: prohibited
- same_path_edits|shared_mutable_state|lockfile_mutation|branch_ref_mutation|final_writeback: serialize

verification:
- order: syntax_static -> focused_tests -> affected_package_tests -> broader_suite
- never_claim_unobserved_execution: true
- remote_ci: only_if_material
- completion_claim: only_after_route_appropriate_remote_verification

long_running_and_recovery:
- local_workspace_runtime: ephemeral_not_durable_job_runner
- split_long_work_into_resumable_bounded_stages_when_practical: true
- preserve_partial_evidence: required
- persist_material_intermediate_evidence_before_next_expensive_stage_when_loss_is_material: required
- local_checkpoint: recovery_aid_not_durable_persistence
- runtime_disappearance_without_durable_terminal_evidence: classify_as_unknown_or_lost
- durable_long_execution_materially_required: consider_GitHub_Actions_only_when_user_intent_and_repository_policy_allow
- patch_partial_remote_write: inspect_actual_remote_state_then_continue_or_compensate_without_blind_retry
- GitHub_Workspace_unavailable: AWA_MCP_Workspace_may_be_used_as_fallback
- AWA_MCP_Workspace_unavailable_when_selected: surface_actual_blocker
- AWA_MCP_Workspace_recycled_or_missing: surface_blocker_and_do_not_create_replacement_automatically
- GitHub_Workspace_recovery: delegate_to_current_GitHub_Workspace_skill
- wrong_commit: prefer_revert_or_compensating_commit

performance_evidence:
- optimize_measured_bottlenecks_first: true
- preserve_domain_semantics_and_contracts: required
- compare_same_workload_before_after: true
- focused_local_measurement_first_when_representative: true

artifacts_and_logs:
- workflow_artifacts: evidence_not_implicit_production_state
- attach_when_relevant: run_or_head_sha|experiment_or_profile|schema_or_version
- failed_run_debug: inspect_exact_failing_step_and_traceback_before_code_change
- volatile_local_artifact_required_for_resume: insufficient_without_durable_preservation
