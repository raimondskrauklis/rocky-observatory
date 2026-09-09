# docs/devops/DEVOPS_FINDINGS.md

# DevOps findings

**Status:** baseline for the general plan. Foreign patterns distilled from Revy into [operations/](./operations/README.md) on 2026-09-09.

**Verified against:** [game-platform-base-plan_v2.1.md](../../game-platform-base-plan_v2.1.md), [docs/devops/README.md](./README.md), repo tree (no `infrastructure/`, no droplets in-repo), and the Revy production deployment (`~/projects/revy` @ `bf39ce5`: `deploy/nginx/`, `deploy/keycloak/`, `deploy/env-examples/`, `.github/workflows/deploy.yml`, `docs/utils/CERTBOT_DIGITALOCEAN_DNS_RENEWAL.md`, `deploy-user-migration.md`, `DATABASE_CONNECTION_GUIDE.md`, `backend/app/core/auth.py`, `jwks.py`, `frontend/src/lib/keycloak.ts`). No live DigitalOcean inventory in this workspace.

---

## Build principles

- **Production-grade, small-scale.** One application Droplet per environment, Managed PostgreSQL, host Nginx. Not HA.
- **Host vs container.** Nginx, Certbot, UFW, SSH, Docker Engine stay on the Droplet. FastAPI, Celery, Redis, Keycloak run in Compose.
- **Adapt, do not paste.** Patterns from another project are inputs. Do not copy kp-platform deploy YAML or another game’s server names.
- **Offline play.** Hosting must not make the Unity client require the API to start.
- **Runbooks are the product of shipping.** Empty runbook stubs are out.

---

## Terminology

| Term | Meaning |
|:---|:---|
| **Application Droplet** | The VM that runs host Nginx + Compose. |
| **Managed PostgreSQL** | DigitalOcean database; not a Postgres container in production. |
| **Operation spec** | Durable `docs/devops/operations/<name>.md` — written from user context, not this findings. |
| **Runbook** | `docs/runbooks/<name>.md` — how to repeat the operation after it exists. |

---

## What exists vs genuinely new

| Item | State |
|:---|:---|
| Product topology, domains, security baseline | Specified in the game plan (**verified**). |
| `infrastructure/` Compose, Nginx, backup trees | **Missing.** |
| Droplets, DNS, certs, registry, UFW | **Not in this repo.** Treat as greenfield. |
| Foreign Nginx/deploy/auth patterns | **Distilled** from Revy into `operations/*.md`. Revy proves: DO Droplet + host Nginx + Certbot DNS-01 with port 80 closed; Keycloak 26 optimized image at 1 GB behind `auth.` vhost; FastAPI JWKS/RS256 validation with issuer split and `azp`/`aud` allowlist; React `keycloak-js` `check-sso` + PKCE; DOCR `doctoken` login; SHA-tagged images; migrations on the Droplet from the deployed image. |
| Unity Web delivery rules | **New** — Revy has no game artifacts. Brotli `.br` MIME/encoding, `application/wasm`, hashed `Build/` immutable cache, `release.json`: written fresh in `operations/web-image.md` (inside the `web` image, not in host Nginx). |
| Static-site container | **Revy's is a corner cut** — Node `serve` (dev tool), `Cache-Control: max-age=0` on everything, ~70 MB RSS. Observatory's `web` image is pinned `nginx:alpine` with explicit cache policy (Q15). |

Reuse trap: leftover kp-platform `deploy.yml` (Celery queue names, `volume_kp`, kp images) is the wrong pattern even if it reappears. Revy's `deploy.yml` is the right *shape* (validate → build/push → migrate → swap) but uses `docker run` per container; Observatory uses Compose with `WEB_TAG` / `API_TAG`.

---

## Catalog — workstreams

Each stream becomes one general-plan phase (or a tight pair). Exact method for Nginx/deploy comes from the user’s other-project files.

