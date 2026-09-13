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
