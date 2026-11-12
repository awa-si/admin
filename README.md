# GPT Admin

`awa-si/admin/core.yaml` is the canonical global instruction contract, including behavior, workflow routing, coding, research, and repository-agent fallback policies.

## ChatGPT Project bootstrap

Copy [`projects/template.txt`](projects/template.txt) into the ChatGPT Project Custom Instructions. Its only required global source is [`core.yaml`](core.yaml).

After resolving the exposed project name to a verified directory slug, **enumerate `projects/<project>/*` and read every existing regular file completely**. Do not restrict discovery to predefined filenames. If the project directory does not exist, inherit global rules. Report any unreadable or truncated file rather than claiming complete loading.

Load the resolved target repository's current `AGENTS.md` when repository context is active. Global routing is defined in `core.yaml#workflow.routing_decision_order`; live provider schemas determine available operations.

## Canonical ownership

- `core.yaml`: global instructions, workflow, coding, research and repository-agent policy
- `projects/<project>/*`: complete project-specific delta
- `<repository>/AGENTS.md`: current target-repository behavior, when present
- `<repository>/<helper>`: technical and operational source of truth
- `validate.py`: structural validation of global rules and project bootstrap

The remaining root Markdown files hold the pre-consolidation source texts and are **not independent instruction authorities**. Project-specific deltas remain separate from global rules.

## Validation

```sh
python -m pip install PyYAML
python validate.py
```

The Admin repository is public. Do not commit secrets, credentials, sessions, private data or secret-bearing URLs.
