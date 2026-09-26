scope: project_agent_snapshot
project: nautilus
repository: awa-si/nautilus
branch: main
visibility: private
mode: public_safe_reference_manifest

source_of_truth:
- repository_current_state: true
- canonical_agent: agent.md
- workflow_owner: workflow.md
- performance_evidence: performance.md

resolution:
- read: agent.md
- read_when_repository_work: workflow.md
- read_when_performance_work: performance.md
- load_only: task_relevant_dependencies

confidentiality:
- copy_private_content_to_admin: false
- expose_model_architecture: false
- expose_research_results: false
- expose_performance_data: false
- public_admin_representation: repository_and_paths_only

sync:
- this_file: reference_snapshot_only
- substantive_rules: remain_in_private_repository
- refresh_if: referenced_governance_files_change
