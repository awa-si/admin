---
title: Metadaten- und Registervertrag
description: Globaler Dateimetadatenvertrag mit repositoryspezifischer Registerpflege.
type: standard
status: active
language: de
owner: AWA
created: 2026-09-26
updated: 2026-10-25
---

scope: global_file_metadata_contract
repository: awa-si/admin
mode: normative_machine_directives

metadata:
- applies_to: every_new_or_materially_edited_markdown_md_file
- format: YAML_frontmatter
- required_fields: title|description|type|status|language|owner|created|updated
- allowed_status: draft|active|review|archived
- created: immutable
- updated: refresh_on_material_change
- non_markdown_including_code_and_configuration: excluded
- existing_markdown_without_metadata: add_on_next_material_edit
- metadata_must_not_duplicate_domain_content: true

registry:
- path: repository_defined_index_or_registry_if_present
- role: repository_specific_map_and_file_registry_not_a_global_mandate
- update_same_operation_when: relevant_file_create|move|rename|archive|delete|material_registry_relevant_change
- entry_fields: path|type|status|purpose|updated_date
- domain_detail: keep_in_owned_file
- agent_description: AI_operating_rules_only

consistency:
- metadata_and_registry_must_match_current_file_state: true
- do_not_create_parallel_registry: true
- global_metadata_applies_independently_of_registry_presence: true
- repository_specific_metadata_schema: explicit_local_override_only
- generated_or_machine_managed_files: preserve_parser_and_tool_compatibility
- repository_specific_fact_or_case_detail: keep_in_owned_file_not_metadata_or_agent