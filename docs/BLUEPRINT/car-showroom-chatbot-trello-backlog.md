# Car showroom chatbot — Trello delivery backlog

Date: 2026-09-10. Status: ready to transfer into a planning board; no Trello cards have been created by this document.

Specification: [Implementation design](./car-showroom-chatbot-implementation.md).
Coding instructions: [LLM build prompt](./car-showroom-chatbot-build-prompt.md).

## 1. How to use this backlog

Use modules as epics and individual tasks as Trello cards. Suggested board lists: **Backlog → Ready → In Progress → Review → Verify → Done**, plus **Blocked**. Use module IDs as labels, not separate workflow lists. Create one optional overview card per module, linking its child cards.

Copy a task heading into the card title. Copy its scope, dependencies and acceptance checklist into the description/checklist. Preserve IDs in branches, pull requests and status reports. Replace dependency IDs with links once cards exist. This Markdown is a copy-ready planning document, not a promise of automatic Trello import.

- **Priority:** P0 = release-critical foundation or control; P1 = required feature/integration; P2 = optional improvement. Priority does not override dependencies.
- **Size:** S = focused change; M = several connected changes. These are relative estimates, not delivery-date commitments. Split a card during planning if it cannot be reviewed independently or needs more than roughly two working days.
- **Role:** suggested discipline, not a named assignee. A person may cover several roles.
- **Dependencies:** `None` means ready once repository access exists. `External` identifies missing business/vendor information. Local fixtures can unblock development but do not satisfy production acceptance.
- **Ready:** scope understood, predecessor contracts available, required fixtures/access available, acceptance criteria testable.
- **Done:** implementation reviewed, relevant checks pass, security behavior verified, documentation/config updated, and evidence attached. Mock-only and live checks must be labeled accurately.

No task authorizes provisioning paid resources or deploying production. Deployment cards include readiness work and require the organization's authorization before live activation.

## 2. Modules and outcomes

| Module | Outcome | Cards |
|---|---|---|
| M01 — Foundation and contracts | Runnable React/FastAPI workspace and shared settings/contracts | T01–T04 |
| M02 — PostgreSQL and SQLAlchemy | Schema, migrations, repositories and integrity controls | T05–T09 |
| M03 — Identity and security | Guest/customer isolation and safe application boundaries | T10–T13 |
| M04 — Business tools | Current catalog/offers, after-sales lookup and approved actions | T14–T18 |
| M05 — RAGFlow knowledge | Cloud retrieval, source governance and verifiable citations | T19–T22 |
| M06 — LLM portability | Stable interface for OpenAI, Claude and DeepSeek | T23–T26 |
| M07 — LangGraph orchestration | Persona, bounded tool execution and grounded answers | T27–T30 |
| M08 — Conversation API and state | Durable, authorized, idempotent chat delivery | T31–T34 |
| M09 — React customer experience | Responsive chat with live data, sources and next steps | T35–T38 |
| M10 — OpenTelemetry and operations | Correlated traces/logs, metrics and privacy controls | T39–T42 |
| M11 — Acceptance and evaluation | Evidence that full customer/security flows work | T43–T46 |
| M12 — Neon and release | Deployable artifacts, staging evidence and operational handover | T47–T50 |
| M13 — Optional next iterations | Public search and measured post-MVP improvements | F01–F04 |

There are **50 implementation cards** and **4 optional future cards**. Tests attached to a feature card are its completion criteria; the acceptance module verifies interactions across features.

## 3. Suggested delivery order

1. **Foundation:** M01, core M02, guest security, telemetry bootstrap. React layout can proceed against typed fixtures.
2. **First vertical slice:** catalog and one RAGFlow adapter, mock/model interface, graph skeleton, conversation API, basic React chat. Prove one grounded answer and trace.
3. **Complete capabilities:** all provider adapters, current offers, governed knowledge, actions, verified after-sales access, rich React cards.
4. **Hardening:** concurrency/recovery, negative security tests, telemetry redaction, evaluation and load checks.
5. **Release readiness:** staging on Neon/RAGFlow with authorized credentials, restore exercise and handover. Track optional M13 separately.

