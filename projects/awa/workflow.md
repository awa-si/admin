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
- do_not_duplicate_workspace_resource_values_in_admin: true
- effective_profile_source: workspace_repository_import.profile|workspace_context
- execution_image: use_generated_repository_profile_image_when_present_else_localhost/workspace:py
- repository_history:
  - complete_history_required: true
  - shallow_or_grafted_history_for_normal_development: prohibited
  - legacy_shallow_workspace: workspace_repository_fetch_must_unshallow_before_history_dependent_sync
- local_git:
  - normal_sync: workspace_repository_fetch -> integrate_FETCH_HEAD -> verify_clean_state
  - allowed_integration: rebase|merge|cherry_pick
  - reset_plus_cherry_pick: recovery_only_not_normal_sync
  - remote_write: workspace_repository_push
  - force_push: prohibited
  - existing_branch_push_requires_expected_remote_head: true

parallel_chat:
- inherit_global_parallel_chat_policy: true
- independent_AWA_workstreams: separate_workspace_id_and_working_branch
- explicit_handoff: inherit_workspace_id_and_active_branch
- same_main_branch_concurrent_direct_work: discouraged
- remote_head_changed_before_push: fetch_integrate_reverify
- shared_integration_point: awa-si/awa@main

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
