---
title: GPT Admin
description: Entry point for global ChatGPT control-plane owners, bootstrapping and repository routing.
type: guide
status: active
language: en
owner: AWA
created: 2026-10-26
updated: 2026-11-04
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
projects/<project>/coding.md          optional project coding delta
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
→ projects/<project>/coding.md          # when present and coding applies
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
        ├── workflow.md        # optional
        └── coding.md          # optional
```

## Workflow routes

The canonical routing bootstrap is [`workflow.md#decision_bootstrap`](workflow.md#decision_bootstrap). Its single decision authority is [`workflow.md#routing_decision_order`](workflow.md#routing_decision_order): **product mode → authorization → repository and branch → eligible retained workspace → capability needs → selected route → native admission**. The [routing acceptance cases](workflow.md#routing_acceptance_cases) cover ordinary edits, existing-workspace reuse, permission failures, test execution, durable orchestration and deployment boundaries. These are policy examples, not live API specifications.

- **Connected GitHub connector**: default when no suitable AWA workspace route has been selected and authorized, provided the connector can complete the requested work and verification. An existing workspace does not itself authorize its use; never create one solely for repository access.
- `GitHub_Patch`: small deterministic repository changes without local execution, using the connected GitHub connector.
- `GitHub_Workspace`: light-to-medium repository coding requiring a temporary local workspace, with connector-mediated remote access.
- `AWA_MCP_Workspace`: heavy or long-running execution, special runtimes, or requirements that cannot be met through the connector/GitHub Workspace alone. Once selected, local Git is run inside AWA and authenticated remote operations use AWA workspace repository tools. In ChatGPT Work mode, explicit current-user authorization for AWA remains required.
- `AWA_Work`: durable, approval-gated multi-step orchestration when specifically authorized and technically needed; an existing Workspace does not replace this route.
- `GitHub_Actions`: hosted, durable, runner-specific, or remote-SHA-tied execution when materially required.

`workflow.md` owns route selection and execution orchestration; tool and workspace mechanics belong to the current provider contracts. Repository scope alone does not justify creating an AWA workspace. Within an authorized AWA workspace, consult the current `mcp/docs/workspace.md` contract and live dispatcher schema for repository mapping, bounded search, execution and authenticated Git transport; historical handler names are not public tool calls.

## AWA MCP authority and reference routing

Admin owns route selection, authorizations, and completion criteria; it does not define MCP tool interfaces or implementation mechanics. Load the current canonical instruction, capability, and subsystem contracts before applicable AWA actions. The authoritative references are [AWA MCP gateway](https://github.com/awa-si/awa/blob/main/mcp/README.md), [Workspace contract](https://github.com/awa-si/awa/blob/main/mcp/docs/workspace.md), current AWA repository owners and live registered tool schemas. Neither discovery nor documentation alone grants execution permission.

## ChatGPT Work mode

Native ChatGPT Work mode does not use AWA MCP by default. AWA MCP is allowed only for the specifically requested scope when the current user explicitly commands its use. Work mode otherwise keeps its native checkpointing, bounded parallelism, long-running preflight, and completion rules.

## Reload

```text
reload admin plane
```

Alias: `reload admin control plane`.

A reload prefers the current AWA instruction resolver for global owners; capability discovery is delegated to the separate current discovery interface when needed. Project deltas and repository agents are read only when applicable. Use connected repository reads if AWA is unavailable. It does not invoke `mcp_reload` or restart the MCP runtime. Previously loaded copies become non-authoritative for that chat.

```text
reload mcp
```

`reload mcp` uses the current canonical MCP reload contract and then rereads applicable instructions. It does not authorize unrelated actions or prove a service process restart.

## Public repository safety

`awa-si/admin` is public. Never commit secrets, credentials, session material, secret-bearing URLs, or private/confidential data. Reference private canonical sources symbolically instead of copying them into Admin.
