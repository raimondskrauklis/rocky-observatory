# docs/devops/DEVOPS_GENERAL_PLAN.md

# DevOps — general plan

**Findings:** [DEVOPS_FINDINGS.md](./DEVOPS_FINDINGS.md)

**Not execution.** No file lists, no click-through. Operation specs are in [operations/](./operations/README.md) (distilled from Revy). Next step is `create-execution-plan`.

Locked: Q1–Q9, Q11–Q13, Q15 (everything deployable is an image; host Nginx edge-only), Q16 (Keycloak profile `identity`, off), Q17 (2 GB Droplet). Deferred: Q10 staging DNS names (with the staging Droplet). Open: Q14 Keycloak memory; region.

**Scale-down (2026-09-09):** one Droplet first, production-named, gated. P1–P5 build that box. Staging Droplet and Keycloak are **P7 / P8** below — postponed, not dropped.

---

## Cross-cutting (every phase)

- **Lineage:** versioned host and Compose config in `infrastructure/`; secrets named in `docs/security/` but not stored in git.
- **Coverage:** every change is made so that a second Droplet can receive it by copying files and changing names; production names are `observatory.createit.digital` and `auth.createit.digital`. Until P7, "staging" in any spec means "the same thing on the second box, later".
- **Runbooks:** each phase that changes a component updates `docs/runbooks/` for that component (create on first ship).
- **i18n:** operator docs in English.
- **Tests:** smoke that matches the phase (SSH, `ufw status`, HTTP/HTTPS, `docker compose ps`) — exact commands live in execution files.
- **Push:** `hosting.kind = github` — private `raimondskrauklis/rocky-observatory`. Revy on PRs. Never push while Revy is pending.
- **Adapt:** operation specs already carry Observatory names; never reintroduce `revy`, kp-platform, or other-product hostnames, container names, or realms.

---

## P0 — Foundations

**Goal:** DigitalOcean access, environment split, and in-repo infrastructure layout exist before any Droplet is treated as production.

**Scope:**

- **In:** DO project; SSH key policy; where secrets live; `infrastructure/` tree (compose, nginx, scripts, backup) as empty-or-stub layout; ADRs for: production Droplet first / staging second (Q3), `web` image not host files (Q15), Keycloak on-box as profile `identity` (Q4/Q16).
- **Out:** creating Droplets; DNS; copying foreign Nginx/deploy files (they are not here yet).

**Deliverables:** documented access + secret locations; repo layout matching the game plan’s `infrastructure/` split; locked env names (local / staging / production).

**Depends on:** nothing.

---

## P1 — Droplet, SSH, UFW

**Goal:** The production application Droplet exists and is reachable only as the security baseline allows.

**Scope:**

- **In:** create **one** Droplet (production, 2 GB / 1 vCPU — Q17; resize to 4 GB when `identity` is enabled); weekly Droplet backups on; non-root `deploy` user, SSH keys only; UFW 22 (restricted) + 443; DO Cloud Firewall mirror; Docker Engine + `observatory-net`; `/srv/observatory` layout (env, compose, keycloak build context) with container-owned dirs set as root; DO monitoring agent; VPC path toward Managed PostgreSQL.
- **Out:** public app ports; Nginx sites; registry; Compose stacks.

**Spec:** [operations/droplet-host.md](./operations/droplet-host.md)

**Deliverables:** one hardened host; `docs/runbooks/host-access.md` written so P7 can repeat it.

**Depends on:** P0.

---

## P2 — DNS

**Goal:** Production hostnames resolve to the production Droplet.

**Scope:**

- **In:** `observatory.createit.digital` and `auth.createit.digital` → the P1 Droplet (the `auth.` record exists now so the cert SAN and later Keycloak need no DNS step). Zone `createit.digital` is on DigitalOcean DNS (verified via Revy) and is shared with `*.revy.createit.digital` — add records, never touch Revy's. Staging names: P7 (Q10).
- **Out:** TLS issuance (next phase).

**Spec:** [operations/dns-certbot.md](./operations/dns-certbot.md) (DNS section)

**Deliverables:** DNS records; short domain runbook.

**Depends on:** P1.

---

## P3 — Nginx and Certbot

**Goal:** Host Nginx is the public edge with TLS; Unity Web and API routes match the game plan.

**Scope:**

- **In:** host Nginx as **edge only**; Certbot **DNS-01** with the DigitalOcean plugin, one SAN cert covering both production names; stub `return 404` vhost first, then the real one; `/` → `web` container and `/api/` → `api` on loopback with rate limits, `gzip off` on the proxied vhost; security-headers and proxy-headers snippets; **basic auth on `/` with `/api/v1/telemetry` exempt** (the pre-launch gate — removed in P7). Close port 80 only after the renewal dry-run passes.
- **Out:** host Nginx serving any application files; putting Nginx-as-edge in Compose; Revy's Node `serve` container; the `auth.` vhost (P8 — file is written, not installed).

**Spec:** [operations/dns-certbot.md](./operations/dns-certbot.md), [operations/nginx.md](./operations/nginx.md)

**Deliverables:** `infrastructure/nginx/` files matching the spec; working edge (proxying to a placeholder `web` image until P5); `docs/runbooks/tls.md`, `docs/runbooks/nginx.md`.

