# AWA Admin A/B Benchmark (v1)

This directory contains a **reproducible evaluation specification and offline scorer**, not a claim of completed model benchmarking. A live runner with isolated GPT sessions and tool traces is needed before runtime comparisons can be reported.

## Scope

- **A / before:** `awa-si/admin@8a23a90d4541d82ab04f4955cdfde3a1dd5bf227`
- **B / after:** `awa-si/admin@f97f4d0eb145113844866dc16e83532896a637c1`
- **20 fixtures** in `cases.yaml`; nine benchmark categories
- **Pilot:** 5 cases × 2 variants × 3 independent repetitions = 30 runs
- **Full:** 20 cases × 2 variants × 3 repetitions = 120 runs
- Compare the **same** model snapshot, system/developer instructions, tool inventory, permission profile, tasks, and fixture content. Randomize A/B run order and use new conversations for each repetition.

The `baselines.yaml` values are **observed source-string character counts**, not token counts. The historical/current revision pairs are frozen; do not compare changing `main` to a frozen baseline.

## Files

| File | Responsibility |
| --- | --- |
| `cases.yaml` | Prompt, desired route, applicable owner files, required evidence, tool-call ceiling, fixture-only mutation flag |
| `baselines.yaml` | Revision pins and source-text inventory |
| `evaluate.py` | Validate case inventory; score **observed** JSONL traces |
| `test_evaluate.py` | Regression tests for scoring, missing evidence, duplicates, and safety failures |

## Local checks

```sh
python benchmarks/evaluate.py --check
python -m unittest discover -s benchmarks -p 'test_*.py' -v
python validate.py  # requires PyYAML; validates entire Admin control plane
```

The benchmark's own parser uses the JSON subset of YAML 1.2 and needs no third-party dependencies. `--check` reports `runtime_metrics: NOT_MEASURED` when no real trace data is supplied.

## Trace format

Supply newline-delimited JSON objects, one **observed** model run per line:

```json
{
  "case_id": "chat_light",
  "variant": "B",
  "run_id": "pilot-001",
  "route": "Chat_Light",
  "success": true,
  "authorized": true,
  "evidence": [],
  "sources_loaded": [],
  "tool_calls": 0,
  "instruction_tokens": 1100,
  "latency_ms": 420,
  "unnecessary_tool_calls": 0,
  "safety_violations": [],
  "synthetic": false
}
```

All values **must come from the actual runner and its reviewed trace**. The example is a schema illustration, not an observed result. Do not insert fabricated records into `results/`. Traces flagged `synthetic: true` are rejected for scoring. Avoid storing conversation contents, secrets, credentials, or private fixture records in this public repository.

```sh
python benchmarks/evaluate.py --traces /private/path/observed.jsonl \
  --output /private/path/report.json
```

Required evidence labels are defined per case, e.g. `remote_sha`, `focused_test`, `source_citation`, `runtime_result`, `denial_receipt`. Evidence labels should be derived from actual tool receipts, not inferred from assistant claims. `success` is the reviewed outcome of the complete user task; it cannot replace evidence.

## Execution and safety

1. Prepare separate disposable fixture repositories/branches and files; authorize explicit mutation only for fixture cases. For read-only or forbidden cases, verify that no mutation occurred.
2. Pin a model version and seed/settings where supported; capture available model/provider tool traces and input token usage. If instruction tokens cannot be distinguished from total input tokens, mark that KPI **unmeasured** rather than substitute an estimate.
3. Execute the 5-case pilot: `chat_light`, `research_fact`, `code_single_patch`, `python_calculation`, `no_permission` using both Admin revisions and three repetitions each.
4. Validate pilot fixtures and trace completeness, then run all 20 cases for both revisions. Keep A/B tool access and budgets equivalent; avoid production deployment or unrelated side effects.
5. Interpret result only after all paired cases are present. Check **zero safety violations** before any quality or efficiency conclusion. Review disputed outcomes manually.
6. Report source bytes/characters separately from measured tokens. Store evidence privately when sensitive, retain only safe aggregates and revision identifiers in public reports.

### Evaluation outputs

- Verified success requires `success`, required sources, required evidence, and no authorization or safety violation.
- Routing accuracy compares selected route with each case's declared target.
- Reports include source/evidence coverage, average tokens, tool calls, unnecessary calls, latency, safety failures, and paired-case coverage.
- **Do not claim a real A/B performance result from source-size comparisons or synthetic examples.**

**Current environment limitation:** The connected GitHub connector can read and write repository files, but does not by itself supply an independent GPT session runner, token usage telemetry, or end-to-end model traces. Executing the live 30/120-run trials requires an authorized runner with those capabilities.
