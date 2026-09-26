scope: project_agent_snapshot
project: private
repository: awa-si/private
branch: main
visibility: private
mode: public_safe_reference_manifest

source_of_truth:
- repository_current_state: true
- canonical_agent: agent.md
- canonical_registry: index.md
- repository_orientation: README.md

resolution:
- read: agent.md
- then: index.md
- resolve: task_relevant_file
- load_only: minimum_required_context

confidentiality:
- copy_private_content_to_admin: false
- expose_personal_data: false
- expose_case_data: false
- expose_financial_or_legal_data: false
- expose_infrastructure_details: false
- public_admin_representation: repository_and_paths_only

sync:
- this_file: reference_snapshot_only
- substantive_rules: remain_in_private_repository
- refresh_if: agent_or_index_changes
