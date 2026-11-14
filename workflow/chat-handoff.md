# Chat handoff — generic context summary

scope: global_chat_handoff_workflow
mode: normative_machine_directives
owner: awa-si/admin/workflow/chat-handoff.md
command_owner: awa-si/admin/command.yaml#chat_handoff
read_when: explicit_chat_handoff_command_only
inherits: awa-si/admin/behavior.yaml|awa-si/admin/command.yaml|applicable_project_deltas
side_effects: read_only|no_MCP_binding|no_workspace_access_or_mutation|no_job_execution|no_checkpoint_creation

## Purpose and invocation

- Input: `chat_handoff [CHAT_NAME]`. Without a name, summarize the current chat; with a name, identify an accessible matching prior chat **inside the verified current ChatGPT Project**.
- This is a generic ChatGPT context-extraction workflow, independent of MCP, repositories, Workspace, Work, task engines or any specific project domain.
- Load this complete file **only** on the explicit `chat_handoff` command. Do not load it for ordinary discussion, implicit continuation, research, GitHub work, workspace selection, or an unrelated session operation.
- Produce an ordinary **structured ChatGPT response** titled **Context Summary** in the current chat, ready to reuse in a new chat. Do not create/open/populate the receiving chat or trigger tools to continue the work.
- Classify project identity as `verified` (explicitly surfaced or independently verified), `inferred` (suggested by context only), or `unknown`. Only `verified` allows claiming a named-chat lookup within that project. Do not silently search across project boundaries.
- If project or named-chat membership cannot be verified, report the limitation, but still produce a grounded, labeled partial handoff from the current chat or material independently known to be in scope. Do not fail needlessly.

## Context extraction

Use `resolve_chat → retrieve_available_context → assess_coverage → summarize` as a **best-effort workflow**, not a guaranteed chat-transcript API.

1. Identify project status and source chat; record title and time range only if actually evidenced. For named chat lookup, prefer verified exact title, then an unambiguous verified close match; disambiguate material collisions.
2. Retrieve accessible original User **and Assistant** messages and authorized conversation-history context. Use direct messages and inspected sources preferentially; supplement with prior summaries only with provenance labels.
3. Reconstruct objectives, user requirements, settled decisions, constraints, relevant outcomes, unfinished steps, blockers and the best next action. Preserve any concrete references already present, such as a repository, document, workspace, job or commit, as **historical context**, not an action to execute.
4. Separate requests, historical Assistant reports and verified outcomes. Note gaps rather than inventing message IDs, attachments, tool receipts, timestamps or a complete transcript.
5. Do not perform live MCP discovery, bind or adopt a workspace, invoke `session_exec`, start jobs, update repositories, create checkpoints, or run verification merely to produce this summary. Other available contextual retrieval may be used only within its own access and project scope.

### Retrieval coverage

- Project chat excerpts and contextual memory are not equivalent to a complete transcript. Original Assistant replies may be accessible through targeted search, but availability varies.
- Show an excerpt count only for entries actually observed: e.g. 22 visible entries means `visible_excerpt_count=22`, not an asserted total of 31.
- Classify coverage as `complete_verified` only when the complete source transcript is demonstrably accessible; otherwise `partial` or `unknown`. Distinguish partial excerpts from full access.
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

Produce a normal structured ChatGPT response with the visible Markdown heading `Context Summary`. Do not claim to render a native persistent UI element. Adapt detail to the source:

- **Short/simple:** Source, Objective, Decisions, Next Action. Omit empty headings.
- **Long/substantial:** Source/Coverage, Objective, Decisions & Constraints, Completed Work with evidence, Open Work / Next Action, References, Verification & Gaps, Continuation Instruction.
- **Partial or uncertain:** Include project status `verified|inferred|unknown`, coverage `complete_verified|partial|unknown`, material evidence labels and missing context.
- **Technical/development:** Include grounded repository/branch/commits, known workspace/slot/job references, tests and affected files. Do not execute or invent evidence.

Conclude with an instruction that the receiving chat treats this as historical context, reloads applicable current rules and verifies any material live state under its own authorization.

After a **usable** Context Summary is visible, render the exact note:

**Previous Context Captured**

*Context Summary generated in this chat. Ready to reuse in a new conversation.*

The note describes **visible response capture only**. It does not assert storage in Memory, a file, an MCP checkpoint or another chat. If no usable summary was produced, omit the note and report the blocker.

## Receiving-chat responsibility (not this workflow)

- The new chat interprets the summary based on its current task and tools.
- If an existing authorized MCP Work or Workspace is relevant, the **new chat** may independently discover and bind/reuse it under the current provider contract, explicit cross-chat consent and admission requirements.
- If no MCP Work/Workspace exists or no MCP route is selected, simply continue with the context using available ChatGPT capabilities.
- Do not imply that a context summary itself establishes identity, cross-chat permission, workspace ownership, live job state, deployment or completion.
- No MCP-specific operation or technical owner contract is required by `chat_handoff` itself.

## Safety and completion

- Restrict named-chat discovery to the verified project. When project status is inferred or unknown, avoid cross-project lookup and retain a useful, labeled current-chat partial summary where possible.
- If access is partial, deliver a labeled partial summary and state the missing details.
- Exclude secrets, bearer tokens, authentication material and unnecessary private content.
- The only success condition is a truthful **Context Summary** shown in this chat, with `Previous Context Captured` marking a reusable visible result. No external persistence or follow-on work is claimed.
