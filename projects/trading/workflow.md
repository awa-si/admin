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
