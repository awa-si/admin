# GPT Admin

`awa-si/admin` is the source of truth for the ChatGPT instruction hierarchy used across AWA projects.

The repository separates global interaction rules from project-specific rules and from repository-local engineering instructions.

## Design

Instruction resolution is hierarchical:

```text
Level 0
admin/instructions.txt
        ↓ inherited
Level -1
project/instructions.txt
        ↓ inherited
Level -2
subproject/instructions.txt
        ↓
repo-local agent.md
        ↓
current task
```

A more specific level inherits all applicable parent instructions and adds only its own project-specific delta.

## Files and responsibilities

### `instructions.txt`

`instructions.txt` defines how ChatGPT should operate in a given scope.

Typical content includes:

- interaction and communication rules
- verification and reasoning requirements
- tool and connector preferences
- project-specific operating behavior
- explicit overrides of inherited instructions

The root `instructions.txt` is Level 0 and contains global user-controlled ChatGPT instructions.

Each project may define its own `instructions.txt`. That file must reference its parent instruction file and should contain only project-specific additions or overrides.

### `agent.md`

Each project or repository should also contain an `agent.md` where repository-specific technical and domain rules belong.

Typical content includes:

- architecture and engineering rules
- repository conventions
- domain-specific methodology
- validation and testing requirements
- runtime and implementation constraints

`agent.md` must not duplicate generic ChatGPT interaction rules that belong in the instruction hierarchy.

## Public repository and secret handling

`awa-si/admin` is a public repository. Treat every committed file as publicly readable.

For all `instructions.txt`, project instruction files, `agent.md` snapshots, examples, documentation, and generated instruction artifacts:

- never commit secrets, API keys, access tokens, passwords, private keys, credentials, session material, or secret-bearing URLs;
- never copy private or confidential user, company, customer, infrastructure, or account data into instruction files;
- never move secret values from private repositories, chats, connected apps, environment files, CI secrets, or runtime state into this repository;
- use symbolic names, placeholders, secret identifiers, or references to the authoritative private source instead of secret values;
- treat copied `agent.md` content as untrusted for publication until checked for secrets and private data;
- redact or omit sensitive values before creating or updating any file in this repository;
- when uncertain whether content is public-safe, do not commit it until verified.

This rule is mandatory and applies even when the source repository itself is private.

## Resolution rules

1. **Parent first**
   - Resolve instructions from the highest applicable parent level down to the active project.

2. **Inheritance by default**
   - Parent rules remain active unless a child explicitly overrides them.

3. **Child specificity wins**
   - When two user-controlled instruction levels conflict, the instruction closest to the active project scope takes precedence.

4. **Delta only**
   - Child instruction files should not copy inherited rules. They should contain only additions, refinements, or explicit overrides.

5. **Explicit parent link**
   - Every non-root `instructions.txt` must identify its parent instruction source.

6. **Separate interaction from implementation**
   - `instructions.txt` controls ChatGPT behavior in the project context.
   - `agent.md` controls technical and domain work inside the repository.

7. **Current repository state is authoritative for implementation**
   - Project instructions may define how repository state is read, but technical facts about code, schemas, APIs, and architecture must come from the current repository rather than duplicated instruction text.

## Repository workspace policy

Repository transport and local execution are separate concerns.

- Small deterministic edits should use the GitHub Patch path directly.
- Broader changes, repository-wide inspection, builds, and tests should use a local runtime workspace when that materially improves verification.
- If direct `git clone` is unavailable, the GitHub connector/API should materialize the required repository snapshot into `/tmp/<repo>` instead of blocking local work.
- A connector-materialized workspace is a snapshot/workspace checkout, not a Git clone unless Git transport actually occurred.
- The workspace must retain the source branch, base commit SHA, and base tree SHA so writes can be concurrency-guarded.
- Multi-file writes should be committed atomically where practical using Git blobs/tree/commit/ref primitives, with force disabled.
- If the branch moved after materialization, refresh and reconcile; never overwrite newer changes from stale local state.
- Verify the resulting commit and changed files. Use CI only where it materially validates the change; documentation-only edits should not trigger CI unless repository rules require it.

The detailed global workflow is defined in `instructions.txt`; project `agent.md` files should contain only repository-specific deviations.

## Recommended project structure

```text
project/
├─ instructions.txt
└─ agent.md
```

A project instruction file should be minimal, for example:

```text
parent: <link-or-path-to-parent-instructions>
scope: awa-si/example

Project-specific instructions:
- ...
- ...
```

Nested scopes may form deeper levels when useful:

```text
admin/instructions.txt
        ↓
projects/awa/instructions.txt
        ↓
projects/nautilus/instructions.txt
        ↓
awa-si/nautilus/agent.md
```

## Source-of-truth boundaries

`awa-si/admin` owns the user-controlled instruction hierarchy.

Individual project repositories own their local `agent.md` and implementation state.

The hierarchy must avoid copying the same rule into multiple levels. Shared behavior belongs at the highest scope where it is universally valid; narrower scopes contain only the differences.
