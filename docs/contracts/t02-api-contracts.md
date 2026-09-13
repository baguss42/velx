# T02 API, tool, and event contracts

Pydantic models in `app/tools/contracts.py` and `app/api/contracts.py` are the canonical
contract source. `scripts/generate_contract_types.py` emits
`frontend/src/types/api.schema.json` and `frontend/src/types/api.generated.ts`; the
compatibility check fails when either generated artifact is stale.

## Correlation identifiers

| Identifier | Meaning | Contract locations |
| --- | --- | --- |
| `request_id` | One client/API request correlation value. | `ChatRequest`, run response, every SSE event, tool call/envelope |
| `conversation_id` | Owned conversation whose history is being changed/read. | `ChatRequest`, run response, every SSE event, tool call/envelope |
| `run_id` | One idempotent model/tool execution attempt within a conversation. | Run response, every SSE event, tool call/envelope |
| `trace_id` | Observability trace correlation for the run. | Run response, every SSE event, tool call/envelope |
| `tool_call_id` | One model-proposed tool call, paired with exactly one `ToolEnvelope`. | `ToolCallRequest`, `ToolEnvelope` |

All identifiers are UUIDs except `tool_call_id`, which is an opaque provider-normalized string.
They must not be used interchangeably. `Idempotency-Key` remains an HTTP header for the message
endpoint; it is not a substitute for any correlation identifier.

## Safe unknowns and actions

- A price that cannot be verified uses `amount: null`, `availability: "unknown"`, and
  `lookup_status: "unavailable"` or `"unknown"`; it must never become zero.
- A verified sold-out result uses `availability: "not_available"` with
  `lookup_status: "verified"`.
- Currency is always explicit on `PriceCard` and uses an uppercase ISO-like three-letter code.
- `as_of`, `expires_at`, `retrieved_at`, and `occurred_at` are ISO-8601 timestamps.
- `ActionCard.requires_auth` tells the client that sign-in is needed. Opening its approved URL
  does not claim that a booking, quote, payment, or application was completed.
- `SafeError` exposes a stable code, safe message, retry hint, and optional approved next action;
  raw exception text and private identifiers do not cross the contract boundary.

Representative JSON for these cases lives in `docs/contracts/t02-contract-examples.json` and is
validated by `scripts/check_contracts.py`.
