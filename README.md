# GPT Admin

`core.yaml` is a **dynamic source index**, not an instruction body. ChatGPT loads it at chat/project level and resolves the relevant canonical owners on demand. AWA MCP does not bootstrap Admin policies.

## Canonical sources

| Source | Loading | Ownership |
| --- | --- | --- |
| [`core.yaml`](core.yaml) | Chat/project bootstrap | Small source router only |
| [`behavior.yaml`](behavior.yaml) | Always | Global ChatGPT behavior and policy |
| [`workflow.md`](workflow.md) | When workflow/execution is relevant | General execution and routing |
| [`coding.md`](coding.md) | When coding or implementation is relevant | Coding guidance |
| [`research.md`](research.md) | When research or material verification is relevant | Research guidance |
| `mcp_model`, `mcp_instructions` | When AWA MCP work is relevant | Live MCP capabilities and local technical sources, **not** ChatGPT policy |
| `projects/<project>/*` | When project is identified | Enumerate all existing project files and read each completely |
| `<repository>/AGENTS.md` | When repository context is active | Repository-specific behavior |
| [`AGENTS.md`](AGENTS.md) | If the active target repository has no agent | Fallback repository-agent policy |

## Project Custom Instructions

Use [`projects/template.txt`](projects/template.txt) as the ChatGPT Project bootstrap. It references only the core index and loads project files after verifying the exposed project slug. Never guess hidden UI state. Optional project deltas extend their parent rules unless explicitly overridden.

## Execution

The ChatGPT layer chooses which source files are material and reads them using the connected GitHub connector. MCP tool discovery and technical contracts are consulted only when an AWA MCP action is relevant; capability discovery alone grants no action authorization. Live provider schemas govern available operations.

## Validation

```sh
python -m pip install PyYAML
python validate.py
```

This repository is public. Never commit secrets, tokens, credentials, session material, or confidential data.
