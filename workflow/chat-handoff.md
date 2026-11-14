# Chat handoff — context summary with optional Workspace continuity

scope: global_chat_handoff_workflow
mode: normative_machine_directives
owner: awa-si/admin/workflow/chat-handoff.md
command_owner: awa-si/admin/command.yaml#chat_handoff
read_when: explicit_chat_handoff_command_only
inherits: awa-si/admin/behavior.yaml|awa-si/admin/command.yaml|applicable_project_deltas
side_effects: default_read_only|explicit_workspace_mode_may_mint_or_consume_authorized_workspace_anchor|no_implicit_MCP|no_job_execution|no_repo_mutation|no_automatic_checkpoint

## Purpose and invocation

- Input: `chat_handoff [CHAT_NAME|list|current|OVERVIEW_NUMBER] [workspace]`. With no argument (or `chat_handoff list`), list discoverable chats in the current verified project as a **Project Chat Overview** and allow the user to select one by title or grounded list reference. Use `chat_handoff current` to summarize the current conversation directly; with a chat name or a valid overview reference, identify that source chat in the verified current project.
- Base mode is a generic ChatGPT context-extraction workflow independent of MCP, repositories, Workspace, Work, task engines or any specific project domain. The explicit optional `workspace` suffix adds a separately authorized continuity phase only when a matching AWA Workspace exists.
- Load this complete file **only** on the explicit `chat_handoff` command. Do not load it for ordinary discussion, implicit continuation, research, GitHub work, workspace selection, or an unrelated session operation.
- Produce an ordinary **structured ChatGPT response** titled **Context Summary** in the current chat, ready to reuse in a new chat. Do not create/open/populate the receiving chat or trigger tools to continue the work. Explicit Workspace continuity may only transfer the existing workspace authorization anchor, not execute the previous task.
- Classify project identity as `verified` (explicitly surfaced or independently verified), `inferred` (suggested by context only), or `unknown`. Only `verified` allows claiming a named-chat lookup within that project. Do not silently search across project boundaries.
- If project or named-chat membership cannot be verified, report the limitation. A `current` handoff can still produce a grounded partial summary, but do not substitute an unrelated current-chat summary for an empty or unavailable project-wide listing.
- A reference such as `chat_handoff 2` resolves **only** to a chat in the most recently displayed overview **in this conversation**, if the overview and exact mapping remain available. Otherwise ask for the title or rerun the overview; never guess a list index.

## Project Chat Overview — first step

1. Determine whether a trustworthy, authorized **project-scoped conversation listing** is actually available. List every chat returned within the confirmed current project. Follow pagination where supported; do not infer entries from Memory, summaries or unrelated project context.
2. Show a compact **Project Chat Overview** with stable-for-this-response ordinal references, titles and relevant last activity dates **only when verified**. Make the list easy to select by `chat_handoff <number>` or `chat_handoff <CHAT_NAME>`. Never fabricate titles, counts or dates.
3. Mark completeness as `complete_verified` **only** if the listing provider confirms exhaustive results (including all pages). Otherwise mark `partial` and state that the overview contains only discoverable chats, not necessarily all project chats.
4. If a successfully completed authoritative project listing returns zero chats, display the exact result **`Nothing found`** and no fabricated entries. If there is no supported listing capability, authorization fails or a listing is incomplete, report **`Project chat listing unavailable`** or **`Partial results`**, not `Nothing found`. Absence of results in Memory or targeted search is not proof the project has no chats.
5. Stop after the overview and await the user's selection, even when `workspace` is supplied; do not preemptively read all transcripts, generate summaries for every chat, or perform MCP/Workspace operations from an overview.
6. After the user selects an item, confirm the selection refers to a discoverable chat in the same project; read available context and produce the individual Context Summary below. Preserve overview references within the active conversation only, not across new chats or sessions.

## Context extraction

Use `resolve_chat → retrieve_available_context → assess_coverage → summarize` as a **best-effort workflow**, not a guaranteed chat-transcript API.

1. Identify project status and the selected source chat from the overview, verified title or explicit `current` option; record title and time range only if actually evidenced. For named chat lookup, prefer verified exact title, then an unambiguous verified close match; disambiguate material collisions.
2. Retrieve accessible original User **and Assistant** messages and authorized conversation-history context. Use direct messages and inspected sources preferentially; supplement with prior summaries only with provenance labels.
3. Reconstruct objectives, user requirements, settled decisions, constraints, relevant outcomes, unfinished steps, blockers and the best next action. Preserve any concrete references already present, such as a repository, document, workspace, job or commit, as **historical context**, not an action to execute.
4. Separate requests, historical Assistant reports and verified outcomes. Note gaps rather than inventing message IDs, attachments, tool receipts, timestamps or a complete transcript.
5. In default mode do not perform live MCP discovery, bind or adopt a workspace, invoke `session_exec`, start jobs, update repositories, create checkpoints, or run verification merely to produce this summary. In explicitly requested `workspace` mode follow the separately gated Workspace continuity section below, after context extraction; no execution or repository mutation. Other available contextual retrieval may be used only within its own access and project scope.

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

