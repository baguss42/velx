"""Validate generated contract artifacts and representative JSON fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generate_contract_types import expected_outputs  # noqa: E402
from pydantic import TypeAdapter  # noqa: E402

from app.api.contracts import ChatRequest, SseEvent  # noqa: E402
from app.tools.contracts import ToolEnvelope  # noqa: E402

FIXTURE_PATH = ROOT / "docs/contracts/t02-contract-examples.json"
SCHEMA_PATH = ROOT / "frontend/src/types/api.schema.json"
TYPES_PATH = ROOT / "frontend/src/types/api.generated.ts"


def main() -> int:
    schema_text, types_text = expected_outputs()
    errors: list[str] = []
    if not SCHEMA_PATH.exists() or SCHEMA_PATH.read_text(encoding="utf-8") != schema_text:
        errors.append(f"stale schema: {SCHEMA_PATH.relative_to(ROOT)}")
    if not TYPES_PATH.exists() or TYPES_PATH.read_text(encoding="utf-8") != types_text:
        errors.append(f"stale TypeScript: {TYPES_PATH.relative_to(ROOT)}")

    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    ChatRequest.model_validate(fixture["chat_request"])
    ToolEnvelope.model_validate(fixture["tool_envelope"])
    event_adapter = TypeAdapter(SseEvent)
    for event in fixture["events"]:
        event_adapter.validate_python(event)

    if errors:
        print("; ".join(errors))
        return 1
    print(f"Contract compatibility check passed for {FIXTURE_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
