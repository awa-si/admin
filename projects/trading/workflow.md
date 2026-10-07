scope: project_workflow_delta
project: trading
mode: extend_parent_and_explicit_override_only

inherit:
- awa-si/admin/workflow.md
- override_only_if_explicit: true

chat_handoff:
- apply_when: new_chat_is_initialized_from_trading_handoff
- default_workspace_behavior: inherit_global_handoff_workspace
- required_project_context:
  - repositories:
    - awa-si/nautilus@main
    - awa-si/nhsmm@develop
    - awa-si/nhsmm-interfaces@dev
  - active_owner
  - active_repository
  - active_branch
  - resume_point
- preserve_when_available: repository_heads|workspace_slot_bindings|active_jobs|artifacts|checkpoints|validation_state|pending_next_step
- active_owner_values: nautilus|nhsmm|nhsmm-interfaces|cross_repository
- active_repository_must_match_active_owner: true
- handoff_repository_heads: evidence_only_until_current_remote_heads_verified_when_material
- inherited_workspace_binding: do_not_reimport_repository_if_existing_verified_slot_binding_matches
- missing_or_changed_repository_state: resolve_current_owner_and_reconcile_before_write
- cross_repository_resume:
  - resolve_owner_before_each_material_change: true
  - preserve_existing_repo_specific_branch: true
  - verify_each_affected_repository_independently: true
- do_not_duplicate_subproject_contracts_in_handoff: true

parallel_chat:
- apply_when: multiple_active_chats_work_on_trading_project_independently
- workspace_policy: separate_workspace_id_per_active_chat_or_workstream
- branch_policy: separate_working_branch_per_repository_per_independent_workstream
- same_workspace_reuse: handoff_only_unless_explicit_user_instruction
- cross_repository_parallelism:
  - different_repositories_may_progress_concurrently: true
  - same_repository_requires_independent_branch: true
  - active_owner_remains_repo_specific_per_chat: true
  - cross_repository_integration_requires_current_heads_for_all_affected_repositories: true
- integration:
  - shared_remote: GitHub
  - preserve_expected_remote_head_guard: true
  - integrate_explicitly_before_shared_branch_push: merge|rebase|cherry_pick|pull_request
