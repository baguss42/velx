# VelX UI design guide

Status: initial MVP design baseline. No frontend has been implemented yet. The visual defaults below are a starting design, not an approved dealership brand identity.

## Purpose and references

Use this document for every frontend task to keep layout, styling, components, and interaction behavior consistent. Update it whenever a shared design decision changes.

- [Implementation design](docs/BLUEPRINT/car-showroom-chatbot-implementation.md): product behavior, architecture, and API contracts.
- [Build prompt](docs/BLUEPRINT/car-showroom-chatbot-build-prompt.md): frontend implementation requirements.
- [Agent instructions](AGENTS.md): task workflow and verification policy.

The implementation design governs business behavior; this document governs UI presentation. Ask the human about conflicting requirements or missing brand decisions. Do not invent dealership logos, official assets, or commercial claims.

## Design direction

Build a calm, readable, mobile-friendly showroom chat. Prioritize the conversation, verified vehicle information, and clear next actions. Use neutral surfaces, restrained blue accents, generous spacing, and simple borders. Avoid decorative effects that compete with vehicle photos or messages.

Default presentation uses Indonesian, IDR, and Asia/Jakarta as specified in the blueprint; all are configurable. Use a system font stack and approved vehicle imagery. No external font or component library is selected by this document.

## Shared design tokens

Define these defaults once as CSS custom properties in the frontend's shared stylesheet. Reuse semantic tokens rather than duplicating values in individual components. The initial implementation lives in `frontend/src/styles.css`; update this guide when shared UI decisions change.

| Token | Initial value | Use |
|---|---|---|
| `--color-background` | `#F8FAFC` | Application background |
| `--color-surface` | `#FFFFFF` | Cards, assistant messages, composer |
| `--color-surface-muted` | `#F1F5F9` | Secondary panels and disabled backgrounds |
| `--color-text` | `#0F172A` | Primary text |
| `--color-text-muted` | `#475569` | Supporting text and timestamps |
| `--color-border` | `#CBD5E1` | Decorative dividers and card outlines |
| `--color-control-border` | `#64748B` | Input and control boundaries |
| `--color-primary` | `#1D4ED8` | Primary buttons and links |
| `--color-primary-hover` | `#1E40AF` | Primary hover state |
| `--color-on-primary` | `#FFFFFF` | Text on primary backgrounds |
| `--color-focus` | `#2563EB` | Visible keyboard focus ring |
| `--color-success` | `#166534` | Confirmed success text and icons |
| `--color-warning` | `#92400E` | Stale information and caution text |
| `--color-danger` | `#B91C1C` | Error text and destructive controls |
| `--font-sans` | `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif` | All UI text |
| `--radius-control` | `8px` | Inputs and buttons |
| `--radius-card` | `12px` | Cards and messages |
| `--shadow-raised` | `0 4px 16px rgb(15 23 42 / 8%)` | Floating surfaces only |

- Spacing scale: `4`, `8`, `12`, `16`, `24`, `32`, `48` px. Default control gap: 8px; card padding: 16px; section gap: 24px.
- Type scale: 12px metadata, 14px supporting text, 16px body/input text, 20px section titles, 24px page titles. Body line height: 1.5. Use weights 400, 500, and 600 consistently.
- Interactive targets: at least 44 × 44px where practical; primary buttons and composer controls use a minimum height of 44px.
- Focus ring: 2px solid focus color with a 2px offset. Never remove focus outlines without an equally visible replacement.
- Motion: 150ms for color/opacity transitions. Respect reduced-motion preferences. Avoid animated message text and unnecessary entrance animations.
- Light theme only for the initial baseline. Ask before introducing additional themes or replacing the palette with brand colors.

## Layout and responsiveness

