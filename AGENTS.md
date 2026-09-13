# Agent instructions — VelX

These instructions apply throughout this repository.

## Implementation references

- Read [implementation design](docs/BLUEPRINT/car-showroom-chatbot-implementation.md) and [build prompt](docs/BLUEPRINT/car-showroom-chatbot-build-prompt.md) completely before implementing code.
- Use the design for architecture, package layout, contracts, behavior, and MVP boundaries. Use the build prompt for implementation guidance.
- Read [UI design guide](DESIGN.md) before frontend work. Reuse its tokens, layout, components, and interaction rules. Update it in the same task PR whenever shared UI design decisions change; clarify missing brand requirements with the human.
- Use [Trello backlog](docs/BLUEPRINT/car-showroom-chatbot-trello-backlog.md) for task IDs, dependencies, scope, and acceptance checklists.
- References in the build prompt to `docs/car-showroom-chatbot-implementation.md` mean the actual file under `docs/BLUEPRINT/` linked above.
- The explicit MVP testing and Trello workflow rules below override conflicting guidance in these reference documents. For other unclear or conflicting requirements, ask the human before proceeding with the affected work.

## Human direction and workflow

- Implement tasks assigned by the human on the Trello **VelX** dashboard. Do not choose additional tasks or expand scope independently.
- Before implementation, identify the assigned card, read its scope and dependencies, and move it to **Dev**.
- Use a dedicated task branch and create a pull request (PR) for every task, including documentation and configuration changes. Push commits only to the task branch; never push directly to `main` or the repository's default branch.
- After implementation is complete, push the task branch and open a PR against the repository's default branch. Include the task ID, change summary, verification results, and deferred work in the PR. Do not merge the PR unless the human explicitly authorizes it.
- Move the card to **Code Review** only after the task branch has been successfully pushed and the PR has been created. Include the PR link in the task handoff.
- Update the matching task checklist in `docs/BLUEPRINT/car-showroom-chatbot-trello-backlog.md`. Check only items actually completed; leave skipped or unverified items unchecked and explain their status. Include these updates in the pushed changes.
- Preserve task IDs in branches, commits, PRs, and progress reports. Code review is a handoff, not approval or completion of human review.
- If the card, board, destination list, access, or push target is missing or ambiguous, ask the human. Never invent Trello state or claim a move or push succeeded without confirmation from the operation.
- Do not assume requirements or business decisions. Ask the human whenever instructions are unclear or information needed for the task is missing.

## Package design layout

Follow the implementation design's suggested package layout and retain its separation of responsibilities:

```text
app/                    # Python/FastAPI backend
  main.py
  api/
  config/
  auth/
  graph/
  llm/
  tools/
  services/
  integrations/
  db/
  observability/
  prompts/
frontend/               # React + TypeScript + Vite
  src/
    api/
    components/
    features/
    types/
  public/
migrations/
evals/
deploy/
```

The design's `tests/` and `frontend/tests/` directories are deferred under the MVP testing policy below. Follow existing package conventions when adding files; ask before changing the architecture or package boundaries.

## MVP verification policy

- Prioritize fast MVP delivery. Skip writing and running unit tests and integration tests unless the human explicitly requests them for the assigned task.
- This policy overrides unit/integration test requirements in the design, build prompt, backlog, and testing workflows. Do not add test scaffolding solely to satisfy those requirements.
- Use relevant lightweight verification, such as formatting, linting, type checks, builds, and manual smoke checks. Report what actually ran and its result.
- Keep skipped test checklist items unchecked and label them deferred under this MVP policy. Never report skipped tests as passing.

## Configuration and dependencies

- Whenever adding or changing configuration, update the corresponding `.env.example` in each affected frontend/backend package in the same change. Create the package example if missing; document the field, purpose, and safe default or placeholder.
- If a setting affects both packages, update both examples. Backend-only credentials must never appear in frontend configuration or `VITE_*` variables.
- Never commit real secrets or populated local `.env` files.
- Use `.venv` for the Python virtual environment. Run Python commands and dependency installation through that environment, for example `.venv/bin/python -m pip install ...`.
- Use `npx` for React dependency tooling, scaffolding, and CLI execution within `frontend/`. Keep dependency manifests and lockfiles synchronized. Since `npx` executes packages rather than saving dependencies, ask the human if the persistent dependency installation command is not established by the project.

## Skills and working style

- Read the [VelX skill](.agents/skills/velx/SKILL.md) before implementation for project skill selection and concise communication rules.
- Use the `caveman` skill when implementing code. Read its `SKILL.md` and follow its concise communication guidance; keep code, documentation, and memory clear and technically complete. If it is unavailable, use the portable fallback in `.agents/skills/velx/SKILL.md`.
- Use [velx-focused-delivery](.agents/skills/velx-focused-delivery/SKILL.md) for assigned features and fixes to keep inspection, scope, verification, and PR handoff focused.
- Use Superpowers workflows for substantial, multi-step, high-risk, or ambiguous work. Handle routine inspections and focused small changes directly. Use worktrees or delegation only when their benefit is proportional to the task.
- Preserve unrelated human changes.

## Project memory

- Use root [MEMORY.md](MEMORY.md) as persistent memory scoped to this project. Read it before starting implementation; create it if absent.
- Update memory after every change, including documentation and configuration changes, and before the final handoff. Include the memory update in the task's committed and pushed changes.
- Record the task ID when available, what changed, decisions made, relevant files, verification results, deferred work, and blockers. Keep entries concise and current.
- Store only VelX project context. Never record secrets, credentials, personal customer data, or unrelated project information.
- Record only confirmed outcomes. Do not claim a commit, push, PR creation, Trello transition, or review happened before it succeeds.

## graphify

Graphify is optional development tooling for repository navigation, not the chatbot's LangGraph orchestration or RAGFlow retrieval. Its project-local skill is [graphify](.agents/skills/graphify/SKILL.md); setup and usage are documented in [Graphify guide](docs/GRAPHIFY.md).

When the user invokes `$graphify` (Codex) or `/graphify`, read the installed skill before executing its workflow. Run the CLI through `.venv/bin/graphify` when installed there; an existing standalone `graphify` installation can also be used. Do not install Python dependencies into the system interpreter.

The generated graph belongs in `graphify-out/`. Do not claim it exists or is current until verified. The initial AST-only smoke check produced an empty graph because application code has not been scaffolded; document semantics have not been indexed.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Generated graphify-out/ files are ignored by Git. If the graph or CLI is unavailable, stale, or does not provide enough evidence, report the limitation and inspect source files directly. Graph output is navigation evidence, not a replacement for required blueprint reads or current source verification.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- Honor `.graphifyignore`. Keep semantic documentation extraction explicit; never silently select a paid API backend or upload project content. AST-only extraction does not index document meaning. Do not install background watchers, Git hooks, or change global agent settings unless requested.
