# GPT Admin

`awa-si/admin` defines the user-controlled ChatGPT instruction, coding-guidance, and workflow hierarchy used across AWA projects.

## Canonical resolution

```text
admin/instructions.txt
        ↓
admin/workflow.md
        ↓
admin/coding.md                              # when coding is material
        ↓
projects/<project>/instructions.txt         # optional project behavior/repository delta
        ↓
projects/<project>/workflow.md              # optional workflow delta
        ↓
<derived-repository>/agent.md               # optional AI repository layer
        ↓
material helper / canonical owner files     # loaded only when needed
        ↓
current task
```

Rules:

- `instructions.txt` controls global ChatGPT behavior, scope, connector/tool preferences, project repository resolution, and the content policy for repository agents.
- `workflow.md` controls repository execution, editing, verification, CI/Actions, profiling, artifact handling, concurrency, and recovery.
- `coding.md` controls global implementation strategy, reuse/dependency selection, custom-code gates, native/compiled-library preference, refactoring principles, and coding-level correctness/performance expectations.
- repository `agent.md` is AI-centric: it controls AI behavior, reasoning, routing, source resolution, decision/completion gates, and repository-specific governance needed by the AI.
- substantive domain, technical, business, runtime, data, model, API, or operational contracts belong in helper or canonical owner files in the target repository.
- project files are delta-only; parent rules remain active unless explicitly overridden.
- if `projects/<project>/instructions.txt` does not exist, use global instructions + global workflow + global coding when applicable.
- `projects/<project>/workflow.md` is optional and extends/overrides only the global workflow.
- target `agent.md` is derived from `projects/<project>/instructions.txt.repository` and loaded only when present.
- helper/owner files are resolved from the repository agent or repository registry and loaded only when material to the task.
- current target repository state is authoritative for implementation facts.

## Repository structure

```text
admin/
├── instructions.txt
├── workflow.md
├── coding.md
├── agent.md
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
├── agent.md                  # optional AI operating/resolution layer
└── <helper-or-owner-files>   # substantive repository/domain contracts
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
- workflow and coding-policy dependency declarations;
- global repository-agent content policy.

Do not duplicate substantive repository contracts, coding details, or execution policy here.

### `workflow.md`

Use for:

- local/disposable workspace policy;
- edit/test/commit/writeback flow;
- GitHub Patch / Workspace / Actions routing;
- AWA MCP operational routing;
- concurrency protection;
- CI and GitHub Actions escalation;
- long-running job observability;
- profiling/benchmark/research artifact handling;
- remote verification and recovery.

Project workflow files contain only project-specific additions or explicit overrides.

### `coding.md`

Use for global coding and implementation principles that apply across repositories, including:

- reuse before invention;
- inspection of existing repository code and dependencies before adding methods;
- preference for standard libraries and mature, stable external libraries before custom implementations;
- preference for mature C/C++/Rust/native-backed implementations when materially better for low-level or performance-sensitive primitives;
- explicit justification gates for custom code;
- dependency quality, maintenance, license, portability, security, and API-stability considerations;
- behavior-preserving refactoring;
- correctness, edge-case, and performance verification expectations.

`coding.md` does not own repository-specific architecture, API, runtime, domain, or business contracts. Those remain in the target repository's narrowest helper/canonical owner.

### repo `agent.md`

Use only for AI-facing repository behavior such as:

- AI role and reasoning priorities;
- source and ownership resolution;
- repository navigation/routing;
- which helper/owner files to load for which task;
- decision and completion gates;
- repository-specific AI governance that cannot be expressed generically in Admin.

Do **not** use `agent.md` as a substantive domain database. Architecture details, model contracts, runtime/data semantics, business rules, API contracts, document standards, and operational procedures belong in their narrowest helper or canonical owner.

### helper / canonical owner files

Use for substantive repository truth, including:

- architecture and engineering contracts;
- domain methodology and invariants;
- model, runtime, data, artifact, and API semantics;
- business and operational rules;
- documentation/metadata standards;
- current implementation or evidence state where that file owns it.

`agent.md` may route to these files but must not duplicate their contents.

## Force reload

To force an already-open chat to discard cached Admin control-plane copies and reload the current applicable hierarchy, send exactly:

```text
reload admin control plane
```

The trigger causes the current chat to reread `admin/instructions.txt`, `admin/workflow.md`, and `admin/coding.md`; reread the active project's instructions/workflow when applicable; rederive the target repository; and reread that repository's `agent.md` when present. Material helper/owner files are reread only when required by the current task or by changed resolution.

This is a per-chat reload. It does not broadcast into other already-open chats; each such chat must receive the trigger independently.

## Instruction language

`instructions.txt`, `workflow.md`, `coding.md`, and `agent.md` are machine-consumed control files.

Prefer:

- stable section names;
- key/value directives;
- short normative imperatives;
- explicit scope, precedence, conditions, exceptions, and fallbacks;
- consistent identifiers across layers.

Avoid narrative prose, motivational text, rhetorical wording, and duplicated rationale. Human-oriented explanation belongs in README/docs; substantive machine-readable contracts belong in their canonical helper/owner files.

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

global coding
< explicit repository-specific coding contract
```

A child overrides only when explicit. Otherwise parent rules remain active.

Repository-local `agent.md` does not replace global/project behavior, workflow policy, or applicable global coding guidance. It adds repository-specific AI reasoning/routing. Helper/owner files add the substantive contracts required by the task and may explicitly refine coding rules for their repository scope.

## Source-of-truth boundaries

- `awa-si/admin` owns global/project ChatGPT behavior, global workflow policy, and global coding guidance.
- target repositories own their `agent.md`, helper/owner files, implementation state, and repository-specific coding/domain contracts.
- repository `agent.md` owns AI-facing repository behavior and resolution logic only.
- helper/canonical owner files own delegated substantive details.
- project `instructions.txt` owns repository resolution for that project.
- project `workflow.md` owns only workflow deltas.
- duplicated active definitions across layers are prohibited.
