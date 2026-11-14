# Chat handoff — two routes: context only or context + Workspace slots

scope: global_chat_handoff_workflow
mode: normative_machine_directives
owner: awa-si/admin/workflow/chat-handoff.md
command_owner: awa-si/admin/command.yaml#chat_handoff
read_when: explicit_chat_handoff_command_only
inherits: awa-si/admin/behavior.yaml|awa-si/admin/command.yaml|applicable_project_deltas
side_effects: default_read_only|explicit_workspace_mode_may_mint_or_consume_authorized_workspace_anchor|no_implicit_MCP|no_job_execution|no_repo_mutation|no_automatic_checkpoint

## Purpose and invocation

- Input: `chat_handoff [CHAT_NAME|list|current|OVERVIEW_NUMBER] [workspace]`. With no argument (or `chat_handoff list`), list discoverable chats in the current verified project as a **Project Chat Overview** and allow the user to select one by title or grounded list reference. Use `chat_handoff current` to summarize the current conversation directly; with a chat name or a valid overview reference, identify that source chat in the verified current project.
- Select exactly one route: **Route 1 — Context only** by default; **Route 2 — Context + Workspace including slots** only when `workspace` is explicitly supplied. Both use the same project chat discovery and context reconstruction. Route 2 adds separately approved AWA slot continuity.
- Load this complete file **only** on the explicit `chat_handoff` command. Do not load it for ordinary discussion, implicit continuation, research, GitHub work, workspace selection, or an unrelated session operation.
- Produce a structured ChatGPT **Context Summary** in the current chat, ready for reuse. Do not create/open/populate the receiving chat or execute its unfinished tasks. Route 2 may transfer server-side slot reservations under independent authorization, preserving existing checkout and jobs.
- Classify project identity as `verified` (explicitly surfaced or independently verified), `inferred` (suggested by context only), or `unknown`. Only `verified` allows claiming a named-chat lookup within that project. Do not silently search across project boundaries.
- If project or named-chat membership cannot be verified, report the limitation. A `current` handoff can still produce a grounded partial summary, but do not substitute an unrelated current-chat summary for an empty or unavailable project-wide listing.
- A reference such as `chat_handoff 2` resolves **only** to a chat in the most recently displayed overview **in this conversation**, if the overview and exact mapping remain available. Otherwise ask for the title or rerun the overview; never guess a list index.

## Route selection — exactly two routes

| Route | Explicit trigger | Behavior |
| --- | --- | --- |
| **1. Context only** | `chat handoff`, `chat handoff list`, `chat handoff current`, or selected chat without `workspace` | Overview when no chat selected; otherwise read-only Context Summary, then stop |
| **2. Context + Workspace including slots** | Selected chat or `current` **with** `workspace` suffix | Same Context Summary **plus** separately approved Workspace and slot handoff/reuse |

- With no source selected, **both routes stop at Project Chat Overview**. Do not inspect or mutate Workspaces from an overview alone.
- An overview-number selection is valid only in the same conversation where the number-to-chat mapping was displayed. Never infer a Workspace request from an earlier listing; the selection must explicitly contain `workspace`.
- The `workspace` suffix selects the route, not approval to adopt an arbitrary other-chat Workspace or change repository state.
- The default route never calls `mcp_model`, `session_exec` or `workspace_exec`.

## Route 1 — Context only

1. Perform same-project chat identification and best-effort context extraction (shared sections below); distinguish verified project membership from inferred context and partial transcripts.
2. Produce **Context Summary** with evidence labels, decisions, completed and pending work, relevant references, gaps and immediate next step.
3. Display **Previous Context Captured** only for a usable visible response, without claiming Memory or other persistence.
4. **Stop.** No MCP discovery, checkpoint creation/reading, Workspace/slot access, jobs, Git mutation or follow-on execution. The receiving chat decides independently how to continue.

## Route 2 — Context + Workspace (including slots)

1. **Context first:** perform the same best-effort chat identification and Context Summary as Route 1. Optionally restore a previously saved `session_exec(handoff)` checkpoint only with an independently available checkpoint credential and authorized provider route. A Session checkpoint restores bounded context notes, never Workspace slot rights.
2. **Identify the existing Workspace and slots:** load applicable Admin MCP route and the current deployed AWA Session/Workspace contracts. Prefer `workspace_exec(operation="session.resolve", payload={"repository":"owner/repo"})` for the current-chat binding; if needed inspect paginated active registry results as discovery evidence. Identify exact Workspace, canonical repository, existing slot(s) and branch/job state. Listing or memory is not authorization.
3. **Prepare from source chat:** `chat handoff current workspace` may invoke `workspace_exec(operation="session.handoff", payload={"workspace_id":"EXISTING", "action":"prepare", "approved":true})` only after current slot ownership, stable chat correlation, explicit consent and provider admission. The result is a **single-use Workspace handoff bearer token** valid for seven days, invalidated by source slot changes. Keep it private; it is distinct from a Session checkpoint token.
4. **Accept in successor chat (valid source token):** with separately approved transfer, a different stable successor conversation correlation, and provider admission, use `workspace_exec(operation="session.handoff", payload={"workspace_id":"EXISTING", "action":"accept", "token":"PRIVATE_WORKSPACE_TOKEN", "approved":true})`. After the server verifies source slots and repository bindings, the source chat's slot reservations move atomically to the successor. Worktrees, uncommitted edits, caches, jobs and environment remain in place; nothing is replayed or restarted.
5. **No source token / exhausted source chat:** do **not** claim a direct slot transfer. Use the guarded repository-first `session.select` procedure after `session.resolve`. Present the specific verified workspace/repository/slot candidate and obtain explicit **reuse / separate / none** consent and independent provider authorization before any binding/provisioning. Reusing a Workspace is not inheriting occupied source slot ownership. Never seize occupied slots or create a Workspace silently.
6. **Verify results separately:** report `context_coverage=complete_verified|partial|unknown` and `workspace_continuity=transferred|reused|already_bound|blocked|not_attempted`. Only report slot transfer or reuse after current native provider receipts, including verified slot reservations, repository HEAD/branch, dirty state, locks and job state. If no Workspace is available or permitted, still deliver Context Summary with the precise blocker.

**Scope and credentials:** Neither route executes jobs, updates Git, cleans worktrees, deploys or replays prior operations. Workspace handoff tokens and Session checkpoint tokens are not interchangeable and must never appear in Context Summary, Memory or public repositories. Route 2 uses current registered provider schema; GitHub documentation alone does not prove deployment. Technical owners: `awa-si/awa@main:mcp/session/contract.md`, `mcp/session/workflow/checkpoint.md`, `mcp/session/workflow/continuity.md`, `mcp/workspace/workflow/session.md` and `reuse.md` as applicable.

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
5. Shared context reconstruction is read-only. Route 1 stops after Context Summary; Route 2 proceeds only to the separately authorized Workspace/slot continuity phase described above. Other context retrieval stays within its own access scope.

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

## Safety and completion

- Restrict project-wide listing and named-chat discovery to the verified project. When project status is inferred or unknown, report the listing blocker; a separate explicit `chat_handoff current` may still produce a grounded current-chat partial summary.
- If access is partial, deliver a labeled partial summary and state the missing details.
- Exclude secrets, bearer tokens, authentication material and unnecessary private content.
- An overview displays **Project Chat Overview** and stops for a source selection. Route 1 ends with a usable **Context Summary** and **Previous Context Captured** (or a truthful blocker). Route 2 adds separately verified Workspace/slot continuity status. Neither route implies destination-chat persistence, job replay or deployment.