## Output — selected-chat Context Summary

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

## Optional Workspace continuity — explicit `workspace` suffix

This is the only coupling point between ChatGPT `chat_handoff` and AWA MCP
`workspace_exec(session.anchor|session.handoff)`. It is **opt-in**, must use
the current live MCP schema and canonical Workspace session contract, and never
changes the behavior of plain `chat_handoff`.

1. **Context first:** Read available authorized original User and Assistant
   messages and project context. If incomplete, supplement with an **already
   available**, valid `session_exec(handoff)` checkpoint only when a
   checkpoint credential is independently available and its separate
   invocation is authorized. If no credential or live `session_exec`
   capability exists, use the partial summary. Do not claim ChatGPT has a
   guaranteed full-transcript API or automatically create a checkpoint.
2. **Source preparation:** Only for `chat_handoff current workspace`, after
   a usable Context Summary and a verified current-chat Workspace reservation,
   use the current exposed `workspace_exec` contract to call
   `session.anchor` with explicit user intent and provider admission.
   It returns a **single-use Workspace bearer token** for slots owned by
   this chat. If the request does not explicitly select Workspace continuity,
   do not mint it. An optional existing context checkpoint remains separate.
3. **Destination adoption:** Only for `chat_handoff CHAT_NAME workspace`
   or a selected overview item with the `workspace` suffix, after a usable
   Context Summary, independently resolve the target Workspace and a valid
   source-issued Workspace anchor supplied by the user or a separately
   authorized secure handoff channel. Require explicit destination consent,
   the current MCP's server-side admission, and live repository-binding checks
   before `workspace_exec(session.handoff)`. Do not infer a token from a chat
   title, Workspace ID, memory, checkpoint, or Git metadata.
4. **No source anchor:** Keep the Context Summary useful and report
   `workspace_continuity=not_transferred` with its exact reason. Do not
   fabricate a transfer or silently allocate a new slot. The separately
   authorized `session.select` cross-chat reuse/recovery flow may be
   described, but is not implicitly executed.
5. **Successful transfer:** Inspect authorized live slot ownership, repository
   branch/HEAD/dirty state and native job status. Keep previous jobs in place;
   do not restart, replay, reset, clean, push or deploy. Report independently
   `context_coverage` and `workspace_continuity=verified` only on provider
   receipts and relevant live verification.
6. **Credential handling:** Never place raw bearer tokens in a Context Summary,
   project overview, file, repository, Memory, or a reusable continuation
   instruction. Keep any source token in an authorized private credential
   transfer channel under the provider contract. Do not pretend such a channel
   exists if unavailable. Do not confuse `session_exec` context-checkpoint
   tokens with `workspace_exec` Workspace-transfer tokens.

For the optional MCP phase, load `awa-si/admin/workflow.md` and
`workflow/mcp.md` as applicable, and the current
`awa-si/awa:mcp/workspace/contract.md` and `workflow/session.md`
technical owner; verify the **deployed** registered operation, not only a
GitHub commit. If unsupported or unadmitted, finish with context-only output.
This workflow supplies no standing authorization for other MCP operations.

## Receiving-chat responsibility (not this workflow)

- The new chat interprets the summary based on its current task and tools; the explicit `workspace` variant may also perform the independently authorized adoption phase above.
- In default mode, if an authorized MCP Work or Workspace is relevant, the **new chat** may independently discover and bind/reuse it under the provider contract. Only explicit `workspace` mode couples the authorized Workspace anchor and handoff steps to this workflow.
- If no MCP Work/Workspace exists or no MCP route is selected, simply continue with the context using available ChatGPT capabilities.
- Do not imply that a context summary itself establishes identity, cross-chat permission, workspace ownership, live job state, deployment or completion.
- No MCP-specific operation or technical owner contract is required by **plain** `chat_handoff`; explicit `workspace` mode loads the matching live MCP technical contract.

## Safety and completion

- Restrict project-wide listing and named-chat discovery to the verified project. When project status is inferred or unknown, report the listing blocker; a separate explicit `chat_handoff current` may still produce a grounded current-chat partial summary.
- If access is partial, deliver a labeled partial summary and state the missing details.
- Exclude secrets, bearer tokens, authentication material and unnecessary private content.
- A successful overview produces a truthful **Project Chat Overview** and then waits for selection. A successful selected-chat handoff produces **Context Summary** and `Previous Context Captured` as a reusable visible result. Neither implies external persistence or follow-on work. With explicit `workspace` mode, separately report whether the optional Workspace transfer was verified, blocked, or not attempted.