- Use a full-height chat shell: compact header, scrollable conversation, and bottom composer. Account for mobile safe areas and the on-screen keyboard; the composer must not obscure messages or focused controls.
- Center the conversation in a container no wider than 800px. Use 16px horizontal gutters on small screens and 24px from 768px upward.
- Below 768px, stack cards and actions vertically. At 768px and above, use up to two columns for compact related vehicle cards when content fits. Reading order must remain unchanged.
- Assistant messages align left; customer messages align right. Customer bubbles use the primary background and on-primary text. Assistant bubbles use the surface background and primary text.
- Text bubbles use up to 85% of available width; structured assistant cards may use the full conversation width. Wrap long text and URLs without page-level horizontal scrolling.
- Use consistent card headers, content spacing, source placement, and action placement. Do not add sidebars or navigation areas without a task requirement.
- Auto-scroll only when the reader is near the latest message or sends a message. Otherwise preserve their position and offer a “Pesan terbaru” control.

## Component inventory

Proposed component names below establish shared responsibilities, not files that already exist. Keep reusable presentation in `frontend/src/components/`, conversation behavior in `frontend/src/features/`, transport in `frontend/src/api/`, and contracts in `frontend/src/types/`.

| Component | Required content and behavior |
|---|---|
| `ChatShell` | Configured showroom name, conversation region, composer, and connection/session notice |
| `MessageBubble` | Sender distinction, safe Markdown, readable text, and delivery/error state |
| `MessageComposer` | Labeled multiline input, send control, pending state, and cancel control during an active run |
| `ProgressStatus` | Short customer-facing status; no internal reasoning, prompts, or raw tool data |
| `VehicleCard` | Model, year, variant, approved image, and supported details; preserve variant identity |
| `OfferCard` | Server-provided price, currency, qualifiers, availability, branch when applicable, and freshness timestamp |
| `SourceCard` | Human-readable approved source title and safe link; citations visibly associated with the answer |
| `ActionCard` | Clear action label and server-approved destination; sign-in requirement or external destination notice when applicable |
| `InlineNotice` | Text plus icon for information, warning, or error; recovery action only when supported |
| `Button` and `TextInput` | Shared sizes, focus styles, labels, disabled state, and pending state |

Use one icon family once selected. Label icon-only buttons accessibly; decorative icons must not add duplicate screen-reader output. Use approved images with meaningful alt text; maintain a 16:9 vehicle image area with `object-fit: contain` to avoid cropping the vehicle. Missing media gets a neutral placeholder, not an invented product image.

## Interaction and state rules

| State | Presentation and behavior |
|---|---|
| Empty conversation | Short introduction and suggested prompts about showroom information, vehicles, or test drives; do not imply unsupported capabilities |
| Draft | Keep typed content while the customer edits; Enter sends, Shift+Enter inserts a newline; Enter during IME composition must not send |
| Request pending | Prevent duplicate sends; show status and allow cancellation when supported; do not fabricate an answer while waiting |
| Answer delivery | Display only validated answer chunks and deterministic cards from the API; do not simulate unvalidated model streaming |
| Completed | Clear pending indicators and retain message, source, and card associations |
| Empty lookup | Explain that no matching result was found; offer clarification when applicable |
| Unavailable or stale lookup | Explain that current information cannot be verified; never replace unknown price or stock with zero |
| Request error | Preserve recoverable input and show a safe explanation; offer retry only using the API's idempotency/status rules |
| Disconnected or reconnecting | Show connection state and recover run status before resubmitting; prevent duplicate messages |
| Cancelled | Show that generation stopped without implying business action occurred |
| Sign-in required or expired | Explain the access requirement and offer the approved sign-in/portal action; do not expose personal records |

## Content and business data

- Use short, friendly, specific wording. Example loading text: “Sedang mencari informasi…”; unavailable price: “Harga saat ini belum dapat diverifikasi.”
- Label actions by their actual outcome: “Buka formulir test drive” rather than “Test drive berhasil dipesan”. Opening a form is not a completed booking, quotation, payment, or application.
- Format currency and timestamps with configured locale and timezone. Preserve authoritative monetary precision; never calculate quotations in presentation code or round into an unsupported claim.
- Display source titles, model year/variant, price qualifiers, and `as_of` where applicable. Explain availability as information, not a reservation.
- Keep development vehicles and prices clearly labeled as fictional. Brand identity, live data, and approved external destinations come from configuration and backend contracts.
- Render restricted Markdown with raw HTML disabled or sanitized, safe link protocols, and approved media URLs. Do not display raw exceptions, internal IDs, credentials, or model reasoning.

