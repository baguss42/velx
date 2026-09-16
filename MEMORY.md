# VelX project memory

## 2026-09-13 — Agent instructions

- Created `AGENTS.md` referencing the implementation design and build prompt in `docs/BLUEPRINT/` and the Trello delivery backlog.
- Recorded the human's workflow: assigned VelX card moves to Dev before implementation and Code Review after successful implementation, task-branch push, and PR creation; matching backlog checklists reflect actual completion.
- Recorded MVP policy to skip unit and integration tests, package layout, package-level `.env.example` updates, `.venv`, `npx`, caveman usage, clarification requirements, and project memory maintenance.
- Explicit MVP testing and Trello status rules override conflicting guidance in the blueprint documents. Other ambiguities require human clarification.
- Verification: documentation and local reference review only; no application code changed or unit/integration tests run.
- No Trello task was assigned for this documentation request. No Trello transition, commit, or push performed.

## 2026-09-13 — Pull request workflow

- Updated `AGENTS.md` to require a dedicated task branch and PR for every task, including documentation and configuration changes.
- Direct pushes to `main` or the default branch are prohibited. PRs target the default branch; merging requires explicit human authorization.
- Code Review handoff now requires a successful task-branch push and PR creation, with the PR link included in the handoff.
- Verification: reviewed the workflow text for consistency; no application code changed or unit/integration tests run.
- This request updated local rules and memory only; no branch, commit, push, PR, or Trello transition performed.

## 2026-09-13 — UI design guide

- Added `DESIGN.md` with a filled MVP design baseline: semantic tokens, typography, spacing, responsive layout, shared component responsibilities, chat states, content rules, accessibility targets, and manual review criteria.
- Included a reusable design decision template and initial entry. Visual defaults are proposed; official brand identity and assets remain unspecified. No frontend exists yet.
- Updated `AGENTS.md` to require reading the guide before frontend work and maintaining it in the same PR as shared UI changes.
- Verification: reviewed document consistency and local Markdown references. No rendered UI, unit tests, or integration tests checked.
- Changes remain local; no Trello card was supplied and no commit, push, or PR was created.

## 2026-09-13 — Project skill entry point

- Added root `SKILL.md` as the agent-referenced entry point with caveman communication guidance and a portable fallback when the installed skill is unavailable.
- Added `skills/velx-focused-delivery/SKILL.md` for scoped implementation, targeted inspection, lightweight verification, and accurate PR/Trello handoff.
- Updated `AGENTS.md` to reference both files. Skills preserve MVP test skipping, human clarification, normal prose in persisted artifacts, and existing authorization boundaries.
- Skill-creator guidance shaped the small entry point and separate focused workflow. These files are read through project instructions; no global skill installation or automatic runtime discovery is claimed.
- Verification: Markdown references and frontmatter reviewed. No application code or unit/integration tests involved.
- Changes remain local; no task ID was supplied and no commit, push, PR, or Trello transition was performed.

## 2026-09-13 — Standard repository skill locations

- Moved root `SKILL.md` to `.agents/skills/velx/SKILL.md` and `skills/velx-focused-delivery/SKILL.md` to `.agents/skills/velx-focused-delivery/SKILL.md`.
- Updated `AGENTS.md` and relative links within both skills. Earlier entries describe historical paths; this entry supersedes their location and discovery notes.
- Kept `AGENTS.md`, `MEMORY.md`, and `DESIGN.md` at the project root. No `.codex/config.toml` is needed for this move.
- Skills now use Codex's documented repository discovery layout; discovery in a fresh session has not been verified.
- Verification: skill frontmatter and all local links in both skills and `AGENTS.md` passed validation; old skill files are absent and their empty directories were removed.
- Changes remain local; no commit, push, PR, or Trello transition performed.

## 2026-09-13 — Graphify project integration

- Found an existing standalone Graphify 0.9.61 installation and Graphify guidance already committed in `AGENTS.md`.
- Registered the upstream skill and references locally using `graphify install --platform agents --project`; files live under `.agents/skills/graphify/`.
- Added the optional `graphifyy==0.9.61` pin in `requirements-tools.txt`, `.venv` setup instructions in `docs/GRAPHIFY.md`, `.graphifyignore`, and Git exclusion for generated `graphify-out/` content.
- Updated agent guidance to link the skill, distinguish missing/stale graphs from verified evidence, and separate development Graphify from application LangGraph/RAGFlow.
- AST-only smoke check (`graphify extract . --code-only --no-cluster`) exited successfully, skipped six documentation files, and generated an empty local graph (0 nodes, 0 edges). Application code does not exist yet; semantic extraction remains explicit. No external model backend, watcher, Git hook, or global configuration was enabled.
- Existing standalone CLI was reused; no project `.venv` created. No unit/integration tests run.
- Verified skill metadata, bundled reference paths, version stamp, and diff whitespace. Changes remain local; no task card was supplied and no commit, push, or PR was created.

## 2026-09-13 — T01 foundation scaffold

