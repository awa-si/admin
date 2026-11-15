# GPT Admin

`awa-si/admin` defines the declarative ChatGPT control plane: global behavior, command dispatch, use-case resolution, execution routing, and project/repository instruction boundaries. It **does not** implement MCP tools, host deployments, or ChatGPT UI features.

**Start at [`core.yaml`](core.yaml).** It is a source resolver, not an instruction-priority system. Read canonical Admin sources through the connected GitHub connector; a prior-chat summary or MCP snapshot does not replace mandatory fresh-chat GitHub reads.

## Source ownership

| Owner | Responsibility | Load |
| --- | --- | --- |
| [`core.yaml`](core.yaml) | Registry, independent matching conditions, source resolution | First |
| [`behavior.yaml`](behavior.yaml) | Global safety, accuracy, context and interaction rules | Always |
| [`command.yaml`](command.yaml) | Minimal command triggers, aliases, workflow pointers and authorization boundaries | Always |
| [`workflow.md`](workflow.md) | Execution lifecycle, route precedence, authorization and verification | When workflow/execution is material |
| [`workflow/github.md`](workflow/github.md) | GitHub access surfaces and routing orientation | When GitHub capability is material |
| [`workflow/mcp.md`](workflow/mcp.md) | Selected MCP bootstrap, targeted schema and technical-owner discovery | Only for a selected permitted MCP route |
| [`workflow/coding.md`](workflow/coding.md) | Coding principles and execution-tier selection | When coding applies |
| [`workflow/research.md`](workflow/research.md) | Research source selection and evidence standards | When research applies |
| [`workflow/chat-handoff.md`](workflow/chat-handoff.md) | Explicit recent-chat context transfer and opt-in Workspace continuity | Only on explicit handoff command |
| [`projects/<project>/`](projects/template.txt) | All verified project-specific instruction deltas | When project scope is verified |
| [`AGENTS.md`](AGENTS.md) | Repository-agent fallback and Admin maintenance rules | When the repository context applies |

The coding modules in [`workflow/coding/`](workflow/coding/) and research modules in [`workflow/research/`](workflow/research/) are selected **independently** by the `core.yaml` registry. They are not an automatic recursive load. A matching module is read in full; nonmatching modules remain unloaded.

The registry is an **ordered source graph**, not a hierarchy of policy authority. Higher-priority ChatGPT instructions and provider admission continue to apply. Project and repository instructions extend parent rules unless an explicit valid override exists.

## What workflows are for

A **workflow** describes how GPT should complete a particular kind of task. It connects the requested outcome to the appropriate execution route, required checks, and completion evidence. Unlike [`behavior.yaml`](behavior.yaml), which defines rules applying across tasks, a workflow is loaded **only when its use case matches**. Unlike [`command.yaml`](command.yaml), it owns the procedure rather than the command trigger.

- **`workflow.md` — execution coordinator:** decides which authorized provider or tool surface fits the task, orders dependent steps, and defines preflight, failure recovery, and verification boundaries.
- **`workflow/*.md` — conditional specializations:** add relevant rules for GitHub, MCP, coding, research, or explicit chat handoff. Topic modules refine their parent without automatically loading unrelated modules.
- **Target-repository technical contracts:** supply the exact tool operations, parameters, and runtime behavior. Admin workflows point to these owners instead of copying their specifications.

**Example:** A request to inspect a repository selects GitHub orientation and an allowed read route; a request to run repository tests additionally needs a permitted execution environment and quality checks. Neither request authorizes deployment simply because a workflow is loaded.

