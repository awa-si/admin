# Chat handoff — two routes: context only or context + Workspace slots

scope: global_chat_handoff_workflow
mode: normative_machine_directives
owner: awa-si/admin/workflow/chat-handoff.md
command_owner: awa-si/admin/command.yaml#chat_handoff
read_when: explicit_chat_handoff_command_only
inherits: awa-si/admin/behavior.yaml|awa-si/admin/command.yaml
side_effects: default_read_only|explicit_workspace_mode_may_transfer_single_owner_source_slots|no_implicit_MCP|no_job_execution|no_repo_mutation|checkpoints_suspended

## Purpose and invocation

- Input: `chat_handoff [CHAT_NAME|list|current|OVERVIEW_NUMBER] [workspace]`. With no argument (or `chat_handoff list`), list discoverable chats in the current verified project as a **Project Chat Overview** and allow the user to select one by title or grounded list reference. Use `chat_handoff current` to summarize the current conversation directly; with a chat name or a valid overview reference, identify that source chat in the verified current project.
- Select exactly one route: **Route 1 — Context only** by default; **Route 2 — Context + Workspace including slots** only when `workspace` is explicitly supplied. Both use the same project chat discovery and context reconstruction. Route 2 attempts provider-authorized automatic transfer of existing Workspace slots.
- Load this complete file **only** on the explicit `chat_handoff` command. Do not load it for ordinary discussion, implicit continuation, research, GitHub work, workspace selection, or an unrelated session operation.
- Produce a **short Context Summary based only on the last 5–10 accessible source-chat interactions**, ready for reuse. Do not create/open/populate the receiving chat or execute its unfinished tasks. Route 2 may transfer server-side slot reservations under independent authorization, preserving existing checkout and jobs.
- Classify project identity as `verified` (explicitly surfaced or independently verified), `inferred` (suggested by context only), or `unknown`. Only `verified` allows claiming a named-chat lookup within that project. Do not silently search across project boundaries.
- If project or named-chat membership cannot be verified, report the limitation. A `current` handoff can still produce a grounded partial summary, but do not substitute an unrelated current-chat summary for an empty or unavailable project-wide listing.
- A reference such as `chat_handoff 2` resolves **only** to a chat in the most recently displayed overview **in this conversation**, if the overview and exact mapping remain available. Otherwise ask for the title or rerun the overview; never guess a list index.

## Route selection — exactly two routes

| Route | Explicit trigger | Behavior |
| --- | --- | --- |
| **1. Context only** | `chat handoff`, `chat handoff list`, `chat handoff current`, or selected chat without `workspace` | Overview when no chat selected; otherwise read-only Context Summary, then stop |
| **2. Context + Workspace including slots** | Selected chat or `current` **with** `workspace` suffix | Same Context Summary **plus** verified automatic Workspace slot adoption |

- With no source selected, **both routes stop at Project Chat Overview**. Do not inspect or mutate Workspaces from an overview alone.
- An overview-number selection is valid only in the same conversation where the number-to-chat mapping was displayed. Never infer a Workspace request from an earlier listing; the selection must explicitly contain `workspace`.
- The `workspace` suffix requests Workspace continuity; provider admission and the existing MCP gateway/provider authorization boundary remain mandatory.
- The default route never calls `mcp_model`, `session_exec` or `workspace_exec`.

## Route 1 — Context only

1. Perform same-project chat identification and read only the latest 5–10 accessible interactions using the shared extraction limit below; distinguish verified project membership from inferred context and partial transcripts.
2. Produce **Context Summary** with evidence labels, decisions, completed and pending work, relevant references, gaps and immediate next step.
3. Display **Previous Context Captured** only for a usable visible response, without claiming Memory or other persistence.
4. **Stop.** No MCP discovery, checkpoint creation/reading, Workspace/slot access, jobs, Git mutation or follow-on execution. The receiving chat decides independently how to continue.

## Route 2 — Context + Workspace (including slots)

1. Recover only the same most recent 5–10 accessible source-chat interactions
   used in Route 1. Historical context is not an MCP access credential.
2. Resolve the existing Workspace ID from grounded recent context or current
   provider evidence. Do not invent the mapping from ChatGPT title to the AWA
   correlation digest. The destination is the invoking MCP conversation.
