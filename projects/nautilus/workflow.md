scope: project_workflow_delta
project: nautilus
repository: awa-si/nautilus
branch: main
mode: normative_machine_directives

inherit:
- awa-si/admin/workflow.md
- override_only_if_explicit: true

historical_ml_validation:
- short_tests_must_preserve: target_maturation|causal_OOF_coverage|purge|embargo
- never_weaken_contract_to_make_short_test_pass: true
- staged_supervised_training:
  - preserve: purged_walk_forward|embargo|OOF_only_upstream_chaining
  - comparison_requires_same: dataset|horizon|folds|seed|estimator_config|label_semantics
  - report_stage_coverage_deficits: true

empirical_progression:
- order: local_contract_unit -> local_short_historical_smoke_if_practical -> committed_remote_state -> runner_integration_if_required -> medium_representative_window -> long_full_empirical_run
- insufficient_data: fail_closed; do_not_silently_change_model_or_causal_contract

multi_timeframe_ablation:
- workflow_role: integration_and_empirical_harness_not_default_dev_loop
- prerequisites: deterministic_compile_contract_unit_checks_normally_pass_locally_first
- canonical_remote_order: install_dependencies -> compile_relevant_path -> deterministic_timeframe_ablation_staged_runtime_tests -> one_historical_replay_collect_dataset -> train_evaluate_requested_profiles_on_same_dataset -> upload_aggregate_and_partial_profile_bundles
- historical_stage_if_contract_tests_fail: prohibited
- outputs: research_only
- deployable_runtime_bundle: false

performance_tracking:
- performance_file: performance.md
- update_when: measured_baseline_changed|bottleneck_ranking_changed|optimization_decision_changed
- preserve: trading_semantics|causal_contracts|schemas|inference_training_order
- hosted_runner_cross_run_wall_time: secondary_evidence
- same_run_ab_for_small_hot_path_changes: preferred

artifacts:
- research_ablation_profile_bundle_requires: run_or_head_sha|profile|schema_or_version
- research_output_promotion_to_live_artifact_location: prohibited
