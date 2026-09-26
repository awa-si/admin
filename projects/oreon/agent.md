# OREON — AGENT

> Mandatory AI operating rules for navigating, reading, editing and verifying the OREON repository.

**File:** `agent.md`  
**Owner:** OREON repository operating rules  
**Scope:** Repository navigation, canonical ownership, evidence use, editing, verification and document-control conventions  
**Status:** Canonical  
**Version:** 3.2  
**AI Instruction:** Read this file first in every OREON project conversation. Apply its repository rules; do not use it as an owner of business, product, counterparty, research or execution facts.  
**Last Write:** 2026-09-18  
**SHA:** tracked in `index.md`

---

## 01 — Initialization

At the beginning of every new OREON project conversation:

1. read `agent.md` in full;
2. read `index.md` in full;
3. use `index.md` only to locate the narrowest canonical owner and its current blob state;
4. read that owner in full;
5. read only dependencies materially required by the task;
6. verify current GitHub `main` before relying on or editing repository content.

Repository files are persistent project truth. Chat is the task workspace.

### Canonical repository

```text
Repository: awa-si/oreon
Branch:     main
Root:       /
Canonical:  github://awa-si/oreon@main/
```

Use the authenticated GitHub repository interface when available. Do not substitute local/container copies, cached content or unauthenticated public-web views for canonical GitHub `main`.

---

## 02 — Authority & Canonical Ownership

For project-specific work use this precedence:

1. explicit current user instruction;
2. applicable authoritative external law/regulation where it controls;
3. current canonical OREON owner file;
4. other directly referenced OREON dependencies;
5. general knowledge or inference.

`index.md` is a map, not a substantive owner.

### Canonical-owner rule

> **Define once in the owner; reference or consume downstream.**

Use the narrowest file that owns the concept. A downstream summary, template, status file, presentation or concrete execution record does not redefine its upstream standard.

If owner files conflict:

1. identify the conflict;
2. apply the authority order;
3. preserve uncertainty where unresolved;
4. do not silently merge incompatible rules.

---

## 03 — Canonical File Metadata

Every canonical Markdown file in the OREON repository must begin with a self-describing metadata block immediately after the title and one-line purpose statement.

Canonical form:

```md
# OREON — <Title>

> <one-line purpose>

**File:** `<repo-relative path>`
**Owner:** <canonical concept owned by this file>
**Scope:** <owned boundary; what this file is responsible for>
**Status:** <Canonical | Active | Template | Evidence | State | ...>
**Version:** <document version>
**AI Instruction:** <short imperative instruction describing how AI must use this file>
**Last Write:** YYYY-MM-DD
**SHA:** tracked in `index.md`

---
```

Rules:

- metadata belongs at the **start of the file**, never only at the end;
- do not duplicate the metadata in a trailing `Document Control` section;
- `Owner` answers **what concept this file canonically owns**;
- `Scope` defines the boundary of that ownership;
- `AI Instruction` tells an AI how to consume or edit the file and must be concise, normative and file-specific;
- `Version` is the document version, not a Git version;
- `Last Write` is secondary metadata; Git blob SHA is the primary repository-state key;
- files must not embed their own concrete SHA because any edit changes it;
- `index.md` is the sole SHA registry and therefore does not record its own SHA.

### Self-describing-file rule

A competent reader or AI should understand a file's purpose, ownership boundary and usage from its own header plus body.

Therefore:

> **`agent.md` governs behavior. `index.md` resolves location/ownership/state. Each canonical file explains itself.**

Do not turn `agent.md` or `index.md` into explanatory databases of domain-specific rules.

---

## 04 — File Semantics

Determine a file's function from its own metadata before relying on or changing it.

| Type | Treatment |
|---|---|
| Governance / resolver / registry | ownership, routing and control; keep stable |
| Standard / architecture | normative for the concepts it owns |
| Research instruction | methodology and source routing; not retained evidence |
| Research log | inspection/run history; not retained evidence by itself |
| Evidence dossier | retained external evidence; freshness matters |
| Template | required record structure; placeholders are not facts |
| Status/state record | current implementation state; time-sensitive |
| Execution record | concrete opportunity/TX facts; cannot redefine generic architecture |
| Business launcher / fact-sheet source | minimum business-readiness control; consumes canonical facts, tracks launch gaps and may feed external fact sheets without redefining upstream owners |
| Presentation/channel artifact | communication layer; may simplify but cannot redefine owners |
| Binary/visual asset | controlled asset; use through applicable identity rules |

### Business launcher file specification

`launcher.md` is the canonical OREON **business launcher and fact-sheet source**.

Its role is to:

1. maintain the minimum business facts required to credibly present OREON;
2. distinguish **CONFIRMED**, **OPEN**, **TX-SPECIFIC** and **NOT APPLICABLE** facts;
3. expose business-readiness and launch gaps without replacing detailed owner files;
4. provide the controlled input set from which an external OREON Fact Sheet may be derived;
5. remain practical and execution-oriented rather than becoming a duplicate business plan, DD dossier or legal memorandum.

