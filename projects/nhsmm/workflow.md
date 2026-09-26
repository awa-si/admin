scope: project_workflow_delta
project: nhsmm
repository: awa-si/nhsmm
branch: develop
extends: awa-si/admin/workflow.md
mode: extend_parent_and_explicit_override_only

local_execution:
- performance_work: prefer_local_workspace
- preferred_workspace: /tmp/nhsmm
- editable_install: preferred
- normal_install: python -m pip install -e .
- offline_or_dependency_preinstalled_install: python -m pip install -e . --no-deps --no-build-isolation
- no_deps_install_claim: must_not_be_described_as_dependency_resolution_or_clean_environment_validation
- local_edit_profile_measure_cycles_before_remote_write: required_when_practical
- github_actions_as_performance_edit_loop: prohibited

performance_method:
- profile_current_head_before_optimization: required
- optimize_measured_hotspot_only: true
- benchmark_same_workload_same_host_before_after: required
- separate_latency_from_allocation_tracing: required
- tracemalloc_during_latency_pass: prohibited
- report: mean|p50|p95_when_available
- preserve_probabilistic_semantics: required
- preserve_public_api_by_default: true
- preserve_artifact_and_state_dict_schema_by_default: true
- global_torch_thread_or_process_runtime_setting_changes: avoid_unless_explicitly_justified_and_benchmarked
- benchmark_absolute_hosted_runner_latency_as_acceptance_threshold: prohibited

streaming_optimization:
- canonical_path: DefaultEncoder(causal=True)|HSMMFilterRuntime.step
- bounded_state_size: preserve
- reference_equivalence_required_for_custom_fast_path: true
- compare_against: full_causal_encoder|public_validating_filter_path|existing_distribution_semantics_as_applicable
- numerical_tolerance: document_observed_error_and_keep_within_existing_contract_tolerance
- reuse_existing_parameters: prefer_over_new_parallel_parameterization
- artifact_schema_change_for_pure_runtime_fast_path: avoid

benchmarking:
- canonical_runtime_benchmark: scripts/benchmark_runtime.py
- artifact_loaded_runtime_measurement: preferred_for_production_reference
- allocation_measurement: separate_pass
- local_profile_may_use_focused_harness: true
- retain_workload_dimensions_in_report: K|F|D|batch_size|steps|warmup
- cross_environment_comparison: label_as_non_direct_when_runtime_or_host_differs

verification:
- focused_equivalence_test_before_broad_suite: required_for_fast_path
- full_pytest_after_shared_encoder_filter_distribution_runtime_change: required
- clean_runner_smoke: use_only_for_final_integration_evidence_when_material
- temporary_push_trigger_if_needed: follow_global_ci_actions_rules
- update_docs_state_after_verified_performance_change: true

completion_evidence:
- distinguish: local_profile|local_benchmark|clean_runner_benchmark|numerical_equivalence|full_test_suite
- performance_improvement_claim_requires_observed_before_after: true
- semantic_equivalence_claim_requires_observed_reference_comparison: true
- unexecuted_static_checks_must_remain_explicitly_unverified: true
