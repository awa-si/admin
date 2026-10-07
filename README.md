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

- `GitHub_Patch`: small deterministic repository changes without local execution.
- `GitHub_Workspace`: default for light-to-medium repository inspection and coding.
- `AWA_MCP_Workspace`: default for heavy or long-running work, custom runtime needs, or explicit selection; also the defined fallback when GitHub Workspace is unavailable.
- `GitHub_Actions`: hosted, durable, runner-specific, or remote-SHA-tied execution when materially required.

`workflow.md` is the canonical owner of route selection and mechanics.

## Reload

```text
reload admin plane
```

Alias: `reload admin control plane`.

A reload rereads the global owners, active project delta, and resolved repository agent. Previously loaded copies become non-authoritative for that chat.

## Public repository safety

`awa-si/admin` is public. Never commit secrets, credentials, session material, secret-bearing URLs, or private/confidential data. Reference private canonical sources symbolically instead of copying them into Admin.
