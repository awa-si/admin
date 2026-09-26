scope: project_agent_snapshot
project: awa
repository: awa-si/awa
branch: main
visibility: private
mode: public_safe_reference_manifest

source_of_truth:
- repository_current_state: true
- canonical_agent: agent.md
- navigation_registry: docs/index.md

resolution:
- read: agent.md
- then_if_present: docs/index.md
- resolve: narrowest_canonical_owner
- load_only: task_relevant_dependencies

confidentiality:
- copy_private_content_to_admin: false
- expose_internal_architecture: false
- expose_business_state: false
- expose_personal_or_account_data: false
- public_admin_representation: repository_and_paths_only

sync:
- this_file: reference_snapshot_only
- substantive_rules: remain_in_private_repository
- refresh_if: canonical_agent_or_registry_changes
