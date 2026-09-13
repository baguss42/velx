# Graphify for VelX

Graphify is development tooling for exploring repository relationships. It does not replace LangGraph or RAGFlow in the application architecture.

Upstream: [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify). Python distribution: `graphifyy`; CLI: `graphify`. This repository pins version `0.9.61` in `requirements-tools.txt` and includes that version's upstream skill and reference files under `.agents/skills/graphify/`.

## Setup

Run from the repository root. Create `.venv` if it does not already exist, then install development tooling:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-tools.txt
.venv/bin/graphify --version
```

The project skill is already included, so normal checkout does not require registration. To regenerate it when deliberately updating the pinned version:

```sh
.venv/bin/graphify install --platform agents --project
```

Review the generated skill/reference diff and update the version pin together. This command targets `.agents/skills/graphify/`; it does not need a global skill install, a Codex hook, or a global configuration change.

An existing standalone installation can run the same commands as `graphify`. During initial setup, an existing standalone `graphify 0.9.61` was found and reused; no project `.venv` was created.

## Usage

In Codex, invoke `$graphify .` for the skill-driven workflow. The skill should appear on the next turn; restart the session if it does not appear. Documentation semantics can be extracted by the host agent; this consumes model context/tokens. A separate API backend is optional and must not be enabled silently.

For local, deterministic code extraction without an API backend:

```sh
.venv/bin/graphify extract . --code-only
```

Once a graph exists:

```sh
.venv/bin/graphify query "How does authentication connect to the API?" --budget 1500
.venv/bin/graphify explain "AuthModule"
.venv/bin/graphify path "AuthModule" "Database"
.venv/bin/graphify update .
```

Concept names above are examples; use names present in the actual graph. `update` refreshes code relationships; it does not perform fresh semantic extraction of Markdown documents. Read current source before changing code, especially when the graph is stale or incomplete.

## Index scope and current status

- `.graphifyignore` excludes dependencies, generated artifacts, local secrets, and installed agent skills from the corpus.
- Graphify also respects Git ignore rules. Files ignored by Git will not automatically be indexed; review exclusions before changing scan scope.
- `graphify-out/` is a local generated artifact and is ignored by Git. It may contain file paths and source-derived content.
- Initial repository content is documentation and agent guidance, with no application code yet. Registration is complete. An AST-only smoke check (`graphify extract . --code-only --no-cluster`) succeeded and generated a local `graph.json` with 0 nodes and 0 edges; it skipped six documentation files. This is not a semantic documentation index.
- The normal skill workflow can create `graph.json`, `GRAPH_REPORT.md`, and `graph.html`. Do not report these artifacts as present until a build succeeds.
- No automatic Git hooks, watchers, MCP server, provider credentials, or application environment fields are configured by this setup.
