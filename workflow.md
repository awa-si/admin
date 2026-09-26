scope: global_workflow
mode: normative_machine_directives
source: adapted_from_awa-si/nautilus/workflow.md

resolution:
- default_workflow: awa-si/admin/workflow.md
- project_extension: awa-si/admin/projects/<project>/workflow.md
- project_extension_required: false
- project_extension_semantics: extend_parent_and_explicit_override_only
- parent_rules_remain_active_unless_overridden: true

github_routing_gate:
- before_any_repository_read_write_or_execution_task: classify_route_as_GitHub_Patch|GitHub_Workspace|GitHub_Actions
- route_decision_is_mandatory_not_advisory: true
- default_for_known_small_deterministic_low_coupling_change: GitHub_Patch
- mandatory_workspace_if_any: broad_search|repository_wide_inspection|local_execution|script_execution|test_or_lint_required|build_required|repeated_edit_test_cycle|multi_file_coupling|generated_artifact_analysis|ci_artifact_analysis|change_scope_uncertain
- patch_must_not_be_stretched_to_avoid_workspace: true
- if_patch_task_expands_beyond_patch_criteria: stop_remote_editing -> open_GitHub_Workspace -> continue_from_current_remote_state
- if_workspace_task_collapses_to_single_known_deterministic_change_before_materialization: GitHub_Patch_allowed
- reclassify_route_when_scope_changes_materially: required
- completion_requires_route_compliance: true
- if_required_route_unavailable: use_documented_safe_fallback_only; never_simulate_or_claim_unperformed_workspace_or_patch

github_routing:
- transport: connected_GitHub_connector
- separate_mcp_for_github_workspace: not_required
- small_deterministic_edit: GitHub_Patch
- docs_only_small_edit: GitHub_Patch
- broad_search|repository_wide_inspection|local_execution|repeated_edit_test|multi_file_coupling|build_or_test_required|ci_artifact_analysis: GitHub_Workspace
- github_actions: only_if_runtime_or_hosted_integration_evidence_required
- direct_contents_api: allowed_for_precise_single_file_or_fallback_write
- force_push_or_force_ref_update: prohibited

github_patch:
- role: precise_remote_patch_path
- required_for: small_deterministic_edit|small_docs_edit|known_file_known_change|focused_low_coupling_fix
- prerequisite: read_current_target_and_current_blob_sha
- inspect_dependencies_before_patch: when_material
- patch_scope: smallest_coherent_diff
- preserve: unrelated_content|formatting|file_mode|newer_remote_state
- blind_global_replace: prohibited
- whole_file_rewrite_when_focused_patch_suffices: avoid
- same_path_writes: sequential
- multi_file_patch: allowed_only_when_one_coherent_change_and_tool_supports_safe_combined_write
- before_write: verify_target_content_matches_patch_assumptions
- before_commit_or_remote_mutation: reread_branch_head_when_concurrency_material
- after_write: refetch_changed_paths|verify_exact_content|verify_resulting_commit_or_branch_head
- tests: run_only_when_change_semantics_require_them; docs_only_default_no_ci
- if_patch_context_stale_or_conflicts: stop_patch -> refresh_current_state -> reapply_intent
- if_change_requires_broad_search_or_execution: route_to_GitHub_Workspace
- if_patch_tool_unavailable: use_precise_contents_API_with_current_blob_sha; do_not_claim_GitHub_Patch_used