- Trello card `T01 — Scaffold Python backend and React frontend` was located on VelX and moved from `Backlog` to `Dev` before implementation.
- Created FastAPI app entry point with `/health/live` and `/health/ready`, design-aligned backend package layout, `pyproject.toml`, and locked Python dependencies in `uv.lock`.
- Created React + TypeScript + Vite frontend with design tokens, placeholder Indonesian chat shell, API health status, frontend package layout, `/api` proxy rewrite, `.env.example`, and `package-lock.json`.
- Updated `README.md` with setup, run, formatting, lint, type-check, build, health, and layout commands. Updated `DESIGN.md` with the implemented stylesheet path, T01 shell decision, and completed manual review evidence.
- Checked all three completed T01 acceptance items in `docs/BLUEPRINT/car-showroom-chatbot-trello-backlog.md`; `uv lock --check` passed after the initial sandbox cache permission error was retried with the required access.
- Verification: `.venv/bin/ruff format --check app`, `.venv/bin/ruff check app`, `.venv/bin/mypy app`, frontend Prettier check, TypeScript check, and Vite build passed. Live `GET /health/live` and Vite `/api/health/live` proxy checks returned `{"status":"ok","service":"velx-api"}`. Browser smoke check found meaningful content, no error overlay, no browser errors, and no horizontal overflow at 360px, 768px, or 1280px.
- Deferred under MVP policy: unit and integration tests; T02 contracts, T03 configuration validation, and later feature work remain outside T01.
- Current state: commits `f7576a5`, `cdcdbc0`, and `f75c409` are pushed on dedicated branch `T01-scaffold-python-backend-react-frontend`; pull request [#1](https://github.com/baguss42/velx/pull/1) is open against `main`; Trello card is in `Code Review`.

## 2026-09-13 — T01 Makefile shortcuts

- Added root `Makefile` shortcuts: `make api`, `make web`, and `make dev` for the FastAPI server, Vite server, or both together.
- Documented the shortcuts in `README.md`.
- Verification: `make dev` started both servers; direct health and Vite `/api` proxy requests returned the FastAPI health response. Unit and integration tests remain deferred under MVP policy.

## 2026-09-13 — Trello MCP routing

- Updated `AGENTS.md` to require Trello MCP tools for all Trello reads and writes, prohibit browser or UI automation for Trello, and require human clarification when MCP access is unavailable or insufficient.
- Verification: reviewed the documentation diff and local references. No Trello operation, card transition, branch, commit, push, PR, or tests performed.

## 2026-09-13 — T02 API, tool, and event contracts

- Trello card `T02 — Define API, tool and event contracts` was found on VelX and moved from `Backlog` to `Dev` before implementation.
- Added canonical Pydantic contracts for chat requests, run correlation, safe SSE events, tool calls/envelopes, source/product/price/action cards, and safe errors under `app/api/contracts.py` and `app/tools/contracts.py`.
- Added generated JSON Schema and TypeScript artifacts plus a compatibility checker and representative fixtures covering unknown/unavailable price data, currency, timestamps, and sign-in-required actions.
- Added contract documentation for distinct request, conversation, run, trace, and tool-call identifiers; updated `Makefile`, `README.md`, and frontend type exports.
- Verification: `make contracts-check`, `.venv/bin/ruff format --check app scripts`, `.venv/bin/ruff check app scripts`, `.venv/bin/mypy app`, frontend Prettier check, TypeScript check, and Vite build passed. `graphify update .` refreshed the local ignored code graph. Unit and integration tests remain deferred under MVP policy.
- Checked all three T02 acceptance items in `docs/BLUEPRINT/car-showroom-chatbot-trello-backlog.md`; checklist update is included in the task branch and PR.

## 2026-09-13 — T03 environment validation and development fixtures

- Trello card `T03 — Implement environment validation and dev fixtures` was found on VelX and moved from `Backlog` to `Dev` before implementation.
- Added Pydantic Settings configuration for all design-defined backend variables, safe local defaults, list/boolean/URL parsing, secret masking, explicit fake/mock local modes, production-like startup guards, and separate PostgreSQL role validation.
- Added root `.env.example` covering every backend setting without usable secrets and clarified the public frontend `.env.example` proxy setting. Added local configuration guidance to `README.md` and declared `pydantic-settings` in `pyproject.toml`/`uv.lock`.
- Added clearly labeled fictional showroom, car, and price fixtures gated to development/test environments; production-like environments cannot retrieve them.
- Verification: configuration and fixture smoke checks passed, including valid production configuration and rejection of fake auth/mock providers, unsafe URLs, missing provider credentials, and enabled integration credentials. Backend Ruff format/check and mypy, contract compatibility, frontend formatting/type-check/build, health endpoint smoke, `uv lock`, and `graphify update .` passed. Unit and integration tests remain deferred under MVP policy.
- Checked all three T03 acceptance items in `docs/BLUEPRINT/car-showroom-chatbot-trello-backlog.md`. Commit `e5c6c23` is pushed on `T03-environment-validation-dev-fixtures`; pull request [#3](https://github.com/baguss42/velx/pull/3) is open against `main`; Trello card is confirmed in `Code Review`. Unit and integration tests remain deferred under MVP policy.

## 2026-09-13 — T04 CI checks (implementation)

- Trello card T04 — Create CI checks for both applications was selected as the next
  unblocked backlog task after T01, T02, and T03; it was moved from Backlog to Dev before
  implementation. The dedicated branch is T04-create-ci-checks-both-applications.
- Added required offline GitHub Actions jobs for locked backend/frontend checks, conditional
  test execution, Gitleaks secret scanning, and pull-request dependency review. Added a
  manual-only PostgreSQL integration workflow and matching make backend-checks,
  make frontend-checks, and make ci-checks targets.
- Updated README.md and the T04 backlog evidence. No package dependencies or environment
  variables changed. Current action versions use Node 24-compatible action runtimes.
- Verification: make backend-checks, make frontend-checks, workflow YAML parsing with Ruby,
  workflow/documentation Prettier checks, conditional test-gate smoke checks, and local
  gitleaks detect --source . --no-banner --redact passed. actionlint and local pip-audit are
  unavailable. No backend/frontend test suite exists; test execution and PostgreSQL
  integration remain deferred under the MVP policy.
- Commit 08d0e2f was created and pushed on T04-create-ci-checks-both-applications. Pull
  request #4 (https://github.com/baguss42/velx/pull/4) was created against main by
  baguss42. Commit 6935446 records the final handoff metadata and is also pushed. Trello
  card was confirmed in Code Review after the final push and PR creation.
- Added explicit AGENTS.md guidance for verifying the baguss42 GitHub actor before PR
  creation, using the connected GitHub API/connector or verified gh CLI, and checking PR
  author/refs before the Trello transition.
- Commit 99a8178 was pushed to the task branch; PR #4 now points to that head and remains
  open against main, with the connected account and PR author verified as baguss42.

## 2026-09-14 — T05 catalog/commercial schema and local PostgreSQL infrastructure

- T05 remains limited to tenant-scoped catalog/commercial tables, Alembic migration, guarded fictional
  development seeding, and the explicitly requested local PostgreSQL Compose infrastructure. T06
  identity/conversation tables were not added.
- Added `docker-compose.yml` with PostgreSQL 16 Alpine, loopback-only binding, healthcheck, and a
  persistent named volume; added `infra-up`, `infra-down`, and `infra-logs` targets plus matching
  `.env.example`, README, and `docs/database.md` guidance.
- Added SQLAlchemy/Alembic schema for tenants, branches, car models/variants, approved assets,
  vehicle units, price offers, and integration sync state. Added tenant-safe foreign keys, lookup
  indexes, monetary/currency/status checks, finite validity bounds, `btree_gist` non-overlap
  enforcement, and an available-only VIN-free view.
- Seed path requires `DEV_SEED_ENABLED=true`, a dedicated validated `MIGRATION_DATABASE_URL`, and a
  local/test target. It is idempotent for matching fixtures, rejects deterministic-ID collisions,
  and verifies every supplied fixture field on read-back. Asset URLs reject credentials, whitespace,
  malformed authorities, and ports outside 1–65535.
- Verification: `make backend-checks`, `uv lock --check`, locked dry-run sync, Gitleaks, Compose
  config validation, Compose PostgreSQL readiness/SQL connectivity, missing/invalid migration URL
  rejection, offline and live Alembic upgrade/downgrade, two seed runs, all eight seeded row counts,
  availability view, URL acceptance/rejection probes, and collision-preservation smoke checks passed.
  Unit and integration tests remain deferred under the MVP policy.
- The local database is downgraded to base after verification. Task files remain uncommitted; PR
  creation and Trello Code Review transition are blocked until `gh` is authenticated as `baguss42`
  instead of the active `bagus-bfi` account.

## 2026-09-14 — T05 seed safety review blockers

- Tightened `seed_development_database()` to compare the supplied SQLAlchemy engine's driver,
  role, password, normalized host, defaulted PostgreSQL port, and database against the validated
  `MIGRATION_DATABASE_URL`; mismatch errors remain credential-free.
- `validate_seed_settings()` now rejects bracketed IPv6 authorities and malformed or out-of-range
  ports while preserving localhost, loopback IPv4, explicit opt-in, local/test, and dedicated-role
  guards. Documentation now states that bracketed IPv6 is rejected.
- Verification: `make backend-checks`, `make contracts-check`, `uv lock --check`, focused seed
  safety smoke checks, and live Compose migration/seed/idempotency/count smoke checks passed.
- No commit, push, PR, or Trello transition performed.

## 2026-09-16 — T05 handoff continuation

- T05 remains the assigned VelX card and is confirmed in `Dev`; its three acceptance items remain checked in the backlog.
- Re-ran `make backend-checks`, `uv lock --check`, locked dry-run sync, `docker compose config --quiet`, and Gitleaks; all passed. Unit and integration tests remain deferred under the MVP policy.
- GitHub connector authentication is confirmed as `baguss42`. Existing PR #5 points to commit `06ad844` but is closed and authored by `bagus-bfi`; it does not satisfy the repository-local account or open-PR handoff rules.
- Unrelated untracked `IDEA.md` is preserved and excluded from T05 changes. A fresh handoff commit and PR are pending.
