# GPT Admin

**Audience:** GPT, ChatGPT client integrations, and users. `awa-si/admin` is the shared GPT/client/user-facing instruction control plane. Its Markdown documentation provides architecture and entry points for developers and users; its declarative owner files define machine-consumed policy, routing, and command contracts.

**Scope:** global instruction source discovery, policy composition, command dispatch, workflow routing, task-based repository resolution, and completion evidence.  
**Non-goals:** MCP implementation, tool registration, deployment, process lifecycle, and ChatGPT UI state.

**Canonical entry point:** [`core.yaml`](core.yaml). Fetch authoritative Admin sources using the connected GitHub connector. Cached conversation context and MCP snapshots are not substitutes for required fresh-chat reads.

**Admin maintenance read contract:** When working on `awa-si/admin` (including its architecture, policies, workflows, or documentation), GPT must read this complete, current `README.md` from the connected GitHub repository before making changes. This is a conditional maintenance read, not an unconditional fresh-chat bootstrap source. The README is orientation, not a replacement for normative `core.yaml`, `behavior.yaml`, `command.yaml`, or applicable workflow and repository-agent contracts.

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
| Technical documentation | [`workflow/documentation.md`](workflow/documentation.md) | Technical docs, API references, READMEs, specifications, and docs audits |
| Chat handoff | [`workflow/chat-handoff.md`](workflow/chat-handoff.md) | Explicit handoff command |
| Repository policy | `<repository>/AGENTS.md` | Active repository context |
| Repository fallback | [`AGENTS.md#fallback_repository_agent`](AGENTS.md#fallback_repository_agent) | Active target without `AGENTS.md` |

Technical documentation and specification handling is owned exclusively by [`workflow/documentation.md`](workflow/documentation.md), independently of coding and research. Its audience contracts separate **GPT-facing machine-readable directives** (structured, explicit, schema-compatible and authorization-safe) from **developer-facing documentation** (precise technical prose, stable symbols, verifiable examples and canonical references). General office-document authoring, binary document processing, and format conversion are outside Admin's technical documentation contract.

The `core.yaml` registry is an **ordered source dependency graph**, not an instruction-precedence hierarchy. Evaluate matching cases independently. Coding modules under [`workflow/coding.md`](workflow/coding.md) and research modules under [`workflow/research.md`](workflow/research.md) load only when their respective registry conditions match; their parent entries do not imply recursive loading.

**Precedence:** higher-priority ChatGPT instructions → applicable global rules → workflow contracts → active repository agent, subject to provider authorization and admission. Repository-specific overrides must be explicit. Children retain parent rules unless explicitly overridden.

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

**Ownership boundaries:** `behavior.yaml` owns global rules; `command.yaml` owns command dispatch; `workflow.md` owns route precedence; `workflow/documentation.md` owns technical documentation. Target repositories own implementation contracts. Loading any workflow does not grant permissions.

## Fresh-chat bootstrap

1. **Read:** complete current `core.yaml`, `behavior.yaml`, and `command.yaml` through the connected GitHub connector. Record revision and file SHA where exposed.
2. **Resolve repository:** use an explicit repository in the request or a verified active task/repository binding. Never infer repository identity from a ChatGPT Project name, session label or chat title. Read the target's `AGENTS.md` when present; otherwise apply the Admin repository-agent fallback.
3. **Select conditional sources:** evaluate `core.yaml` registry gates independently and load only relevant complete workflows and repository-owned helpers.
4. **Reuse or refresh:** reuse verified sources at unchanged revision and scope; refresh on source change, active repository scope change or explicit request.
5. **Report:** `loaded_verified`, `not_applicable`, `absent_verified`, `unavailable`, `partial`, or `unknown`; identify incomplete sources precisely.

Bootstrap is **read-only**. It does not create a ChatGPT chat, discover MCP tools without cause, bind Workspace slots, execute code, or activate a service. Repository-specific GPT rules and task-specific workflows are owned by the resolved repository, not by an Admin project overlay. The [global ChatGPT Custom Instructions bootstrap](global.txt) is designed for **Settings → Personalization → Custom Instructions**, while the [ChatGPT Project Custom Instructions bootstrap](bootstrap.txt) is designed for **Project → ••• → Project settings → Project instructions**. Both point to the same canonical Admin sources; project instructions should be used only where the respective Project requires them. Neither template independently establishes GitHub connector availability or access. It loads global Admin sources and resolves repositories only from explicit or verified task context; it replaces the retired `projects/template.txt`. Project instructions apply within that ChatGPT Project and are not deployed automatically by a GitHub commit.

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

[`workflow.md#routing_decision_order`](workflow.md#routing_decision_order) selects the permitted route. [`workflow/github.md`](workflow/github.md) classifies remote committed refs versus local Workspace state. For an admitted AWA MCP route, [`workflow/mcp.md`](workflow/mcp.md) dispatches remote reads through `github_exec` and authorized local worktree operations through `workspace_exec`; the [AWA MCP GitHub contract](https://github.com/awa-si/awa/blob/main/mcp/github/contract.md) owns operation schemas.

| Required capability | Preferred eligible route |
| --- | --- |
| Remote repository read/patch/write without local execution | Connected GitHub connector or Patch wrapper |
| Repository tests/builds/debugging requiring a runtime | Authorized AWA MCP Workspace |
| Isolated calculation, processing, temporary artifacts | Available native sandbox |
| Selected MCP operation | Live MCP schema plus matching technical workflow |

For generic requests such as `use <owner/repository> ws`, treat the text as Workspace intent rather than an Admin command. Resolve the exact repository and current-chat slot using the [MCP workflow](workflow/mcp.md) and the [Workspace session contract](https://github.com/awa-si/awa/blob/main/mcp/workspace/workflow/session.md); do not infer repository identity from a ChatGPT Project label. A cross-chat transfer requires explicit approval and live destination verification.

**Routing is conditional:** product mode, explicit user provider selection, scope, repository ownership, current schema, and provider admission constrain the choice. Connector and AWA credentials are independent; a workspace is not implicitly authorized or reusable.

For MCP, [`workflow/mcp.md`](workflow/mcp.md) owns selective `mcp_model` discovery and `mcp_instructions` loading. An Admin snapshot via `mcp_instructions(topic="admin", compact=false)` is supplemental or an explicitly permitted recovery source; it cannot override canonical GitHub-read requirements.

**MCP first-contact SessionRegistry:** After the first successful authorized AWA MCP call in a chat, [`workflow/mcp.md`](workflow/mcp.md) defines a best-effort `session.record` read, one conditional `session.update` for explicitly known missing labels, and one concise visible session summary for subsequent chat context. For example, `awa wip` is a valid client-declared `chat_title` only when supplied explicitly; `project_name` requires explicit or client-verified Project identity. Neither label verifies the ChatGPT UI, authorizes Workspace access, or creates a transcript/checkpoint. The technical owner remains [`awa-si/awa/mcp/session/contract.md`](https://github.com/awa-si/awa/blob/main/mcp/session/contract.md).

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

For repository-specific maintenance, read the target repository's `AGENTS.md` or use the fallback in [`AGENTS.md`](AGENTS.md) when it is absent. Multi-repository coordination requires an explicit or verified owner rather than a client Project-name mapping.
