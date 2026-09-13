---
name: velx
description: Coordinate VelX showroom chatbot implementation using concise caveman communication and the project's task delivery workflow. Use for assigned implementation tasks in this repository.
---

# VelX implementation skills

Read [AGENTS.md](../../../AGENTS.md) for project rules and [MEMORY.md](../../../MEMORY.md) for current context. These skills support the assigned task; they do not authorize additional tasks, deployments, or external actions.

This is the project entry point referenced by `AGENTS.md`, located in Codex's standard repository skill directory. Agents can also read the linked files directly. This is a project-local skill, not a global installation.

## Caveman communication

Use the installed `caveman` skill for implementation communication when available. Read its instructions before first use. The skill name is `caveman`, even when the human calls it “cavemen”.

If that skill is unavailable, use this project-local fallback:

- Lead with the result, blocker, or next necessary decision. Use short sentences or clear fragments; remove filler, repeated explanations, and decorative formatting.
- Preserve exact technical names, commands, paths, numbers, errors, and negations. Never shorten text in a way that changes meaning.
- Keep the human's language. Do not introduce invented abbreviations.
- Give brief, meaningful progress updates when required. Do not narrate every tool call or paste long logs when a short decisive excerpt suffices.
- Ask a focused question when instructions are unclear. Do not replace missing requirements with guesses to save tokens.
- Keep code, comments, documentation, memory, commits, and PR descriptions in clear normal prose. Compression applies to conversational output, not persisted artifacts.
- Use full sentences whenever a warning, clarification, or ordered procedure would otherwise become ambiguous. Honor a request for normal or more detailed communication.

Example handoff style: “Offer card added. Frontend build passed. Unit/integration tests skipped per MVP policy. PR: <actual URL>.” Include a claim only when it is true; omit unavailable details.

## Focused task delivery

For implementation tasks, read [velx-focused-delivery](../velx-focused-delivery/SKILL.md). It covers scope control, efficient inspection, focused verification, and completion tracking without duplicating the blueprint.

For a routine question or small documentation edit, follow `AGENTS.md` directly; do not create an elaborate implementation plan solely to use a skill.

## Other available workflows

- For substantial or ambiguous work, use an available Superpowers workflow that fits the task. Do not invoke test-driven development against the explicit MVP testing policy.
- When implementing UI, read [DESIGN.md](../../../DESIGN.md) and reuse existing components. Load framework-specific skills only when they match the actual stack; this project specifies React/Vite, not Next.js.
- For future skill edits, use `skill-creator` when available. Keep this entry point short, link specialized instructions, and avoid copying the full blueprint or a global skill catalog here.
