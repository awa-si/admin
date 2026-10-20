# GPT Admin

`awa-si/admin` is the control plane for ChatGPT behavior, repository workflow, coding guidance, project deltas, and repository-agent resolution across managed projects.

## Canonical owners

```text
instructions.txt                       global behavior + resolution
workflow.md                           repository execution/workflow
coding.md                             coding/design/performance guidance
AGENTS.md                             Admin repository agent + fallback repository agent
projects/<project>/instructions.txt   project behavior/repository delta
projects/<project>/workflow.md        optional project workflow delta
<repository>/AGENTS.md                repository-specific AI behavior
<repository>/<helper>                 substantive technical/domain contracts
```

Each active rule has one canonical owner. Project files are delta-only, parent rules remain active unless explicitly overridden, and current repository state is authoritative.

Project repository resolution is defined by `projects/<project>/instructions.txt`: single-repository projects use `repository.source_of_truth`; multi-repository projects use `repository_resolution`, with the active target selected from the current task/project owner context before loading that repository's `AGENTS.md`.

## Resolution order

```text
instructions.txt
→ workflow.md
→ coding.md                              # when applicable
→ projects/<project>/instructions.txt   # when active
→ projects/<project>/workflow.md        # when present
→ <resolved-repository>/AGENTS.md       # otherwise AGENTS.md#fallback_repository_agent
→ material helper / canonical owner
→ current task
```

## Repository structure

```text
admin/
├── instructions.txt
├── workflow.md
├── coding.md
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

A reload rereads the global owners, active project delta, and resolved repository agent through a read-only path. Previously loaded copies become non-authoritative for that chat.

```text
reload mcp
```

`reload mcp` performs `mcp_reload(scope="all")` and then rereads the current AWA `mcp_instructions` contract. The trigger does not authorize unrelated AWA MCP actions.

## Public repository safety

`awa-si/admin` is public. Never commit secrets, credentials, session material, secret-bearing URLs, or private/confidential data. Reference private canonical sources symbolically instead of copying them into Admin.
