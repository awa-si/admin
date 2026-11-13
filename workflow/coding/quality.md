scope: conditional_coding_detail
mode: normative_machine_directives
inherits: awa-si/admin/workflow/coding.md
parent_rules_remain_active: true
module: quality
read_when: code_change|bugfix|lint|format|type_check|static_analysis|build_validation|test_execution|verification|benchmark|quality_review|documentation_validation
owner_sections: quality_gates|verification|quality_review_gate|completion

quality_gates:
- read_when: code_change|test_request|lint_request|format_request|type_check_request|build_request|benchmark_request|documentation_validation
- first_select: explicit_user_request|repository_mandatory_checks|changed_behavior_and_risk
- specialized_detail: select_matching_sources_from_core.yaml_coding_modules
- syntax_gate:
  - read_when: new_or_modified_source|generated_code|configuration
  - checks: parser|compile|configuration_schema_when_applicable
- lint_gate:
  - read_when: lint_requested|modified_code|repository_lint_required
  - checks: repository_declared_linter|affected_paths|relevant_rule_set
  - policy: prefer_existing_tool_and_configuration|no_unrequested_global_reformat_or_lint_cleanup
- format_gate:
  - read_when: formatting_requested|format_gate_required|modified_code_with_format_policy
  - checks: repository_declared_formatter_check|changed_files
  - autofix: only_within_requested_scope_and_authorized_edit_flow
- type_gate:
  - read_when: typed_language|type_check_requested|type_sensitive_interface_change|repository_type_gate
  - checks: declared_compiler_or_type_checker|affected_packages|public_types
  - policy: preserve_repository_strictness_and_version|no_silent_suppression_or_broad_any_cast
- test_gate:
  - read_when: bugfix|new_or_changed_behavior|test_requested|repository_test_gate
  - checks: focused_regression|affected_module_bundle|integration_when_boundary_or_risk_requires
  - policy: use_existing_framework|include_invalid_and_failure_cases_when_material|isolated_test_resources
- build_gate:
  - read_when: compile_target|packaging|dependency_change|deployment_artifact|build_requested
  - checks: affected_build|lockfile_consistency|packaged_entrypoints
- security_gate:
  - read_when: untrusted_input|auth|permissions|secrets|cryptography|dependency_security_change
  - checks: boundary_validation|least_privilege|secret_leakage|dependency_advisories_when_material
- documentation_gate:
  - read_when: public_API|configuration|schema|operational_contract|docs_changed
  - checks: owner_consistency|links|examples|repository_docs_validator_when_available
- performance_gate:
  - read_when: hot_path_change|performance_claim|benchmark_request|material_resource_tradeoff
  - checks: representative_before_after|correctness_equivalence|latency|throughput|memory|allocations|IO_as_material
  - prohibit: flaky_fixed_wall_clock_assertions_on_shared_CI_without_stable_budget
- long_or_costly_gate:
  - read_when: broad_suite|heavy_benchmark|training|large_integration
  - policy: execute_global_workflow_preflight_and_short_smoke_before_expensive_run
- failure:
  - inspect_actual_error_and_root_cause|repair|rerun_affected_check
  - missing_tool_or_dependency: follow_global_workflow_recovery_not_fake_pass
- gate_status: passed|failed|blocked|not_run|not_applicable
- test_detail: workflow/coding/testing.md_when_relevant
- async_test_detail: workflow/coding/async-testing.md_when_relevant
- no_pass_from: tool_available|source_written|CI_triggered|old_unrelated_build|skipped_tests

verification:
- read_when: tests|lint|format|type_check|static_analysis|build|integration|benchmark|documentation_check|code_change
- selection: apply_quality_gates_by_change_type|risk|repository_contract
- execution_order_and_preflight: awa-si/admin/workflow.md#verification;awa-si/admin/workflow.md#dependency_preflight;awa-si/admin/workflow.md#rights_preflight;awa-si/admin/workflow.md#environment_preflight
- evidence: actual_command|scope|exit_status|relevant_results|skips_and_blockers
- rerun: failed_gate_after_cause_fixed|affected_suite_after_material_change
- do_not: assert_success_from_unrun_checks|change_assertions_to_hide_defects|treat_static_pass_as_runtime_proof

quality_review_gate:
- read_when: material_code_change|review|refactor|performance_change|security_change
- inspect_relevant: behavior|security|failure_modes|ownership|dependencies|interfaces|complexity|IO|allocations|concurrency|maintainability|tests
- reject_when_material: N_plus_1|avoidable_quadratic_hot_path|unbounded_queue_or_parallelism|unsafe_side_effect_retry|lost_resource_cleanup|duplicated_domain_logic
- tradeoff: explicitly_document_material_legacy_or_compatibility_constraint

completion:
- read_when: completed_or_blocked_coding_or_quality_task
- required: requested_behavior_or_quality_outcome|applicable_gates_and_source_contract|observed_evidence
- report: changed_files|tests_lint_type_format_build_benchmarks_as_applicable|pass_fail_blocked_skipped|remote_revision|deployment_separately
- prohibit: unverified_success_claim|scope_expansion|running_unrelated_full_suite_without_material_need