The sequence is **task intent → matching registry cases → applicable workflows → authorized provider operation → verified result**. The [registry](core.yaml) controls loading, [`workflow.md#routing_decision_order`](workflow.md#routing_decision_order) controls execution-route precedence, and the live provider controls admission. Loading a workflow is not an action or an authorization grant.

## Fresh-chat bootstrap

1. Use the connected GitHub connector to read **complete current** `core.yaml`, then `behavior.yaml` and `command.yaml`. Retain verified repository revision and file SHA where available.
2. If the current ChatGPT Project name is explicitly supplied or verifiably exposed, verify its slug against `projects/`, enumerate **all existing files** in `projects/<slug>/`, and read each completely. Verified absence means inherit global rules; missing or truncated inventory does not.
3. If a target repository is active, resolve it from verified project instructions or the current task, then read its `AGENTS.md` when present. Otherwise apply [`AGENTS.md#fallback_repository_agent`](AGENTS.md#fallback_repository_agent).
4. Evaluate each `core.yaml` use-case trigger independently. Load only relevant workflows and topic modules. Load `workflow.md` when execution or routing calls for it; project recognition alone does not authorize tools.
5. Reuse verified sources within an unchanged chat/revision/scope. Refresh when sources or scope change, or the user requests it. Report gaps using `loaded_verified`, `not_applicable`, `absent_verified`, `unavailable`, `partial`, or `unknown` as appropriate.

**Bootstrap is read-only.** A new chat does not create a Workspace, inspect MCP automatically, transfer slots, restart a service, or grant a repository write. See [`projects/template.txt`](projects/template.txt) for the ChatGPT Project bootstrap pointer.

## Commands

[`command.yaml`](command.yaml) retains exactly four fields per command: `command`, `aliases`, `workflow` and `authorization`. It is a **dispatcher**, not a duplicate workflow implementation.

| Command | Alias | Delegated behavior |
| --- | --- | --- |
| `reload admin` | `reload admin plane`, `reload admin control plane` | Refresh the Admin instruction sources from [`core.yaml`](core.yaml); no runtime restart |
| `chat handoff` | `chat_handoff` | Follow [chat handoff](workflow/chat-handoff.md); context-only by default, opt-in `workspace` suffix |
| `reload mcp` | — | Invoke the registered `mcp_reload()` with default scope; in-process reload, **not** an MCP process restart |
| `update mcp` | `auto update` | Follow the [AWA self-update contract](https://github.com/awa-si/awa/blob/main/mcp/host/workflow/update.md#gpt-operated-awa-self-update-sequence); bounded host pull and conditional `awa:mcp` restart |
| `update host` | `sync host` | Follow [AWA host Git maintenance](https://github.com/awa-si/awa/blob/main/mcp/host/workflow/maintenance.md#awa-organization-host-git-update); guarded fast-forward pull of `awa-si/awa@main` into `/opt/awa`, no push/restart/deploy |

Only an **explicit current command**, its applicable policy, and live provider admission can authorize the described effect. `update host` is not `update mcp`; neither is a standing authorization. Do not infer execution success from a command definition or a source commit.

### Chat handoff boundary

`chat handoff` with no source selected requests a same-project Chat Overview when an authoritative listing is available. Selecting a source produces a bounded summary of at most the last 5–10 accessible interactions. `chat_handoff current` targets the current chat. Adding `workspace` explicitly requests separately authorized continuity of existing Workspace slots; the [handoff owner](workflow/chat-handoff.md) also covers unreserved imported slots and ambiguity recovery.

An unavailable chat listing is **not** an empty project. A visible Context Summary is **not** a new chat, persistent checkpoint or proof of Workspace adoption. Follow the workflow's evidence and failure rules rather than reconstructing unavailable chat history.

## Behavior contract

[`behavior.yaml`](behavior.yaml) contains 23 ordered rule blocks, each with `priority`, `scope`, `apply_when`, and `rules`. Lower numeric priority wins only for unresolved same-authority conflicts among applicable rules. `rules.apply_when` provides narrower gates for individual directives; `rules.directives` preserves list-structured policy where needed.

Keys describe policy intent (for example `prohibited_fabrications` and `evidence_based_verification`), while values retain normative behavior. Refer to the current file rather than duplicating its rules in project instructions or this README.

## Tool and execution boundaries

[`workflow.md#routing_decision_order`](workflow.md#routing_decision_order) is the only normative route-precedence owner. Classify the desired effect before choosing a provider:

| Need | Default orientation |
| --- | --- |
| Remote GitHub read, inspect, patch or write without local execution | Connected GitHub connector or its suitable patch wrapper |
| Repository tests, builds or development requiring a full runtime | Authorized AWA MCP Workspace when selected and permitted |
| Lightweight isolated calculation, parsing or artifact processing | Available native sandbox, when sufficient |
| MCP-specific operations | Selected MCP route; [`workflow/mcp.md`](workflow/mcp.md), live schema and matching technical owner |

These are **routing defaults**, not permissions or guarantees of tool availability. Product-mode restrictions, explicit provider selection, ownership, and live admission can change the eligible route. [`workflow/github.md`](workflow/github.md) distinguishes the ChatGPT connector, Patch, GitHub Workspace, AWA MCP GitHub, and AWA MCP Workspace Git surfaces; their credentials are not interchangeable.

For an authorized MCP route, select only the relevant current `mcp_model` schema and `mcp_instructions` technical sources. An Admin snapshot through `mcp_instructions(topic="admin", compact=false)` is supplemental or an explicitly permitted bounded fallback; it does not silently replace required connected-GitHub canonical reads. Discovery and documentation **never** confer execution authorization.

Mixed coding, research, repository and MCP requirements can combine under [`workflow.md#mixed_case_handling`](workflow.md#mixed_case_handling). An unmatched task uses [`workflow.md#unknown_case_handling`](workflow.md#unknown_case_handling) without bypassing authorization.

## Maintenance and verification

- **Canonical ownership:** put policy in `behavior.yaml`, command recognition in `command.yaml`, execution routing in `workflow.md`, project deltas under `projects/<project>/`, and domain technical contracts in their target repository. Keep the README an orientation document.
- **Before editing:** resolve the current branch, relevant consumers, rule owner, public-repository safety, and existing contracts. Preserve unrelated content and avoid semantic drift.
- **After editing:** inspect the changed source, check YAML/Markdown structure, source paths, anchors and applicability keys, and verify the remote commit. When public API or cross-repository behavior changes, separately validate affected consumers with authorized tooling.
- **Evidence boundaries:** source committed, remote pushed, host pulled, service restart requested, runtime activated and tests passed are different claims. Report only observed results and identify missing checks.
- **Public repository:** never commit credentials, secrets, private keys, session material or confidential information. Use symbolic references where sensitive detail is unnecessary.

Admin is declarative; it contains no in-repository Python validation runner. Use focused review or separately authorized validation rather than claiming a local suite passed. Cross-repository checks need independently verified revision pairs and provider receipts.
