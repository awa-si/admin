# GPT Admin

`awa-si/admin` is the ChatGPT control plane for shared behavior, use-case resolution, workflow execution, and project/repository-specific instructions. **`core.yaml` is the authoritative use-case registry and source resolver, not an instruction body.** Read the current files through the connected GitHub connector. AWA MCP is not an alternative source for Admin policy.

## Registry and ownership

The `core.yaml#registry` is an **ordered parent/case source graph**. Its order guides source evaluation; it does **not** supersede ChatGPT's instruction hierarchy. Each case is evaluated independently when its load condition matches: nesting under `workflow` does **not** automatically load `workflow.md`. The `unknown` case reuses `workflow.md` for an uncovered execution requirement; it does not introduce another tool provider.

```text
core.yaml  (registry / resolver)
├── behavior.yaml                  always
├── command.yaml                   always (user-command contracts)
├── workflow.md                    workflow or execution
│   ├── workflow/coding.md         coding or code-quality selection
│   │   ├── coding/architecture.md  design, security, code structure
│   │   ├── coding/documentation.md coding documentation contracts
│   │   ├── coding/quality.md       quality gates and verification
│   │   ├── coding/dependencies.md  dependencies and toolchains
│   │   ├── coding/concurrency.md   async and parallelism
│   │   ├── coding/performance.md   performance and resource costs
│   │   ├── coding/testing.md       test design
│   │   └── coding/async-testing.md Python asyncio pytest
│   ├── workflow/research.md       search/research bootstrap
│   │   └── research/{knowledge,code,docs,legal}.md on demand
│   ├── workflow/github.md         GitHub capability orientation before final route selection
│   ├── workflow/mcp.md            minimal MCP discovery bootstrap
│   ├── workflow/chat-handoff.md   conditional chat continuation workflow
│   └── unknown → workflow.md      unmatched execution case
├── projects/<project>/*           verified ChatGPT project
└── <repository>/AGENTS.md         active repository context
    └── fallback: admin/AGENTS.md  if target agent is absent
```

| Source | Responsibility |
| --- | --- |
| [`core.yaml`](core.yaml) | Registry, matching conditions, source references and resolution semantics |
| [`behavior.yaml`](behavior.yaml) | Always-loaded global behavior, safety and authorization principles |
| [`command.yaml`](command.yaml) | Always-loaded explicit command contracts (`reload admin`, `chat_handoff [CHAT_NAME]`, `reload mcp`, `mcp_auto_update`) |
| [`workflow.md`](workflow.md) | Common execution lifecycle, known routing cases, route precedence, preflight and verification |
| [`workflow/coding.md`](workflow/coding.md) | Coding bootstrap, general principles and three latency-aware execution tiers |
| `workflow/coding/*.md` | Conditionally selected technical coding guidance; full module only when registry `read_when` matches |
| [`workflow/research.md`](workflow/research.md) | Direct ChatGPT search/research by default; permitted MCP Agent/Intelligence for heavy cross-source or specialized research; topic modules on demand |
| [`workflow/github.md`](workflow/github.md) | GitHub connector, patch, workspace and Actions route contracts |
| [`workflow/mcp.md`](workflow/mcp.md) | Minimal MCP bootstrap; live discovery resolves provider-specific technical contracts |
| [`workflow/chat-handoff.md`](workflow/chat-handoff.md) | Generic same-project context extraction; loaded only by `chat_handoff`; produces Context Summary with Previos Context Saved note |
| [`projects/template.txt`](projects/template.txt) | ChatGPT Project bootstrap pointing to the registry |
| `projects/<project>/*` | Verified project deltas; **enumerate every existing file and read each completely** |
| `<repository>/AGENTS.md` | Active repository agent; fall back to [`AGENTS.md`](AGENTS.md) when absent |

## Source resolution

