---
title: Odoo Project Workflow
description: Machine-readable Odoo addon development, activation, testing and release gates.
type: standard
status: active
language: en
owner: AWA
created: 2026-10-31
updated: 2026-11-02
---

scope: project_workflow_delta
project: odoo
mode: normative_machine_directives

resolution:
- parent: awa-si/admin/workflow.md
- project_instructions: awa-si/admin/projects/odoo/instructions.txt
- project_coding: awa-si/admin/projects/odoo/coding.md
- repository: awa-si/odoo@main
- repository_agent: awa-si/odoo@main:AGENTS.md
- inheritance: delta_only|explicit_override_only|parent_rules_remain_active
- repository_state: source_of_truth_not_running_Odoo_installation
- Odoo_target: 19.0_by_default|verify_installed_Odoo_and_OCA_versions
- first_party_modules: modules/<technical_name>/

development:
- inspect: active_repo_and_branch|git_state|manifest|dependency_addons|models|views|security|Odoo_and_OCA_APIs
- scope: changed_modules|dependent_modules|ORM_invariants|migrations|ACL|record_rules|multi_company|billing|concurrency|HTTP
- implement: production_code_and_tests_as_coherent_bundle
- tests: native_TransactionCase_for_ORM|HttpCase_for_HTTP_or_UI_when_required|setUpClass_for_shared_fixtures|test_isolation
- gates: static -> focused_integration -> full_integration_when_release_or_risk_requires
- review: data_loss|privilege_escalation|compatibility|races|idempotency
- deliver: commit_and_remote_verify_when_authorized|report_observed_gate_status
- prohibit: production_database_tests|production_secrets_or_filestore|unverified_runtime_success_claims

activation_gate:
- apply_when: existing_installable_addon_contains_new_or_modified_untested_functionality
- keep_active: previously_tested_production_behavior
- prohibit_before_required_tests: importing|registering|wiring_new_code_into_active_runtime_entrypoints
- entrypoints: __init__.py|manifests|XML_data_and_views|cron|controllers|hooks|menus|model_inheritance|automation|external_routing
- stage: unimported_implementation_and_tests_when_possible
- feature_flag_alone: insufficient_when_import_changes_models_or_registry
- imported_code_change: disabled_by_default_only_if_import|registry|schema|existing_behavior|install_and_upgrade_remain_safe
- otherwise: keep_change_out_of_deployable_path_until_verified
- installed_addon_installable_false_as_staging: prohibited
- production_functionality_disable_or_uninstall_for_staging: prohibited
- stage_validation: isolated_database_and_filestore|gate_1|gate_2|gate_3_when_required
- test_scope: installation|upgrade|permissions|downstream_modules|disabled_default_behavior
- activation: after_tests_and_explicit_release_acceptance -> wire_into_addon -> rerun_integrated_bundle -> authorized_deploy
- commit_import_static_or_dry_run_as_activation_authorization: prohibited
- report: staging_status|outstanding_tests|actual_release_state
- active_imports_may_execute_after_service_restart: true

gate_1_static:
- apply: every_change_or_commit
- commands: python_dev/check.py|python_-m_compileall_-q_modules
- checks: manifest|dependencies|Python_syntax|XML_CSV_JSON_references|security|license|version|formatting|Odoo_lint
- OCA_checks_when_installed: bash_dev/oca-checks.sh
- installed_dependency_verification: python_dev/oca-verify.py_--addons-path=/opt/odoo/env/odoo/addons,/opt/odoo/env/addons,/opt/odoo/addons,/opt/odoo/modules
- OCA_tools: pylint-odoo|oca-checks-odoo-module
- archived_MQT_as_current_framework: prohibited
- execution: local_or_manual_CI
- PostgreSQL: not_required
- gate_1_not_equal: Odoo_runtime_or_integration_success

host_runtime:
- preference: reuse_verified_existing_Odoo_binary|Python_environment|compatible_OCA_checkout_when_isolation_safe
- execution_identity: host_odoo_OS_account_only_through_authorized_host_runner
- require: verified_binary|Python_environment|separate_disposable_PostgreSQL_database|credentials|filestore|logs|test_config
- test_filestore_root: /var/lib/awa-data/odoo/filestore
- historical_host_test_database: odoo
- historical_test_configuration: /opt/odoo/test.config
- historical_host_details: verify_current_state_via_host_odoo_preflight|never_assume_still_safe
- production_database: never_modify|drop|initialize|upgrade_or_test
- production_config: do_not_use_without_proof_of_isolated_test_configuration
- versions: verify_Odoo_19_and_compatible_OCA_before_host_tests
- external_effects: disable_mail|external_endpoints|cron|live_payment|provisioning
- workspace_container: not_host_odoo_identity|do_not_assume_host_binary_or_PostgreSQL_socket_access
- host_boundary: explicit_authorized_host_executor_or_isolated_test_container_with_required_mounts
- gate_2: reuse_isolated_host_runtime_if_verified
- gate_3: fresh_disposable_database_with_isolation_or_OCA_style_CI
- isolation_or_capacity_missing: use_safe_CI_route|report_blocker