3. For an operator-verified **single-owner MCP**, call
   `workspace_exec(operation="session.handoff", payload={"workspace_id":"EXISTING", "approved":true})`.
   The MCP resolves the only other slot-holding conversation automatically.
   If multiple sources are present, use an exact independently grounded
   `source_conversation_id` selector; never guess from title or recency.
   If the old chat is inaccessible or has reached the ChatGPT context limit,
   use `workspace_exec(operation="session.handoff_candidates",
   payload={"workspace_id":"EXISTING"})` to obtain read-only slot-owner groups.
   Report each candidate's `source_slot`, `source_ref`, slots and repositories
   without claiming it corresponds to a ChatGPT title. Request selection of
   one group and transfer only with `session.handoff` using `approved=true`,
   the selected `source_slot` and matching `source_ref`. The pair prevents
   switching to a different source owner if a slot is reassigned. Source title
   verification is not supplied by a slot candidate; preserve that uncertainty.
**Unreserved imported slot (same Route 2, not a legacy transfer):** If the
requested Workspace has an imported repository but
`session.handoff_candidates` has no source groups, distinguish a current-chat
reservation (`current_slots` nonempty) from an unreserved slot (registry has
no `session_slots` reservations). Do not invent a source conversation or
call `session.handoff` with fabricated selectors. Only when exactly one
imported repository is bound to the sole primary slot, explicit `workspace`
suffix requests continuity, and the provider independently admits the
operation, use the separately registered
`workspace_exec(operation="session.adopt_unreserved", payload={
"workspace_id": "EXISTING", "repository": "owner/repo",
"expected_head": "FULL_VERIFIED_HEAD", "approved": true})`.
Read the current live operation schema and Git HEAD first. This opt-in,
atomic **reservation**, unlike a handoff, transfers no source-chat slots;
preserve the existing worktree, dirty changes, jobs, and environment. Verify
`session.resolve` from the current chat and live Workspace repository
context before reporting `adopted` or `already_bound`. Existing foreign
reservations, multiple slots, active jobs, mismatched repository/HEAD,
uncertain authorization or missing provider capability must fail closed.
Never claim source-chat identity or recovered transcript from an unreserved
repository. Technical owner:
`awa-si/awa:mcp/workspace/workflow/session.md`.

4. The backend relies on the existing MCP gateway authentication and
   provider admission; no additional handoff-specific environment switch is
   required. It validates live Git bindings and atomically transfers all
   source-chat reservations within the Workspace to the current chat.
   Existing destination slots remain; worktrees, dirty state, jobs and
   environment are untouched.
5. Verify the destination's actual slot reservations and native Workspace
   receipt. Report `transferred|adopted|already_bound|ambiguous|blocked|not_found`
   without claiming success from an unavailable or unverified provider.
   A different source-chat owner or shared MCP ingress must fail closed.
6. The transfer covers **one Workspace per call**; it is not an atomic
   cross-Workspace transfer. Do not start jobs, re-import repositories, clean
   worktrees, restart services or replay unfinished tasks.

**Checkpoint suspended:** `session_exec` checkpoint code and historical
records remain in MCP but are disabled by default and are not used by either
route, including MCP self-update. No prepare/accept handshake, bearer token,
signed assertion or external ChatGPT identity bridge participates in the
normal Workspace handoff.

## Project Chat Overview — first step

1. Determine whether a trustworthy, authorized **project-scoped conversation listing** is actually available. List every chat returned within the confirmed current project. Follow pagination where supported; do not infer entries from Memory, summaries or unrelated project context.
2. Show a compact **Project Chat Overview** with stable-for-this-response ordinal references, titles and relevant last activity dates **only when verified**. Make the list easy to select by `chat_handoff <number>` or `chat_handoff <CHAT_NAME>`. Never fabricate titles, counts or dates.
3. Mark completeness as `complete_verified` **only** if the listing provider confirms exhaustive results (including all pages). Otherwise mark `partial` and state that the overview contains only discoverable chats, not necessarily all project chats.
4. If a successfully completed authoritative project listing returns zero chats, display the exact result **`Nothing found`** and no fabricated entries. If there is no supported listing capability, authorization fails or a listing is incomplete, report **`Project chat listing unavailable`** or **`Partial results`**, not `Nothing found`. Absence of results in Memory or targeted search is not proof the project has no chats.
5. Stop after the overview and await the user's selection, even when `workspace` is supplied; do not preemptively read all transcripts, generate summaries for every chat, or perform MCP/Workspace operations from an overview.
6. After the user selects an item, confirm the selection refers to a discoverable chat in the same project; read available context and produce the individual Context Summary below. Preserve overview references within the active conversation only, not across new chats or sessions.