**Depends on:** P2.

---

## P4 — Container registry

**Goal:** Application images are pulled from DigitalOcean Container Registry with pinned tags.

**Scope:**

- **In:** registry `observatory`; images `observatory-web` and `observatory-api`; read-write token for builds, read-only token per Droplet (`doctoken` login, per-command `DOCKER_AUTH_CONFIG`); tag policy SHA + semver (+ `-staging` for web), never `latest`-only; `web` image Dockerfile + inner `nginx.conf` with Unity rules; `registry-prune.sh` + monthly GC.
- **Out:** running the Unity build itself in this program (CI/tools concern); pushing Keycloak (built on-box).

**Spec:** [operations/container-registry.md](./operations/container-registry.md), [operations/web-image.md](./operations/web-image.md)

**Deliverables:** registry in use; `docs/runbooks/registry.md`.

**Depends on:** P0 (can proceed in parallel with P1–P3 once foundations exist; **production pull** depends on P1).

---

## P5 — Compose deploy

**Goal:** The production Droplet runs the launch Compose set from the game plan against Managed PostgreSQL.

**Scope:**

- **In:** one Managed PostgreSQL cluster, `observatory` database + `observatory_app` user, extensions, grants (pooled runtime / direct migrations); Compose file for web (`WEB_TAG`), api (`API_TAG`), redis (cache), plus profile `identity` (keycloak — KC 26 optimized image, realm `createit` from JSON) and profile `jobs` (redis-broker, celery-worker, celery-beat), **both defined but not started**; restart/log-rotation/memory-limit/read-only rules; `api.env` / `keycloak.env` on the Droplet; one deploy procedure for both images (pull → migrate from new api image → write tags → `compose up -d` → verify `release.json` + `/version` + smoke); rollback = previous tag; staging → production promotion by matching `artifact_checksum`.
- **Out:** Postgres container in production; publishing Redis/Keycloak/API on public interfaces; Unity CI; player registration; Revy's Keycloak webhook provider; the `keycloak` database, `keycloak.env`, and realm import (P8).

**Spec:** [operations/managed-postgres.md](./operations/managed-postgres.md), [operations/compose-deploy.md](./operations/compose-deploy.md) (keycloak section of the Compose file is written now, activated in P8)

**Deliverables:** `infrastructure/compose/`, `infrastructure/keycloak/` (files only), `infrastructure/web-image/`; `web`/`api`/`redis` running privately behind Nginx; `docs/runbooks/deploy.md`, `rollback.md`, `web-release.md`.

**Depends on:** P3, P4. Managed PostgreSQL may be created earlier (P1) so DNS/TLS work is not blocked on it.

---

## P6 — Backup, restore, incident

**Goal:** Recovery and incident runbooks exist for what this program actually deployed.

**Scope:**

- **In:** Managed PostgreSQL backup/restore expectations; Droplet rebuild notes; `docs/runbooks/restore.md` and `incident.md`; DO Monitoring alerts named in the game plan that apply to this topology.
- **Out:** Terraform; HA; full log aggregation.

**Deliverables:** restore + incident runbooks; listed alerts; RPO/RTO statements the game plan requires, filled with real numbers from DO.

**Depends on:** P5.

---

## P7 — Staging Droplet (postponed; before first public release)

**Goal:** A second Droplet mirrors production under `staging.*` names, and the basic-auth gate moves from production to staging.

**Scope:**

- **In:** confirm Q10; DNS records; second Droplet via `docs/runbooks/host-access.md`; own Managed PostgreSQL cluster; own SAN cert; same Nginx/Compose files with staging names; `web` images tagged `<sha>-staging`; remove basic auth from production; promotion procedure staging → production exercised once.
- **Out:** anything that differs from production other than names, secrets, and the gate.

**Spec:** all of `operations/` — every file already states its staging variant.

**Deliverables:** staging live; production gate removed; `docs/runbooks/promote.md`.

**Depends on:** P6. **Trigger:** first public release candidate exists (M1 approaching).

---

## P8 — Identity: Keycloak + `/admin/` (postponed; first named consumer)

**Goal:** Keycloak runs because something uses it: `/admin/` with operator login showing feedback and release state.

**Scope:**

- **In:** Managed PG `keycloak` database + `keycloak_app` user; `keycloak.env`; `auth.createit.digital` vhost with IP-restricted `/admin`; Droplet resize to 4 GB; `docker compose --profile identity up -d`; realm `createit` import; `observatory-web` PKCE flow in React; FastAPI JWKS validation + `require_operator()`; `/admin/` page. Then the same on staging.
- **Out:** player accounts, registration, `observatory-mobile`, webhook providers.

**Spec:** [operations/keycloak.md](./operations/keycloak.md) — complete and waiting.

**Deliverables:** `identity` profile on in both environments; `docs/runbooks/keycloak.md`.

**Depends on:** P5 (and P7 for staging parity). **Trigger:** feedback volume makes reading it in the database impractical, or any other feature needs an authenticated operator page. Not before.

---

## Open item / next step

**Open:** region; Q14 Keycloak memory (P8). Q10 deferred to P7.

**Next:** `create-execution-plan` for P0–P6 from this plan + `operations/*.md`. P7/P8 execution files are written when their triggers fire.
