# GPT Admin

`awa-si/admin` defines the user-controlled ChatGPT behavior, coding guidance, repository workflow, project deltas, and repository-agent resolution used across managed projects.

## Canonical owners

```text
admin/instructions.txt                  global behavior + resolution
admin/workflow.md                      repository execution/workflow
admin/coding.md                        coding/design/performance guidance
admin/AGENTS.md                        Admin repo agent + fallback repo agent
projects/<project>/instructions.txt    project behavior/repository delta
projects/<project>/workflow.md         optional project workflow delta
<repository>/AGENTS.md                 repository-specific AI behavior
<repository>/<helper>                  substantive technical/domain contracts
```

Each active rule should have one canonical owner. References are preferred over duplicated rule text. Consolidation must preserve information flow and semantics.

## Resolution order

```text
admin/instructions.txt
→ admin/workflow.md
→ admin/coding.md                         # when applicable
→ projects/<project>/instructions.txt    # when active project exists
→ projects/<project>/workflow.md         # when present
→ <resolved-repository>/AGENTS.md        # when present
  otherwise admin/AGENTS.md#fallback_repository_agent
→ material helper / canonical owner files
→ current task
```

Project files are delta-only; parent rules remain active unless explicitly overridden. Current repository state is authoritative.

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

- `GitHub_Patch`: connected GitHub fast path for known small deterministic changes.
- `GitHub_Workspace`: default workspace route for workspace-class repository tasks.
- `AWA_MCP_Workspace`: fallback when GitHub Workspace is unavailable, or when explicitly selected; isolated workspace with full local Git and MCP-owned repository credential boundary.
- `GitHub_Actions`: only when hosted, durable, or runner-specific evidence is materially required.

Route mechanics are owned only by `workflow.md`.

## Force reload

```text
reload admin plane
```

Legacy alias: `reload admin control plane`.

A reload rereads the three global owners, the active project delta when present, and the resolved repository agent. Previously cached copies become non-authoritative for that chat.

## Public repository safety

`awa-si/admin` is public. Never commit secrets, credentials, session material, secret-bearing URLs, or private/confidential data. Reference private canonical sources symbolically instead of copying them into Admin.
