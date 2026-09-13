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