| Stream | Why | Method (locked intent) |
|:---|:---|:---|
| Foundations | Every later op needs access, env split, secret locations | DigitalOcean project; SSH keys; secrets **outside** git; `infrastructure/` layout per game plan |
| Droplet + SSH + UFW | Runtime + host security | Separate staging and production Droplets; non-root `deploy` user (root SSH disabled); UFW allows 22 (restricted) + **443 only**; DO Cloud Firewall mirrors it; no public Redis/API/Keycloak/Postgres ports |
| DNS | Names in the game plan | Zone `createit.digital` is on DigitalOcean DNS (verified via Revy). `observatory.createit.digital`, `auth.createit.digital` → production Droplet. Staging names: Q10 |
| Nginx + Certbot | Public edge + TLS | Host Nginx **edge-only** (no application files); Certbot **DNS-01** via `python3-certbot-dns-digitalocean` (port 80 closed); one SAN cert per Droplet; `/` → `web` container, `/api/` → `api`; second `server` for `auth.` with IP-restricted `/admin` |
| `web` image | The product as an artifact | Pinned `nginx:alpine` + React build + Unity Web build; one image per release; Unity MIME/encoding/cache rules inside the image; `release.json` served |
| Container registry | Pinned images | DigitalOcean Container Registry; no `latest`-only deploys |
| Compose deploy | App processes | Images `web` + `api`; launch services web + api + redis; profile `identity` (keycloak) and profile `jobs` (redis-broker, celery-worker, celery-beat) defined but off; Managed PG off-box |
| Observability + backup docs | Game plan day-one | DO Monitoring; PG backups; runbooks deploy/rollback/restore/incident as those ops become real |

---

## Advice

- **Keycloak on the same application Droplet** as the game stack (Compose service, Nginx `auth.createit.digital`), **as profile `identity`, off** until `/admin/` exists. A Keycloak with zero relying parties does not exercise the identity seam — the seam is exercised the first time React does PKCE and FastAPI validates a token. A third identity Droplet is rejected unless a later requirement appears.
- **Two Droplets, production first.** The box that owns the public name is production from day one and is gated, not renamed later. Staging is the second box. Not Terraform.
- **Operation specs live in `operations/`**, not here. Each one names its Revy source and its Observatory delta.
- **Keep Revy's Keycloak separate.** `auth.revy.createit.digital` (realm `revy`) and `auth.createit.digital` (realm `createit`) are two instances in one DNS zone. Do not merge realms or share the Keycloak database.
- **Everything deployable is an image.** Revy's shape (host Nginx proxies `/` to a static container) is kept, but the container is `nginx:alpine`, not Node `serve`, and it also carries the Unity Web build. No `/srv/game-platform` file releases, no symlink flips — `web` and `api` roll forward and back the same way (Q15).

---

## Data scope & exclusions

**In:** DigitalOcean Droplets, VPC/private DB connectivity where available, host Nginx/TLS/UFW, DOCR, Compose on the Droplet, DNS for the two production hostnames, staging Droplet as a mirror process.

**Out:** Terraform, CDN, Kubernetes, multi-region, exposing app ports publicly, production Postgres in Compose, GitHub Actions from kp-platform, Unity editor install on the Droplet, building the game in this program.

---

## Edge cases

- Certbot needs DNS pointing at the Droplet first.
- Unity Web cache and content-type headers are set **inside the `web` image**; host Nginx must pass them through (`gzip off` on the proxied vhost, no `add_header` in the `/` location).
- `VITE_*` is baked at build, so staging and production `web` images differ; the Unity `play/` payload inside them must be byte-identical (checksum in `release.json`).
- Staging (when added) must not share production DB, OAuth clients, or secrets (game plan).
- Basic auth on production `/` must exempt `/api/v1/telemetry` (smoke beacon) and must be removed at launch by config, not by forgetting.
- Enabling `identity` later is: Managed PG `keycloak` DB + user → `keycloak.env` → `auth.` vhost → `docker compose --profile identity up -d` → realm import → Droplet resize. Runbook it when the trigger arrives, not before.
- Registry exists before first image push; first Compose deploy may wait on `apps/api` existing — deploy **files** can still land.

---

## Decisions registry

