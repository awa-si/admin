# GPT Admin

`awa-si/admin` defines the user-controlled ChatGPT instruction and workflow hierarchy used across AWA projects.

## Canonical resolution

```text
admin/instructions.txt
        ↓
admin/workflow.md
        ↓
projects/<project>/instructions.txt        # optional project behavior/repository delta
        ↓
projects/<project>/workflow.md             # optional workflow delta
        ↓
<derived-repository>/agent.md              # optional repo/domain layer
        ↓
current task
```

Rules:

- `instructions.txt` controls ChatGPT behavior, scope, connector/tool preferences, and project repository resolution.
- `workflow.md` controls repository execution, editing, verification, CI/Actions, profiling, artifact handling, concurrency, and recovery.
- `agent.md` lives in the target repository and controls repository/domain/engineering contracts.
- project files are delta-only; parent rules remain active unless explicitly overridden.
- if `projects/<project>/instructions.txt` does not exist, use global instructions + global workflow only.
- `projects/<project>/workflow.md` is optional and extends/overrides only the global workflow.
- target `agent.md` is derived from `projects/<project>/instructions.txt.repository` and loaded only when present.
- current target repository state is authoritative for implementation facts.

## Repository structure

```text
admin/
├── instructions.txt
├── workflow.md
├── README.md
└── projects/
    ├── template.txt
    └── <project>/
        ├── instructions.txt
        └── workflow.md        # optional
```

Target repository:

```text
<owner>/<repo>/
└── agent.md                  # optional canonical repo/domain instructions
```

Admin does not retain `projects/*/agent.md` snapshots. Repository-local `agent.md` is always read from the derived target repository when needed.

## File responsibilities

### `instructions.txt`

Use for:

- communication and decision behavior;
- accuracy and verification expectations;
- tool/connector preferences;
- project scope and target repository identity;
- explicit project-level behavioral overrides;
- workflow dependency declaration.

Do not duplicate implementation/domain rules that belong in repo `agent.md` or execution policy that belongs in `workflow.md`.

### `workflow.md`

Use for:

- local/disposable workspace policy;
- edit/test/commit/writeback flow;
- concurrency protection;
- CI and GitHub Actions escalation;
- long-running job observability;
- profiling/benchmark/research artifact handling;
- remote verification and recovery.

Project workflow files contain only project-specific additions or explicit overrides.

### repo `agent.md`

Use for:

- repository ownership/navigation conventions;
- architecture and engineering contracts;
- domain-specific methodology;
- runtime/model/data semantics;
- repository-local validation requirements.

Do not duplicate generic ChatGPT behavior or global workflow policy.

## Instruction language

`instructions.txt`, `workflow.md`, and `agent.md` are machine-consumed control files.

Prefer:

- stable section names;
- key/value directives;
- short normative imperatives;
- explicit scope, precedence, conditions, exceptions, and fallbacks;
- consistent identifiers across layers.

Avoid narrative prose, motivational text, rhetorical wording, and duplicated rationale. Human-oriented explanation belongs in README/docs.

## Public repository safety

`awa-si/admin` is public. Treat every committed file as publicly readable.

Never commit:

- secrets, keys, tokens, passwords, private keys, credentials, or session material;
- secret-bearing URLs;
- private/confidential user, customer, company, infrastructure, or account data;
- copied content from private repositories unless independently verified public-safe.

For confidential project state, reference the authoritative private repository/path instead of copying content into Admin.

## Precedence

For user-controlled Admin layers:

```text
global instructions
< project instructions

global workflow
< project workflow
```

A child overrides only when explicit. Otherwise parent rules remain active.

Repository-local `agent.md` does not replace global/project behavior or workflow policy; it adds repository/domain-specific contracts.

## Source-of-truth boundaries

- `awa-si/admin` owns global/project ChatGPT behavior and workflow policy.
- target repositories own their `agent.md` and implementation/domain state.
- project `instructions.txt` owns repository resolution for that project.
- project `workflow.md` owns only workflow deltas.
- duplicated active definitions across layers are prohibited.
