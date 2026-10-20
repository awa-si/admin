scope: project_workflow_delta
project: awa
mode: extend_parent_and_explicit_override_only

inherit:
- awa-si/admin/workflow.md
- override_only_if_explicit: true

repository:
- source_of_truth: awa-si/awa@main
- branch: main
- agent: AGENTS.md

awa_workspace:
- preferred_heavy_execution_route: AWA_MCP_Workspace
- repository_slot_default: 1
- repository_profile_owner: awa-si/awa/workspace.ini
- repository_profile_must_be_applied_after_import: true
- workspace_create_resources: provisional_workspace_defaults_not_repository_profile
- required_bootstrap_sequence: workspace_create -> workspace_repository_import(awa-si/awa@main) -> inspect_import_profile -> workspace_context(include_toolchain=true) -> execute
- before_first_execution: verify_bound_repository_is_awa-si/awa|verify_profile_base_image|verify_effective_resources|verify_dataset_and_network_configuration
- profile_source_of_truth: repository_root_workspace.ini_as_validated_by_MCP
- never_infer_profile_applied_from: workspace_create_success|repository_name_in_chat|GitHub_connector_file_read
- profile_missing_or_rejected: stop_and_report_actual_error_before_execution
- execution_image: select_exact_effective_profile_image_from_import_or_workspace_context
- default_image_fallback: allowed_only_when_no_repository_profile_exists_and_native_contract_permits
- post_profile_change_on_existing_bound_workspace: workspace_profile_reload_when_idle_then_verify_context_before_execution
- do_not_duplicate_workspace_resource_values_in_admin: true
- effective_profile_source: workspace_repository_import.profile|workspace_context
- repository_history:
  - complete_history_required: true
  - shallow_or_grafted_history_for_normal_development: prohibited
  - legacy_shallow_workspace: workspace_repository_fetch_must_unshallow_before_history_dependent_sync
- local_git:
  - normal_sync: workspace_repository_fetch -> integrate_FETCH_HEAD -> verify_clean_state
  - allowed_integration: rebase|merge|cherry_pick
  - reset_plus_cherry_pick: recovery_only_not_normal_sync
  - remote_transport_from_workspace_exec: prohibited
  - direct_git_fetch_pull_push_clone_from_workspace_exec: prohibited
  - remote_read: workspace_repository_fetch
  - remote_write: workspace_repository_push
  - direct_remote_credential_error: wrong_transport_path_not_missing_credentials
  - force_push: prohibited
  - existing_branch_push_requires_expected_remote_head: true

compute_readiness:
- repository_import_state: source_ready_not_automatically_compute_ready
- profile_system_packages: deferred_until_first_execution_using_profile_image
- dependency_owner: repository_instructions_and_workload_manifests_or_lockfiles
- shared_environment:
  - canonical_reuse_scope: workspace
  - setup_access: shared_env_access_write
  - normal_compute_access: shared_env_access_read
  - setup_network: enable_only_when_package_retrieval_required
- parallel_slots:
  - initial_parallelism: 1
  - expand_lazily_with: workspace_expand_slots
  - extra_slots_require_real_parallel_work: true
  - dependency_setup_is_workspace_wide_exclusive: true
- jobs:
  - running_timeout_extension: workspace_exec_extend_when_material
  - completed_result_history_after_MCP_restart: reusable_evidence
  - detached_job: cannot_extend_requires_inspect_terminate_or_restart

parallel_chat:
- inherit_global_parallel_chat_policy: true
- independent_AWA_workstreams: separate_workspace_id_and_working_branch
- explicit_handoff: inherit_workspace_id_and_active_branch
- same_main_branch_concurrent_direct_work: discouraged
- remote_head_changed_before_push: fetch_integrate_reverify
- shared_integration_point: awa-si/awa@main

awa_work:
- canonical_contract: awa-si/awa/mcp/work/workflow.md
- use_for_repo_work_only_when_durable_orchestration_is_material: true
- ordinary_AWA_repo_edit_test_commit_without_durability_need: use_AWA_MCP_Workspace_not_AWA_Work
- public_work_tool_change:
  - update_owner_docs: mcp/work/README.md|mcp/work/workflow.md
  - focused_tests_required_for_affected_surface: plan_validation|start_status_result|approval_resume|reconciliation|cancellation|audit|restart_or_durability_when_affected|work_recursion_rejection
  - runtime_claim_requires_live_endpoint_verification: true

mcp_runtime_change:
- canonical_runtime_contract: awa-si/awa/mcp/README.md|awa-si/awa/mcp/workspace.md
- mcp_reload_env: configuration_reload_only
- mcp_reload_toolchain: environment_backed_interface_reconstruction_without_python_code_hot_reload
- python_implementation_or_tool_registration_change: normal_MCP_process_restart_or_redeploy_required
- WorkspaceInterface_constructor_policy_change: normal_MCP_process_restart_or_redeploy_required
- do_not_claim_runtime_active_from_repository_commit_alone: true
- post_restart_or_redeploy: verify_live_MCP_capability_when_material

verification:
- workspace_or_GitHub_boundary_change:
  - focused_tests_first: mcp/tests/test_github_workspace.py|mcp/tests/test_workspace_interface.py_as_affected
  - git_diff_check: required
  - broader_tests: only_when_material_to_changed_contract
- runtime_behavior_claim: requires_live_runtime_evidence
- repository_write: verify_remote_head_or_changed_files_as_material
