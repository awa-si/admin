# Chat handoff — generic context summary

scope: global_chat_handoff_workflow
mode: normative_machine_directives
owner: awa-si/admin/workflow/chat-handoff.md
command_owner: awa-si/admin/command.yaml#chat_handoff
read_when: explicit_chat_handoff_command_only
inherits: awa-si/admin/behavior.yaml|awa-si/admin/command.yaml|applicable_project_deltas
side_effects: read_only|no_MCP_binding|no_workspace_access_or_mutation|no_job_execution|no_checkpoint_creation

## Purpose and invocation

- Input: `chat_handoff [CHAT_NAME]`. Without a name, summarize the current chat; with a name, identify a matching previous chat **inside the current verified ChatGPT Project**.
- This is a generic ChatGPT context-extraction workflow, independent of MCP, repositories, Workspace, Work, task engines or any specific project domain.
- Load this complete file **only** on the explicit `chat_handoff` command. Do not load it for ordinary discussion, implicit continuation, research, GitHub work, workspace selection, or an unrelated session operation.
- Produce a structured **Context Summary** in the current chat, ready to reuse in a new chat. Do not create/open/populate the receiving chat or trigger tools to continue the work.
- Verify source-project membership rather than inferring hidden UI state. If the project or named chat cannot be verified, report the scope/lookup limitation and summarize only actually accessible material.

## Context extraction

1. Identify the current verified project and selected source chat; record title and time range only if actually evidenced.
2. Retrieve accessible original User **and Assistant** messages and authorized conversation-history context. Use direct messages and inspected sources preferentially; supplement with prior summaries only with provenance labels.
3. Reconstruct objectives, user requirements, settled decisions, constraints, relevant outcomes, unfinished steps, blockers and the best next action. Preserve any concrete references already present, such as a repository, document, workspace, job or commit, as **historical context**, not an action to execute.
4. Separate requests, historical Assistant reports and verified outcomes. Note gaps rather than inventing message IDs, attachments, tool receipts, timestamps or a complete transcript.
5. Do not perform live MCP discovery, bind or adopt a workspace, invoke `session_exec`, start jobs, update repositories, create checkpoints, or run verification merely to produce this summary. Other available contextual retrieval may be used only within its own access and project scope.

### Retrieval coverage

- Project chat excerpts and contextual memory are not equivalent to a complete transcript. Original Assistant replies may be accessible through targeted search, but availability varies.
- Show an excerpt count only for entries actually observed: e.g. 22 visible entries means `visible_excerpt_count=22`, not an asserted total of 31.
- Clearly distinguish partial source visibility from genuine complete transcript access.
- Preserve specific original wording when material, but summarize rather than reproducing an entire inaccessible conversation.

### Evidence labels

| Label | Meaning |
| --- | --- |
| `original_message` | Accessible original User or Assistant message |
| `assistant_report` | Historical Assistant claim without its native receipt |
| `context_summary` | Previously condensed conversation context, potentially incomplete |
| `checkpoint` | Previously available structured snapshot, if already present as historical context; no new retrieval |
| `live_verified` | Result already verified from an authoritative source within the visible evidence; include revision/scope/time where available |
| `unknown` | Missing, inaccessible, ambiguous or unverified information |

- Do not relabel a historical test result or deployment assertion `live_verified` unless the actual authoritative evidence is accessible and supports it.
- A later passing targeted test does not establish a subsequent full-suite pass.
- When exact provider receipts are missing, retain their reported values only as `assistant_report` or `context_summary`.

## Output — Context Summary

Render an immediately usable text summary with the **visible heading** `Context Summary`. Use these sections in a compact, actionable format:

1. **Source:** verified project, source chat, accessible date range, retrieval coverage.
2. **Objective:** what the next chat should accomplish.
3. **Decisions & constraints:** agreed architecture, choices and requirements.
4. **Completed work:** outcomes with evidence labels and relevant references.
5. **Open work / next action:** unfinished work and the most useful first step.
6. **Context references:** historical files, repositories, commits, workspace/job IDs or other relevant identifiers, only when known and safe to share.
7. **Verification & gaps:** facts requiring renewed verification, inaccessible content and material uncertainty.
8. **Continuation instruction:** tell the receiving chat to use this context, verify current facts where material, and proceed with the next task under its own available tools, permission gates and applicable instructions.

After **successfully producing** a usable Context Summary, render the exact note **`Previos Context Saved`**. This note means the previous context has been **captured in the visible response for reuse**, not persisted to Memory, a file, another chat or an MCP checkpoint. Do not show the note when no usable summary could be produced.

## Receiving-chat responsibility (not this workflow)

- The new chat interprets the summary based on its current task and tools.
- If an existing authorized MCP Work or Workspace is relevant, the **new chat** may independently discover and bind/reuse it under the current provider contract, explicit cross-chat consent and admission requirements.
- If no MCP Work/Workspace exists or no MCP route is selected, simply continue with the context using available ChatGPT capabilities.
- Do not imply that a context summary itself establishes identity, cross-chat permission, workspace ownership, live job state, deployment or completion.
- No MCP-specific operation or technical owner contract is required by `chat_handoff` itself.

## Safety and completion

- Stay within the current verified project for named source-chat identification; never assume hidden project scope from Memory alone.
- If access is partial, deliver a labeled partial summary and state the missing details.
- Exclude secrets, bearer tokens, authentication material and unnecessary private content.
- The only success condition is a truthful **Context Summary** shown in this chat, with the note `Previos Context Saved` indicating a reusable visible result. No external persistence or follow-on work is claimed.