Do not wait for all modules to finish before integrating. Use the explicit task dependencies below and keep mocks clearly distinguishable from verified live integrations.

## M01 — Foundation and contracts

### T01 — Scaffold Python backend and React frontend

Priority: P0 | Size: S | Role: Full stack | Depends on: None

Scope: Create the package layout in the design, React/TypeScript/Vite project, FastAPI skeleton, dependency locks and standard developer commands.

- [x] Backend health endpoint runs; frontend renders a placeholder chat page.
- [x] Frontend `/api` proxy reaches FastAPI locally without exposing provider credentials.
- [x] Python and frontend formatting/type-check/build commands are documented and reproducible.

### T02 — Define API, tool and event contracts

Priority: P0 | Size: M | Role: Backend + frontend | Depends on: T01

Scope: Define Pydantic schemas and TypeScript types for chat requests, SSE events, tool envelopes, source/product/price/action cards and safe errors.

- [x] Examples cover unknown/unavailable values, currency, timestamps and sign-in-required actions.
- [x] Schema generation or a compatibility check prevents Python/TypeScript contract drift.
- [x] Distinct request, conversation, run, trace and tool-call identifiers are documented.

### T03 — Implement environment validation and dev fixtures

Priority: P0 | Size: S | Role: Backend | Depends on: T01

Scope: Implement settings from the design and public frontend settings; separate explicit mock and production modes.

- [ ] `.env.example` documents every setting with no usable secret values.
- [ ] Production rejects fake auth/providers, unsafe URLs and missing enabled-feature credentials.
- [ ] Fictional showroom, car and price fixtures are clearly labeled in development.

### T04 — Create CI checks for both applications

Priority: P0 | Size: S | Role: Platform | Depends on: T01, T02, T03

Scope: Run backend/frontend static checks, tests and frontend build; make room for PostgreSQL integration tests.

- [ ] Pull requests run repeatable checks without real cloud credentials.
- [ ] Secret and dependency scanning are configured with actionable output.
- [ ] Failed tests/builds fail CI; optional live tests are separate from required offline checks.

## M02 — PostgreSQL and SQLAlchemy

### T05 — Create catalog and commercial schema migrations

Priority: P0 | Size: M | Role: Backend/data | Depends on: T03

Scope: Migrate tenants, branches, car models/variants, approved assets, vehicle units, price offers and sync-state tables from the design.

- [ ] Tenant-safe foreign keys, unique keys and lookup indexes exist.
- [ ] Numeric/currency/status checks and nonoverlapping offer validity rules are enforced.
- [ ] Migrations and fictional seeding run from an empty PostgreSQL database.

### T06 — Create customer and conversation schema migrations

Priority: P0 | Size: M | Role: Backend/data | Depends on: T05

Scope: Add principals/roles, customers, orders/items, service cases, action/source registries, conversations/runs/messages, citations, tool summaries and audit tables.

- [ ] Ownership relations and tenant-safe foreign keys match the design.
- [ ] Idempotency and message ordering constraints exist; run-lease fields are present.
- [ ] Schema supports archival/deletion policy without removing referenced commercial history.

### T07 — Implement async SQLAlchemy repository foundation

Priority: P0 | Size: M | Role: Backend | Depends on: T05, T06

Scope: Add async engines/session factories, business-read versus app-state transactions, repository interfaces and DTO mapping.

- [ ] Tool queries use SQLAlchemy ORM/Core bound values and allowlisted filters/sorting.
- [ ] Each concurrent task receives its own AsyncSession; sessions always close on failure/cancellation.
- [ ] Short read-only consistent snapshots and statement timeouts have PostgreSQL integration tests.
- [ ] No generic SQL agent, model-generated SQL endpoint or ORM objects in tool responses.

### T08 — Implement PostgreSQL roles and row isolation

Priority: P0 | Size: M | Role: Backend/security | Depends on: T06, T07

