---
title: OREON Project Workflow
description: Generischer projektspezifischer Ablauf für Repository-, Architektur-, Dokumentations- und Implementierungsarbeiten.
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
- parent: awa-si/admin/workflow.md
- project_instructions: awa-si/admin/projects/oreon/instructions.txt
- repository_agent: awa-si/oreon/AGENTS.md
- semantics: delta_only|inherit_parent|explicit_override_only
- current_branch_and_repository_state: authoritative
- priorities_and_domain_scope: resolve_from_current_project_instructions|actual_task|canonical_repository_owners
- do_not_hardcode: current_domain_priority|pilot_case|product|transaction_type|specific_gate

routing:
- classify_work: research|review|documentation|architecture|code|tests|integration|operations
- resolve: requested_outcome -> smallest_canonical_owner -> material_dependencies -> affected_consumers
- preserve: domain_boundaries|distinct_legal_and_operational_roles|actual_repository_state
- new_domain_or_case: reuse_existing_framework_and_interfaces_before_adding_project_specific_structures
- domain_specific_rules: load_from_their_actual_canonical_owners_when_relevant
- avoid: copied_domain_contracts|duplicated_registries|unsupported_case_assumptions

repository_preflight:
- bootstrap: read_current_AGENTS_md|entire_current_INDEX_md
- graph_summary: python_-m_scripts.graph_dependencies_summary
- semantic_registry: python_-m_scripts.graph_registry_validate
- impact: python_-m_scripts.graph_dependencies_impact_<registered_owner_path>
- evaluate: relevant_direct_and_transitive_review_candidates|actual_source_code_and_tests_when_applicable
- graph_limit: explicit_document_reference_projection_only|not_complete_semantic_or_runtime_dependency_graph
- invalid_graph: report_or_fix_before_relying_on_graph_results
- read_only_work: do_not_mutate_registry_merely_for_analysis

execution:
- default_scope: one_coherent_material_work_unit
- explicit_all_or_bundle: complete_safe_materially_related_steps_across_requested_scope
- sequence: canonical_evidence_review -> identify_real_gap -> select_smallest_compatible_change -> execute -> validate -> writeback
- reuse: existing_models|libraries|scripts|templates|contracts|interfaces|tests
- avoid: speculative_implementations|parallel_specifications|unrequested_cleanup|synthetic_operational_success
- change_impact: review_material_consumers_and_cross_domain_interfaces_before_editing
- case_examples: distinguish_illustrations_from_actual_operational_or_legal_readiness

validation:
- index_sync_after_registered_change: python_scripts/sync_graph_metadata.py_--write
- document_integrity: python_scripts/check_docs.py
- graph_validation: python_-m_scripts.graph_registry_validate|python_scripts/sync_graph_metadata.py_--check
- code_validation: focused_tests_for_changed_behavior|broader_tests_if_material_risk_or_coupling_requires
- post_change_review: graph_impact_for_changed_owners|material_consumers|permissions_and_contracts_when_relevant
- quality: git_diff_--check|consistent_metadata|no_unrelated_changes
- writeback: prefer_one_coherent_commit_per_validated_change_set|verify_remote_state_after_push
- report: actual_change|tests|graph_and_index_consistency|commit_and_push_status|remaining_blockers

evidence_and_authority:
- classify: framework_definition|structural_validation|external_verified_fact|case_specific_authorization
- no_authority_inference: documentation|test_pass|graph_state|template|example
- external_actions: require_real_party_permissions|signed_instruments|provider_acceptance_where_applicable
- changed_external_facts: revalidate_affected_evidence_and_dependencies_without_fictitious_rollback
- private_or_sensitive_evidence: keep_out_of_public_repositories
