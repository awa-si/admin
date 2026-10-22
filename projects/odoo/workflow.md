# Odoo addon development workflow

This file defines the **Odoo project-specific** development and test workflow for `awa-si/odoo@main`. It extends `awa-si/admin/workflow.md` and the global coding and project controls; parent instructions remain authoritative unless explicitly overridden.

## Objective and scope

- Develop, maintain, validate and test **all first-party Odoo modules** under `modules/<technical_name>/`.
- Target Odoo **19.0** by default. Confirm the installed Odoo and OCA revisions before relying on framework behavior; pin external dependencies for reproducibility.
- Treat the repository as source of truth, not as a running Odoo installation. Never use production databases, secrets or filestores for tests.

## Standard execution loop

1. **Inspect:** Resolve the active repository/branch, current Git state, target addon manifest, dependent addons, related models/views/security and applicable Odoo/OCA APIs. Do not assume existing code is correct.
2. **Scope:** Identify changed modules and downstream dependent modules. Specify the behavior/invariants at risk (ORM, migrations, ACL/record rules, multi-company, billing, concurrency, HTTP).
3. **Implement:** Change code and tests together; use native Odoo `TransactionCase` for ORM/business invariants and `HttpCase` for HTTP/UI when necessary. Reuse class fixtures via `setUpClass`, keeping tests independent and isolated.
4. **Validate progressively** using the three gates below. Batch related work, parallelize independent checks when resources permit, and report any skipped gate explicitly.
5. **Review:** Inspect diffs for data-loss risk, privilege escalation, compatibility, race conditions, and idempotency; do not silently alter production configuration.
6. **Deliver:** Commit/push and verify remote state when requested/authorized by the active control plane. Record what was actually tested; never equate syntax validation with Odoo runtime success.

## Untested changes in already installable addons — activation gate

- Apply when an existing addon has `installable=True` and newly added or modified functionality has not passed its required isolated Odoo tests.
- Keep the current tested production behavior active. Do **not** import, register, or wire untested additions into runtime entry points (for example `__init__.py`, manifests, XML data/views, cron, controllers, hooks, menus, model inheritance, automation or external routing) until the relevant validation gates pass.
- Stage new implementation and tests in separate, unimported files when possible. An opt-in parameter alone is **not** a substitute for this gate: imported Python can register models, add fields or change behavior before the feature flag is checked.
- For modifications to already-imported code, preserve the verified path and isolate the new behavior behind an explicit disabled-by-default gate **only when** imports, model registry, schema, existing execution and installation/upgrade remain safe; otherwise keep the modification out of the deployable path until tested.
- Never switch `installable` to `False` for a previously installed addon just to stage changes; this can disrupt installation and upgrade lifecycle. Do not disable or uninstall currently active functionality to satisfy staging.
- Test the staged change against a disposable database/filestore with relevant Gate 1 and Gate 2 checks, then Gate 3 when required by scope or release policy. Test installation/upgrade, permissions, affected downstream modules and disabled/default behavior where material.
- After successful tests and explicit release acceptance, wire the code into the addon, verify the resulting integrated bundle again, and only then promote/deploy. A commit, successful import, static check, dry-run or code review alone does not authorize activation.
- Record staging status and outstanding tests in the change report. The production deployment script must not be assumed to distinguish tested and untested files; code included in active addon imports can execute after a normal service restart.

## Gate 1 — static (every change/commit)

Run:
```bash
python dev/check.py
python -m compileall -q modules
```

Check module manifests and dependencies, Python syntax, XML/CSV/JSON references, security declarations, license/version conventions, formatting and Odoo-specific linting as tools become available. Run `bash dev/oca-checks.sh` when OCA dev requirements are installed; use `python dev/oca-verify.py --addons-path=/opt/odoo/env/odoo/addons,/opt/odoo/env/addons,/opt/odoo/addons,/opt/odoo/modules` for actual installed Odoo/OCA dependency resolution. Run these locally or through manual CI only. `pylint-odoo` and `oca-checks-odoo-module` are provided by OCA; do not use archived MQT as the active framework. Gate 1 does not require PostgreSQL.

## Existing host Odoo runtime (preferred when safely available)