Rules:

- `launcher.md` **consumes** facts from canonical business, funding, SPV, validation, access and TX owners; it does not override them;
- a fact may be marked **CONFIRMED** only when it is supportable from canonical repository state and, where required, current external evidence;
- external fact sheets may contain only confirmed facts, plus clearly labelled indicative or TX-specific information;
- open checklist items are readiness gaps, not negative facts and not external claims;
- when a canonical owner changes materially, review `launcher.md` for stale business facts or launch gates;
- when `launcher.md` becomes sufficiently complete for external use, generate the Fact Sheet as a downstream communication artifact rather than turning `launcher.md` itself into marketing copy.

Documentation must remain understandable in context. Concision is subordinate to clarity, ownership boundaries and execution safety.

---

## 05 — Read Workflow

For every substantive task:

1. identify the subject and requested action;
2. consult `index.md`;
3. load the canonical owner;
4. read the owner's metadata and body;
5. load only material dependencies referenced by that owner;
6. compare current Git blob SHA with `index.md`;
7. if different, treat current GitHub content as canonical and synchronize the stale registry during material repository work;
8. classify relevant information as structural, current-state, research-sensitive, counterparty-specific, opportunity-specific or execution-specific;
9. refresh external evidence where freshness is material;
10. answer or edit from repository truth plus verified evidence.

Do not load the entire repository when a narrower dependency set is sufficient.

---

## 06 — Research & Freshness

Current external verification is required where material reliance depends on changing facts such as law, sanctions, tax/customs, licensing, receiver requirements, AML/KYC, banking, settlement, counterparties, logistics, prices or market conditions.

Use the applicable research owner identified through `index.md` and the target file's dependencies.

An unchanged repository SHA does not prove external conditions remain current.

When material, distinguish:

- **FACT** — supported by evidence;
- **ASSUMPTION** — planning input requiring verification;
- **ILLUSTRATION** — example only;
- **PROPOSAL** — suggested future structure.

Do not promote chat history, examples, estimates or presentation simplifications into canonical facts without support.

---

## 07 — Write Workflow

Before editing:

1. identify the narrowest canonical owner;
2. fetch its full current content and blob SHA;
3. read material dependencies;
4. check whether the proposed content belongs under another owner;
5. make the smallest coherent canonical change;
6. preserve unrelated valid content;
7. verify the resulting file;
8. review direct consumers for stale interfaces, paths, states or assumptions;
9. propagate only semantic changes that materially affect consumers;
10. synchronize `index.md` after changed blobs are verified.

### No-information-loss rule

Cleanup means **migration before deletion**.

Before removing duplicated or misplaced information:

1. identify its canonical destination;
2. verify the destination already contains it at equal or better fidelity;
3. migrate first if needed;
4. remove the duplicate;
5. verify both source and destination.

---

## 08 — Editing & Verification

For material repository edits:

```text
FETCH FULL CURRENT FILE + SHA
→ BUILD COHERENT CHANGE
→ APPLY THROUGH THE HIGHEST-LEVEL AVAILABLE PATCH/EDIT WORKFLOW
→ REFETCH
→ VERIFY CONTENT / DIFF / BLOB
→ REVIEW DIRECT DEPENDENCIES
→ SYNC index.md
```

Rules:

- use the current blob SHA;
- same-path writes are sequential;
- never overwrite concurrent changes silently;
- never replace a whole file with partial or placeholder content;
- preserve unrelated valid content;
- prefer the requested higher-level repository patch workflow when available;
- commit directly to the selected branch unless instructed otherwise;
- verify resulting content before reporting success.

---

## 09 — Dependency Review

For every material change ask:

1. Which file owns the concept?
2. Which files consume it?
3. Did an interface, path, state or assumption change?
4. Does another file now contain a stale competing definition?
5. Is information being removed without a verified canonical destination?
6. Does `index.md` still point to the correct owner and SHA?

An upstream change triggers dependency review, not automatic rewriting.

---

## 10 — Index Discipline

`index.md` must remain a concise navigation and repository-state registry.

It should contain only what is needed to locate canonical files:

```text
FILE
→ OWNER
→ CURRENT SHA
```

Optional section labels may group related files, but `index.md` must not duplicate:

- detailed scope;
- AI instructions;
- dependency chains;
- domain logic;
- readiness rules;
- implementation explanations;
- file-local metadata.

Those belong in the files themselves.

After a material repository change:

1. verify every changed file;
2. update its SHA in `index.md`;
3. add/remove/move index rows only when project structure changes;
4. change the short Owner label only when canonical ownership changes.

`agent.md` changes only when repository-wide operating rules or document conventions change.

---

## Core Rule

> **Read `agent.md` → read `index.md` → resolve the narrowest owner → read that self-describing file and material dependencies → execute against repository truth → verify → review consumers → synchronize `index.md`.**
