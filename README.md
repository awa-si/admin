# GPT Admin

Declarative instruction control plane for ChatGPT. Repository: `awa-si/admin`.

**Scope:** source discovery, policy composition, command dispatch, workflow routing, project/repository overlays, and completion evidence.  
**Non-goals:** MCP implementation, tool registration, deployment, process lifecycle, and ChatGPT UI state.

**Canonical entry point:** [`core.yaml`](core.yaml). Fetch authoritative Admin sources using the connected GitHub connector. Cached conversation context and MCP snapshots are not substitutes for required fresh-chat reads.

## Architecture

| Component | Contract owner | Activation |
| --- | --- | --- |
| Source graph | [`core.yaml`](core.yaml) | First read |
| Global policy | [`behavior.yaml`](behavior.yaml) | Always |
| Command dispatcher | [`command.yaml`](command.yaml) | Always |
| Execution router | [`workflow.md`](workflow.md) | Workflow or execution task |
| GitHub routing | [`workflow/github.md`](workflow/github.md) | Material GitHub capability |
| MCP routing | [`workflow/mcp.md`](workflow/mcp.md) | Selected, permitted MCP route |
| Coding | [`workflow/coding.md`](workflow/coding.md) | Coding use case |
| Research | [`workflow/research.md`](workflow/research.md) | Research or material fact check |
| Chat handoff | [`workflow/chat-handoff.md`](workflow/chat-handoff.md) | Explicit handoff command |
| Project overrides | `projects/<verified-project-slug>/*` | Verified project scope |
| Repository policy | `<repository>/AGENTS.md` | Active repository context |
| Repository fallback | [`AGENTS.md#fallback_repository_agent`](AGENTS.md#fallback_repository_agent) | Active target without `AGENTS.md` |

The `core.yaml` registry is an **ordered source dependency graph**, not an instruction-precedence hierarchy. Evaluate matching cases independently. Coding modules under [`workflow/coding/`](workflow/coding/) and research modules under [`workflow/research/`](workflow/research/) load only when their respective registry conditions match; their parent entries do not imply recursive loading.

**Precedence:** higher-priority ChatGPT instructions → applicable global rules → workflow contracts → explicit project deltas → active repository policy, subject to provider authorization and admission. Children retain parent rules unless explicitly overridden.

## Workflow model

A workflow specifies the **execution algorithm and evidence contract** for a class of requests:

- **Trigger:** matching task intent, registered command, or material capability requirement.
- **Resolution:** applicable owner files and dependencies, without unrelated source loading.
- **Routing:** permitted execution provider and operation under [`workflow.md#routing_decision_order`](workflow.md#routing_decision_order).
- **Execution:** ordered preflight, action, failure recovery, and required validation.
- **Completion:** native receipts and independently observed target state; unresolved requirements remain explicit.

```text
user request
  -> core.yaml: classify independent use cases
  -> behavior.yaml: apply global policy
  -> conditional workflow(s): resolve route and checks
  -> live provider: authenticate, authorize, admit, execute
  -> verify: report observed result or exact blocker
```

**Ownership boundaries:** `behavior.yaml` declares cross-task invariants; `command.yaml` maps command names to workflows; `workflow.md` selects execution routes; specialized workflows define conditional procedures; target repositories own implementation-specific APIs and host operations. A workflow load never grants mutation permission.

## Fresh-chat bootstrap

1. **Read:** complete current `core.yaml`, `behavior.yaml`, and `command.yaml` through the connected GitHub connector. Record revision and file SHA where exposed.
2. **Resolve project:** only from explicit or client-verified ChatGPT Project identity. Verify the slug in `projects/`; enumerate every existing file under the matching project directory and read each fully. `absent_verified` requires authoritative absence evidence.
3. **Resolve repository:** from verified project instructions or task context; read its `AGENTS.md` if present, otherwise use the Admin fallback. Do not map project names to repositories by inference.
4. **Select conditional sources:** independently evaluate `core.yaml` registry gates; load relevant full workflow/module files. Do not eagerly load every workflow.
5. **Reuse or refresh:** cache verified sources within an unchanged revision and scope; invalidate on source change, scope change, or explicit refresh.
6. **Report:** `loaded_verified`, `not_applicable`, `absent_verified`, `unavailable`, `partial`, or `unknown`; identify incomplete sources precisely.

Bootstrap is **read-only**. It does not create a ChatGPT chat, discover MCP tools without cause, bind Workspace slots, execute code, or activate a service. See [`projects/template.txt`](projects/template.txt).

## Behavior schema

[`behavior.yaml`](behavior.yaml) defines 23 prioritized rule blocks using the invariant structure:

```yaml
<rule_id>:
  priority: <integer>
  scope: <semantic_scope>
  apply_when: <activation_condition>
  rules:
    apply_when:  # optional narrower applicability gates
      <rule_key>: <condition>
    <rule_key>: <normative_directive>
```

Priority `1` is highest **within the same instruction authority**. Only applicable rules participate in conflict resolution. `rules.directives` retains list-form rules where required. Current semantic rule keys and values are authoritative; the README is not a second policy definition.

## Command dispatch

[`command.yaml`](command.yaml) defines five commands. Each entry contains `command`, `aliases`, `workflow`, and `authorization`. Execution procedures remain in the referenced owners.

| Command | Aliases | Operation / boundary |
| --- | --- | --- |
| `reload admin` | `reload admin plane`, `reload admin control plane` | Re-read Admin sources via `core.yaml`; no runtime restart |
| `chat handoff` | `chat_handoff` | [Handoff workflow](workflow/chat-handoff.md); context-only default, `workspace` explicit opt-in |
| `reload mcp` | — | `mcp_reload()` with default scope; in-process reload only |
| `update mcp` | `auto update` | [AWA self-update](https://github.com/awa-si/awa/blob/main/mcp/host/workflow/update.md#gpt-operated-awa-self-update-sequence); guarded host pull and conditional `awa:mcp` restart |
| `update host` | `sync host` | [Host Git maintenance](https://github.com/awa-si/awa/blob/main/mcp/host/workflow/maintenance.md#awa-organization-host-git-update); fast-forward-only `awa-si/awa@main` pull into `/opt/awa`; no push, restart, or deployment |

The exact current command provides only its bounded authorization. Provider admission is still required; discovery and command definitions are not execution receipts. `update host` does not authorize `update mcp` effects.

### Handoff semantics

With no selected source, `chat handoff` requests an authoritative project-chat overview. `chat_handoff current` selects the current conversation. Source summaries cover the last 5–10 accessible interactions; missing data is labeled, not reconstructed. The `workspace` suffix requests separately admitted Workspace continuity under the [canonical handoff contract](workflow/chat-handoff.md).

An unavailable project-chat listing is not an empty listing. A generated Context Summary is not proof of chat creation, persistence, slot transfer, or adoption.

## Provider routing

[`workflow.md#routing_decision_order`](workflow.md#routing_decision_order) is the route-precedence authority. [`workflow/github.md`](workflow/github.md) documents connector, Patch, GitHub Workspace, AWA MCP GitHub, and AWA MCP Workspace Git surfaces.

| Required capability | Preferred eligible route |
| --- | --- |
| Remote repository read/patch/write without local execution | Connected GitHub connector or Patch wrapper |
| Repository tests/builds/debugging requiring a runtime | Authorized AWA MCP Workspace |
| Isolated calculation, processing, temporary artifacts | Available native sandbox |
| Selected MCP operation | Live MCP schema plus matching technical workflow |

**Routing is conditional:** product mode, explicit user provider selection, scope, repository ownership, current schema, and provider admission constrain the choice. Connector and AWA credentials are independent; a workspace is not implicitly authorized or reusable.

For MCP, [`workflow/mcp.md`](workflow/mcp.md) owns selective `mcp_model` discovery and `mcp_instructions` loading. An Admin snapshot via `mcp_instructions(topic="admin", compact=false)` is supplemental or an explicitly permitted recovery source; it cannot override canonical GitHub-read requirements.

For overlapping use cases, follow [`mixed_case_handling`](workflow.md#mixed_case_handling). For uncovered execution requirements, follow [`unknown_case_handling`](workflow.md#unknown_case_handling). Both retain authorization and verification gates.

## Development and verification

**Source changes**
1. Identify the narrowest normative owner and affected consumers before editing.
2. Resolve current repository, branch, source revision, explicit overrides, and public-safety constraints.
3. Preserve semantics and update cross-references; avoid copying technical contracts into Admin.
4. Validate changed YAML/Markdown, applicability mappings, links, and owner boundaries.
5. Verify the remote commit and report checks that were not executed.

**Evidence levels:** instruction source loaded ≠ repository committed ≠ remote pushed ≠ host synchronized ≠ process restarted ≠ runtime activated. Each claim needs a matching native receipt or independent observation.

**Repository policy:** this public repository must not contain credentials, tokens, private keys, confidential records, or session secrets. Admin has no in-repository Python test runner; use focused inspection or an independently authorized validator. Cross-repository checks require verified revision pairs.

For project bootstrap integration, use [`projects/template.txt`](projects/template.txt). For repository-specific maintenance, follow [`AGENTS.md`](AGENTS.md).
