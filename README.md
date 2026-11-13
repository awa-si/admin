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
│   │   ├── coding/dependencies.md  dependencies and toolchains
│   │   ├── coding/concurrency.md   async and parallelism
│   │   ├── coding/performance.md   performance and resource costs
│   │   ├── coding/testing.md       test design
│   │   └── coding/async-testing.md Python asyncio pytest
│   ├── workflow/research.md       research or fact verification
│   ├── workflow/github.md         selected GitHub route
│   ├── workflow/mcp.md            selected AWA MCP route
│   └── unknown → workflow.md      unmatched execution case
├── projects/<project>/*           verified ChatGPT project
└── <repository>/AGENTS.md         active repository context
    └── fallback: admin/AGENTS.md  if target agent is absent
```

| Source | Responsibility |
| --- | --- |
| [`core.yaml`](core.yaml) | Registry, matching conditions, source references and resolution semantics |
| [`behavior.yaml`](behavior.yaml) | Always-loaded global behavior, safety and authorization principles |
| [`command.yaml`](command.yaml) | Always-loaded explicit command contracts (`reload admin`, `reload mcp`, `mcp_auto_update`) |
| [`workflow.md`](workflow.md) | Common execution lifecycle, known routing cases, route precedence, preflight and verification |
| [`workflow/coding.md`](workflow/coding.md) | Global engineering decisions and quality gates |
| `workflow/coding/*.md` | Conditionally selected technical coding guidance; full module only when registry `read_when` matches |
| [`workflow/research.md`](workflow/research.md) | Research guidance for knowledge, code, documentation and legal investigations |
| [`workflow/github.md`](workflow/github.md) | GitHub connector, patch, workspace and Actions route contracts |
| [`workflow/mcp.md`](workflow/mcp.md) | AWA-MCP-specific route and delegated technical contracts |
| [`projects/template.txt`](projects/template.txt) | ChatGPT Project bootstrap pointing to the registry |
| `projects/<project>/*` | Verified project deltas; **enumerate every existing file and read each completely** |
| `<repository>/AGENTS.md` | Active repository agent; fall back to [`AGENTS.md`](AGENTS.md) when absent |

## Source resolution

1. Load `core.yaml` from the connected GitHub repository, then load `behavior.yaml` and `command.yaml` **always**.
2. Evaluate relevant registry entries by task intent, scope and current product context. Load only matching files. For mixed requests, combine matching cases using `workflow.md#mixed_case_handling`, without redundant reads. For unmatched execution needs, use `workflow.md#unknown_case_handling` while retaining authorization and verification gates.
3. Use `workflow.md#routing_decision_order` as the **sole normative execution-route precedence** when routing is material. The known cases in `workflow.md` aid classification but never grant permissions.
4. Load `workflow/github.md` or `workflow/mcp.md` only for an applicable, permitted provider route. The registry declares that these routes require workflow routing. Coding and research modules can be loaded directly when their cases match. Within coding, independently evaluate each `core.yaml` nested module `read_when` gate. Load only matching complete module files; `read_when` does not stream partial file sections.
5. When a ChatGPT Project is explicitly identified or exposed, verify its slug and read **all** existing files under `projects/<project>/*`. Never infer hidden UI project state. For an active target repository, read its `AGENTS.md` if present, otherwise use the Admin fallback.
6. For unknown cases, preserve the existing workflow and authorization gates; do not invent permission, capability or completion evidence. Report unavailable required sources and incomplete reads precisely.

Project and repository rules extend applicable parent rules; overrides must be explicit. Higher-priority ChatGPT instructions remain authoritative. Repository state and live provider schemas determine the actual available operations.

## Governed host update command

`mcp_auto_update` selects the AWA checkout update and MCP activation contract in [`command.yaml`](command.yaml), with the technical steps owned by [AWA Host](https://github.com/awa-si/awa/blob/main/mcp/host/README.md#gpt-operated-awa-self-update-sequence). When requested, present a native **Confirm & Execute** button with both effects explicitly selected; clicking it submits authorization as a new user message, never a direct host-tool call. If the UI control is unavailable, request equivalent explicit textual authorization. After confirmation, recheck preflight and provider admission. With approval for **both** operations: inspect the host checkout, fast-forward `awa-si/awa@main` using `host_exec(operation="git.pull")`, inspect the resulting checkout, then request `host_exec(operation="supervisor.control", arguments={"service":"awa:mcp","action":"restart"})` only if the running MCP revision is stale. After an accepted MCP restart request, wait **5 seconds** before the first post-restart `mcp_version` retrieval, then verify activation independently; a queued restart or elapsed delay is not completion evidence. The command definition is not standing approval or an unattended updater. `mcp_reload` does not restart Python code.

## Tool discovery responsibility

Admin does not maintain a second inventory of client, MCP, or plugin tool schemas. [`workflow.md#tool_discovery_boundary`](workflow.md) separates the responsibilities:

| Layer | Owns |
| --- | --- |
| OpenAI client / current host | Exposes available tools, dynamically searches deferred tools when supported, and supplies current invocation schemas |
| `core.yaml` | Matches use cases to applicable instruction sources, without cataloging tool parameters |
| `workflow.md` | Chooses a permitted execution route and defines required evidence |
| `workflow/mcp.md` | Defines the **AWA-specific** discovery boundary; live AWA provider contracts and tool schemas remain authoritative for technical invocation |
| Capability provider | Authenticates, authorizes, admits operations, executes, and returns observable results |

Evaluate a currently available native sandbox (including Code Interpreter) before provisioning an external workspace for isolated calculations, analysis, temporary Python processing or artifact creation. A sandbox does **not** imply repository access, persistent host state, or deployment rights. Repository mutations continue through an authorized repository route. Tool discovery alone never grants permission or proves execution.

OpenAI's [Tool Search](https://developers.openai.com/api/docs/guides/tools-tool-search) and [Code Interpreter](https://developers.openai.com/api/docs/guides/tools-code-interpreter) guides document **API capabilities**; they do not establish that every documented option is exposed by the current ChatGPT client. Always use the actual available tool surface.

## Mixed and unknown cases

`workflow.md#mixed_case_handling` composes multiple applicable cases into a dependency-aware plan. Research/coding cases and GitHub/MCP execution routes are distinct dimensions; the presence of one does not grant permission to use another. Apply every material case's source and verification contract without duplicated reads.

`workflow.md#unknown_case_handling` covers only work not adequately described by a registered case. It may use current client tool discovery and select a suitable authorized route, but never guesses tools, skips provider admission, or interprets a discovered capability as permission.

## Execution and verification

Use the smallest permitted route that can complete the requested outcome, including its necessary tests or verification. `workflow.md` owns the shared lifecycle; provider-specific mechanics stay with their respective route files. For AWA MCP, use `mcp_model` for live capability discovery and `mcp_instructions` for **local technical documentation only**, not Admin policy loading. Discovery is not authorization or execution admission.

Differentiate an observed GitHub write, a successful test, a deployed revision and an active runtime. Claim completion only to the level supported by actual evidence. Deployment and other material side effects require their applicable authorization.

## Project bootstrap

Use [`projects/template.txt`](projects/template.txt) as the starting point for ChatGPT Project instructions. It resolves the same `core.yaml#registry` and project/repository boundaries. Avoid duplicating the global policies in project files.

## Benchmarks

The [AWA Admin benchmark](benchmarks/README.md) contains 20 version-pinned A/B use cases, an offline trace evaluator, regression tests, and an [observed static validation report](benchmarks/results/static-2026-11-12.json). The source-size comparison and automated static checks are complete; **live GPT A/B latency, token, and task-success measurements remain unmeasured until an isolated model runner supplies authentic traces**.

## Validation

```sh
python -m pip install PyYAML
python validate.py
```

The validator checks the registry structure and canonical owner references; execution of the validator and remote-state verification are separate steps.

This repository is public. Never commit secrets, credentials, tokens, private keys, session material or confidential data.

## Cross-repository MCP contract validation

Run `python -m unittest test_cross_repo_contract` for offline negative/positive
regressions. To validate real paired checkouts, use
`python cross_repo_contract.py --admin-root /path/to/admin --awa-root /path/to/awa
--expected-admin-sha <exact-admin-HEAD> --expected-awa-sha <exact-awa-HEAD>`.
The two SHA arguments are required; the validator fails on revision mismatch.
It checks the Admin route owner, MCP local-only technical topics, the public
instruction tool argument list, documentation parity, the single canonical
Knowledge and Browser documentation owners (including their generator markers),
and the discovery/authority boundary. It never fetches a repository or activates MCP. CI must explicitly
check out both repositories at known revisions and pass their verified SHAs;
repository checkout permissions remain independently required.
