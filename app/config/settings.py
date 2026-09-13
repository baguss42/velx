"""Validated environment-backed settings for the VelX backend."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from typing import Annotated, Literal
from urllib.parse import urlsplit
from uuid import UUID
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import AnyHttpUrl, Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

EnvironmentName = Literal["development", "test", "staging", "production"]
AuthMode = Literal["fake", "oidc"]
BusinessDataMode = Literal["authoritative_postgres", "imported_read_model"]
LLMProviderName = Literal["mock", "openai", "anthropic", "deepseek"]
OTLPProtocol = Literal["http/protobuf", "http/json", "grpc"]

_EnvList = Annotated[list[str], NoDecode]
_LOCAL_ENVIRONMENTS = frozenset({"development", "test"})
_PRODUCTION_ENVIRONMENTS = frozenset({"staging", "production"})
_POSTGRES_SCHEMES = frozenset({"postgresql", "postgresql+psycopg"})
_RESERVED_HOST_SUFFIXES = (".local", ".test", ".invalid", ".example")
_HOST_PATTERN = re.compile(
    r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)*"
    r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$"
)
_PLACEHOLDER_MARKERS = (
    "<",
    ">",
    "configure_real",
    "change-me",
    "placeholder",
    "replace-me",
    "your-",
    "your_",
    "example.",
    "example.com",
    "example.invalid",
    "fictional",
    "development only",
)
_LOCAL_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})


def _blank_as_none(value: object) -> object:
    if isinstance(value, str) and not value.strip():
        return None
    return value


def _parse_env_list(value: object) -> list[str]:
    """Parse JSON or comma-separated environment lists without accepting objects."""

    if value is None:
        return []
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return []
        if stripped.startswith("["):
            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError("must be valid JSON or comma-separated values") from exc
        else:
            value = stripped.split(",")
    if not isinstance(value, (list, tuple, set)):
        raise ValueError("must be a list or comma-separated values")

    values: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError("must contain non-empty strings only")
        values.append(item.strip())
    return list(dict.fromkeys(values))


def _contains_placeholder(value: str) -> bool:
    normalized = value.strip().lower()
    return any(marker in normalized for marker in _PLACEHOLDER_MARKERS)


def _is_local_host(host: str) -> bool:
    normalized = host.lower().rstrip(".")
    return normalized in _LOCAL_HOSTS or normalized.endswith(".localhost")


def _is_reserved_host(host: str) -> bool:
    normalized = host.lower().rstrip(".")
    return _is_local_host(normalized) or normalized.endswith(_RESERVED_HOST_SUFFIXES)


def _validate_http_url(
    name: str,
    value: AnyHttpUrl,
    *,
    production: bool,
    allow_path: bool = False,
) -> list[str]:
    errors: list[str] = []
    parsed = urlsplit(str(value))
    host = parsed.hostname

    if parsed.scheme not in {"http", "https"} or host is None:
        errors.append(f"{name} must use an HTTP(S) URL with a hostname")
        return errors
    if parsed.username is not None or parsed.password is not None:
        errors.append(f"{name} must not include URL userinfo or credentials")
    if parsed.query or parsed.fragment:
        errors.append(f"{name} must not include a query string or fragment")
    if not allow_path and parsed.path not in {"", "/"}:
        errors.append(f"{name} must not include a path")
    if production and parsed.scheme != "https":
        errors.append(f"{name} must use HTTPS outside local development")
    if production and _is_reserved_host(host):
        errors.append(f"{name} must not point to a local host outside local development")
    if production and _contains_placeholder(host):
        errors.append(f"{name} must not use a placeholder host outside local development")
    return errors


def _validate_action_hosts(hosts: list[str], *, production: bool) -> list[str]:
    errors: list[str] = []
    for host in hosts:
        normalized = host.lower().rstrip(".")
        if normalized != host:
            errors.append(f"ACTION_ALLOWED_HOSTS must use lowercase hostnames: {host}")
        if not _HOST_PATTERN.fullmatch(normalized):
            errors.append(f"ACTION_ALLOWED_HOSTS contains an invalid hostname: {host}")
            continue
        if _is_reserved_host(normalized):
            errors.append(f"ACTION_ALLOWED_HOSTS must not include a local host: {host}")
        if _contains_placeholder(normalized):
            errors.append(f"ACTION_ALLOWED_HOSTS must not include a placeholder host: {host}")
        if production and (normalized == "*" or normalized.startswith("*.")):
            errors.append(f"ACTION_ALLOWED_HOSTS must use exact hosts: {host}")
    return errors


def _validate_database_url(name: str, value: str, *, production: bool) -> list[str]:
    errors: list[str] = []
    parsed = urlsplit(value)
    if parsed.scheme not in _POSTGRES_SCHEMES or parsed.hostname is None:
        errors.append(f"{name} must be a PostgreSQL URL using postgresql or postgresql+psycopg")
        return errors
    if parsed.username is None:
        errors.append(f"{name} must include a dedicated database role")
    if parsed.password is None and production:
        errors.append(f"{name} must include an injected database credential")
    if parsed.fragment:
        errors.append(f"{name} must not include fragment data")
    if production and (
        "<" in value
        or ">" in value
        or _contains_placeholder(value)
        or _is_reserved_host(parsed.hostname)
    ):
        errors.append(f"{name} must not contain placeholder values outside local development")
    return errors


def _secret_is_configured(value: SecretStr | None) -> bool:
    if value is None:
        return False
    secret = value.get_secret_value().strip()
    return bool(secret) and not _contains_placeholder(secret)


class Settings(BaseSettings):
    """Application settings with local-safe defaults and production guardrails."""

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        validate_default=True,
    )

    app_env: EnvironmentName = "development"
    app_version: str = "local"
    app_base_url: AnyHttpUrl = AnyHttpUrl("http://localhost:5173")
    showroom_name: str = "VelX Development Showroom"
    brand_name: str = "Fictional VelX Motors (development only)"
    default_locale: str = Field(default="id-ID", min_length=2, max_length=16)
    default_currency: str = Field(default="IDR", pattern=r"^[A-Z]{3}$")
    showroom_timezone: str = "Asia/Jakarta"
    tenant_id: UUID = UUID("00000000-0000-0000-0000-000000000001")
    cors_allowed_origins: _EnvList = ["http://localhost:5173"]

    database_url: str | None = None
    business_database_url: str | None = None
    migration_database_url: str | None = None
    checkpoint_database_url: str | None = None
    db_pool_size: int = Field(default=5, ge=1, le=100)
    db_max_overflow: int = Field(default=0, ge=0, le=100)
    db_statement_timeout_ms: int = Field(default=3000, ge=100, le=120_000)
    business_data_mode: BusinessDataMode = "authoritative_postgres"
    business_data_max_age_seconds: int = Field(default=60, ge=1, le=86_400)

    ragflow_base_url: AnyHttpUrl | None = None
    ragflow_api_key: SecretStr | None = None
    ragflow_dataset_ids: _EnvList = []
    ragflow_timeout_seconds: int = Field(default=8, ge=1, le=120)
    ragflow_result_limit: int = Field(default=5, ge=1, le=50)

    llm_provider: LLMProviderName = "mock"
    llm_model: str = "velx-local-mock"
    llm_allowed_providers: Annotated[list[LLMProviderName], NoDecode] = [
        "mock",
        "openai",
        "anthropic",
        "deepseek",
    ]
    openai_api_key: SecretStr | None = None
    anthropic_api_key: SecretStr | None = None
    deepseek_api_key: SecretStr | None = None
    llm_timeout_seconds: int = Field(default=15, ge=1, le=120)
    llm_max_output_tokens: int = Field(default=1500, ge=1, le=32_000)
    llm_fallback_enabled: bool = False
    llm_fallback_provider: LLMProviderName | None = None
    llm_fallback_model: str | None = None
    prompt_version: str = "showroom-v1"
    max_tool_rounds: int = Field(default=4, ge=1, le=20)
    max_tool_calls: int = Field(default=8, ge=1, le=100)
    max_parallel_tools: int = Field(default=3, ge=1, le=20)
    chat_deadline_seconds: int = Field(default=30, ge=1, le=300)

    auth_mode: AuthMode = "fake"
    oidc_issuer_url: AnyHttpUrl | None = None
    oidc_audience: str | None = None
    guest_session_ttl_seconds: int = Field(default=86_400, ge=60, le=31_536_000)
    csrf_secret: SecretStr | None = None
    pii_encryption_key_ref: str | None = None
    rate_limit_requests_per_minute: int = Field(default=20, ge=1, le=10_000)
    action_allowed_hosts: _EnvList = []
    web_search_enabled: bool = False
    web_search_provider: str = "tavily"
    web_search_api_key: SecretStr | None = None

    otel_service_name: str = "showroom-chatbot"
    otel_resource_attributes: str = "deployment.environment.name=development,service.version=local"
    otel_exporter_otlp_endpoint: AnyHttpUrl = AnyHttpUrl("http://localhost:4318")
    otel_exporter_otlp_protocol: OTLPProtocol = "http/protobuf"
    otel_exporter_otlp_headers: str | None = None
    otel_traces_sampler: str = "parentbased_always_on"
    telemetry_capture_content: bool = False
    log_level: str = "INFO"
    conversation_retention_days: int = Field(default=30, ge=1, le=3_650)
    audit_retention_days: int = Field(default=90, ge=1, le=3_650)

    @field_validator(
        "cors_allowed_origins",
        "ragflow_dataset_ids",
        "llm_allowed_providers",
        "action_allowed_hosts",
        mode="before",
    )
    @classmethod
    def parse_list_settings(cls, value: object) -> list[str]:
        return _parse_env_list(value)

    @field_validator(
        "database_url",
        "business_database_url",
        "migration_database_url",
        "checkpoint_database_url",
        "ragflow_api_key",
        "oidc_issuer_url",
        "oidc_audience",
        "csrf_secret",
        "pii_encryption_key_ref",
        "llm_fallback_provider",
        "llm_fallback_model",
        "web_search_api_key",
        "otel_exporter_otlp_headers",
        mode="before",
    )
    @classmethod
    def blank_optional_settings(cls, value: object) -> object:
        return _blank_as_none(value)

    @field_validator("openai_api_key", "anthropic_api_key", "deepseek_api_key", mode="before")
    @classmethod
    def blank_provider_keys(cls, value: object) -> object:
        return _blank_as_none(value)

    @model_validator(mode="after")
    def validate_cross_field_configuration(self) -> Settings:
        errors: list[str] = []
        production = self.app_env in _PRODUCTION_ENVIRONMENTS

        try:
            ZoneInfo(self.showroom_timezone)
        except ZoneInfoNotFoundError:
            errors.append("SHOWROOM_TIMEZONE must be a valid IANA timezone")

        errors.extend(
            _validate_http_url(
                "APP_BASE_URL", self.app_base_url, production=production, allow_path=True
            )
        )
        errors.extend(self._validate_cors_origins(production=production))
        errors.extend(self._validate_service_urls(production=production))
        errors.extend(_validate_action_hosts(self.action_allowed_hosts, production=production))
        errors.extend(self._validate_database_configuration(production=production))
        errors.extend(self._validate_llm_configuration(production=production))
        errors.extend(self._validate_auth_configuration(production=production))
        errors.extend(self._validate_optional_integrations(production=production))

        if production and _contains_placeholder(self.showroom_name):
            errors.append("SHOWROOM_NAME must be configured with a real production name")
        if production and _contains_placeholder(self.brand_name):
            errors.append("BRAND_NAME must be configured with a real production brand")
        if production and not self.csrf_secret:
            errors.append("CSRF_SECRET is required outside local development")
        if production and not self.pii_encryption_key_ref:
            errors.append("PII_ENCRYPTION_KEY_REF is required outside local development")
        if production and self.telemetry_capture_content:
            errors.append("TELEMETRY_CAPTURE_CONTENT must remain false outside local development")

        if errors:
            raise ValueError("; ".join(errors))
        return self

    def _validate_cors_origins(self, *, production: bool) -> list[str]:
        errors: list[str] = []
        if not self.cors_allowed_origins:
            errors.append("CORS_ALLOWED_ORIGINS must contain at least one origin")
        for origin in self.cors_allowed_origins:
            if origin == "*":
                errors.append("CORS_ALLOWED_ORIGINS must not use a wildcard")
                continue
            try:
                parsed = urlsplit(origin)
            except ValueError:
                errors.append(f"CORS_ALLOWED_ORIGINS contains an invalid URL: {origin}")
                continue
            if parsed.scheme not in {"http", "https"} or parsed.hostname is None:
                errors.append(f"CORS_ALLOWED_ORIGINS contains an invalid URL: {origin}")
                continue
            if parsed.path not in {"", "/"} or parsed.query or parsed.fragment:
                errors.append(f"CORS_ALLOWED_ORIGINS must contain origins only: {origin}")
            if parsed.username is not None or parsed.password is not None:
                errors.append(f"CORS_ALLOWED_ORIGINS must not contain credentials: {origin}")
            if production and parsed.scheme != "https":
                errors.append(
                    f"CORS_ALLOWED_ORIGINS must use HTTPS outside local development: {origin}"
                )
            if production and (
                _is_reserved_host(parsed.hostname) or _contains_placeholder(parsed.hostname)
            ):
                errors.append(
                    f"CORS_ALLOWED_ORIGINS must not use a local or placeholder host: {origin}"
                )
        return errors

    def _validate_service_urls(self, *, production: bool) -> list[str]:
        errors: list[str] = []
        for name, value in (
            ("RAGFLOW_BASE_URL", self.ragflow_base_url),
            ("OIDC_ISSUER_URL", self.oidc_issuer_url),
            ("OTEL_EXPORTER_OTLP_ENDPOINT", self.otel_exporter_otlp_endpoint),
        ):
            if value is not None:
                errors.extend(_validate_http_url(name, value, production=production))
        return errors

    def _validate_database_configuration(self, *, production: bool) -> list[str]:
        errors: list[str] = []
        database_fields = (
            ("DATABASE_URL", self.database_url),
            ("BUSINESS_DATABASE_URL", self.business_database_url),
            ("MIGRATION_DATABASE_URL", self.migration_database_url),
            ("CHECKPOINT_DATABASE_URL", self.checkpoint_database_url),
        )
        if production and any(value is None for _, value in database_fields):
            missing = ", ".join(name for name, value in database_fields if value is None)
            errors.append(f"production database roles are missing: {missing}")
        for name, value in database_fields:
            if value is not None:
                errors.extend(_validate_database_url(name, value, production=production))

        if production and all(value is not None for _, value in database_fields):
            roles = [urlsplit(value).username for _, value in database_fields if value is not None]
            if len(set(roles)) != len(roles):
                errors.append("production database URLs must use distinct roles")
        return errors

    def _validate_llm_configuration(self, *, production: bool) -> list[str]:
        errors: list[str] = []
        if self.llm_provider not in self.llm_allowed_providers:
            errors.append("LLM_PROVIDER must be included in LLM_ALLOWED_PROVIDERS")
        if production and "mock" in self.llm_allowed_providers:
            errors.append("LLM_ALLOWED_PROVIDERS must not include mock outside local development")
        if production and self.llm_provider == "mock":
            errors.append("LLM_PROVIDER=mock is only allowed in local development")

        provider_keys: dict[LLMProviderName, SecretStr | None] = {
            "mock": None,
            "openai": self.openai_api_key,
            "anthropic": self.anthropic_api_key,
            "deepseek": self.deepseek_api_key,
        }
        if self.llm_provider != "mock" and not _secret_is_configured(
            provider_keys[self.llm_provider]
        ):
            errors.append(
                f"{self.llm_provider.upper()}_API_KEY is required for the selected LLM provider"
            )

        if self.llm_fallback_enabled:
            if self.llm_fallback_provider is None or self.llm_fallback_model is None:
                errors.append(
                    "LLM_FALLBACK_PROVIDER and LLM_FALLBACK_MODEL are required "
                    "when fallback is enabled"
                )
            elif self.llm_fallback_provider not in self.llm_allowed_providers:
                errors.append("LLM_FALLBACK_PROVIDER must be included in LLM_ALLOWED_PROVIDERS")
            elif self.llm_fallback_provider == "mock" and production:
                errors.append("LLM_FALLBACK_PROVIDER=mock is only allowed in local development")
            elif self.llm_fallback_provider != "mock" and not _secret_is_configured(
                provider_keys[self.llm_fallback_provider]
            ):
                errors.append(
                    f"{self.llm_fallback_provider.upper()}_API_KEY is required "
                    "for the fallback LLM provider"
                )
        return errors

    def _validate_auth_configuration(self, *, production: bool) -> list[str]:
        errors: list[str] = []
        if production and self.auth_mode == "fake":
            errors.append("AUTH_MODE=fake is only allowed in local development")
        if self.auth_mode == "oidc":
            if self.oidc_issuer_url is None:
                errors.append("OIDC_ISSUER_URL is required when AUTH_MODE=oidc")
            if not self.oidc_audience or _contains_placeholder(self.oidc_audience):
                errors.append(
                    "OIDC_AUDIENCE is required and must not be a placeholder when AUTH_MODE=oidc"
                )
        return errors

    def _validate_optional_integrations(self, *, production: bool) -> list[str]:
        errors: list[str] = []
        ragflow_enabled = bool(self.ragflow_dataset_ids)
        if ragflow_enabled:
            if self.ragflow_base_url is None:
                errors.append("RAGFLOW_BASE_URL is required when RAGFLOW_DATASET_IDS is configured")
            if not _secret_is_configured(self.ragflow_api_key):
                errors.append("RAGFLOW_API_KEY is required when RAGFLOW_DATASET_IDS is configured")
            if any(_contains_placeholder(dataset_id) for dataset_id in self.ragflow_dataset_ids):
                errors.append("RAGFLOW_DATASET_IDS must not contain placeholder values")

        if self.web_search_enabled:
            if self.web_search_provider != "tavily":
                errors.append("WEB_SEARCH_PROVIDER must be tavily when web search is enabled")
            if not _secret_is_configured(self.web_search_api_key):
                errors.append("WEB_SEARCH_API_KEY is required when WEB_SEARCH_ENABLED=true")

        if production and self.action_allowed_hosts == []:
            errors.append(
                "ACTION_ALLOWED_HOSTS must configure one approved host outside local development"
            )
        return errors

    @property
    def is_local(self) -> bool:
        """Whether local-only fake integrations and development fixtures are allowed."""

        return self.app_env in _LOCAL_ENVIRONMENTS

    @property
    def is_production_like(self) -> bool:
        """Whether production safety rules apply to this deployment."""

        return self.app_env in _PRODUCTION_ENVIRONMENTS

    @property
    def ragflow_enabled(self) -> bool:
        """Whether an approved RAGFlow dataset scope enables retrieval."""

        return bool(self.ragflow_dataset_ids)

    def public_summary(self) -> dict[str, str | bool]:
        """Return non-secret configuration facts suitable for diagnostics."""

        return {
            "app_env": self.app_env,
            "app_version": self.app_version,
            "showroom_name": self.showroom_name,
            "brand_name": self.brand_name,
            "llm_provider": self.llm_provider,
            "auth_mode": self.auth_mode,
            "ragflow_enabled": self.ragflow_enabled,
            "web_search_enabled": self.web_search_enabled,
            "development_fixtures_enabled": self.is_local,
        }


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load settings once per process after validating the active environment."""

    return Settings()