mcp_host_odoo_execution:
- applicability: when_Odoo_host_inspection|host_sync|native_Odoo_integration_testing_is_requested_or_required
- source_of_truth: awa-si/awa@main:mcp/host/odoo_.py|mcp/host/odoo_contract.py|mcp/tools/host_tools.py|worker/services/odoo.py
- boundary: ChatGPT -> AWA_MCP_host_odoo_* -> /run/awa-odoo/odoo.sock -> separate_awa-odoo-executor_process_as_OS_user_odoo
- host_executor: fixed_allowlist_only|validated_arguments|no_arbitrary_shell|never_use_generic_worker_as_privileged_executor
- discovery: use_current_registered_MCP_tools_and_schemas|do_not_assume_older_tool_names_or_supported_operations
- step_1_read_only: host_odoo_inspect({}) -> host_odoo_version({}) -> host_odoo_preflight({})
- step_1_verify: installed_binary|Python_venv|Odoo_19|config_valid|database_verified|Odoo_schema|matching_OCA|approved_addons_path
- step_2_source: complete_related_changes_and_gate_1_in_awa-si/odoo@main|commit_and_verify_remote_before_host_sync
- step_3_host_sync: host_exec(operation="git.inspect",arguments={"repository":"odoo"})_when_registered -> host_exec(operation="git.pull",arguments={"repository":"odoo"})_when_registered_and_authorized -> verify_host_SHA_matches_required_remote_commit
- git_pull_semantics: fast_forward_only|fixed_/opt/odoo_checkout|verified_origin_and_branch|does_not_deploy_or_restart|failure_or_divergence_stop_and_diagnose_not_force_reset
- step_4_test_admission: ensure_proven_disposable_isolated_DB_and_filestore|approved_test_config|explicit_test_enablement|external_integrations_isolated|not_production|matching_dependency_versions
- observed_test_contract: config=/opt/odoo/test.config|db=odoo|filestore_root=/var/lib/awa-data/odoo/filestore|executor_owned_by_odoo
- observed_test_db_name: historical_allowlisted_value_only|not_proof_of_disposability|never_interpret_as_permission_to_reset
- preflight_limit: config_valid_and_existing_Odoo_schema_do_not_alone_prove_isolation_or_safe_writes
- step_5_focused_test: host_odoo_test(module="<technical_name>")_only_after_test_admission|installs_if_uninitialized_else_updates_module|native_--test-enable_--test-tags_/module|600s_timeout|exclusive_lock
- step_5_install_test: host_odoo_install_test(module="<technical_name>")_only_if_explicitly_needed_and_safe|forces_install_flow|never_install_into_production
- step_5_script: host_odoo_script(script="<approved_identifier>")_only_for_verified_allowlisted_script_ids|never_infer_arbitrary_script_support
- step_6_results: examine_returncode|stdout_tail|stderr_tail|Odoo_test_failures|registry_install_upgrade|record_actual_gate_2_pass_fail_block
- step_7_release: gate_3_on_fresh_disposable_database_when_required|separate_explicit_authorization_for_deploy_or_restart|verify_deployed_runtime_independently
- host_reset: host_odoo_reset_preflight({})_is_read_only|eligible_false_means_no_reset|never_reset_initialized_odoo_DB_without_separate_verified_attestation_and_backup_and_authorization
- host_scripts: scripts_are_approved_by_mcp/host/odoo_contract.py|validate_current_allowlist_before_use
- safety: prohibit_prod_DB_write|prod_filestore_access|unsafe_reset|unverified_host_sha|tests_before_isolation_proof|deployment_by_git_pull_alone
- fallback: if_host_executor_or_isolation_unavailable_use_separate_disposable_CI_runtime|report_gate_2_blocked_not_passed
- reporting: report_repository_SHA|host_SHA_if_verified|preflight|isolation_evidence|tool_invocations|returncodes|gate_1_2_3_status|deployment_status

gate_2_focused_integration:
- database: preinitialized_disposable_isolated_Odoo_19_and_filestore
- dependencies: matching_OCA
- tests: native_Odoo_--test-tags_/module[:Class[.method]]
- optional_adapter: pytest-odoo_when_compatible|not_substitute_for_native_install_or_upgrade_tests
- update_affected_modules_when: models|manifests|data|views_changed
- avoid_full_database_reinitialization: for_pure_method_changes_when_safe
- assertions: accepted_and_rejected_operations|invalid_transitions|ACL_violations|duplicate_requests|cross_company_denial
- example_runner: dev/test-odoo.sh
- runner_requires: ODOO_BIN|ODOO_TEST_DB|ODOO_CONFIG|ODOO_ADDONS_PATH|ODOO_TEST_MODULES
- runner_modes: ODOO_TEST_MODE=install|update
- runner_not_environment_provisioner: true
- runner_database_guard: test_*|*_test_only
- host_database_odoo: host_odoo_test_executor_only|never_whitelist_in_shell_runner
- never_point_runner_at_production: true

