scope: project_agent_snapshot
project: oreon
repository: awa-si/oreon
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
- resolve: narrowest_canonical_owner
- read_target_file: required
- load_only: material_dependencies

confidentiality:
- copy_private_content_to_admin: false
- expose_business_state: false
- expose_counterparty_data: false
- expose_transaction_data: false
- expose_research_or_route_data: false
- public_admin_representation: repository_and_paths_only

sync:
- this_file: reference_snapshot_only
- substantive_rules: remain_in_private_repository
- refresh_if: agent_or_index_changes