github_workspace:
- role: local_materialized_repository_work_path
- required_for: broad_search|repository_wide_inspection|local_execution|scripts|tests|linters|builds|repeated_edit_test|multi_file_coupling|generated_artifact_analysis|ci_artifact_analysis|uncertain_change_scope
- transport: connected_GitHub_connector_or_installed_GitHub_app
- separate_workspace_mcp: not_required
- preferred_path: /tmp/<repo>
- open_steps: resolve_repository_branch_head_sha_base_tree_sha -> read_applicable_instructions -> materialize_required_repo_state -> write_workspace_metadata
- complete_snapshot: prefer_for_small_or_medium_repo
- sparse_snapshot: allowed_for_large_or_narrow_task_only_if_dependency_closed_and_marked_partial
- tree_enumeration: recursive_when_available; inspect_truncation_before_assuming_complete
- metadata_file: .chatgpt-github/workspace.json
- metadata_required: repository|branch|base_sha|base_tree_sha|scope|blob_shas|modes|skipped_paths|complete_flag
- terminology_without_real_git_clone: snapshot_or_workspace_checkout
- special_entries: preserve_when_supported; never_fake_binary|LFS|submodule|symlink|executable_semantics
- unsupported_special_entry: record_limit_and_exclude_from_unsafe_rewrite
- local_use: search|inspect|edit|run_scripts|tests|linters|builds|generate_artifacts|status|diff
- local_edit_test_cycles_before_remote_mutation: preferred
- status_without_git: modified|added|deleted|mode_changed|ignored|rename_candidates
- before_nontrivial_writeback: inspect_changed_paths_and_complete_diff_when_practical
- exclude_from_writeback: ignored|caches|venvs|generated_outputs_unless_intended|editor_state|workspace_metadata
- dry_run|preview|show_diff|do_not_commit: stop_before_remote_mutation
- writeback: guarded_against_base_sha_and_current_branch_head
- writeback_preference: one_coherent_atomic_commit_when_supported
- writeback_fallback: GitHub_Patch_or_precise_per_file_write_with_current_blob_sha
- after_writeback: verify_resulting_commit|branch_head|changed_file_set|absence_of_unintended_files
- preserve_workspace_and_intended_diff_until_remote_verified: true
- if_workspace_transport_or_materialization_unavailable: use_GitHub_Patch_only_for_safe_small_deterministic_work; otherwise report_execution_limit_without_faking_local_run
- github_actions_as_edit_test_loop: prohibited

awa_mcp:
- availability: available
- scope: AWA_specific_state|operations|authoritative_internal_resolution
- prefer_when: authoritative_or_most_direct_AWA_source
- use_before_generic_repository_or_web_path_when_it_owns_the_requested_AWA_state: true
- do_not_substitute_for_GitHub_when_repo_content_is_canonical: true
- never_assume: undocumented_tools|data|permissions|side_effects
- if_not_capable_for_requested_operation: continue_with_next_authoritative_source
- cross_source_conflict: identify_explicitly; prefer_canonical_owner_for_the_fact_or_operation

workspace_lifecycle:
- state_machine: OPEN->DIRTY->VERIFIED->PREVIEWED->COMMITTED->VERIFIED_REMOTE
- recovery_paths: REFRESH|REAPPLY|RECOVER
- open: materialize_repo_state
- status: classify_local_changes_vs_baseline
- diff: inspect_changed_paths_and_text_diff
- refresh: detect_remote_branch_movement
- reapply: move_local_intent_to_new_base_when_safe
- test: run_narrowest_meaningful_verification
- preview: inspect_exact_intended_writeback
- commit: guarded_atomic_commit_when_supported
- verify: verify_commit_branch_files_ci_artifacts_when_relevant
- recover: preserve_and_reconcile_local_work

workspace:
- default: local_disposable_workspace
- preferred_path: /tmp/<repo>
- repository_source_of_truth: remote_current_state
- checkout_source: current_selected_branch
- if_git_clone_unavailable: use_connected_GitHub_transport
- resolve_before_materialization: repository|branch|head_sha|base_tree_sha
- enumerate_tree: recursive_when_available; inspect_truncation
- metadata_file: .chatgpt-github/workspace.json
- metadata_required: repository|branch|base_sha|base_tree_sha|scope|blob_shas|modes|skipped_paths|complete_flag
- terminology: snapshot_or_workspace_checkout_unless_actual_git_clone
- snapshot_policy_small_medium: complete
- snapshot_policy_large_or_narrow: dependency_closed_sparse
- sparse_workspace_must_be_marked_partial: true
- preserve_repo_relative_paths_and_modes_when_possible: true
- preserve_special_semantics: executable|symlink|submodule|binary|LFS
- unsupported_special_entries: no_placeholders; record_binary|oversized|LFS|submodule|special_limits
- exclude_from_commit: ignored|caches|venvs|generated_outputs|editor_state|workspace_metadata
- status_without_git: modified|added|deleted|mode_changed|ignored|rename_candidates
- local_edit_test_cycles_before_remote_mutation: preferred
- dry_run|preview|show_diff|do_not_commit: stop_before_remote_mutation
- refresh_before_new_coherent_change_if_remote_may_have_moved: true

edit_flow:
- steps: classify_GitHub_route -> read_current_target -> inspect_material_dependencies -> make_smallest_coherent_change -> run_lightest_relevant_local_checks -> inspect_status_and_complete_diff -> correct_unintended_changes -> commit -> verify_remote_result
- route_reclassification_on_material_scope_change: required
- prefer_focused_patch_over_full_file_rewrite: true
- unrelated_refactors_in_same_change: prohibited
- docs_only_ci: avoid_unless_executable_examples_or_machine_checked_contracts_changed

