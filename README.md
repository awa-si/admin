# GPT Admin

`awa-si/admin` is the ChatGPT control plane for shared behavior, use-case resolution, workflow execution, and project/repository-specific instructions. **`core.yaml` is the authoritative use-case registry and source resolver, not an instruction body.** Read the current files through the connected GitHub connector. AWA MCP is not an alternative source for Admin policy.

## Registry and ownership

The `core.yaml#registry` is an **ordered parent/child source graph**. Its order guides source evaluation; it does **not** supersede ChatGPT's instruction hierarchy. A child is considered independently when its load condition matches: nesting under `workflow` does **not** automatically load `workflow.md`.

```text
core.yaml  (registry / resolver)
├── behavior.yaml                  always
├── workflow.md                    workflow or execution
│   ├── workflow/coding.md         coding or implementation
│   ├── workflow/research.md       research or fact verification
│   ├── workflow/github.md         selected GitHub route
│   └── workflow/mcp.md            selected AWA MCP route
├── projects/<project>/*           verified ChatGPT project
└── <repository>/AGENTS.md         active repository context
    └── fallback: admin/AGENTS.md  if target agent is absent
```

| Source | Responsibility |
| --- | --- |
| [`core.yaml`](core.yaml) | Registry, matching conditions, source references and resolution semantics |
| [`behavior.yaml`](behavior.yaml) | Always-loaded global behavior, safety and authorization principles |
| [`workflow.md`](workflow.md) | Common execution lifecycle, known routing cases, route precedence, preflight and verification |
| [`workflow/coding.md`](workflow/coding.md) | Coding and implementation guidance |
| [`workflow/research.md`](workflow/research.md) | Research guidance for knowledge, code, documentation and legal investigations |
| [`workflow/github.md`](workflow/github.md) | GitHub connector, patch, workspace and Actions route contracts |
| [`workflow/mcp.md`](workflow/mcp.md) | AWA-MCP-specific route and delegated technical contracts |
| [`projects/template.txt`](projects/template.txt) | ChatGPT Project bootstrap pointing to the registry |
| `projects/<project>/*` | Verified project deltas; **enumerate every existing file and read each completely** |
| `<repository>/AGENTS.md` | Active repository agent; fall back to [`AGENTS.md`](AGENTS.md) when absent |

## Source resolution

1. Load `core.yaml` from the connected GitHub repository, then load `behavior.yaml` **always**.
2. Evaluate relevant registry entries by task intent, scope and current product context. Load only matching files. Combine overlapping use cases without redundant reads.
3. Use `workflow.md#routing_decision_order` as the **sole normative execution-route precedence** when routing is material. The known cases in `workflow.md` aid classification but never grant permissions.
4. Load `workflow/github.md` or `workflow/mcp.md` only for an applicable, permitted provider route. The registry declares that these routes require workflow routing. Coding and research modules can be loaded directly when their cases match.
5. When a ChatGPT Project is explicitly identified or exposed, verify its slug and read **all** existing files under `projects/<project>/*`. Never infer hidden UI project state. For an active target repository, read its `AGENTS.md` if present, otherwise use the Admin fallback.
6. For unknown cases, preserve the existing workflow and authorization gates; do not invent permission, capability or completion evidence. Report unavailable required sources and incomplete reads precisely.

Project and repository rules extend applicable parent rules; overrides must be explicit. Higher-priority ChatGPT instructions remain authoritative. Repository state and live provider schemas determine the actual available operations.

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

## Execution and verification

Use the smallest permitted route that can complete the requested outcome, including its necessary tests or verification. `workflow.md` owns the shared lifecycle; provider-specific mechanics stay with their respective route files. For AWA MCP, use `mcp_model` for live capability discovery and `mcp_instructions` for **local technical documentation only**, not Admin policy loading. Discovery is not authorization or execution admission.

Differentiate an observed GitHub write, a successful test, a deployed revision and an active runtime. Claim completion only to the level supported by actual evidence. Deployment and other material side effects require their applicable authorization.

## Project bootstrap

Use [`projects/template.txt`](projects/template.txt) as the starting point for ChatGPT Project instructions. It resolves the same `core.yaml#registry` and project/repository boundaries. Avoid duplicating the global policies in project files.

## Validation

```sh
python -m pip install PyYAML
python validate.py
```

The validator checks the registry structure and canonical owner references; execution of the validator and remote-state verification are separate steps.

This repository is public. Never commit secrets, credentials, tokens, private keys, session material or confidential data.
