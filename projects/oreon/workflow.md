---
title: OREON Project Workflow
description: Projektspezifische Ausführungsreihenfolge für das wiederverwendbare OREON-Framework.
type: standard
status: active
language: de
owner: AWA
created: 2026-10-26
updated: 2026-10-26
---

scope: oreon_project_workflow
mode: normative_machine_directives

resolution:
- project: oreon
- repository: awa-si/oreon
- default_branch: main
- parent: awa-si/admin/workflow.md
- project_instructions: awa-si/admin/projects/oreon/instructions.txt
- repository_agent: awa-si/oreon/AGENTS.md
- semantics: delta_only|inherit_parent|explicit_override_only
- precedence: global_workflow_unless_explicit_project_override
- source_of_truth: current_awa-si/oreon@main

project_execution:
- objective: complete_reusable_framework_before_case_specific_pilot
- priority: transaction_domain_first
- transaction_owner_set: domains/transaction/model.md|domains/transaction/logic.md|domains/transaction/payment.md|domains/transaction/template.md|contracts/transaction/|capital/funding.md|core/settlement.md
- other_domains: review_material_interfaces|defer_independent_completeness_until_transaction_complete
- pilot_operations: only_if_explicitly_requested|required_as_reference_for_reusable_rule
- proof_boundary: repository_documentation_and_structural_tests_are_not_live_gate_or_legal_authorization

graph_first:
- before_repository_work: read_actual_AGENTS_md|entire_current_INDEX_md|identify_narrowest_canonical_owner
- preflight: python_-m_scripts.graph_dependencies_summary|python_-m_scripts.graph_registry_validate
- impact: python_-m_scripts.graph_dependencies_impact_<canonical_owner_path>
- review: material_direct_and_transitive_consumers|affected_contracts|tests|external_dependencies
- graph_scope: explicit_document_references_only|not_complete_semantic_or_runtime_dependency_map
- for_non_document_assets: use_registered_architecture_owner_then_native_source_and_test_inspection
- failure: correct_or_report_stale_or_invalid_graph|no_silent_bypass

work_unit:
- scope: smallest_coherent_verified_transaction_framework_gap
- explicit_all_or_bundle: complete_all_safe_materially_related_steps_in_one_change_set
- order: evidence_and_canonical_owner_review -> gap_definition -> smallest_compatible_edit -> relevant_regression_tests -> registry_and_graph_sync -> verification -> writeback
- reuse_existing: canonical_documents|existing_validators|tests|templates
- avoid: duplicating_domain_rules|parallel_condition_registers|new_state_machine_without_proven_need|pilot_specific_assumptions_as_generic_rules
- document_changes: preserve_canonical_owner|repository_metadata_contract|consumer_compatibility
- no_simulated_operational_success: true

transaction_invariants:
- physical_gates: G0-G7_as_owned_by_domains/transaction/logic.md
- separate_dimensions: framework_specification|internal_structural_validation|external_legal_and_operational_readiness
- G3: scoped_local_handover_is_a_qualifier_not_a_new_gate_or_full_route_approval
- G4: readiness_only_not_payment_instruction
- G5: actual_party_and_provider_release_authority_required
- G6: evidence_and_value_finality_follow_signed_delivery_scope
- G7: settlement_and_discharge_require_actual_credit_and_contractual_authority
- completed_service_order: does_not_advance_physical_gate
- condition_register: contracts/model.md_is_owner|transaction_template_is_case_record_interface
- immutable_exposure: previously_executed_payment_title_or_custody_cannot_be_reverted_by_internal_gate_status
- authority: documentary_DAG_or_test_pass_does_not_waive_conditions_or_authorize_funds_movement

validation_and_writeback:
- sync: python_scripts/sync_graph_metadata.py_--write_before_graph_postflight
- required_docs: python_scripts/check_docs.py
- required_graph: python_-m_scripts.graph_registry_validate|python_scripts/sync_graph_metadata.py_--check
- code: focused_tests_for_changed_behaviour|broader_tests_only_when_coupling_or_risk_requires
- postflight: graph_impact_for_changed_owners|check_material_consumers
- quality: git_diff_--check|no_unrelated_edits|clean_worktree_after_commit
- writeback: one_coherent_commit_per_verified_change_set|push_only_after_validation|verify_remote_head
- report: changed_owner|test_results|graph_consistency|commit_and_push_state|remaining_real_blockers
