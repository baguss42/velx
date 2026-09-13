# VelX

VelX is a configurable customer-service chatbot for an enterprise car showroom.
The repository contains a FastAPI backend and a React + TypeScript frontend.

## Local development

Requirements: Python 3.12+, `uv`, Node.js 22+, and npm.

Create the locked Python environment and install frontend dependencies:

```sh
uv sync
npm --prefix frontend install
```

Run the backend and frontend in separate terminals:

```sh
.venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
npm --prefix frontend run dev
```

Or start both development servers from one terminal:

```sh
make dev
```

Use `make api` or `make web` when only one server is needed.

Open the Vite URL shown in the frontend terminal. The frontend `/api` proxy forwards local
requests to FastAPI at `http://127.0.0.1:8000`; provider and database credentials are never
loaded by the browser.

## Developer checks

Backend commands use the locked `.venv` tools:

```sh
.venv/bin/ruff format app
.venv/bin/ruff check app
.venv/bin/mypy app
```

Frontend commands use the locked `frontend/package-lock.json` dependencies:

```sh
npm --prefix frontend run format:check
npm --prefix frontend run typecheck
npm --prefix frontend run build
```

The local health endpoints are `GET /health/live` and `GET /health/ready`.

## Project layout

The backend packages follow the implementation design: API, configuration, auth, graph, LLM,
tools, services, integrations, database, observability, and prompts. Frontend transport,
components, features, and types live under `frontend/src/`.

Developer repository navigation: [Graphify setup and usage](docs/GRAPHIFY.md).