Scope: Create restricted roles, RLS policies, transaction-local identity context and private checkpoint-schema grants.

- [ ] Business-read cannot write and runtime roles do not bypass ownership policies.
- [ ] Missing scope denies access; cross-tenant/customer fixtures fail under actual restricted roles.
- [ ] Sequential pooled requests cannot inherit another request's identity context.

### T09 — Implement data lifecycle and encryption boundaries

Priority: P0 | Size: M | Role: Backend/security | Depends on: T06, T07, T08

Scope: Define customer contact/VIN encryption adapter, retention services and deletion orchestration contract, including a checkpoint purge hook.

- [ ] Ciphertext and key references remain separate; production refuses a fake encryption implementation.
- [ ] Retention rules preserve required business history and remove eligible conversation records.
- [ ] Deletion orchestration is idempotent; checkpoint purge contract is tested with a stub and finalized in T32.

## M03 — Identity and security

### T10 — Implement scoped guest sessions

Priority: P0 | Size: M | Role: Backend | Depends on: T02, T06, T08

Scope: Issue expiring opaque guest sessions and implement the trusted principal boundary.

- [ ] Only session hashes are stored; cookie protections and expiry are enforced.
- [ ] Guest ownership is enforced for each conversation request.
- [ ] Guests cannot invoke personal order/service access even with known reference numbers.

### T11 — Integrate OIDC and verified customer mapping

Priority: P1 | Size: M | Role: Backend/security | Depends on: T10

Scope: Implement identity adapter, token/session verification, role mapping and verified principal-to-customer association. External: OIDC provider details and mapping rules.

- [ ] Issuer, audience, signature and expiry are checked; customer IDs are never accepted as proof of identity.
- [ ] Restricted customer lookups succeed only for owned records.
- [ ] Dev auth is isolated; production capability stays disabled until real configuration is verified.

### T12 — Add request and browser security controls

Priority: P0 | Size: M | Role: Backend/frontend | Depends on: T10, T03

Scope: CSRF/origin checks, exact CORS, payload limits, rate limiting and safe error responses.

- [ ] Cross-origin/CSRF abuse and oversized requests fail predictably.
- [ ] Rate limits cover guest session creation and chat; document the multi-replica enforcement mechanism.
- [ ] Errors disclose no credentials, private SQL details or customer records.

### T13 — Implement outbound and action URL policy

Priority: P0 | Size: S | Role: Security/backend | Depends on: T03, T06

Scope: Canonical URL validation, configured provider hosts, approved action hosts/paths and safe query parameters.

- [ ] Unsafe schemes, encoded host bypasses, URL userinfo and unapproved destinations are rejected.
- [ ] Query strings cannot carry private customer data or tokens.
- [ ] External integration redirects are checked or disabled; no arbitrary fetch tool is exposed.

## M04 — Business tools

### T14 — Implement catalog, showroom and media tools

Priority: P1 | Size: M | Role: Backend | Depends on: T02, T07, T08, T13

Scope: SQLAlchemy-backed `search_cars`, `get_car_details`, `get_showroom_info` and typed tool results.

- [ ] Model/year/variant filters and bounded results work against fictional seed records.
- [ ] Brochures/images come from approved asset records; VINs/private fields never appear.
- [ ] Ambiguous matches return candidates for clarification, not an arbitrary selection.

### T15 — Implement live offer and availability tool

Priority: P0 | Size: M | Role: Backend/data | Depends on: T14

Scope: `get_current_offer` through SQLAlchemy with consistent price/stock snapshot and freshness rules.

- [ ] Returns Decimal-backed values, currency, qualifiers, validity and snapshot timestamp.
- [ ] Only available units count; reserved/in-transit/sold are distinguished.
- [ ] Conflicting offers, stale imported feeds and DB failures produce explicit outcomes.
- [ ] Concurrent price-update test proves a valid snapshot; no transaction spans LLM work.

### T16 — Implement authorized order and service tools

