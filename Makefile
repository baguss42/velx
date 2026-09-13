.PHONY: api web dev infra-up infra-down infra-logs contracts contracts-check backend-checks frontend-checks ci-checks db-upgrade db-seed

api:
	.venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

web:
	npm --prefix frontend run dev -- --host 127.0.0.1

dev:
	@trap 'kill $$(jobs -p) 2>/dev/null || true' INT TERM EXIT; \
		$(MAKE) api & \
		$(MAKE) web & \
		wait

infra-up:
	docker compose up -d postgres

infra-down:
	docker compose down

infra-logs:
	docker compose logs -f postgres

contracts:
	.venv/bin/python scripts/generate_contract_types.py

contracts-check:
	.venv/bin/python scripts/check_contracts.py

backend-checks:
	.venv/bin/ruff format --check app scripts migrations
	.venv/bin/ruff check app scripts migrations
	.venv/bin/mypy app
	.venv/bin/python scripts/check_contracts.py

frontend-checks:
	npm --prefix frontend run format:check
	npm --prefix frontend run typecheck
	npm --prefix frontend run build

ci-checks: backend-checks frontend-checks

db-upgrade:
	.venv/bin/alembic upgrade head

# Applies migrations first, then writes only local/test fictional fixtures.
db-seed:
	.venv/bin/python scripts/seed_dev_db.py --upgrade
