# AWA — Repository Agent

> Mandatory operating rules for AI and automated work in `awa-si/awa`.

## 1. Purpose

This file governs how agents navigate, interpret, modify, and verify the AWA repository.

It is a repository-governance file, not a product specification. Product architecture, business rules, implementation details, and project-specific operating procedures belong in their narrowest canonical owner.

## 2. Canonical Repository

- Repository: `awa-si/awa`
- Branch: `main`
- Canonical root: `/`
- Repository files represent persistent AWA project state.
- Chat, memory, generated artifacts, local copies, and legacy files are working context only when canonical repository state is available.

Always work from the current GitHub `main`.

## 3. Initialization

Before substantive AWA work:

1. Read this file in full.
2. Read `docs/index.md` when it exists.
3. Resolve the relevant project area.
4. Identify the narrowest canonical owner for the task.
5. Read that owner and only materially required dependencies or referenced files.
6. Execute against the current repository state.

Preferred resolution flow:

```text
agent.md → docs/index.md → project area → canonical owner → dependencies → task
```

If `docs/index.md` does not exist, resolve ownership from the current repository structure and applicable owner files; do not invent registry state.

Do not load unrelated project areas merely for additional context.

## 4. Authority

For AWA project decisions, use this order:

1. Explicit current user instruction
2. Applicable authoritative law or regulation
3. This `agent.md`
4. Relevant canonical owner
5. Other directly relevant repository files
6. Current conversation context
7. General knowledge or assumptions

A more specific canonical owner governs its domain unless it conflicts with a higher authority.

If authoritative files conflict, identify the conflict rather than silently combining incompatible rules.

## 5. Canonical Ownership

Use the narrowest canonical owner.

> Define once in the owner; consume downstream.

Before adding or changing a fact, rule, configuration, business definition, architectural decision, or operating procedure:

1. Determine whether an owner already exists.
2. Update that owner when the concept belongs there.
3. Update consumers only where synchronization is required.
4. Prefer references to canonical definitions over copied definitions.
5. Avoid parallel sources of truth.

Directory presence alone does not establish canonical ownership.

## 6. Project Boundaries

AWA contains multiple initiatives, services, applications, infrastructure components, and shared resources.

Resolve ownership before changing shared or project-specific information.

- Project-specific rules belong in that project's canonical owner.
- Shared definitions belong in the narrowest common AWA owner.
- Do not duplicate definitions across projects for convenience.
- Project-specific overrides must remain explicit and intentional.
- AWA-level documentation must not absorb detailed project state merely because the project is related to AWA.

## 7. External Canonical Projects

An AWA project or subsystem may delegate substantive ownership to another repository.

When an authoritative AWA file delegates a domain, continue resolution there:

```text
AWA owner/reference
  → external canonical repository
  → external agent.md
  → external index.md
  → canonical owner
```

Once delegated:

- substantive reads and writes for that domain target the delegated repository;
- duplicated, archived, cached, or legacy AWA files are not authoritative;
- AWA retains only integration, ownership, public-facing, or reference information intentionally assigned to it;
- do not recreate an external project's canonical state inside AWA.

### OREON

OREON substantive project state is canonical in `awa-si/oreon`.

For OREON business rules, transaction architecture, research, routes, products, counterparties, execution state, or project documentation:

```text
awa-si/awa → awa-si/oreon → agent.md → index.md → canonical owner
```

AWA may own integrations or public-facing references to OREON, but those consumers must not become competing OREON owners.

## 8. Cross-Repository Work

Repository boundaries do not limit technical access; canonical ownership determines where work belongs.

A task may require coordinated changes across repositories. In that case:

1. Resolve the shared or originating owner first.
2. Follow any repository delegation.
3. Read the target repository's governance before substantive work there.
4. Change each definition only in its canonical owner.
5. Update affected consumers or integration references where required.
6. Verify each repository independently.

Do not use cross-repository access as a reason to copy project state between repositories.

## 9. Repository Changes

When the user asks to update, create, move, rename, delete, align, or otherwise modify repository state, perform the repository change unless the user explicitly requests only analysis, a proposal, or a draft.

For material writes:

```text
fetch current file + SHA
→ edit from current state
→ write
→ refetch
→ verify resulting content and SHA
→ review affected consumers
→ synchronize docs/index.md when applicable
```

Rules:

- Never reconstruct a canonical file from memory when current content can be fetched.
- Never silently overwrite concurrent changes.
- Do not force-push or use stale SHAs to bypass conflicts.
- Treat multi-file changes as one logical operation.
- Preserve existing architecture, naming, terminology, and ownership unless the requested change intentionally changes them.
- Prefer direct commits to `main` when authorized; use a branch or pull request when requested or when direct writes are unavailable.

## 10. Moves, Renames, and Deletions

Follow:

> Migrate before delete.

Before removing or replacing a canonical source:

1. Identify the information it owns.
2. Determine which information remains valid.
3. Migrate valid information to its new canonical owner.
4. Update references and consumers.
5. Verify the destination.
6. Remove the obsolete source.
7. Synchronize `index.md` when applicable.

Do not leave two active canonical owners for the same concept after migration.

Pure legacy duplicates whose canonical state has already been migrated may be removed without duplicating their content elsewhere.

## 11. docs/index.md

When present, `docs/index.md` is the documentation-level navigation and ownership registry, not a substantive owner.

Keep it concise. Preferred registry model:

```text
FILE → OWNER → CURRENT SHA
```

Update it when:

- files are created, moved, renamed, or deleted;
- canonical ownership changes;
- repository structure materially changes;
- tracked blob SHAs change.

Detailed architecture, business logic, procedures, and project rules belong in their canonical owner files, not in `index.md`.

Do not invent or maintain a synthetic `docs/index.md` solely because this agent expects one; create it only through an intentional repository-structure decision.

## 12. Freshness and Evidence

Verify current authoritative external sources when material decisions depend on changing facts, including:

- law and regulation;
- sanctions;
- tax and customs;
- licensing;
- AML/KYC;
- banking and settlement;
- counterparties;
- logistics;
- prices and market conditions;
- software/API behavior;
- external technical dependencies.

Prefer primary and authoritative sources.

Where relevant, distinguish:

**FACT · ASSUMPTION · ILLUSTRATION · PROPOSAL**

Do not promote chat discussion, estimates, exploratory analysis, or outdated external information into canonical facts without adequate support.

Record material assumptions explicitly when they are necessary for execution.

## 13. Verification

A repository write is not complete merely because the write operation succeeded.

After material changes:

1. Refetch the changed file or resulting repository state.
2. Verify the resulting content and SHA.
3. Check directly affected references and consumers.
4. Confirm obsolete definitions were not left active.
5. Synchronize `index.md` where applicable.
6. Verify the final repository state.

Report completion only after verification. If a connector or permission prevents verification or completion, state exactly what remains unverified or unchanged.

## 14. Scope Discipline

Do not mix repository governance with implementation blueprints.

Detailed subjects such as execution-agent architecture, application stacks, API design, role matrices, workflow graphs, ERP policy, or AI product design belong in their respective project or system owner files.

This file should change only when AWA-wide repository operating rules, ownership conventions, or governance change.

## 15. Working Principle

> Repository truth over conversational memory.  
> Canonical ownership over duplication.  
> Narrow context over indiscriminate loading.  
> Migration before deletion.  
> Verification before completion.

Core execution flow:

```text
read agent.md
→ read docs/index.md when present
→ resolve project area
→ resolve canonical owner
→ read required dependencies
→ execute against current repository truth
→ verify affected state
→ synchronize docs/index.md when applicable
```
