.PHONY: api web dev contracts contracts-check backend-checks frontend-checks ci-checks

api:
	.venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

web:
	npm --prefix frontend run dev -- --host 127.0.0.1

dev:
	@trap 'kill $$(jobs -p) 2>/dev/null || true' INT TERM EXIT; \
		$(MAKE) api & \
		$(MAKE) web & \
		wait

contracts:
	.venv/bin/python scripts/generate_contract_types.py

contracts-check:
	.venv/bin/python scripts/check_contracts.py

backend-checks:
	.venv/bin/ruff format --check app scripts
	.venv/bin/ruff check app scripts
	.venv/bin/mypy app
	.venv/bin/python scripts/check_contracts.py

frontend-checks:
	npm --prefix frontend run format:check
	npm --prefix frontend run typecheck
	npm --prefix frontend run build

ci-checks: backend-checks frontend-checks
