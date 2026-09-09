# docs/devops/README.md

# DevOps program

DigitalOcean hosting for Observatory: droplets, host Nginx, domains, TLS, firewall, container registry, Compose deploy. Product topology is locked in [game-platform-base-plan_v2.1.md](../../game-platform-base-plan_v2.1.md). This folder is the **program**. Living how-to lives under `docs/runbooks/`.

**Provider:** DigitalOcean. **Not** Terraform, Kubernetes, or CDN (game plan: out of current scope).

---

## How we work

```text
findings  →  general plan  →  one markdown file per operation  →  LOOP
                │
                └── each shipped operation updates docs/runbooks/<component>.md
```

| Layer | Where | Role |
|:---|:---|:---|
| **Findings** | `DEVOPS_FINDINGS.md` | Baseline: what exists, exclusions, locked decisions. No steps. |
| **General plan** | `DEVOPS_GENERAL_PLAN.md` | Phases/goals only. One phase ≈ one operation (or a tight cluster). |
| **Operation spec** | [`operations/<name>.md`](./operations/README.md) | Durable “how this component is set up here” — Nginx, domain, Certbot, UFW, registry, droplet, deploy. Distilled from Revy with per-file source + delta. |
| **Execution** | `*_Pn_EXECUTION.md` | LOOP steps for that phase. Written after the general plan. |
| **Runbook** | `docs/runbooks/<name>.md` | Operator repeat: deploy, rollback, restore, renew certs, open ports. Updated **when the operation ships**, not invented empty. |

Do not paste kp-platform `.github/workflows/deploy.yml`. Patterns come from Revy (`~/projects/revy`) and are adapted to **this** stack (edge-only host Nginx, `web` image carrying React + Unity Web, Compose on the Droplet, Managed PostgreSQL off-box, realm `createit`).

---

## Operation catalog

| Operation | Spec | Game-plan role |
|:---|:---|:---|
| Droplet / SSH / UFW / Docker | [droplet-host.md](./operations/droplet-host.md) | One production Droplet now (gated, 2 GB), staging later; `deploy` user; 22 (restricted) + 443 only |
| Domain / DNS / Certbot | [dns-certbot.md](./operations/dns-certbot.md) | DO DNS zone `createit.digital`; DNS-01, port 80 closed; one SAN cert per Droplet |
| Host Nginx | [nginx.md](./operations/nginx.md) | Edge only: TLS, headers, rate limits, basic-auth gate until launch, `/` → `web`, `/api/` → `api`; `auth.` vhost when `identity` is on |
| `web` image | [web-image.md](./operations/web-image.md) | `nginx:alpine` + React shell + Unity Web build; one image per release; owns Unity MIME/cache rules |
| Managed PostgreSQL | [managed-postgres.md](./operations/managed-postgres.md) | Off-box DB; pooled runtime vs direct migrations; separate Keycloak DB |
| Container registry | [container-registry.md](./operations/container-registry.md) | DOCR; SHA + semver tags; never `latest`-only |
| Keycloak + auth | [keycloak.md](./operations/keycloak.md) | **Postponed (P8)** — profile `identity`; realm `createit`; JWKS validation rules; React PKCE flow. Enabled with `/admin/` |
| Compose deploy | [compose-deploy.md](./operations/compose-deploy.md) | web, api, redis; profiles `identity` + `jobs` **off**; `WEB_TAG` / `API_TAG` rollback |
| Monitoring / backups | P6 — after deploy ships | DO Monitoring + Managed PostgreSQL backups |

---

## Doc split (do not collapse)

- `docs/devops/` — planning and operation specs for the program.
- `docs/runbooks/` — what you run at 2am (deploy, rollback, restore, incident, plus per-component pages as they exist).
- `docs/architecture/` — diagrams and service boundaries (not click-by-click setup).
- `docs/adr/` — decisions that outlive the LOOP (droplet count, registry, DNS).
- `docs/security/` — secrets inventory and access (game plan).

Game plan also requires `docs/runbooks/deploy.md`, `rollback.md`, `restore.md`, `incident.md` — create them when that operation is real, not as empty stubs.

---

## Agent rules for this program

- Propose a plan before changing identity, DNS, production networking, secrets, or deploy.
- Host Nginx and UFW stay on the Droplet; app processes stay in Compose.
- PostgreSQL is DigitalOcean Managed — not a Droplet Postgres container in production.
- Offline play is a product contract; hosting work must not make the game require the API to start.
- `hosting.kind` in `.agent/manifest.json` is still `none` until this product has its own git remote. DevOps on DigitalOcean is **not** GitHub.

---

## Status

| Doc | Status |
|:---|:---|
| Findings | [DEVOPS_FINDINGS.md](./DEVOPS_FINDINGS.md) |
| General plan | [DEVOPS_GENERAL_PLAN.md](./DEVOPS_GENERAL_PLAN.md) |
| Operation files | [operations/](./operations/README.md) — 8 specs distilled from Revy, 2026-09-09 |
| Execution files | next: `create-execution-plan` from general plan + operations |
| Runbooks | empty on purpose until first operation ships |