Priority: P1 | Size: M | Role: Backend | Depends on: T11, T07, T08

Scope: `get_my_order_status` and `get_my_service_status` with server-injected customer identity.

- [ ] Customer sees only allowed public fields for owned records.
- [ ] Known references cannot bypass identity/ownership checks.
- [ ] Missing identity integration yields sign-in/portal guidance, not fake personal status.

### T17 — Implement approved next-action resolver

Priority: P1 | Size: S | Role: Backend | Depends on: T13, T02, T07, T08

Scope: `get_next_action` and action resolution for quote, test-drive, finance enquiry, service and human support.

- [ ] Tool takes action codes, not arbitrary URLs; registry controls audience/enabled status.
- [ ] Output conforms to action-card contract and indicates authentication requirements.
- [ ] No form is auto-submitted and no booking completion is claimed.

### T18 — Validate business tool repository contracts

Priority: P0 | Size: M | Role: Backend/QA | Depends on: T14, T15, T16, T17

Scope: Consolidate restricted-role integration cases and validate all business-tool outputs against shared envelopes.

- [ ] Empty, denied, unavailable and invalid-input outcomes remain distinguishable.
- [ ] SQL injection/filter abuse tests pass through SQLAlchemy repositories.
- [ ] Session cleanup, timeout and cancelled-query tests show no pool leak.

## M05 — RAGFlow knowledge

### T19 — Implement RAGFlow Cloud retrieval client

Priority: P1 | Size: M | Role: Backend | Depends on: T02, T03, T13

Scope: Async HTTPX client for retrieval with auth, deadline, body-code checking and normalized document evidence.

- [ ] Contract fixtures cover success, empty retrieval, malformed response and HTTP/business failures.
- [ ] API key stays server-side; customer input cannot choose datasets or cloud URLs.
- [ ] Configured result limits are enforced and source identifiers retained.

### T20 — Enforce source publication and document scope

Priority: P0 | Size: M | Role: Backend/content | Depends on: T19, T06, T08

Scope: Join retrieval evidence with approved source metadata and effective market/year/variant rules.

- [ ] Unapproved/expired/wrong-market/private evidence is excluded before generation.
- [ ] Citation IDs resolve to accessible titles/assets without leaking private cloud URLs.
- [ ] Conflicting policy/specification evidence produces an explicit ambiguity outcome.

### T21 — Document content publishing and onboarding

Priority: P1 | Size: S | Role: Content/backend | Depends on: T20

Scope: Operator instructions for uploading, parsing, validating and publishing official brand documents. External: actual approved brand content.

- [ ] Workflow distinguishes upload, processing completion and approval for retrieval.
- [ ] Required metadata and document-owner responsibilities are documented.
- [ ] Fictional sample documents demonstrate questions and citations; real-content gap is visible.

### T22 — Verify deployed cloud retrieval contract

Priority: P1 | Size: S | Role: Backend/QA | Depends on: T19, T20, T21

Scope: Opt-in live smoke test against authorized RAGFlow Cloud configuration. External: endpoint/key and approved test dataset.

- [ ] Tests verify actual response shape, authentication, scoping and citations.
- [ ] Fixture/version changes discovered in cloud are documented and tested.
- [ ] Report distinguishes live verification from mocks; no credentials or source content in logs.

## M06 — LLM portability

### T23 — Define canonical provider interface and mock model

Priority: P0 | Size: M | Role: AI/backend | Depends on: T02, T03

Scope: Canonical messages/tool calls/events/usage/errors, provider registry and deterministic local adapter.

- [ ] Graph contracts contain no provider-specific objects.
- [ ] Stream handling waits for complete tool arguments and preserves call/result pairing.
- [ ] Mock mode supports representative tool routing and is rejected in production.

### T24 — Implement OpenAI adapter

Priority: P1 | Size: S | Role: AI/backend | Depends on: T23

Scope: Provider package integration with configurable model, tool schema binding and normalized streaming/errors.

