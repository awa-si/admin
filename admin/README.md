---
title: Admin YAML Contract Migration Candidates
description: Lossless comparison of source snapshots and dictionary-deduplicated runtime inventory.
type: guide
status: experimental
language: en
owner: AWA
created: 2026-11-12
updated: 2026-11-12
---

# Admin YAML contract candidates

These files are **parallel comparison artifacts**, not the active Admin control
plane. The authoritative sources remain `instructions.txt`, `workflow.md`,
`research.md`, `coding.md`, `metadata.md`, `AGENTS.md`, and the applicable
`projects/<project>/` deltas. No consumer, bootstrap route, precedence or
permission boundary has been switched to YAML.

## Two alternatives

- [`core.yaml`](core.yaml): a lossless, reviewable YAML snapshot with each
  source document preserved verbatim, ordered, and pinned to its Git blob SHA.
- [`runtime.yaml`](runtime.yaml): a **lossless, exact-line-deduplicated**
  inventory. It stores each distinct line once and reconstructs each document
  from ordered integer references. The small `entrypoint` is metadata, not a
  substitute for the documents or a second routing decision owner.

Both include the verified **global + AWA-project** instruction scope:
`instructions.txt`, `workflow.md`, `research.md`, `coding.md`,
`metadata.md`, `AGENTS.md`, `projects/awa/instructions.txt`, and
`projects/awa/workflow.md`. Other project deltas and narrow technical owners
are outside this comparison. Missing optional `projects/awa/coding.md` is not
invented.

## Initial measured comparison (2026-11-12)

| Measure | Original sources | `core.yaml` | `runtime.yaml` |
| --- | ---: | ---: | ---: |
| Source characters | 129,335 | Lossless | Lossless |
| Artifact characters | — | 141,801 | 150,748 |
| Source lines represented | 1,903 | 1,903 | 1,903 |
| Unique dictionary lines | — | — | 1,692 |
| Repeated line occurrences eliminated from dictionary | — | — | 211 |

The dictionary removes repeated line storage but adds index/provenance overhead,
so the experimental runtime artifact is **larger** than the sources. Neither
candidate is approved as a context-saving GPT bootstrap. Follow-up semantic
consolidation must pass the same no-rule-loss and routing acceptance gates.

## Validation

```bash
python -m pip install PyYAML
python admin/validate.py
```

The validator checks strict YAML parsing (including duplicate mapping keys),
schema identifiers, exact dictionary uniqueness, line-by-line reconstruction,
document coverage, pinned Git blob hashes, and current local source content.
It fails when a source changes without regenerating the candidates.

`--skip-source-check` checks snapshot consistency only; it must **not** be
used to claim freshness. No automatic migration, source replacement, or admin
resolver redirection occurs.

## Interpretation and next design gate

This is **syntactic deduplication**, not a semantic consolidation or a
minimized GPT runtime context. Explicit duplicate source lines are stored
once; provenance, original line order, indentation, conditions and exact
wording remain reconstructable. The indexed YAML may be larger in bytes than
the original files. It is not suitable for direct whole-file injection into
the model as an optimization.

Before making a real authoritative `admin/runtime.yaml`, compare the sources
rule by rule, identify a single owner for each normative rule, model explicit
conditions and overrides, validate against routing/authorization acceptance
cases, and measure the complete execution context cost. **Do not discard
canonical content based only on textual duplication or byte savings.**