The VPS already has an `odoo` OS account and an Odoo installation. **Reuse its installed Odoo binary, Python environment and compatible OCA checkout** instead of provisioning a second runtime, but separate execution from production operation:

- Run tests under the existing `odoo` identity, using an explicit, verified executable path and environment (for example `sudo -u odoo ...` through an authorized host runner).
- Use **a separate disposable PostgreSQL database**, credentials, filestore, log path and test-only Odoo configuration.
- Keep the isolated test filestore beneath `/var/lib/awa-data/odoo/filestore`. The current verified disposable database is `odoo` and the test configuration is `/opt/odoo/test.config`; validate both with `host_odoo_preflight` before host tests. Do not copy production secrets. Do not modify, drop, initialize or upgrade the production database.
- Verify the installed Odoo major version is 19.0 and that the required OCA addons match that version; if not, use a dedicated test environment rather than adapting production code to mismatched versions.
- Disable network side effects: outgoing email, external endpoints, scheduled integrations/cron and live payment/provisioning actions in the test configuration.
- Never run a test command using the production `/opt/odoo/config` without first proving it is an isolated test configuration.
- AWA's `workspace_exec_start` executes in an isolated container, **not as the host `odoo` user**. Do not assume host binaries, PostgreSQL sockets or services are accessible there. Host tests require an explicitly authorized host execution boundary or an isolated test container with mounted dependencies.
- Prefer the existing host runtime for Gate 2 and a fresh disposable database on the same host for Gate 3 only if safe isolation and adequate capacity are established; otherwise use OCA-style CI.

## Gate 2 — focused integration (development cycle)

Use an already initialized, **isolated and disposable** Odoo 19 database and filestore with matching OCA dependencies.

- Prefer focused native Odoo `--test-tags /module[:Class[.method]]` runs for changed behavior.
- `pytest-odoo` may be used for faster red/green cycles when configured and compatible; it does **not** replace native installation/update tests.
- Reinstall/update affected modules whenever changes modify models, manifests, data or views. Avoid unnecessary full DB initialization for pure method changes.
- Test both successful and rejected operations, e.g. invalid state transitions, access violations, duplicated requests, and cross-company access.

Example with a provisioned Odoo test environment:
```bash
python /path/to/odoo-bin -c /path/to/isolated-test.conf \
  -d test_odoo_dev --addons-path=/path/to/odoo/addons,/path/to/oca/addons,/path/to/repo/modules \
  -u awa --test-tags /awa --stop-after-init
```

The provided `dev/test-odoo.sh` is an **integration runner**, not a complete environment provisioner. It requires `ODOO_BIN`, `ODOO_TEST_DB`, `ODOO_CONFIG`, `ODOO_ADDONS_PATH`, and `ODOO_TEST_MODULES`; its default mode installs named modules, so do not use it to update an already-installed module without adapting the invocation. Never point it at production.

## Gate 3 — full integration (PR/release)

Provision a fresh PostgreSQL database and separate filestore with Odoo 19 and pinned OCA 19.0 addons. Install all changed modules and their declared dependencies, run the native Odoo test suite, verify install/upgrade and exercise relevant end-to-end flows. Use an OCA-style isolated CI environment (e.g. GitHub Actions with PostgreSQL), rather than the production VPS.

The minimum release checks are:

- fresh addon installation, XML views/data loading, registry initialization and cron setup;
- ACLs, record rules, permitted/denied operations and multi-company isolation;
- workflow transitions, consistency constraints, idempotency and competing transactions;
- contracts, line-level fixed pricing, dates, currency and recurring invoicing for billing modules;
- update/migration against representative sanitized data, including rollback/recovery planning.

Keep full-install tests separate from fast development tests; no real customer data.

## Test code conventions

- Put Odoo tests in `modules/<name>/tests/test_*.py`, exported from `tests/__init__.py` and imported in the addon as required for test discovery.
- Use `TransactionCase`, `HttpCase`, Odoo test tagging and reusable helpers; favor actual ORM behavior over mocks for computed fields, constraints and record rules.
- Use controlled, deterministic test data; no real network or external service dependencies in normal unit tests. Fake external responses at service boundaries.
- For concurrency-sensitive behavior, use database-level integration tests and separate transactions/cursors where warranted; a sequential mock is insufficient.

