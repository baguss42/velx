"""Canonical typed envelopes and customer-visible cards returned by tools."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, StringConstraints


class ContractModel(BaseModel):
    """Base model shared by the public contract schemas."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_serialization_defaults_required=True,
    )


type CurrencyCode = Annotated[
    str,
    StringConstraints(
        min_length=3,
        max_length=3,
        pattern=r"^[A-Z]{3}$",
    ),
]
type AmountString = Annotated[str, StringConstraints(pattern=r"^\d+(\.\d{1,2})?$")]
type ToolStatus = Literal[
    "success",
    "empty",
    "denied",
    "unavailable",
    "invalid_input",
]
type SafeErrorCode = Literal[
    "invalid_request",
    "not_authenticated",
    "not_authorized",
    "not_found",
    "unavailable",
    "stale_data",
    "conflict",
    "rate_limited",
    "timeout",
    "cancelled",
    "internal_error",
]


class ActionCard(ContractModel):
    """A server-approved next step; opening it is not completion of that step."""

    kind: Literal["action"] = "action"
    action_id: str = Field(min_length=1, max_length=80, pattern=r"^[a-z0-9][a-z0-9._-]*$")
    label: str = Field(min_length=1, max_length=120)
    url: HttpUrl
    external: bool
    requires_auth: bool
    auth_reason: str | None = Field(default=None, max_length=200)


class SafeError(ContractModel):
    """Safe customer-facing error; never carry raw exception text or private data."""

    code: SafeErrorCode
    message: str = Field(min_length=1, max_length=240)
    retryable: bool
    next_action: ActionCard | None = None


class SourceCard(ContractModel):
    """Approved citation metadata safe to render beside an answer."""

    kind: Literal["source"] = "source"
    source_id: str = Field(min_length=1, max_length=160)
    title: str = Field(min_length=1, max_length=240)
    url: HttpUrl | None = None
    retrieved_at: datetime
    as_of: datetime | None = None
    document_version: str | None = Field(default=None, max_length=80)


class ProductCard(ContractModel):
    """Approved public vehicle identity and media metadata."""

    kind: Literal["product"] = "product"
    variant_id: UUID
    model_name: str = Field(min_length=1, max_length=120)
    model_year: int = Field(ge=2000, le=2100)
    variant_name: str = Field(min_length=1, max_length=120)
    body_type: str | None = Field(default=None, max_length=80)
    image_url: HttpUrl | None = None
    brochure_url: HttpUrl | None = None


class PriceCard(ContractModel):
    """Current commercial snapshot with explicit unknown and unavailable states."""

    kind: Literal["price"] = "price"
    variant_id: UUID
    branch_id: UUID | None = None
    amount: AmountString | None = None
    currency: CurrencyCode
    availability: Literal["available", "not_available", "unknown"]
    lookup_status: Literal["verified", "unavailable", "unknown"]
    freshness: Literal["current", "stale", "unknown"]
    qualifiers: list[str] = Field(default_factory=list, max_length=12)
    as_of: datetime | None = None
    expires_at: datetime | None = None
    message: str = Field(min_length=1, max_length=240)


type ToolCard = Annotated[
    SourceCard | ProductCard | PriceCard | ActionCard,
    Field(discriminator="kind"),
]


class ToolEnvelope(ContractModel):
    """Normalized result paired to exactly one model tool call."""

    request_id: UUID
    conversation_id: UUID
    run_id: UUID
    trace_id: UUID
    tool_call_id: str = Field(min_length=1, max_length=160)
    tool_name: str = Field(min_length=1, max_length=100)
    status: ToolStatus
    data: ToolCard | list[ToolCard] | None = None
    source_refs: list[str] = Field(default_factory=list, max_length=32)
    as_of: datetime | None = None
    expires_at: datetime | None = None
    error: SafeError | None = None


class ToolCallRequest(ContractModel):
    """Model-proposed call metadata before application validation and execution."""

    request_id: UUID
    conversation_id: UUID
    run_id: UUID
    trace_id: UUID
    tool_call_id: str = Field(min_length=1, max_length=160)
    tool_name: str = Field(min_length=1, max_length=100)
    arguments: dict[str, Any]


TOOL_CONTRACT_MODELS = [
    ActionCard,
    SafeError,
    SourceCard,
    ProductCard,
    PriceCard,
    ToolEnvelope,
    ToolCallRequest,
]