## Accessibility and manual review

Use semantic buttons, links, headings, and form labels. Keep keyboard order aligned with visual order. Announce short progress/completion updates through a polite live region without repeatedly reading the entire streaming response. Errors must remain visible and understandable without color alone.

Design targets: text contrast of at least 4.5:1 for normal text and 3:1 for large text; meaningful controls and focus indicators should remain distinguishable with at least 3:1 contrast against adjacent colors. Verify actual foreground/background pairs when styles are implemented; token values alone do not establish compliance.

For each UI task, manually review relevant items and record results in the PR. Follow `AGENTS.md`: unit and integration tests are skipped under the MVP policy.

- Check the changed view at 360px, 768px, and 1280px widths, plus 200% zoom, for overflow and obscured controls.
- Walk through keyboard navigation, visible focus, labels, and relevant screen-reader announcements.
- Inspect relevant empty, pending, error, unavailable, and success states.
- Check long messages, long source titles, missing images, and localized prices/timestamps.
- Confirm shared tokens/components are reused, approved actions remain accurate, and the mobile composer stays usable.
- Record actual checks and limitations; leave unperformed checks unverified.

## Maintenance and decision template

Before a frontend task, read this guide and inspect existing shared components. When changing a shared token, component, or interaction, update this document and `MEMORY.md` in the same task PR. Record the implemented file paths once they exist. Ask the human before changing business behavior, brand identity, or unclear requirements.

Use this template for future shared design decisions:

```markdown
### YYYY-MM-DD — Decision title

- Task / PR: <task ID and PR link, when available>
- Status: <proposed / accepted / superseded>
- Problem: <user need or inconsistency>
- Decision: <exact token, component, layout, or behavior change>
- Affected components / files: <actual paths>
- States / responsive behavior: <relevant cases>
- Accessibility: <impact and checks>
- Verification: <checks actually performed and results>
- Human clarification: <confirmed direction or unresolved question>
```

### 2026-09-13 — Initial UI baseline

- Task / PR: documentation request; no task ID or PR supplied.
- Status: proposed visual defaults; product behavior follows the existing blueprint.
- Decision: neutral light surfaces, blue primary actions, system typography, shared spacing, and a responsive conversation-first layout.
- Affected files: `DESIGN.md`, `AGENTS.md`, `MEMORY.md`. Frontend component and stylesheet paths are pending scaffolding.
- Verification: document consistency and local references reviewed. No rendered UI exists to inspect.
- Human clarification: official brand identity and approved media remain unspecified. Do not invent them.

### 2026-09-13 — T01 placeholder chat shell

- Task / PR: T01 — Scaffold Python backend and React frontend
- Status: implemented foundation
- Decision: use `frontend/src/styles.css` for the shared design tokens and a conversation-first placeholder shell with the configured `/api` health status.
- Affected components / files: `frontend/src/App.tsx`, `frontend/src/components/ChatShell.tsx`, `frontend/src/styles.css`, `frontend/src/vite.config.ts`.
- States / responsive behavior: checking, connected, and disconnected API status; mobile composer stacks below 768px; safe-area padding is included.
- Accessibility: semantic heading, labeled composer, status announcement, visible focus ring, and minimum 44px controls.
- Verification: `npm --prefix frontend run format:check`, `npm --prefix frontend run typecheck`, and `npm --prefix frontend run build` passed. Browser smoke review passed at 360px, 768px, and 1280px with no horizontal overflow; interactive labels and visible focus styles were inspected.
- Human clarification: official brand identity and approved media remain unspecified; placeholder copy stays generic.