## Context extraction

Use `resolve_chat → retrieve_last_5_to_10_interactions → assess_coverage → summarize` as a **bounded best-effort workflow**, not a guaranteed chat-transcript API.

### Summary window — hard limit

- The Context Summary is based **only on the latest 5–10 interactions of the selected source chat** (prefer 10 if available; otherwise use all available up to 10). An interaction is one user turn and its associated Assistant response(s), not an arbitrary number of individual messages or tool calls.
- Apply the limit to **source conversation content**, not the current chat's tool-operation messages. Do not expand the summary with older original messages, historical Memory or earlier chat summaries, even if they are accessible.
- If the retrieval API supplies fewer than 5 complete interactions, summarize the available recent interactions, label the lower count and do not extrapolate missing turns. If chronology cannot be established, label the selection/window uncertain; do not assert they are the most recent.
- Include an earlier decision, commit, file, reference or unfinished task **only when it is explicitly visible within the selected recent window**. Older state may independently inform Route 2 live Workspace resolution but must **not** be silently injected into the Context Summary.
- Record `interaction_window=last_N_accessible` and `window_coverage=verified_recent|partial|unknown` where evidence permits. These describe the 5–10 interaction window, **not** completeness of the source chat.
- Treat the summary as a compact recent-state delta; never assert that it represents the entire historical chat or permanently removes old context from ChatGPT.


1. Identify project status and the selected source chat from the overview, verified title or explicit `current` option; record title and time range only if actually evidenced. For named chat lookup, prefer verified exact title, then an unambiguous verified close match; disambiguate material collisions.
2. Retrieve the most recent accessible original User **and Assistant** turns within the 5–10 interaction window; use direct messages preferentially. A contextual summary may identify missing chronology, but must not contribute substantive claims from outside the window.
3. Extract only objectives, decisions, constraints, completed work, blockers and next action **that occur or are restated in the selected recent window**; carry repository/document/workspace/job/commit references only when present there. Mark them historical context, not instructions to execute.
4. Separate requests, historical Assistant reports and verified outcomes. Note gaps rather than inventing message IDs, attachments, tool receipts, timestamps or a complete transcript.
5. Shared context reconstruction is read-only. Route 1 stops after Context Summary; Route 2 proceeds only to the separately authorized Workspace/slot continuity phase described above. Other context retrieval stays within its own access scope.

### Retrieval coverage

- Project chat excerpts and contextual memory are not equivalent to a complete transcript. The handoff deliberately excludes older interactions; it is a **recent-context snapshot**, not a full-history reconstruction.
- Show an excerpt count only for entries actually observed: e.g. 22 visible entries means `visible_excerpt_count=22`, not an asserted total of 31.
- Classify the **selected window** as `verified_recent`, `partial` or `unknown`; never label an excerpt `complete_verified` for the entire source transcript. Distinguish recent-window coverage from total-chat coverage.
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
- **Long/substantial:** Still summarize **only the latest 5–10 interactions**; include Source/Window Coverage, Objective, Decisions & Constraints, Recent Completed Work, Next Action, References and material gaps in compact form.
- **Partial or uncertain:** Include project status `verified|inferred|unknown`, `interaction_window` and window coverage `verified_recent|partial|unknown`, material evidence labels and missing recent turns.
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
- An overview displays **Project Chat Overview** and stops for a source selection. Route 1 ends with a **recent 5–10-interaction Context Summary** and **Previous Context Captured** (or a truthful blocker). Route 2 adds separately verified Workspace/slot continuity status. Neither route implies destination-chat persistence, job replay or deployment.