1. Load `core.yaml` from the connected GitHub repository, then load `behavior.yaml` and `command.yaml` **always**.
2. Evaluate relevant registry entries by task intent, scope and current product context. Load only matching files. For mixed requests, combine matching cases using `workflow.md#mixed_case_handling`, without redundant reads. For unmatched execution needs, use `workflow.md#unknown_case_handling` while retaining authorization and verification gates.
3. Use `workflow.md#routing_decision_order` as the **sole normative execution-route precedence** when routing is material. The known cases in `workflow.md` aid classification but never grant permissions.
4. Load `workflow/github.md` when GitHub capability is material, **including AWA MCP GitHub routes**, so GPT can orient among all five surfaces before final routing. Load `workflow/mcp.md` only when a permitted MCP route is selected. Both remain subject to the workflow and authorization gates. Coding and research modules can be loaded directly when their cases match. Within coding, independently evaluate each `core.yaml` nested module `read_when` gate. Load only matching complete module files; `read_when` does not stream partial file sections.
5. When a ChatGPT Project is explicitly identified or exposed, verify its slug and read **all** existing files under `projects/<project>/*`. Never infer hidden UI project state. For an active target repository, read its `AGENTS.md` if present, otherwise use the Admin fallback.
6. For unknown cases, preserve the existing workflow and authorization gates; do not invent permission, capability or completion evidence. Report unavailable required sources and incomplete reads precisely.

Project and repository rules extend applicable parent rules; overrides must be explicit. Higher-priority ChatGPT instructions remain authoritative. Repository state and live provider schemas determine the actual available operations.

## Same-project chat handoff

`chat_handoff [CHAT_NAME]` loads [`workflow/chat-handoff.md`](workflow/chat-handoff.md) **only when explicitly invoked**. Without a name it summarizes the current chat; with a name it identifies an accessible previous chat within the current verified ChatGPT Project. The output is a structured **Context Summary**, followed by the note **Previos Context Saved** once a usable summary is displayed. This is visible-response capture for copy/reuse, **not** evidence of Memory, checkpoint, file or cross-chat persistence.

The command is **generic and read-only**: it never binds MCP, adopts a Workspace, creates checkpoints, starts Work or executes jobs. The receiving chat decides how to continue: if relevant existing MCP Work/Workspace is available and authorized, it can independently resolve and reuse it; otherwise it simply works from the summarized context. Original messages, historical reports, condensed summaries and independently verified receipts remain distinct evidence levels. Source history can be partial.

## Governed host update command