- [ ] Tool calls, text, nullable usage and cancellation pass canonical contract tests.
- [ ] Missing credentials and unsupported configured capabilities fail explicitly.
- [ ] No hardcoded model alias or browser-side secret dependency.

### T25 — Implement Anthropic Claude adapter

Priority: P1 | Size: S | Role: AI/backend | Depends on: T23

Scope: Claude integration behind the same interface, including provider-specific tool-result conversion.

- [ ] Multi-turn tool history and streaming normalize correctly.
- [ ] Errors/context limits do not leak provider-specific types into graph state.
- [ ] Same canonical test scenarios used for OpenAI pass for Claude fixtures.

### T26 — Implement DeepSeek and switching policy

Priority: P1 | Size: M | Role: AI/backend | Depends on: T23, T24, T25

Scope: DeepSeek adapter plus cross-provider configuration/capability and disabled-by-default fallback policy.

- [ ] DeepSeek passes canonical tools/stream/usage/error fixtures.
- [ ] Provider can change between turns without changing tools or corrupting history; active-run changes are rejected.
- [ ] Fallback only uses approved configured providers and does not mix partial answers or replay completed work.
- [ ] Opt-in smoke command reports live compatibility separately for each supplied provider/model.

## M07 — LangGraph orchestration

### T27 — Implement persona, graph state and intent routing

Priority: P1 | Size: M | Role: AI/backend | Depends on: T02, T23

Scope: Versioned showroom persona, canonical state and routing/clarification nodes using typed mocked evidence.

- [ ] Greetings, product, live offer, after-sales and next-action requests route correctly.
- [ ] Unresolved variant/branch prompts one focused clarification.
- [ ] State excludes raw secrets; principal scope is injected from the current request.

### T28 — Implement bounded authorized tool executor

Priority: P0 | Size: M | Role: AI/backend | Depends on: T27, T14, T15, T16, T17, T20

Scope: Register tools; enforce schemas, authorization, dependency ordering, deadlines, retries and concurrency limits.

- [ ] Unknown/malformed/unauthorized calls never execute.
- [ ] Current-price requests require fresh commercial evidence; personal-status requests require identity.
- [ ] Round/call/deadline limits and cancellation terminate work predictably.
- [ ] Independent tools preserve separate DB sessions and correct result pairing.

### T29 — Implement evidence validation and response assembly

Priority: P0 | Size: M | Role: AI/backend | Depends on: T28

Scope: Gather evidence, generate draft, validate sources/numerical claims and render deterministic commercial/action cards.

- [ ] Old chat/brochure prices cannot override current offer facts.
- [ ] Unsupported statements trigger bounded repair or safe partial-answer template.
- [ ] Final response uses approved sources/actions; missing data never becomes zero.

### T30 — Integrate graph with all model providers

Priority: P1 | Size: M | Role: AI/backend | Depends on: T29, T26

Scope: Complete graph invocation interface and provider-independent customer scenario fixtures.

- [ ] Same graph works with OpenAI/Claude/DeepSeek adapters without tool changes.
- [ ] Model/provider/prompt versions are recorded per run.
- [ ] Provider timeout and tool failure paths preserve verified evidence and produce safe responses.

## M08 — Conversation API and state

### T31 — Implement owned conversation and run endpoints

Priority: P0 | Size: M | Role: Backend | Depends on: T02, T10, T12, T06

Scope: Conversation create/read/delete request, run creation/status and database-backed idempotency/lease repository.

- [ ] Every endpoint validates current principal ownership.
- [ ] Duplicate idempotency keys do not create duplicate runs/messages.
- [ ] Concurrent requests acquire one lease per conversation across processes; no long-lived DB lock.

### T32 — Integrate PostgreSQL graph checkpoints

Priority: P0 | Size: M | Role: Backend | Depends on: T31, T27, T09

Scope: Restricted checkpointer persistence, opaque thread mapping, authorized load/resume and deletion hook.

- [ ] Restart can load persisted conversation state without public checkpoint access.
- [ ] Current authorization is revalidated on resume; saved identity does not grant access.
- [ ] Conversation deletion purges its checkpoints idempotently and passes lifecycle tests.

