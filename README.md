# GPT Admin

`awa-si/admin` defines the user-controlled ChatGPT instruction, coding-guidance, and repository-workflow hierarchy used across managed projects.

## Resolution

```text
admin/instructions.txt
→ admin/workflow.md
→ admin/coding.md                  # when coding is material
→ projects/<project>/instructions.txt   # optional project delta
→ projects/<project>/workflow.md        # optional workflow delta
→ <derived-repository>/agent.md         # if present
→ admin/agent.md#fallback_repository_agent
→ material helper / canonical owner files
→ current task
```

Rules:

- project files are delta-only; parent rules remain active unless explicitly overridden;
- project `instructions.txt` resolves the target repository;
- project `workflow.md` contains only workflow deltas;
- repository `agent.md` is AI-centric and must not become a substantive domain database;
- substantive technical, runtime, model, API, business, and operational contracts stay in the target repository's narrowest helper/canonical owner;
- current repository state is authoritative.

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

## Workflow routes

- `GitHub_Patch`: native connected GitHub-connector fast path for known small deterministic changes.
- `GitHub_Workspace`: default connector-materialized workspace for workspace-class repository tasks.
- `AWA_MCP_Workspace`: fallback workspace when GitHub Workspace is unavailable, or when explicitly selected; uses the AWA MCP isolated workspace, real local Git, and MCP-controlled repository credential boundary.
- `GitHub_Actions`: only when durable hosted or runner-specific evidence is materially required.

For workspace-class tasks, use the independent `GitHub_Workspace` skill by default. Treat `AWA_MCP_Workspace` as a fallback when GitHub Workspace is unavailable, or use it when explicitly selected. The two routes remain independent.

## Force reload

```text
reload admin plane
```

Legacy alias:

```text
reload admin control plane
```

A reload rereads `instructions.txt`, `workflow.md`, `coding.md`, the active project delta when present, and the resolved repository agent. Previously cached copies become non-authoritative for that chat.

## Public repository safety

`awa-si/admin` is public. Never commit secrets, credentials, session material, secret-bearing URLs, or private/confidential data. Reference private canonical sources symbolically instead of copying them into Admin.