The ChatGPT command is `update mcp` (alias `auto update`, registry key `mcp_auto_update`) in [`command.yaml`](command.yaml). The exact current user command `update mcp` (or `auto update`) authorizes one fixed AWA host Git update and, if needed, the conditional `awa:mcp` restart. **Do not ask for an additional confirmation or render a Confirm & Execute control.** After read-only preflight and revalidated provider admission, invoke **`mcp_diagnostic(operation="update")` exactly once** as the primary executor. Its canonical implementation performs `git.inspect` → fast-forward `git.pull` → verified `git.inspect` → conditional restricted `supervisor.control` restart. Do **not** repeat these mutations as separate `host_exec` calls after the diagnostic update. After an accepted restart request, wait **5 seconds** before the first post-restart `mcp_version` retrieval; separately confirm process identity, deployed revision and health. A queued restart or elapsed delay is not completion evidence. The command grants no standing permission, unattended execution, other repository update or unrelated service restart. See the [AWA host technical contract](https://github.com/awa-si/awa/blob/main/mcp/host/README.md#gpt-operated-awa-self-update-sequence).

## Tool discovery responsibility

For GitHub tasks, GPT first classifies intent: **GitHub** names the domain, not a specific execution tool. **Read / inspect / search / patch / write** without repository execution defaults to the ChatGPT GitHub Connector or its Patch wrapper (load current applicable plugin/skill instructions). **Repository tests / development / run / build / debug** requiring repository execution defaults to the authorized **AWA MCP Workspace** (load current MCP instructions, workspace contract and live tool schema). Explicit provider selection and product-mode restrictions take precedence; an unavailable or unauthorized default is a blocker or requires a separately permitted fallback. Broad repository search alone does not require a workspace.

Global `behavior.yaml` now delegates GitHub tool selection to `workflow.md#routing_decision_order` and its `workflow/github.md#github_tool_orientation` surface map. The ChatGPT Connector preference is a tie-breaker, not a ban on an explicitly selected, independently authorized AWA route. Workspace creation requires a material execution need or explicit user selection and current provider admission; AWA and ChatGPT credentials remain separate.

GitHub execution has five distinct surfaces described in [`workflow/github.md`](workflow/github.md#github_tool_orientation): native ChatGPT GitHub connector, GitHub Patch (connector wrapper), GitHub Workspace (connector-backed local execution wrapper), AWA MCP `github_exec` (independent AWA host credentials), and AWA MCP Workspace Git through `workspace_exec` (independent workspace admission/transport). `workspace.github_exec` is a conceptual label, not a separately registered public MCP tool. GPT uses that orientation during [`workflow.md#routing_decision_order`](workflow.md#routing_decision_order), considering eligible surfaces without automatically probing every provider or conflating connector credentials with AWA permissions.

Admin does not maintain a second inventory of client, MCP, or plugin tool schemas. [`workflow.md#tool_discovery_boundary`](workflow.md) separates the responsibilities:

| Layer | Owns |
| --- | --- |
| OpenAI client / current host | Exposes available tools, dynamically searches deferred tools when supported, and supplies current invocation schemas |
| `core.yaml` | Matches use cases to applicable instruction sources, without cataloging tool parameters |
| `workflow.md` | Chooses a permitted execution route and defines required evidence |
| `workflow/mcp.md` | Introduces MCP discovery only; selected provider schemas, technical instructions and native receipts govern execution |
| Capability provider | Authenticates, authorizes, admits operations, executes, and returns observable results |

Evaluate a currently available native sandbox (including Code Interpreter) before provisioning an external workspace for isolated calculations, analysis, temporary Python processing or artifact creation. A sandbox does **not** imply repository access, persistent host state, or deployment rights. Repository mutations continue through an authorized repository route. Tool discovery alone never grants permission or proves execution.

OpenAI's [Tool Search](https://developers.openai.com/api/docs/guides/tools-tool-search) and [Code Interpreter](https://developers.openai.com/api/docs/guides/tools-code-interpreter) guides document **API capabilities**; they do not establish that every documented option is exposed by the current ChatGPT client. Always use the actual available tool surface.

## Mixed and unknown cases

`workflow.md#mixed_case_handling` composes multiple applicable cases into a dependency-aware plan. Research/coding cases and GitHub/MCP execution routes are distinct dimensions; the presence of one does not grant permission to use another. Apply every material case's source and verification contract without duplicated reads.

`workflow.md#unknown_case_handling` covers only work not adequately described by a registered case. It may use current client tool discovery and select a suitable authorized route, but never guesses tools, skips provider admission, or interprets a discovered capability as permission.

## Execution and verification

Use the smallest permitted route that can complete the requested outcome, including its necessary tests or verification. `workflow.md` owns the shared lifecycle; provider-specific mechanics stay with their respective route files. For a selected MCP route, use `mcp_model` for live capability discovery and `mcp_instructions` for **matching technical documentation only**, not Admin policy loading. Discovery is not authorization or execution admission.

Differentiate an observed GitHub write, a successful test, a deployed revision and an active runtime. Claim completion only to the level supported by actual evidence. Deployment and other material side effects require their applicable authorization.

## Project bootstrap

Use [`projects/template.txt`](projects/template.txt) as the starting point for ChatGPT Project instructions. It resolves the same `core.yaml#registry` and project/repository boundaries. Avoid duplicating the global policies in project files.

## Validation boundary

This repository contains declarative instructions and reference data, with **no tracked Python scripts, benchmark suite or local execution harness**. Validate source references, registry changes and command gates with a separately maintained approved checker or focused reviewed inspection; no current in-repository CLI validator exists. A GitHub commit or structural review does not establish runtime compliance.

This repository is public. Never commit secrets, credentials, tokens, private keys, session material or confidential data.

## Cross-repository MCP contract validation

The previous Python cross-repository contract validator and tests have been removed from `awa-si/admin`. Cross-repository contract checks must use an independently maintained, authorized checker and verified revision pairs. Do not claim those checks were executed merely because Admin's declarative sources were updated.