### T33 — Connect graph execution and SSE delivery

Priority: P1 | Size: M | Role: Backend | Depends on: T30, T31, T32

Scope: Run the graph from the message API; persist finalized output and emit the agreed streaming events.

- [ ] Status/heartbeat events precede validated answer chunks, sources, cards and `done`.
- [ ] Internal reasoning, tool arguments and private results are never streamed.
- [ ] Final message/run status is recoverable through the status API.

### T34 — Implement cancellation and abandoned-run recovery

Priority: P0 | Size: M | Role: Backend | Depends on: T33

Scope: Cancellation, lease heartbeat/expiry, crash cleanup and reconnect semantics.

- [ ] Browser disconnect cancels read work where possible and records a terminal/recoverable outcome.
- [ ] Expired leases cannot corrupt a newer run; lease updates verify ownership/run ID.
- [ ] Retry/status recovery after process failure does not duplicate customer-visible messages.

## M09 — React customer experience

### T35 — Build React chat layout and typed client

Priority: P1 | Size: M | Role: Frontend | Depends on: T01, T02

Scope: Responsive transcript, composer, React state and typed API client developed against contract fixtures.

- [ ] Keyboard interaction, labels, focus and mobile layouts work.
- [ ] Sending/loading/empty/error states are clear; duplicate send is prevented locally.
- [ ] Restricted Markdown rendering rejects raw HTML/unsafe links.

### T36 — Integrate conversation, identity and SSE state

Priority: P1 | Size: M | Role: Frontend | Depends on: T35, T33, T11

Scope: Connect real guest/customer APIs and streaming fetch to React conversation state.

- [ ] Parser handles network-fragmented SSE frames and safe error/done events.
- [ ] Expired sessions and sign-in-required actions are handled without private-data flashes.
- [ ] Conversation switching does not append events to the wrong transcript.

### T37 — Build product, price, source and action cards

Priority: P1 | Size: M | Role: Frontend | Depends on: T35, T14, T15, T17, T20

Scope: Approved media, brochure links, source references, offer qualifiers/availability and external action UI.

- [ ] Money/currency/time are localized and `as_of` is displayed clearly.
- [ ] Unavailable data is visibly different from zero stock; cards do not invent facts.
- [ ] Actions show destination purpose/auth requirement and do not imply completion.

### T38 — Finish recovery and browser interaction checks

Priority: P1 | Size: M | Role: Frontend/QA | Depends on: T36, T37, T34

Scope: Reconnect/status recovery, cancellation, accessible notifications and browser tests.

- [ ] Reload/disconnect recovers the run state without duplicate answers.
- [ ] Guest/new-customer and authenticated after-sales flows work at desktop/mobile sizes.
- [ ] Frontend bundle contains no secrets; sanitization and unsafe asset/link cases are tested.

## M10 — OpenTelemetry and operations

### T39 — Bootstrap OTel SDK, Collector and Jaeger

Priority: P0 | Size: S | Role: Platform/backend | Depends on: T01, T03

Scope: Instrument HTTP entry/client boundaries and configure local OTLP export and trace viewer.

- [ ] A local API request is visible with service/version/environment attributes.
- [ ] SDK/Collector queues are bounded and exporter failure does not fail the request.
- [ ] Local startup and trace inspection commands are documented.

### T40 — Instrument graph, tools, models and database

Priority: P1 | Size: M | Role: Backend/platform | Depends on: T39, T30, T33, T07

Scope: Explicit span wrappers and safe attributes for graph/model/tool/retry/validation operations.

- [ ] Async tools and retries appear under the correct request trace.
- [ ] Stream/cancellation spans end correctly; SQLAlchemy/psycopg instrumentation is not duplicated.
- [ ] RAGFlow HTTP timing is shown without claiming visibility into cloud internals.

### T41 — Add structured logs, metrics and dashboards

Priority: P1 | Size: M | Role: Platform | Depends on: T40

