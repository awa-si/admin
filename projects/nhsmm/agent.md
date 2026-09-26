scope: project_agent_snapshot
project: nhsmm
repository: awa-si/nhsmm
branch: develop
visibility: public
mode: extracted_machine_directives

source_of_truth:
- repository_current_state: true
- canonical_agent: agent.md
- public_orientation: README.md
- governance: docs/model.md

project:
- type: neural_probabilistic_sequence_modeling_library
- framework: PyTorch
- python: ">=3.9"
- maturity: pre_1_0_research
- public_api_stability: evolving

role:
- operate_as: probabilistic_modeling_engineer|ml_researcher|pytorch_systems_engineer
- priority: mathematical_correctness>probabilistic_semantics>temporal_causal_validity>tensor_contracts>numerical_stability>reproducibility>clean_interfaces>minimal_testable_implementation

model_contract:
- latent_components: initial|transition|duration|emission
- explicit_duration_semantics: preserve
- canonical_config: nhsmm.config.ModelConfig
- canonical_model: nhsmm.models.base.NHSMM
- public_construction: ModelConfig -> NHSMM
- configured_emissions: gaussian|student_t
- configured_transitions: ergodic|semi|left_to_right
- distinguish: filtering|smoothing|decoding|forecasting|training

causality:
- prohibit: lookahead|future_contamination|target_leakage|train_eval_contamination
- full_sequence_inference: retrospective_only_unless_causal_contract_proven
- never_label_smoothed_state_as: causal_filtered_state
- padding: must_not_become_model_information

numerics:
- prefer: log_space|logsumexp|log_softmax
- preserve: dtype|device|mask|batch|time|duration_axes
- verify: normalization_axes|boundary_conditions|duration_indexing|nan_inf|cpu_cuda_consistency
- avoid: implicit_device_mismatch|ambiguous_broadcasting|off_by_one_duration

api_evolution:
- canonical_representation_over: aliases|duplicate_paths
- stale_consumers: migrate_or_remove_after_contract_resolution
- update_together: implementation|callers|tests|scripts|exports|docs
- historical_names_not_canonical: HSMM|NeuralHSMM|GaussianHSMM

testing:
- order: targeted_tests -> broader_suite_if_shared_contract_changed
- commands: pytest_-v|ruff_check_nhsmm_tests_scripts|black_--check_nhsmm_tests_scripts
- never_claim_execution_without_observed_run: true
- prefer_invariants: normalization|finite_log_prob|masking|shape|gradient|state_duration_range|batch_equivalence

repository_workflow:
- default_branch: develop
- preferred_workspace: /tmp/nhsmm
- local_checks_before_actions: true
- github_actions: only_if_material_additional_evidence
- direct_remote_edit_fallback: connected_GitHub_tools
- verify_remote_result_after_write: true

documentation:
- describe_only: implemented_current_behavior
- unsupported_claims_prohibited: production_ready|memory_efficient|scalable|causal|gpu_optimized
- public_examples: verify_against_current_exports_and_signatures

governance:
- nhsmm_open_core: public
- domain_or_product_layers: separate_from_core
- source_for_release_relationships: docs/model.md

sync:
- this_file: public_reference_snapshot
- refresh_if: agent.md|README.md|docs/model.md changes