| Q# | Question | Status | Resolution |
|:---|:---|:---|:---|
| Q1 | Cloud | **locked** | DigitalOcean. |
| Q2 | IaC | **locked** | No Terraform. Console/API + versioned config in `infrastructure/`. |
| Q3 | Droplet count | **locked**, sequenced (2026-09-09) | One application Droplet per environment, **production first**: it owns `observatory.createit.digital`, is configured as `production`, and sits behind Nginx basic auth until launch. Staging Droplet (`staging.*`) is added before the first public release. Never rename or move the public name between boxes. |
| Q4 | Keycloak placement | **locked** | Compose on the application Droplet; Nginx serves `auth.createit.digital`. Runs only when profile `identity` is on (Q16). |
| Q5 | Edge / TLS / firewall | **locked** | Host Nginx, host Certbot, host UFW. |
| Q6 | Database | **locked** | DigitalOcean Managed PostgreSQL; not a production container. |
| Q7 | Registry | **locked** | DigitalOcean Container Registry; pinned tags. |
| Q8 | Foreign patterns | **resolved** | Distilled from Revy (`~/projects/revy`) into `operations/*.md` with per-file source + delta. Not pasted. |
| Q9 | GitHub | **locked** (updated 2026-09-09) | Product remote is private `raimondskrauklis/rocky-observatory` (`hosting.kind = github`). Production Revy reviews PRs — same GitHub App as `raimondskrauklis/revy` (dogfood). Consumer setup: [docs/runbooks/github-revy.md](../runbooks/github-revy.md). DevOps runtime is DigitalOcean, not GitHub Actions. |
| Q10 | Staging DNS names | **deferred** (default proposed) | Not needed until the staging Droplet exists (Q3). Default: `staging.observatory.createit.digital` + `auth.staging.observatory.createit.digital`, one SAN cert on the staging Droplet. Confirm when that phase starts. |
| Q11 | Launch Compose set | **locked** (plan v2.1, revised 2026-09-09) | `web`, `api`, `redis` (cache). Profile `identity`: `keycloak` — off (Q16). Profile `jobs`: broker Redis + Celery/Beat — off until a named task exists. Weekly Droplet backups on. |
| Q12 | Port 80 / TLS challenge | **locked** (from Revy) | Certbot DNS-01 with the DigitalOcean plugin; port 80 closed in UFW and Cloud Firewall; no HTTP→HTTPS redirect exists, publish `https://` links only. |
| Q13 | Keycloak admin console | **locked** (plan v2.1) | `/admin` on `auth.createit.digital` allow-listed to operator IPs in Nginx. Revy exposes it publicly; Observatory does not. |
| Q14 | Keycloak memory | **calibration** | Revy runs KC 26 optimized at `mem_limit: 1g`. Start at 1 GB; raise to 2 GB on OOM. Droplet resized to 4 GB when `identity` is enabled. |
| Q16 | Keycloak timing | **locked** (user, 2026-09-09) | **Postponed, not dropped.** Compose profile `identity`, defined, off. No relying party exists: no `/admin/`, and pre-launch gating is basic auth. Enabled by the first named consumer — `/admin/` with operator login (feedback + release view). Until then: no Keycloak DB/user, no `auth.` vhost, no realm import. TLS cert still includes `auth.createit.digital` (SAN is free with DNS-01). |
| Q17 | Initial Droplet size | **locked** (2026-09-09) | 2 GB / 1 vCPU while `identity` is off. Resize (reboot, not rebuild) to 4 GB / 2 vCPU when Keycloak is enabled. |
| Q15 | Static delivery shape | **locked** (user, 2026-09-09) | `web` image: pinned `nginx:alpine` + React build + Unity Web build, one image per release, `WEB_TAG` in Compose. Host Nginx edge-only. Rejected: files under `/srv/game-platform` on host Nginx (second release mechanism); Revy's Node `serve` container (dev tool, no cache headers). Plan v2.1 updated. |

---

## Parking lot

- Droplet size / region — calibration (Revy's region is `fra1` per its DB host; same region keeps DB latency low).
- Lift Revy's `deploy.yml` `validate → deploy` shape into CI when this repo gets a remote.
- Independent `pg_dump` to object storage — first real `jobs` task or host cron.
- Object storage for raw Unity build outputs (provenance) and DB/realm exports; `web` images themselves live in DOCR.
- `infrastructure/scripts/registry-prune.sh` — tag hygiene (readability, not cost; user: registry cost is not a concern).
- Keycloak on a **separate** Droplet — rejected for v1 of this program (Q4).

---

## Devil's advocate

- Shipping Compose before Nginx/TLS leaves API ports easy to mis-publish.
- Calling the first Droplet "staging" because it is gated would force a rename of the live box later; it is production with a gate.
- Running Keycloak "to keep the realm warm" with no consumer is 1 GB of RAM and a second database for nothing measurable.
- Copying another project’s Nginx without Unity Web `Content-Type` / cache rules will break `/play/`.
- Host Nginx with `gzip on` for the proxied `/` location would double-encode Unity `.br` responses; the edge must not compress proxied content.
- Carrying Revy's hard-coded `Connection "upgrade"` into the proxy snippet disables upstream keepalive — one new TCP connection per request to the `web` container. Use the `$connection_upgrade` map.

---

## Experiment / verification

Pass when each environment that this program claims to own has: SSH-key login, UFW default-deny except intended ports, both production names on TLS, basic auth on `/` with the telemetry exemption, Compose running `web`/`api`/`redis` only (both profiles defined, `docker compose ps` shows neither), nothing published to `0.0.0.0`, images from DOCR with pinned tags, and a runbook page for each shipped operation.

---

## References

- [game-platform-base-plan_v2.1.md](../../game-platform-base-plan_v2.1.md) — topology, Nginx duties, container policy, security, docs list
- [docs/devops/README.md](./README.md) — program vs runbook split
- [operations/README.md](./operations/README.md) — per-component specs distilled from Revy