Scope: Correlated JSON logs, latency/error/usage/freshness/pool/exporter metrics and dashboard/alert definitions.

- [ ] Request/run/trace correlation supports debugging without capturing raw content.
- [ ] No customer/conversation identifiers appear as metric labels.
- [ ] Unknown token usage stays unknown; estimated cost uses an explicit dated rate configuration.
- [ ] Dashboards distinguish status-event latency from validated-answer latency.

### T42 — Verify telemetry redaction and resilience

Priority: P0 | Size: S | Role: Security/platform | Depends on: T40, T41

Scope: Sensitive sentinel tests, exporter-outage tests and sampling/retention runbook.

- [ ] Test secrets, VINs, contact info and prompt/tool content are absent from default spans/logs.
- [ ] Telemetry outage drops/buffers within limits without failing chat.
- [ ] Runbook explains retention, access controls and sampling limits; audits remain separate.

## M11 — Acceptance and evaluation

### T43 — Create showroom evaluation scenarios

Priority: P1 | Size: S | Role: QA/product | Depends on: T02, T05, T21

Scope: Fictional labeled examples covering the five business capabilities and language/variant ambiguity.

- [ ] Expected tools, sources, facts and approved next steps are specified per case.
- [ ] Stale brochure price and conflicting year/variant examples are included.
- [ ] Dataset contains no real customer records and separates deterministic checks from optional model judges.

### T44 — Run end-to-end customer acceptance suite

Priority: P0 | Size: M | Role: QA/full stack | Depends on: T38, T43, T30

Scope: Execute React → API → graph → tools → database/retrieval → response scenarios.

- [ ] All five required capabilities work with documented fixtures.
- [ ] Numeric/citation/action correctness assertions pass, not just HTTP success checks.
- [ ] Test report explicitly names mocked versus live dependencies.

### T45 — Run authorization and abuse regression suite

Priority: P0 | Size: M | Role: Security/QA | Depends on: T18, T20, T34, T38, T42

Scope: Cross-customer/tenant access, expired sessions, prompt injection, SQL/filter abuse, unsafe redirect and frontend XSS cases.

- [ ] Restricted-role tests demonstrate database isolation as well as API checks.
- [ ] Documents/tool outputs cannot bypass mandatory authorization or tool policies.
- [ ] No private data leaks through UI, traces, logs, assets or errors.

### T46 — Run failure, concurrency and load suite

Priority: P0 | Size: M | Role: QA/platform | Depends on: T34, T41, T44

Scope: Retry/deadline/provider failures, concurrent updates/runs, disconnects, database pool pressure and restart recovery.

- [ ] Run/message idempotency and consistent-offer behavior hold under concurrency.
- [ ] Measured latency/error/pool behavior is reported against a stated test load.
- [ ] Bottlenecks and unmet proposed targets are documented rather than hidden by mock timings.

## M12 — Neon and release

### T47 — Package frontend, backend and local services

Priority: P1 | Size: M | Role: Platform/full stack | Depends on: T04, T38, T39

Scope: Container builds, React static bundle, ingress routing, Compose and configuration documentation.

- [ ] Clean checkout starts the documented local stack and fictional demo.
- [ ] Production artifact separates public frontend settings from server secrets.
- [ ] Ingress supports streaming/heartbeats and routes `/api` correctly.

### T48 — Validate Neon staging and live integrations

Priority: P0 | Size: M | Role: Platform/backend | Depends on: T47, T08, T22, T26, T32

Scope: Authorized staging configuration for pooled runtime/direct migration connections, TLS and checkpoint behavior. External: approved Neon environment and integration credentials.

- [ ] Migrations run with the migration role; restricted runtime queries pass against Neon.
- [ ] Pooling/transaction-local identity/checkpointer compatibility are tested, including cold-start behavior.
- [ ] Live provider and RAGFlow results are recorded individually; unavailable credentials remain explicit blockers.

### T49 — Prepare release gates and restore runbook

