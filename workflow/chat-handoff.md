# Chat handoff — same-project continuation

scope: global_chat_handoff_workflow
mode: normative_machine_directives
owner: awa-si/admin/workflow/chat-handoff.md
command_owner: awa-si/admin/command.yaml#chat_handoff
read_when: explicit_chat_handoff_command
inherits: awa-si/admin/behavior.yaml|awa-si/admin/command.yaml|applicable_project_deltas
routing_owner: awa-si/admin/workflow.md#routing_decision_order_when_MCP_or_repository_execution_is_material
side_effects: read_only|do_not_create_or_adopt_workspace|do_not_run_jobs|do_not_create_checkpoint_unless_separately_requested

## Intent and scope

- Input: `chat_handoff [CHAT_NAME]`; no name means the current chat, unless the user explicitly identifies a prior conversation.
- Output: a structured, self-contained continuation message for a **new** chat in the same **verified** ChatGPT Project.
- Confirm the active project is actually exposed or verifiable; never infer project membership from the chat title, memory or a guessed UI state.
- With a name, find the best verified title match **within that project**; if multiple material matches remain, disambiguate. Do not silently search outside the current project.
- Do not use a summary of another project's conversation to claim that it belongs to this project. When the project or chat cannot be verified, say exactly what is available and what is blocked.
- The response is a handoff document, not proof that a new chat already received it, read it or acquired workspace permission.

## Context-first reconstruction

1. Identify project and source chat; record verified title and date range only when actually available.
2. Read accessible original messages in chronological order and any authorized conversation-history results. Prefer direct original User **and Assistant** messages and inspected sources over summaries.
3. Use relevant past context or summaries to fill gaps, but preserve provenance. Targeted retrieval can surface Assistant messages; availability is not guaranteed and differs by session/tool.
4. Determine scope and completeness from **what was actually returned**, not what was inferred from a title, Memory, a history summary or an assistant claim.
5. Reconcile objectives, user decisions, constraints, completed steps, pending work and blockers. Separate requested changes from executed and verified outcomes.
6. Collect references needed to resume: repository/branch/commit, changed files, workspace ID/slot, jobs, tests and checkpoint presence, **only if visible or independently verified**.
7. Do not spend time on exhaustive discovery when a bounded, useful handoff can be produced. Never invent missing messages, tool calls, timestamps or receipts.

### Source granularity and counting

- Distinguish a project-conversation excerpt, targeted context results, historical context summary and complete inspected transcript. Memory is not a full transcript.
- Original User entries can be shown without intervening Assistant replies; targeted search **may** supply some Assistant replies. Neither implies full access to message IDs, arbitrary message lookup, attachments or original tool-call receipts.
- For an excerpt, count only entries **actually visible** and label them `visible_excerpt_count`. Do not claim a larger total unless the actual source proves it.
- When a source says “31 messages” but the actual list has 22, use “22 visible entries; total unknown” rather than silently retaining or extrapolating 31.
- Quote excerpts accurately; treat historical Assistant assertions about test runs, deployments and status as reports, not independently verified provider receipts.

### Evidence classification

| Label | Meaning | Safe conclusion |
| --- | --- | --- |
| `original_message` | Directly retrieved or present User/Assistant message | Message exists in accessible context; the stated action may still be unverified |
| `assistant_report` | Earlier Assistant-reported result, without original provider receipt | Historically reported, **not** live verified |
| `context_summary` | Condensed past-conversation or memory-derived context | Supporting context; may omit detail and change chronology |
| `checkpoint` | Structured `session_exec` snapshot returned through authorized handoff | Restored state/hints, **not** job ownership, permission or live reality |
| `live_verified` | Newly inspected authoritative GitHub/MCP/Workspace result or native receipt | Current only for the observed revision, time and scope |
| `unknown` | Missing, inaccessible, ambiguous or unsupported fact | State precisely what is unavailable |

