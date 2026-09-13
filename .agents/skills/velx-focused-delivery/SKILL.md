---
name: velx-focused-delivery
description: Deliver one assigned VelX task with targeted repository inspection, minimal implementation scope, lightweight verification, and accurate PR handoff. Use when implementing a VelX feature or fix.
---

# Focused VelX delivery

Follow [AGENTS.md](../../../AGENTS.md); it owns the Trello, branch, PR, configuration, tooling, and MVP testing rules. Read [MEMORY.md](../../../MEMORY.md) before implementation. This skill improves execution efficiency without changing those rules.

## Establish the task boundary

- Read the assigned card and matching [backlog](../../../docs/BLUEPRINT/car-showroom-chatbot-trello-backlog.md) section. Identify the requested behavior, dependencies, and completion criteria.
- Read the [implementation design](../../../docs/BLUEPRINT/car-showroom-chatbot-implementation.md) and [build prompt](../../../docs/BLUEPRINT/car-showroom-chatbot-build-prompt.md) completely as required by project instructions. Reuse that context during the task instead of repeatedly dumping the same files.
- Inspect Git state and existing implementations before editing. Locate relevant paths with `rg --files` and search symbols with `rg`; expand the search only when needed.
- Resolve missing requirements with the human. Record concrete blockers; continue independent, in-scope work when it does not depend on the answer.
- Complete the required Dev transition and task-branch setup before implementation. Missing Trello or Git access must be reported, not silently treated as success.

## Implement the smallest complete change

- For multi-step tasks, keep a short checklist linking acceptance items to affected files and planned verification. Small edits do not need a separate plan document.
- Reuse existing APIs, settings, services, repositories, and shared UI components before adding another abstraction or dependency.
- Keep changes within the assigned card. Do not perform unrelated cleanup or start another backlog item.
- Batch independent read-only inspections. Keep edits and dependent operations sequential; avoid duplicate reads and repeated checks without new evidence.
- Use the package layout in the blueprint. Read [DESIGN.md](../../../DESIGN.md) for UI work. Preserve the typed tool/service/repository boundaries and existing API contracts.
- Keep configuration examples, contracts, and relevant documentation synchronized with the behavior change. Use `.venv` and frontend tooling as specified in `AGENTS.md`.

## Verify proportionally

- Inspect the final diff for unintended changes, incomplete paths, and exposed secrets.
- Run the relevant existing formatter, lint, type-check, or build commands for the affected package. Use manual smoke checks when needed to establish the changed behavior.
- Skip unit and integration tests under the MVP policy unless the human explicitly requests them. Do not install an additional verification framework merely to complete a small task.
- Distinguish static inspection, executable checks, mocks, and live verification. A successful build does not prove an external integration works.
- Fix failures caused by the change. Report unrelated failures or missing access with concise evidence. Repeat checks only when changes or unresolved failures justify it.

## Complete the handoff

- Update only genuinely completed backlog checklist items. Keep skipped or unverified criteria unchecked with a short explanation.
- Update project memory with changes, decisions, verification, and remaining work. Update `DESIGN.md` when shared UI rules change.
- Commit task changes, push only the task branch, and create the required PR. Include task ID, behavior change, verification, and limitations; preserve unrelated human changes.
- Move the assigned card to Code Review only after successful push and PR creation. Do not merge without human authorization.
- Report the result, actual checks, PR link, and blockers concisely. If an operation fails, leave its state incomplete and report the failure; never advance tracking based on an intended outcome.
