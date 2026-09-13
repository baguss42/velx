.PHONY: api web dev

api:
	.venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

web:
	npm --prefix frontend run dev -- --host 127.0.0.1

dev:
	@trap 'kill $$(jobs -p) 2>/dev/null || true' INT TERM EXIT; \
		$(MAKE) api & \
		$(MAKE) web & \
		wait
