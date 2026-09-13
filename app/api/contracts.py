"""Public API request, run, and safe SSE event contracts."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import Field

from app.tools.contracts import (
    ActionCard,
    ContractModel,
    PriceCard,
    ProductCard,
    SafeError,
    SourceCard,
)


class ChatRequest(ContractModel):
    """Request body for starting one customer-visible conversation run."""

    request_id: UUID
    conversation_id: UUID
    message: str = Field(min_length=1, max_length=4000)
    locale: str = Field(default="id-ID", min_length=2, max_length=16)


type RunStatus = Literal["queued", "running", "validating", "completed", "cancelled"]


class RunCreatedResponse(ContractModel):
    """Identifiers returned when an idempotent run is accepted."""

    request_id: UUID
    conversation_id: UUID
    run_id: UUID
    trace_id: UUID
    status: RunStatus


class StatusEvent(ContractModel):
    event: Literal["status"] = "status"
    request_id: UUID
    conversation_id: UUID
    run_id: UUID
    trace_id: UUID
    occurred_at: datetime
    status: RunStatus
    message: str = Field(min_length=1, max_length=240)


class AnswerDeltaEvent(ContractModel):
    event: Literal["answer_delta"] = "answer_delta"
    request_id: UUID
    conversation_id: UUID
    run_id: UUID
    trace_id: UUID
    occurred_at: datetime
    delta: str
    message_id: UUID | None = None


class SourcesEvent(ContractModel):
    event: Literal["sources"] = "sources"
    request_id: UUID
    conversation_id: UUID
    run_id: UUID
    trace_id: UUID
    occurred_at: datetime
    sources: list[SourceCard]


class CardsEvent(ContractModel):
    event: Literal["cards"] = "cards"
    request_id: UUID
    conversation_id: UUID
    run_id: UUID
    trace_id: UUID
    occurred_at: datetime
    cards: list[Annotated[ProductCard | PriceCard | ActionCard, Field(discriminator="kind")]]


class DoneEvent(ContractModel):
    event: Literal["done"] = "done"
    request_id: UUID
    conversation_id: UUID
    run_id: UUID
    trace_id: UUID
    occurred_at: datetime
    message_id: UUID
    status: Literal["completed", "cancelled"]


class ErrorEvent(ContractModel):
    event: Literal["error"] = "error"
    request_id: UUID
    conversation_id: UUID
    run_id: UUID
    trace_id: UUID
    occurred_at: datetime
    error: SafeError


type SseEvent = Annotated[
    StatusEvent | AnswerDeltaEvent | SourcesEvent | CardsEvent | DoneEvent | ErrorEvent,
    Field(discriminator="event"),
]


API_CONTRACT_MODELS = [
    ChatRequest,
    RunCreatedResponse,
    StatusEvent,
    AnswerDeltaEvent,
    SourcesEvent,
    CardsEvent,
    DoneEvent,
    ErrorEvent,
]