Priority: P0 | Size: M | Role: Platform/security | Depends on: T48, T45, T46, T42

Scope: Backup/restore exercise, rollback procedure, alert ownership, retention and deployment checklist.

- [ ] Staging restore/rollback is exercised without production/customer-data copying.
- [ ] Real brand sources, prices, identity mapping, URLs and enabled models are approved/configured.
- [ ] Release gate records evidence and unresolved risks; production activation awaits authorization.

### T50 — Handover documentation and implementation status

Priority: P1 | Size: S | Role: Full stack/product | Depends on: T49

Scope: README, support runbook, architecture delta and card-to-acceptance completion report.

- [ ] Setup/test/trace/troubleshooting commands work from a clean environment.
- [ ] Operators can diagnose failed retrieval, stale offers, provider failures and customer-access problems.
- [ ] Completed, mock-only, blocked and deferred features are distinguished; no unverified production claim.

## M13 — Optional next iterations

### F01 — Add public web search tool

Priority: P2 | Size: M | Role: AI/backend | Depends on: T28, T13, T42

Scope: Implement the optional configured search provider for relevant public updates.

- [ ] Disabled by default; no private identifiers/history in search queries.
- [ ] Sources/dates are retained and public news cannot override showroom commercial data.
- [ ] Live structured information uses an appropriate service API where search freshness is insufficient.

### F02 — Integrate DMS/CRM data synchronization

Priority: P2 | Size: M | Role: Data/backend | Depends on: T15, T41

Scope: First approved feed with idempotent updates, version/cursor tracking and lag visibility. Split by upstream resource once the external contract is known.

- [ ] Out-of-order/duplicate events do not overwrite newer values.
- [ ] Freshness threshold can disable unverified offers.
- [ ] Source-of-truth and recovery procedures are documented.

### F03 — Add confirmed booking or lead creation

Priority: P2 | Size: M | Role: Backend/product | Depends on: T17, T11, T45

Scope: Design and implement one explicitly authorized write workflow after business API/consent requirements are approved; split by action.

- [ ] Customer confirmation is explicit and operation idempotency prevents duplicates.
- [ ] Reliable delivery/reconciliation and audit records exist.
- [ ] No completion is claimed until the target system confirms it.

### F04 — Optimize provider routing and answer latency

Priority: P2 | Size: M | Role: AI/platform | Depends on: T46, T26, T43

Scope: Use measured quality/cost/latency to propose routing or streaming changes.

- [ ] Changes retain deterministic commercial facts and approved provider boundaries.
- [ ] Evaluation and load comparison show benefit before rollout.
- [ ] Rollback and per-provider budget controls are documented.

## 4. External inputs register

| Input | Affected cards | Local development approach |
|---|---|---|
| Brand identity, catalog, approved documents | T14, T21, T43, T49 | Clearly fictional showroom fixtures |
| Pricing/inventory source-of-truth and commercial rules | T15, T48, F02 | Authoritative local PostgreSQL fixtures |
| OIDC/customer mapping | T11, T16, T36, T49 | Dev-only identity adapter; production personal tools disabled |
| RAGFlow Cloud key/endpoint/test dataset | T22, T48 | Recorded/synthetic contract fixtures |
| Exact LLM IDs and provider credentials | T24–T26, T48 | Adapter fixtures plus deterministic mock |
| Approved form/media/application URLs | T13, T17, T37, T49 | Nonproduction fixtures; no fabricated production destination |
| Authorized Neon/hosting/OTLP destination | T48–T49 | Local PostgreSQL/Collector/Jaeger and deploy configuration |

## 5. Suggested card description template

```text
Card: [ID] Verb + concrete outcome
Module:
Priority / size:
Owner:
Dependencies: linked cards
Specification: link to relevant design section

Scope:
Acceptance checklist:
Test / review evidence:
External inputs or blockers:
Implementation links:
```

Keep feature dependencies in the description and use checklists for execution steps. A blocked external integration is not complete merely because its mock passes; retain the card in Blocked/Verify and attach the local progress evidence.