verification:
- order: syntax_static -> focused_tests -> affected_package_tests -> broader_suite
- escalate_only_if: risk|coupling|repo_rules|failure|runner_specific_evidence_needed
- record: material_commands|results|runtime_limits|sparse_workspace_limits
- never_claim_unobserved_execution: true
- remote_ci: only_if_material

concurrency:
- guard: base_sha
- before_writeback: reread_branch_head
- head_unchanged: continue
- head_moved: never_overwrite; never_force
- head_moved_nonoverlap: refresh -> reapply -> rerun_affected_verification
- head_moved_overlap: preserve_diff -> fetch_new_content -> reconcile_explicitly -> inspect_diff -> rerun_verification

commit_writeback:
- one_coherent_change: one_coherent_commit
- atomic_path_when_supported: create_blob* -> create_tree(base_tree_sha) -> create_commit(parent=base_sha) -> update_ref(force=false)
- atomic_tree_base: must_use_base_tree_sha
- replacement_tree_from_changed_paths_only: prohibited
- deletions: use_supported_tree_delete_semantics
- fallback: GitHub_Patch_or_per_file_write_with_current_blob_sha
- per_file_fallback_atomic_claim: prohibited
- commit_message: user_supplied_else_concise_factual
- split_commits_only_if: user_requests|repo_requires|independent_rollback_boundary
- direct_selected_branch: default_when_allowed
- pull_request: only_if_explicitly_requested|required_by_repo|direct_write_blocked_and_authorized_fallback
- merge_pull_request: only_if_explicitly_requested
- force_push: prohibited

remote_verification:
- verify: resulting_commit|changed_file_set|branch_head|absence_of_unintended_files
- inspect_status_checks_jobs_logs_artifacts: when_material
- ci_failure: identify_earliest_causal_failure
- completion_claim: only_after_remote_verification

ci_actions:
- use_when: hosted_runner_behavior|workflow_integration|platform_difference|artifact_contract|matrix_execution|long_reproducible_experiment|remote_sha_tied_evidence
- do_not_use_merely_because_code_changed: true
- expensive_empirical_workflows_default_trigger: workflow_dispatch
- temporary_push_trigger_if_dispatch_unavailable:
  - scope_narrowly: true
  - run_only_intended_validation: true
  - restore_canonical_trigger_immediately_after_start: true
  - retain_as_architecture: false
- old_run_rerun_after_code_change: prohibited; start_new_run_on_new_head

long_running_jobs:
- preserve_partial_evidence: required
- emit_incremental: progress|stage_timings|logs|counters
- structure_into_observable_stages: true
- write_partial_reports_or_checkpoints_when_meaningful: true
- upload_useful_diagnostics_on_failure_or_cancel_when_possible: true
- make_last_completed_stage_and_active_bottleneck_obvious: true
- inspect_existing_partial_logs_and_artifacts_before_rerun: true

performance:
- optimize_measured_bottlenecks_first: true
- preserve_domain_semantics_and_contracts: required
- compare_same_workload_before_after: true
- focused_local_measurement_first_when_representative: true
- same_run_ab_when_environment_variance_material: preferred
- cross_runner_wall_clock: treat_cautiously

artifacts_logs:
- workflow_artifacts: evidence_not_implicit_production_state
- attach_when_relevant: run_or_head_sha|experiment_or_profile|schema_or_version
- research_output_to_live_location_as_promotion: prohibited
- failed_run_debug: inspect_exact_failing_step_and_traceback_before_code_change
- reproduce_locally_first_when_possible: true

workflow_maintenance:
- obsolete_one_off_workflow: remove_unless_intentional_reusable_tool
- prefer_one_clear_workflow_per_repeatable_empirical_purpose: true
- workflow_changes: engineering_changes
- verify_yaml_or_diff_locally_when_possible: true
- execute_remote_workflow_only_if_integration_behavior_materially_needs_runtime_evidence: true

recovery:
- preserve_workspace_and_intended_diff_until_remote_verified: true
- git_objects_created_before_ref_update: not_branch_mutation
- partial_remote_write: inspect_actual_remote_state_before_repair
- wrong_commit: prefer_revert_or_compensating_commit
- github_dns_failure: do_not_loop_clone; use_connected_GitHub_transport
