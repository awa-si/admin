# GPT Admin

`awa-si/admin` defines the user-controlled ChatGPT instruction, coding-guidance, MCP/tool-guidance, and workflow hierarchy used across AWA projects.

## Canonical resolution

```text
admin/instructions.txt
        ↓
admin/workflow.md
        ↓
admin/coding.md                              # when coding is material
        ↓
admin/mcp.md                                 # when MCP/tool capability is material
        ↓
projects/<project>/instructions.txt         # optional project behavior/repository delta
        ↓
projects/<project>/workflow.md              # optional workflow delta
        ↓
<derived-repository>/agent.md               # when present
        ↓ otherwise
admin/agent.md#fallback_repository_agent    # default repository AI layer
        ↓
material helper / canonical owner files     # loaded only when needed
        ↓
current task
```

Rules:

- `instructions.txt` controls global ChatGPT behavior, scope, project repository resolution, dependency declarations, and the content policy for repository agents.
- `workflow.md` controls repository execution, editing, verification, GitHub Patch / Workspace / Actions routing, CI/Actions, profiling, artifact handling, concurrency, recovery, and AWA MCP operational routing.
- `coding.md` controls global implementation strategy, reuse/dependency selection, custom-code gates, native/compiled-library preference, refactoring principles, and coding-level correctness/performance expectations.
- `mcp.md` controls global MCP/tool capability discovery, authority, invocation, freshness, security, retry, and verification behavior.
- repository `agent.md` is AI-centric: it controls AI behavior, reasoning, routing, source resolution, decision/completion gates, and repository-specific governance needed by the AI.
- if a resolved target repository has no `agent.md`, use `admin/agent.md#fallback_repository_agent`; Admin-specific control-plane sections do not become target-repository rules in fallback mode.
- substantive domain, technical, business, runtime, data, model, API, or operational contracts belong in helper or canonical owner files in the target repository.
- project files are delta-only; parent rules remain active unless explicitly overridden.
- if `projects/<project>/instructions.txt` does not exist, use global instructions + global workflow + global coding when applicable + global MCP guidance when applicable; when a repository context is otherwise resolved, apply the Admin fallback repository agent.
- `projects/<project>/workflow.md` is optional and extends/overrides only the global workflow.
- helper/owner files are resolved from the repository agent, fallback agent, or repository registry and loaded only when material to the task.
- current target repository state is authoritative for implementation facts.

## Repository structure

```text
admin/
├── instructions.txt
├── workflow.md
├── coding.md
├── mcp.md
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
├── agent.md                  # optional repository-specific AI layer
└── <helper-or-owner-files>   # substantive repository/domain contracts
```

Admin does not retain `projects/*/agent.md` snapshots. Repository-local `agent.md` is read from the target repository when present; otherwise the fallback section in `admin/agent.md` is used.

## File responsibilities

### `instructions.txt`

Use for:

- communication and decision behavior;
- accuracy and verification expectations;
- project scope and target repository identity;
- explicit project-level behavioral overrides;
- workflow, coding, and MCP-policy dependency declarations;
- global repository-agent content policy and repository-agent fallback resolution.

Do not duplicate substantive repository contracts, coding details, MCP/tool mechanics, or execution policy here.

### `workflow.md`

Use for:

- repository task routing;
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

### `mcp.md`

Use for global MCP and connector-backed tool behavior, including:

- capability/schema discovery before use when not already loaded;
- authority and source routing;
- invocation and identifier discipline;
- freshness, pagination, and completeness checks;
- secret/data handling;
- bounded retry and partial-success recovery;
- verification of MCP writes and multi-step side effects.

Server- or domain-specific MCP contracts stay in their narrowest project/repository helper or canonical owner.

### repo `agent.md`

Use only for AI-facing repository behavior such as:

- AI role and reasoning priorities;
- source and ownership resolution;
- repository navigation/routing;
- which helper/owner files to load for which task;
- decision and completion gates;
- repository-specific AI governance that cannot be expressed generically in Admin.

Do **not** use `agent.md` as a substantive domain database. Architecture details, model contracts, runtime/data semantics, business rules, API contracts, document standards, and operational procedures belong in their narrowest helper or canonical owner.

### `admin/agent.md#fallback_repository_agent`

Use only when a target repository has no local `agent.md`. It provides generic repository AI routing, inherits global/project workflow/coding/MCP rules, resolves the narrowest target-repository helper/owner, and does not import Admin-repository ownership, visibility, or maintenance semantics into the target repository.

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

The default command to force an already-open chat to discard cached Admin control-plane copies and reload the current applicable hierarchy is:

```text
reload admin plane
```

Legacy alias, retained for compatibility:

```text
reload admin control plane
```

Both commands trigger the same full reload: reread `admin/instructions.txt`, `admin/workflow.md`, `admin/coding.md`, and `admin/mcp.md`; reread the active project's instructions/workflow when applicable; rederive the target repository; and reread that repository's `agent.md` when present, otherwise the Admin fallback repository-agent section. Material helper/owner files are reread only when required by the current task or by changed resolution.

This is a per-chat reload. It does not broadcast into other already-open chats; each such chat must receive a reload command independently.

## Instruction language

`instructions.txt`, `workflow.md`, `coding.md`, `mcp.md`, and `agent.md` are machine-consumed control files.

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

global MCP guidance
< explicit project/repository-specific MCP contract
```

A child overrides only when explicit. Otherwise parent rules remain active.

Repository-local `agent.md`, or the Admin fallback repository-agent section when no local agent exists, does not replace global/project behavior, workflow policy, applicable global coding guidance, or applicable global MCP guidance. It adds repository-specific or fallback AI reasoning/routing. Helper/owner files add the substantive contracts required by the task and may explicitly refine coding or MCP rules for their repository scope.

## Source-of-truth boundaries

- `awa-si/admin` owns global/project ChatGPT behavior, global workflow policy, global coding guidance, global MCP/tool guidance, and fallback repository-agent behavior.
- target repositories own their local `agent.md` when present, helper/owner files, implementation state, and repository-specific coding/domain contracts.
- repository `agent.md` owns AI-facing repository behavior and resolution logic only.
- the Admin fallback agent applies only when a target repository lacks a local `agent.md` and never becomes substantive owner of target-repository state.
- helper/canonical owner files own delegated substantive details.
- project `instructions.txt` owns repository resolution for that project.
- project `workflow.md` owns only workflow deltas.
- duplicated active definitions across layers are prohibited.
