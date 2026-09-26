scope: global_workflow
mode: normative_machine_directives
source: adapted_from_awa-si/nautilus/workflow.md

resolution:
- default_workflow: awa-si/admin/workflow.md
- project_extension: awa-si/admin/projects/<project>/workflow.md
- project_extension_required: false
- project_extension_semantics: extend_parent_and_explicit_override_only
- parent_rules_remain_active_unless_overridden: true

working_mode:
- default: local_disposable_workspace
- preferred_path: /tmp/<repo>
- repository_source_of_truth: remote_current_state
- refresh_before_new_coherent_change_if_remote_may_have_moved: true
- direct_remote_edit: fallback_or_small_deterministic_change
- github_actions: not_default_edit_test_loop

edit_flow:
- steps: read_current_target -> inspect_material_dependencies -> make_smallest_coherent_change -> run_lightest_relevant_local_checks -> inspect_status_and_complete_diff -> correct_unintended_changes -> commit -> verify_remote_result
- prefer_focused_patch_over_full_file_rewrite: true
- unrelated_refactors_in_same_change: prohibited
- docs_only_ci: avoid_unless_executable_examples_or_machine_checked_contracts_changed

verification_order:
- sequence: local_static_compile_import -> deterministic_contract_unit_functional -> local_status_diff_review -> focused_commit_push -> remote_compare_patch_verification -> github_actions_if_justified -> larger_empirical_run_if_justified
- escalate_only_if: risk|coupling|repo_rules|failure|runner_specific_evidence_needed
- never_claim_unobserved_execution: true

workspace:
- checkout_source: current_selected_branch
- if_git_clone_unavailable: use_connected_GitHub_transport
- preserve_repo_relative_paths_and_modes_when_possible: true
- exclude_from_commit: ignored|caches|venvs|generated_outputs|editor_state|workspace_metadata
- preserve_special_semantics: executable|symlink|submodule|binary|LFS

concurrency:
- guard: base_sha
- before_writeback: reread_branch_head
- head_unchanged: continue
- head_moved_nonoverlap: refresh -> reapply -> rerun_affected_verification
- head_moved_overlap: preserve_diff -> fetch_new_content -> reconcile_explicitly -> inspect_diff -> rerun_verification
- force_update_or_overwrite_newer_state: prohibited

commit_writeback:
- one_coherent_change: one_coherent_commit
- atomic_preferred_when_supported: create_blob* -> create_tree(base_tree_sha) -> create_commit(parent=base_sha) -> update_ref(force=false)
- fallback: precise_patch_or_per_file_write_with_current_blob_sha
- commit_message: user_supplied_else_concise_factual
- split_commits_only_if: user_requests|repo_requires|independent_rollback_boundary
- direct_selected_branch: default_when_allowed
- pull_request: only_if_explicitly_requested|required_by_repo|direct_write_blocked_and_authorized_fallback
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
- partial_remote_write: inspect_actual_remote_state_before_repair
- wrong_commit: prefer_revert_or_compensating_commit
- github_dns_failure: do_not_loop_clone; use_connected_GitHub_transport
