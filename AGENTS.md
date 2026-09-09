# Observatory — agent entry point

Self-hosted Unity game platform; first game is *The Lost Observatory*. Stack and coding rules: [.cursorrules](.cursorrules).

Planned layout: `apps/game-unity` (Unity 6.3 LTS / C#), `apps/web` (React + TypeScript), `apps/api` (FastAPI), Keycloak at `auth.createit.digital` (profile, off until `/admin/`). One production-named Droplet first, gated; staging Droplet later. See [game-platform-base-plan_v2.1.md](game-platform-base-plan_v2.1.md).

## Agent workflow

| Topic | File |
|-------|------|
| **Flow manifest** | [.agent/manifest.json](.agent/manifest.json) — `hosting`, `pack_source`, `default_scope` |
| **Skill catalog** | [.agent/skills.catalog.json](.agent/skills.catalog.json) |
| **Review context SSOT** | [.agent/review-context.json](.agent/review-context.json) |
| **Orchestration** | [docs/agents/README.md](docs/agents/README.md) |
| **Quick ref** | [docs/utils/CURSOR_AGENT_WORKFLOW.md](docs/utils/CURSOR_AGENT_WORKFLOW.md) |
| **Bugbot (pre-push)** | [.cursor/BUGBOT.md](.cursor/BUGBOT.md) |
| **Roles + verbs** | [docs/agents/prompts/ROLES.md](docs/agents/prompts/ROLES.md) |

Active LOOP program: see review-context SSOT → `active_program` (`null` when idle).

**LOOP contract:** The agent **executes until the program is done**. Do **not** ask “Continue?”. Local commit every phase. Honour `hosting.kind` — no GitHub PR or Revy unless this repo actually has them. **Only pause:** migration subphase.

Read **only** the current `*_Pn_EXECUTION.md`. Each subphase Deliverable must be green before the next heading — then continue immediately.

### Skills (installed)

| Tier | Skills |
|------|--------|
| **Meta** | `bootstrap-workflow` |
| **Core** | `phase-execution`, `ship-changes`, `chunk-execution` |
| **Planning** | `create-findings`, `create-general-plan`, `create-execution-plan`, `architecture-peer-review`, `execution-peer-review`, `devils-advocate`, `post-finish-gap-pass` |
| **Docs export** | `md-formatting`, `mermaid-diagrams`, `md-docx-export`, `docx-md-export` |

Not installed: `babysit-revy-pr` (no GitHub/Revy), `sentry-fix-issues` (no Sentry MCP yet), `staging-validation`.

Re-audit: invoke `bootstrap-workflow` against `pack_source.path` (sibling `../agent-workflow`).

**Default gate:** local Bugbot before every ship.

**Scope:** manifest default is `docs/**` until application trees exist. Widen in `review-context.json` `programs[].scope` when a program needs `.agent/**`, `.cursor/**`, `apps/**`, or `infrastructure/**`.

## DevOps docs

DigitalOcean work uses [docs/devops/README.md](docs/devops/README.md): findings → general plan → one spec per operation in [docs/devops/operations/](docs/devops/operations/README.md) (distilled from Revy, adapted). Each shipped operation updates `docs/runbooks/` (created on first ship). Locked shape: everything deployable is an image (`web`, `api`; `keycloak` as profile `identity`), host Nginx is edge-only, one production Droplet first behind basic auth. Do not use Terraform/Kubernetes. Do not copy kp-platform deploy workflows.

Program state: bootstrap **done**; DevOps at *general plan + operations* — next is `create-execution-plan` for P0–P6.