## AWA module acceptance matrix

1. Deployment creation on order confirmation and repeated confirmation; correct line/order/product linkage.
2. Registry and line state transitions, invalid transitions, uniqueness and runtime lookup.
3. Service wizard defaults, allowed activation states, repeated/concurrent activation and one-to-one service binding.
4. Service lifecycle and immutable billing terms after activation.
5. **OCA contract 19.0**: explicit lines after ORM `create()`, `automatic_price=False`, `specific_price`, quantity, currency, `date_start`, `date_end`, `recurring_next_date`, and at least one recurring invoice.
6. ACLs, record rules and multi-company separation (currently a known area requiring hardening).

## Resource and reporting policy

- The AWA workspace is intended for inspection, Gate 1 and bounded focused tests; its configured profile is 2 CPU / 2048 MB RAM. Do not assume this is adequate for full installation or large OCA dependency trees.
- Prefer cached, prepared test environments and targeted reruns over reinstalling Odoo after every edit.
- CI owns reproducible Gate 3 runs. A CI workflow that only executes static checks must be described as **Gate 1 only**.
- Report per gate: **passed / failed / blocked / not run**, and state the exact command/environment where useful.
- If a required runtime is missing, finish supported checks, explain the blocker, and do not claim integration coverage.

## References

- Odoo 19 developer testing: https://www.odoo.com/documentation/19.0/developer/reference/backend/testing.html
- OCA pytest-odoo: https://github.com/OCA/pytest-odoo
- OCA addon repository template: https://github.com/OCA/oca-addons-repo-template
- OCA contract 19.0: https://github.com/OCA/contract/tree/19.0/contract

## Reply model rename upgrade gate

The `awa.reply.operation` → `reply.operation` rename is handled in
`modules/awa/upgrades/19.0.1.0.1/pre-rename_reply.py` with the official Odoo
upgrade-util `rename_model(..., rename_table=False)`. Install a version-compatible
`odoo-upgrade-util` in the host Odoo Python environment before updating an
existing database. Do not bypass the migration when historical operations exist.
Run the preflight, compare `ir.model` references and record count before and after
the upgrade, then exercise ACLs and the reservation/completion integration tests.
The SQL table `awa_reply_operation` must be preserved.

`dev/test-odoo.sh` requires an explicitly disposable database matching
`test_*` or `*_test`; it accepts `ODOO_TEST_MODE=install|update`.
The existing host `odoo` database is restricted to the separately controlled
AWA `host_odoo_test` executor and must not be whitelisted in this shell script.

## Optional disposable test tools

- `dev/test-db-snapshot.sh`: create a **new** test DB from an explicitly
  approved existing `test_*` or `*_test` database. Requires PostgreSQL
  client tools, access, `ODOO_SNAPSHOT_SOURCE`, `ODOO_SNAPSHOT_TARGET`,
  `ODOO_SNAPSHOT_CONFIRM_SOURCE` and
  `ODOO_SNAPSHOT_SOURCE_ACK=isolated-test-only`. It refuses overwrite and
  **does not copy the filestore**. Never treat it as a full Odoo clone without
  copying the approved filestore to a separately isolated test data directory.
  The current host DB `odoo` is deliberately not eligible as a source.
- `dev/check-migration.py --database test_odoo_dev`: read-only checks of
  renamed `reply.operation` metadata, retained table and ACL references.
  Run on a verified disposable DB after update.
- `dev/test-coverage.sh`: run native Odoo module tests under coverage on
  an explicitly disposable DB, producing `coverage.xml`. It assumes a
  provisioned matching Odoo and OCA runtime and isolated config. Coverage
  reports are not a substitute for behavior assertions.
- `pytest-odoo` is an optional accelerated test adapter; verify installed
  plugin compatibility with Odoo 19 before using it. Native `TransactionCase`
  and `odoo-bin --test-enable` remain the release gate.
- GitHub CI currently provides only manual static checks; Gate 3 requires a
  separately provisioned fresh DB, isolated filestore and verified disabled
  external side effects. Do not mark it passed from CI static checks.