gate_3_release_integration:
- apply_when: PR|release|repository_policy|material_risk
- environment: fresh_disposable_PostgreSQL_and_filestore|Odoo_19|pinned_OCA_19
- execution: install_changed_modules_and_dependencies|native_tests|upgrade|relevant_end_to_end_flows
- preferred: OCA_style_isolated_CI_with_PostgreSQL
- coverage: installation|XML_and_data|registry|cron|ACL|record_rules|multi_company|state_transitions|constraints|idempotency|concurrency
- billing: contracts|fixed_line_pricing|dates|currency|recurring_invoicing
- migration: sanitized_representative_records|rollback_and_recovery_plan
- production_or_real_customer_data: prohibited

test_conventions:
- location: modules/<name>/tests/test_*.py
- discovery: tests/__init__.py|addon_import_when_required_by_Odoo
- framework: TransactionCase|HttpCase|Odoo_test_tags
- ORM_semantics: use_real_ORM_for_computed_fields|constraints|record_rules
- data: controlled|deterministic|isolated
- external_services: fake_at_service_boundary
- concurrency: distinct_transactions_or_cursors_when_material|sequential_mock_insufficient
- additional_conventions: inherit_awa-si/admin/coding.md#test_writing_conventions

AWA_module_acceptance:
- deployment: confirmation_creates_once|repeated_confirmation_idempotent|correct_line_order_product_links
- registry: transitions|invalid_transitions|uniqueness|runtime_lookup
- wizard: defaults|activation_states|repeated_and_concurrent_activation|one_to_one_binding
- lifecycle: service_states|immutable_billing_terms_after_activation
- OCA_contract_19: explicit_lines_after_create|automatic_price_false|specific_price|quantity|currency|date_start|date_end|recurring_next_date|at_least_one_recurring_invoice
- security: ACL|record_rules|multi_company_isolation
- known_hardening_area: security_access_controls_verify_actual_repo_state

resource_and_reporting:
- workspace_role: inspection|gate_1|bounded_focused_tests
- historical_workspace_profile: 2_CPU|2048_MB_RAM|verify_current_profile_not_hardcode
- full_Odoo_installation_capacity: do_not_assume
- performance: reuse_cached_test_environments|avoid_reinstall_per_edit
- CI_static_only: report_gate_1_only
- report_each_gate: passed|failed|blocked|not_run
- include: actual_commands_and_environment_when_material|missing_runtime_blocker
- never_claim_unexecuted_integration: true

reply_model_rename_migration:
- from: awa.reply.operation
- to: reply.operation
- owner: modules/awa/upgrades/19.0.1.0.1/pre-rename_reply.py
- method: official_odoo_upgrade_util.rename_model(rename_table=False)
- require: compatible_odoo-upgrade-util_in_host_Python_environment
- existing_database_upgrade: never_bypass_migration_if_historical_operations_exist
- validate: preflight|ir.model_references|record_counts_before_after|ACL|reservation_and_completion_tests
- preserve_SQL_table: awa_reply_operation

optional_test_tools:
- dev/test-db-snapshot.sh: isolated_source_test_*_or_*_test|new_target|no_overwrite|does_not_clone_filestore
- snapshot_requires: PostgreSQL_clients|access|ODOO_SNAPSHOT_SOURCE|ODOO_SNAPSHOT_TARGET|ODOO_SNAPSHOT_CONFIRM_SOURCE|ODOO_SNAPSHOT_SOURCE_ACK=isolated-test-only
- source_database_odoo: not_eligible_for_snapshot
- snapshot_filestore: separately_copy_only_approved_isolated_filestore_when_required
- dev/check-migration.py_--database_test_odoo_dev: read_only_metadata_table_and_ACL_verification_on_disposable_db
- dev/test-coverage.sh: native_tests_on_disposable_DB|coverage.xml|requires_provisioned_matching_runtime_and_config
- coverage: supplementary_not_substitute_for_behavior_assertions
- pytest_odoo: optional_if_Odoo_19_compatible|native_TransactionCase_and_odoo-bin_--test-enable_remain_release_gate
- Github_CI_static_only: do_not_mark_gate_3_passed
- external_effects_in_gate_3: verified_disabled

references:
- Odoo_testing: https://www.odoo.com/documentation/19.0/developer/reference/backend/testing.html
- OCA_pytest_odoo: https://github.com/OCA/pytest-odoo
- OCA_addon_template: https://github.com/OCA/oca-addons-repo-template
- OCA_contract_19: https://github.com/OCA/contract/tree/19.0/contract
