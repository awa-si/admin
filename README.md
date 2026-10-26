---
title: GPT Admin
description: Entry point for global ChatGPT control-plane owners, bootstrapping and repository routing.
type: guide
status: active
language: en
owner: AWA
created: 2026-10-26
updated: 2026-10-26
---

# GPT Admin

`awa-si/admin` is the control plane for ChatGPT behavior, repository workflow, coding guidance, project deltas, and repository-agent resolution across managed projects.

## Canonical owners

```text
instructions.txt                       global behavior + resolution
workflow.md                           repository execution/workflow
coding.md                             coding/design/performance guidance
research.md                           knowledge/code/docs/legal research and evidence standards
metadata.md                           Markdown-only file metadata contract
AGENTS.md                             Admin repository agent + fallback repository agent
projects/<project>/instructions.txt   project behavior/repository delta
projects/<project>/workflow.md        optional project workflow delta
<repository>/AGENTS.md                repository-specific AI behavior
<repository>/<helper>                 substantive technical/domain contracts
```

Each active rule has one canonical owner. Project files are delta-only, parent rules remain active unless explicitly overridden, and current repository state is authoritative.

Project-specific instructions and repository bindings are optional. Resolve the project slug from available ChatGPT project context, not a guessed name. If project instructions exist, use their repository configuration to resolve an active target. Load a repository agent or the Admin fallback only when a repository is active.

## Resolution order

```text
instructions.txt
→ workflow.md
→ research.md                            # when applicable
→ coding.md                              # when applicable
→ projects/<project>/instructions.txt   # if present
→ projects/<project>/workflow.md        # when present
→ <resolved-repository>/AGENTS.md       # only with repository context; fallback if missing
→ material helper / canonical owner
→ current task
```

## Repository structure

```text
admin/
├── instructions.txt
├── workflow.md
├── coding.md
├── research.md
├── metadata.md
├── AGENTS.md
├── README.md
└── projects/
    ├── template.txt
    └── <project>/
        ├── instructions.txt
        └── workflow.md        # optional
```

## Workflow routes

- **Connected GitHub connector**: first choice whenever it can complete repository inspection, editing, and required verification; no AWA workspace is created in that case.
- `GitHub_Patch`: small deterministic repository changes without local execution, using the connected GitHub connector.
- `GitHub_Workspace`: light-to-medium repository coding requiring a temporary local workspace, with connector-mediated remote access.
- `AWA_MCP_Workspace`: heavy or long-running execution, special runtimes, or requirements that cannot be met through the connector/GitHub Workspace alone. Once selected, local Git is run inside AWA and authenticated remote operations use AWA workspace repository tools. In ChatGPT Work mode, explicit current-user authorization for AWA remains required.
- `GitHub_Actions`: hosted, durable, runner-specific, or remote-SHA-tied execution when materially required.

`workflow.md` is the canonical owner of route selection and mechanics. Repository scope alone does not justify creating an AWA workspace. In an AWA MCP workspace, ChatGPT should prefer the native bounded `workspace_repository_map` and `workspace_search` capabilities for initial repository narrowing before reconstructing the same state through multiple shell scans.

## ChatGPT Work mode

Native ChatGPT Work mode does not use AWA MCP by default. AWA MCP is allowed only for the specifically requested scope when the current user explicitly commands its use. Work mode otherwise keeps its native checkpointing, bounded parallelism, long-running preflight, and completion rules.

## Reload

```text
reload admin plane
```

Alias: `reload admin control plane`.

A reload prefers AWA MCP `mcp_instructions()` for the current global owners and capability index, then reads an available project delta and repository agent only when applicable. Use connected repository reads if AWA is unavailable. It does not invoke `mcp_reload` or restart the MCP runtime. Previously loaded copies become non-authoritative for that chat.

```text
reload mcp
```

`reload mcp` performs `mcp_reload(scope="all")` and then rereads the current AWA `mcp_instructions` contract. The trigger does not authorize unrelated AWA MCP actions.

## Public repository safety

`awa-si/admin` is public. Never commit secrets, credentials, session material, secret-bearing URLs, or private/confidential data. Reference private canonical sources symbolically instead of copying them into Admin.
