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

## Optional Workspace continuity — successor-chat-first

The normal invocation is **in the receiving chat**:
`chat_handoff CHAT_NAME workspace` (or a selected overview item plus
`workspace`). Plain `chat_handoff` stays independent of MCP and read-only.
The `workspace` suffix opts into the continuity workflow; it is **not**
authorization to reuse an arbitrary foreign Workspace.

1. **Recover context first.** Identify the previous chat within the verified
   project and retrieve accessible original messages and associated context.
   When incomplete, use an already saved and separately accessible
   `session_exec(operation="handoff", payload={"token": ...})` checkpoint
   only with its own valid checkpoint credential and independent provider
   admission. If unavailable, preserve a clearly labeled partial Context
   Summary. This restores bounded v2 context, not the full transcript,
   job state or Workspace permissions. Its token is **different from**
   the Workspace transfer token; never interchange them.
2. **Resolve the work, not the chat ID.** If Workspace continuity was requested
   and the source context identifies a repository or existing Workspace,
   consult the current live MCP contract. Prefer an already authorized
   *current-chat* binding. Otherwise enumerate all active registry pages and
   compare exact canonical repository identities, slot reservations, live
   branch/HEAD, dirty edits and jobs. A chat title, memory, Workspace ID or
   registry listing is discovery evidence, not proof of permission.
3. **Valid source handoff token available:** After explicitly approved
   destination adoption and separate server admission, invoke
   `workspace_exec(operation="session.handoff",
   payload={"workspace_id": "EXISTING", "action": "accept",
   "token": "PRIVATE_SOURCE_WORKSPACE_TOKEN", "approved": true})`.
   This requires a stable session correlation for a **different successor
   chat**, an unexpired source-issued token, matching authorized source
   slots, current live repository binding checks and provider admission.
   On success the server transfers the reserved slots, preserving checkout,
   uncommitted edits, jobs and environment without job replay; the source
   relinquishes the transferred reservations. Verify the returned receipt,
   current-chat slot binding and repository/job state independently.
   Source handoff grants are one-use, expire after **7 days** and are
   invalidated by source-slot changes. Never reconstruct, invent or
   persist a one-use token from historical context.
4. **No source token, including an exhausted source chat:** The original chat
   is **not required** for the recovery path. Use the current canonical
   `workspace_exec(operation="session.resolve", payload={"repository":
   "owner/repo"})` and the current `session.select` repository-first
   protocol to identify any matching foreign Workspace. Present the specific verified workspace/repository/slot
   candidate and obtain the user's explicit **reuse / separate / none**
   choice if not already specifically authorized. Only after this choice
   and independent server authorization may `session.select` bind or
   provision an available slot. This is a **separately authorized reuse**,
   not an `session.handoff` transfer of the previous chat's slot ownership.
   Never automatically seize occupied slots or silently create a Workspace.
5. **Optional source preparation:** `chat_handoff current workspace` in the
   source chat may call `workspace_exec(session.handoff, action="prepare")`
   with `payload={"workspace_id": "EXISTING", "action": "prepare",
   "approved": true}` after verifying that the invoking chat owns the
   source slots, has stable correlation and satisfies provider admission.
   It creates a single-use **Workspace handoff token** for future direct
   slot transfer (not a `session_exec` checkpoint token), but
   **is not a prerequisite** for the normal successor-chat recovery path.
   Re-preparation revokes the previous grant for that source. Never claim
   direct transfer is possible once the source chat is exhausted if it
   did not previously prepare a valid token.
6. **Verify and report separately.** Distinguish
   `context_coverage=complete_verified|partial|unknown` from
   `workspace_continuity=transferred|reused|already_bound|blocked|not_attempted`.
   A source checkpoint (when actually retrieved) should separately report
   `context_checkpoint=restored|unavailable|not_attempted`, never
   `workspace_continuity=transferred`.
   Only claim transfer or reuse after relevant live provider receipts.
   Preserve worktrees, pending edits, jobs and shared environment; never
   replay, restart, reset, clean, push or deploy as a side effect.
7. **Credential boundary.** Never place bearer tokens, credential values or
   authentication secrets in Context Summary, chat overview, repository,
   Memory or a continuation instruction. No secure cross-chat token relay is
   presumed to exist. If no token or authorized selection is available,
   finish with the best grounded Context Summary and state the precise blocker.

For optional MCP use, load the applicable `awa-si/admin/workflow.md`
and `workflow/mcp.md` under routing rules, followed by the current
`awa-si/awa@main:mcp/session/contract.md` and the matching technical workflow:
`mcp/session/workflow/checkpoint.md` for bounded notes,
`mcp/session/workflow/continuity.md` for rights separation, and
`mcp/workspace/workflow/session.md` plus `reuse.md` for slot transfer.
Load only owners applicable to the requested operation. Obtain the
**deployed registered schema** from `mcp_model` and the provider; GitHub
source does not prove deployment or grant authorization.

## Receiving-chat responsibility (not this workflow)

- The receiving chat owns the normal `chat_handoff` execution; it interprets the summary based on its current task and tools. The explicit `workspace` variant may additionally perform the separately authorized recovery or adoption phase above.
- In default mode, relevant existing MCP work remains historical context only. In explicit `workspace` mode, the receiving chat may discover and reuse a matching authorized Workspace with a valid handoff token or the independently approved `session.select` flow.
- If no MCP Work/Workspace exists or no MCP route is selected, simply continue with the context using available ChatGPT capabilities.
- Do not imply that a context summary itself establishes identity, cross-chat permission, workspace ownership, live job state, deployment or completion.
- No MCP-specific operation or technical owner contract is required by **plain** `chat_handoff`; explicit `workspace` mode loads the matching live MCP technical contract.

## Safety and completion

- Restrict project-wide listing and named-chat discovery to the verified project. When project status is inferred or unknown, report the listing blocker; a separate explicit `chat_handoff current` may still produce a grounded current-chat partial summary.
- If access is partial, deliver a labeled partial summary and state the missing details.
- Exclude secrets, bearer tokens, authentication material and unnecessary private content.
- A successful overview produces a truthful **Project Chat Overview** and then waits for selection. A successful selected-chat handoff produces **Context Summary** and `Previous Context Captured` as a reusable visible result. Neither implies external persistence or follow-on work. With explicit `workspace` mode, separately report whether the optional Workspace transfer was verified, blocked, or not attempted.