- Record evidence labels next to consequential facts, including test counts and deployment claims. A historical report such as “3,975 passed / 1 failed / 35 skipped” must not be upgraded to `live_verified` without a fresh receipt.
- If a targeted test passed after a failed full suite, do not imply a full-suite rerun or clean overall pass unless verified.
- Store source references when supported; never invent message IDs, source links, tool results or immutable receipts.

## Checkpoint fallback and workspace continuation

1. **Context first:** use the project-scoped chat material to produce the most complete legitimate handoff possible.
2. **Checkpoint fallback:** if important state remains missing and a valid user-supplied or otherwise authorized token exists, consult the selected, permitted MCP session contract. `session_exec(operation="handoff", payload={"token": TOKEN})` restores bounded structured notes. No token or authorization means no automatic lookup or checkpoint creation.
3. **Live workspace verification in the new chat:** retrieve the current authoritative GitHub HEAD and relevant MCP Workspace/Work job receipts before declaring the past work current. The source chat's workspace reference is a **candidate**, not adoption permission.
4. Follow the current AWA owners only when MCP is explicitly selected/permitted: `awa-si/awa:mcp/session/README.md`, `mcp/workspace/contract.md`, `mcp/workspace/workflow/session.md`, `mcp/workspace/workflow/reuse.md`. Discover current schemas via the live MCP provider; do not pin schemas in Admin.
5. For Workspace reuse, resolve the new chat's existing binding first, then inspect eligible registry candidates; cross-chat adoption requires the user's **explicit reuse/separate/none choice**, current server authorization, repository and slot compatibility, branch/dirty-state/job/lock checks. Never silently import, fork, overwrite or create a duplicate.
6. Workspace jobs, DBOS Work and Task execution have independent owner contracts and receipts; a checkpoint cannot grant permission, restart them or replay side effects.
7. Protect bearer handoff tokens: do not place them in public repositories, summaries shared beyond the authorized user, or logs. An unknown token cannot be recovered from workspace listings; checkpoint creation does not run automatically just because the chat nears its context limit.

## Output contract — paste-ready new-chat brief

Produce one coherent handoff with these headings:

1. `PROJECT_AND_SOURCE_CHAT`: verified project, chat title, accessible time range and retrieval scope (partial/full/unknown).
2. `CONTINUATION_OBJECTIVE`: what should be done next and what success means.
3. `DECISIONS_AND_CONSTRAINTS`: settled design, explicit user requirements, authorization and safety boundaries.
4. `COMPLETED_WITH_EVIDENCE`: completed tasks separated from requested tasks; cite available evidence labels and receipts.
5. `OPEN_WORK_AND_NEXT_ACTION`: highest-priority unfinished task and bounded immediate next step.
6. `REPOSITORY_AND_WORKSPACE_REFERENCES`: source repository, branch, revisions, workspace/slot/job IDs **if known**; avoid secrets.
7. `LIVE_REVALIDATION_REQUIRED`: exact GitHub, session, workspace, job and test status checks needed in the new chat.
8. `CONTEXT_GAPS`: unread chat portions, unverified results, missing provenance, inaccessible attachments and ambiguous state.

End with a concise **instruction to the receiving chat** to verify current Admin/project instructions and live execution state, reuse existing authorized workspace where possible, avoid duplicative jobs/checkpoints and continue only the next unfinished goal. Keep enough specific information to act; do not paste a speculative transcript.

## Failure and safety gates

- When the project boundary, target chat or history access is unavailable, produce a labeled **partial handoff** using only actually available context; clearly report the blocker rather than implying a complete project search.
- Never present conversation-memory summaries or chat excerpts as proof of live repository state, committed code, deployed MCP revision, successful tests or authorized workspace ownership.
- This command prepares a *textual* handoff only. It neither changes ChatGPT project membership nor creates, resumes, binds, releases or executes a Workspace. Those are separate, authorized operations in the receiving chat.
