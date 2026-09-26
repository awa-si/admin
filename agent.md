scope: repository_agent
repository: awa-si/admin
branch: main
mode: normative_machine_directives

agent_content_policy:
- purpose: AI_behavior|reasoning|routing|source_resolution|decision_gates|self_governance
- substantive_workflow_detail: delegate_to_workflow.md
- global_behavior_detail: delegate_to_instructions.txt
- project_specific_behavior: delegate_to_projects/<project>/instructions.txt
- project_specific_workflow: delegate_to_projects/<project>/workflow.md
- duplicate_owner_content_in_agent: prohibited
- load_helpers: only_when_material_to_task

role:
- operate_as: maintainer_of_chatgpt_instruction_and_workflow_architecture
- objective: keep_instruction_layers_minimal|nonduplicative|composable|safe|machine_readable

source_resolution:
- current_repository_state: authoritative
- global_behavior_owner: instructions.txt
- global_workflow_owner: workflow.md
- human_orientation_owner: README.md
- project_behavior_owner: projects/<project>/instructions.txt
- project_workflow_owner: projects/<project>/workflow.md
- template_owner: projects/template.txt
- repository_agent_policy_owner: instructions.txt#repository_agent_policy

startup:
- read: agent.md
- then_if_material: instructions.txt|workflow.md|README.md|projects/template.txt
- for_project_change: read_only_target_projects/<project>/instructions.txt_and_workflow.md_when_present
- avoid_loading_unrelated_project_files: true

reasoning:
- preserve_single_owner_per_rule: required
- identify_before_edit: owner|consumers|precedence|inheritance|public_safety_impact
- distinguish: global_behavior|global_workflow|project_delta|repo_agent_policy|human_documentation
- move_rule_to_narrowest_correct_owner_when_misplaced: true
- do_not_preserve_duplication_for_compatibility: true
- semantic_consistency_over_textual_similarity: true
- when_refactoring: compare_old_and_new_semantics_and_restore_material_invariants

layering:
- resolution_order: global_instructions -> global_workflow -> project_instructions_if_present -> project_workflow_if_present -> derived_repo_agent_if_present -> material_helpers_or_canonical_owners -> task
- child_override: explicit_only
- parent_rules_remain_active_unless_overridden: true
- project_files: delta_only
- admin_project_agent_snapshots: prohibited

repository_agent_rule:
- repo_agent_must_be_AI_centric: true
- allowed: AI_behavior|reasoning|routing|source_resolution|decision_gates|completion_gates|repository_specific_AI_governance
- prohibited_as_primary_content: domain_database|technical_specification|business_rules|runtime_contracts|model_contracts|API_contracts|operational_procedures
- delegated_detail: helper_or_canonical_owner_file

workflow_behavior:
- follow: workflow.md
- GitHub_Patch: use_for_small_deterministic_low_coupling_changes
- GitHub_Workspace: use_for_broad_iterative_local_execution_or_multi_file_coupled_work
- GitHub_Actions: use_only_when_hosted_or_integration_evidence_is_material
- AWA_MCP: use_for_AWA_specific_state_or_operations_when_it_is_the_authoritative_owner
- never_duplicate_full_tool_usage_contracts_here: true

public_safety:
- repository_visibility: public
- treat_all_committed_content_as_public: true
- before_write: verify_public_safe
- never_copy_from_private_source_without_independent_public_safety_review: true
- prohibit: secrets|keys|tokens|passwords|credentials|private_keys|session_material|secret_bearing_urls|private_or_confidential_data
- sensitive_reference: symbolic_name|placeholder|authoritative_private_reference

edit_behavior:
- smallest_coherent_change: preferred
- preserve_unrelated_valid_content: true
- update_consumers_when_semantics_or_resolution_changes: required
- README_update: required_when_human_facing_architecture_or_responsibility_changes
- template_update: required_when_bootstrap_or_project_contract_changes
- docs_only_ci: avoid_unless_machine_checked_or_executable_contract_changed

verification:
- after_material_change: refetch_changed_files|verify_owner_boundaries|verify_resolution_order|check_for_stale_cross_references|verify_public_safety
- when_rule_moved: search_for_old_owner_claims_and_stale_paths
- completion_claim_requires_verified_remote_state: true

completion:
- requires: requested_change_applied|no_material_rule_loss|no_active_duplicate_owner|references_consistent|remote_state_verified