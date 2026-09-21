# docs/initial-planning/game-platform-base-plan_v2.1.md

# Game Platform Base Plan — v2.1

## Status

**Status:** Production foundation specification — v2.1, revised after five independent reviews (Perplexity, OpenAI, Kimi, Claude, Grok) and the author's decisions of 2026-09-09.

**Supersedes:** `docs/initial_reviews/game-platform-base-plan_v1.1.md`. Reviews: `docs/initial_reviews/`.

**First game:** The Lost Observatory

**Primary product domain:** `observatory.createit.digital`

**Platform identity domain:** `auth.createit.digital`

**Roles:** platform owner (hosting, identity, data, operations) and game creator (Unity loop, playable build, public link). The game creator must never need the platform to press Play.

## Purpose — ranked

1. **Capacity.** Build and keep the ability to take a small game idea to a public, versioned, playable, reversible web release — and do the next one without rebuilding the stack.
2. **Foundation.** Reusable hosting, delivery, API, identity, data, and operations conventions for future games.
3. **Product.** A complete, publicly hosted first game, *The Lost Observatory*, as proof that the capacity exists.

**Tiebreaker:** when goals conflict, capacity wins. A platform that never ships a game is unvalidated; a game shipped by bypassing the release path teaches nothing. Both count as failure.

The first game is not the money, not the curriculum, and not a throwaway. It is the acceptance test of the foundation.

## Creator platform — hypothesis, not product

The long-horizon idea is a platform on which other young creators build and publish games. **v2.1 does not build that product.** It would require multi-tenant accounts, other people's builds on our domain, minors' data handling (GDPR-K / COPPA), moderation, takedown, and quotas — none of which exist here and all of which are shaped by real creators, not guessed.

What v2.1 does build is the thing that hypothesis needs first: a publishing path a second person can use.

**Gate:** a second creator ships a playable web build on this stack in under one week using only the documented path. When that passes, plan v3 scopes the creator platform. Until then, no multi-tenant abstractions, no generic multi-game API.

## Core Intent

The game creator focuses on:

- Game ideas and player experience
- Unity scenes, interactions, visuals, audio, gameplay
- A public link other people can open, a version number, and a rollback

The platform owner focuses on:

- Hosting, TLS, deploy, rollback, backups, monitoring
- Identity and data as dark-but-ready seams
- Runbooks that are exercised, not written and forgotten

Simple work stays simple. Real architecture is available when a feature requires it — and not running loud before that.

## Why Self-Hosted

A managed web-game platform or a web-only AI coding workflow is fine for experiments and becomes a dead end when the product needs a game engine, platform builds, controlled hosting, private networking, owned identity decisions, versioned releases with rollback, and direct ownership of player data. This project keeps stack ownership.

Managed services are used where they give clear operational value: DigitalOcean Managed PostgreSQL, DigitalOcean Monitoring and Uptime, Sentry.

## Production Scope

The foundation is production-grade and small-scale. **Production-grade** here means versioned artifacts, staging, tested rollback, backups, monitoring, error tracking, and runbooks. It does not mean high availability. The single-Droplet topology is itself a scoped, revisitable decision, in the same category as the deferred items below.

### Included from day one

- Unity **6.3 LTS (6000.3.x)** game client, C#
- Blender **LTS** asset workflow (pin current LTS version in `tools/blender/BLENDER_VERSION`; see `docs/game-design/asset-pipeline.md`)
- Git + Git LFS
- Self-hosted delivery on `observatory.createit.digital` via host Nginx
- Docker Compose for application services
- DigitalOcean Droplets (staging and production), Managed PostgreSQL, Monitoring, Uptime checks
- FastAPI application service
- Redis container (cache and rate limiting)
- Keycloak at `auth.createit.digital` — **Compose profile `identity`, off until `/admin/` exists** (see Launch Capability)
- Celery worker and Celery Beat — **built as a Compose profile, off at launch**
- Sentry error tracking
- Versioned release artifacts, deploy and rollback procedures
- Backup, restore, incident, security runbooks
- Privacy and data-handling rules for the public release
- **Web Build Budgets enforced in CI**

### Intentionally out of current scope

Deferred platform capabilities. They can be added without changing the core architecture:

- Terraform or other infrastructure-as-code
- CDN
- Multi-node high availability
- Kubernetes
- Product analytics stack
- Large-scale log aggregation
- Multi-region delivery
- Console or mobile store automation
- Real-time multiplayer
- Payments and entitlements
- User-generated content and moderation
- Multi-tenant creator accounts (see Creator platform hypothesis)
- Monetization and portal distribution (see Distribution)

## Architectural Principles

1. **The game is independently playable.** Gameplay, rendering, audio, interaction, and local saves must not depend on backend availability.
2. **Production discipline starts immediately.** Version control, reproducible builds, CI, staging, deploy runbooks, monitoring, error tracking, backups, rollback — from the first public release.
3. **Production-grade does not require production-scale.** One Droplet per environment with managed data, backups, and tested rollback is production-grade for this scope. It is not HA, and the plan says so.
4. **Capabilities are exercised or dark — never idle-and-claimed.** A service that nothing calls is not "production standard". It is either gated behind a real (possibly operator-only) use, or shipped as a ready recipe that is off.
5. **The game client is untrusted.** The server validates everything that affects other players, durable progress, competition, entitlement, or money.
6. **Standards at boundaries.** HTTPS, OpenAPI, OAuth 2.0 / OpenID Connect, PostgreSQL, Docker images, versioned artifacts.
7. **Clear ownership.** Unity owns runtime behavior. FastAPI owns public APIs. PostgreSQL owns durable data. Redis owns ephemeral state. Keycloak owns identity.
8. **Small, coherent, reversible releases.**
9. **Reuse must be earned.** Applies to abstractions *and* to running infrastructure. Platform-wide APIs come after a second game repeats a need.
10. **Keep simple paths simple.** Unity opens, Play works, no containers.

## Technology Decisions

| Area | Decision | Notes |
|:---|:---|:---|
| Game engine | Unity 6.3 LTS (6000.3.x) | Supported to Dec 2027. Do not use 6.0 LTS (ends Oct 2026) or 6.x update releases for production. ADR. |
| Renderer (Web) | WebGL 2 | WebGPU evaluated at the next LTS. ADR. |
| Web memory / threading | wasm32, ≤ 2 GB heap, threading **off** | Keeps Safari; avoids COOP/COEP. ADR. |
| Game language | C# | |
| 3D assets | Blender | |
| Public web | React + TypeScript | Landing page is static-first; the React app owns interactive surfaces (`/feedback/`, `/admin/`). |
| Public API | FastAPI | |
| Durable data | DigitalOcean Managed PostgreSQL | |
| Cache / rate limit | Redis container (`allkeys-lru`, `maxmemory` set) | Broker Redis is separate — see Celery. |
| Background jobs | Celery worker + Beat, Compose profile `jobs` | Off at launch. |
| Identity | Keycloak | Realm as code (JSON import). Compose profile `identity`, off until the first relying party (`/admin/` with operator login). |
| Web delivery | `web` container: pinned `nginx:alpine` + React build + Unity Web build, one image per release | Same artifact type as the API (SHA/version-tagged image in the registry); rollback is a tag change. |
| Reverse proxy | Host Nginx | TLS, routing, security headers, rate limits, proxy to `web` and `api` on loopback. Host Nginx serves no application files. |
| Runtime | DigitalOcean Droplets + Docker Compose | One application Droplet per environment. |
| Monitoring | DigitalOcean Monitoring + **Uptime** (separate product) | |
| Error tracking | Sentry | Not a funnel — see Telemetry. |
| Source control | Git + Git LFS | LFS bandwidth budgeted in CI. |
| CI/CD | Repository-hosted CI + self-managed deploy | Pipeline named in `docs/runbooks/deploy.md` when it exists. |
| Secrets | Env files on the Droplet host, outside git, `0600`, owner root | Register in `docs/security/SECRETS.md`. No secrets manager on DO. |

## Domain Model

### Public product domain

```text
https://observatory.createit.digital/
```

```text
/             Landing page (static)
/play/        Unity Web build
/privacy/     Privacy information
/feedback/    Feedback page
/status/      Optional public status surface
/api/v1/      FastAPI public API
/admin/       Feedback and operations view — Keycloak-gated (operator role)
```

### Platform identity domain

```text
https://auth.createit.digital/
```

Keycloak is a reusable identity service, not coupled to one game URL. Future games use their own product domains and this identity domain.

## Runtime Architecture

```text
Browser
  |
  v
observatory.createit.digital  (host Nginx on the production Droplet — TLS, headers, rate limits, routing only)
  |------------------------------------------------|
  v                                                v
web container (127.0.0.1:8081)                 /api/v1/  → api container (127.0.0.1:8000)
  nginx:alpine + React build + Unity Web build        |
  /  /privacy/  /feedback/  /admin/  /play/           v
  one image per release, tag = release version   FastAPI
                                                   |----------------|
                                                   v                v
                                    Managed PostgreSQL          Redis (cache / rate limit)

Compose profile `jobs` (off at launch):  redis-broker  +  celery-worker  +  celery-beat
Compose profile `identity` (off at launch): keycloak → auth.createit.digital  (enabled with /admin/)
```

### Identity flow (corrected)

OAuth belongs to the **browser page**, not to the WebAssembly canvas.

```text
React shell  --Authorization Code + PKCE-->  Keycloak (auth.createit.digital)
React shell  --short-lived access token-->   Unity via JS bridge (when a game feature needs identity)
FastAPI      validates issuer, signature, expiry, audience, roles
```

Unity never performs the redirect, never stores refresh tokens, never holds client secrets.

## Launch Capability (first public release, 0.1)

| Component | State at 0.1 | Why |
|:---|:---|:---|
| Host Nginx + TLS | Live | Public edge |
| `web` image: landing + React + Unity Web `/play/` | Live | The product, as one versioned image |
| React `/feedback/` | Live | Public feedback, synchronous |
| FastAPI | Live | Feedback endpoint, health, version, telemetry beacons |
| Managed PostgreSQL | Live | Feedback + operational tables only |
| Redis (cache) | Live | Rate limiting, idempotency for feedback |
| Keycloak | **Profile `identity`, off** | No relying party exists yet: there is no `/admin/`, and pre-launch access gating is Nginx basic auth. A Keycloak with zero consumers does not exercise the identity seam; it only costs 1 GB. Enabled by the first named consumer: `/admin/` with operator login (feedback + release view). Spec is complete and waiting (`docs/devops/operations/keycloak.md`). |
| Celery worker + Beat | **Profile `jobs`, off** | No launch job exists. Feedback email is synchronous. Enable when a real async or scheduled task appears. |
| Sentry | Live | API, web, Unity (with WebGL blind spots documented) |
| DO Monitoring + Uptime | Live | |
| Droplets | **One**, production-named, gated | The Droplet that owns `observatory.createit.digital` is production from day one and sits behind basic auth until launch. A second Droplet (staging, `staging.*` names) is added before the first public release; the gate then moves to it. |

Keycloak clients when the `identity` profile is enabled: `observatory-web` (public SPA, PKCE) and `observatory-api` (bearer audience). `operator` is a **realm role**, not a client. `observatory-mobile` is created when a mobile build exists.

## Service Boundaries

### Unity game client

Owns gameplay, scenes, prefabs, UI, physics, input, audio, visuals, local saves, offline play, and presentation of remote data when online features exist.

Must not contain database credentials, Keycloak admin credentials, payment secrets, privileged API keys, or trust in player-submitted scores, inventory, currency, or purchases.

Works when FastAPI, Redis, Celery, or Keycloak is unavailable. Only optional online features degrade.

Local saves on Web live in browser storage (IndexedDB). Clearing browser data wipes progress. The privacy page says so.

### React web application

Owns interactive public surfaces: feedback UI, `/admin/` feedback and operations view, future account pages. The landing page is static so discoverability and load time do not depend on a SPA boot.

### FastAPI service

Owns public HTTP API contracts, validation, authorization, server-side validation of sensitive game actions, feedback endpoints, **telemetry beacons**, and future cloud-save / leaderboard / entitlement / account-linking capabilities.

### PostgreSQL

System of record for feedback, operational records, telemetry beacons, and — when introduced — player records, cloud-save metadata, leaderboards, entitlements, audit.

Launch schema is **feedback + operational + beacons only**. Do not pre-model leaderboards, entitlements, or payments.

Keycloak uses a separate database (or isolated schema and user). Least-privilege roles per service.

### Redis

Cache Redis: rate limiting, idempotency keys, short-lived state. `maxmemory` set, `allkeys-lru`, no persistence required.

Broker Redis (profile `jobs` only): `maxmemory-policy noeviction`, `appendonly yes`, `appendfsync everysec`. Never share a broker with an evicting cache.

Redis is never the authoritative store for accounts, purchases, entitlements, permanent progress, or permanent leaderboards.

### Celery (profile `jobs`)

Provides background processing and scheduled dispatch when a real task exists. First candidate tasks: feedback digest, scheduled backup verification, release cleanup. When enabled:

- `task_acks_late = True`
- `visibility_timeout` set above the longest task
- Durable effects idempotent; PostgreSQL constraints establish correctness; Redis locks optimize only
- Exactly one Beat instance

## Environments

| Environment | Purpose | Required behavior |
|:---|:---|:---|
| Local | Unity iteration and automated tests | Unity runs without Docker or backend services |
| Production (first, gated) | The only hosted environment until launch approaches; owns `observatory.createit.digital` | Production-shaped from day one: images, env files, runbooks, backups. Nginx basic auth on `/` until public release. Configured as `production` — never renamed. |
| Staging (added later) | Integration, deploy validation, tester access | Second Droplet with `staging.*` names, added before the first public release; same routes and deploy process; separate secrets, database, realm, OAuth clients; access gated (basic auth, or Keycloak operator role once `identity` is on) |

**Sequence:** production first, staging second. The name that stays public is never moved between boxes. Nothing is shared between staging and production: not databases, credentials, OAuth clients, realm exports, or signing material.

## Topology, Sizing, Cost

```text
Production Droplet   host Nginx + Compose (web, api, redis; profiles identity + jobs off)   ← first
Staging Droplet      same shape, may be smaller                                            ← added before launch
Managed PostgreSQL   one instance per environment
Container registry   web + api images, tagged by release version and git SHA; retention policy + GC
Object storage       logical DB exports, realm exports, raw Unity build outputs (provenance)
```

**Sizing (initial, verify at provisioning):** production 2 GB RAM / 1 vCPU is sufficient while `identity` is off (FastAPI, Redis, host Nginx, `web` ~10 MB). Resize to 4 GB / 2 vCPU when Keycloak is enabled — it wants ~1 GB and a 1–2 GB container limit. Droplet resize is a reboot, not a rebuild. Staging 2 GB.

**Cost model (order of magnitude, verify against current DigitalOcean pricing):** production Droplet + weekly Droplet backups + Managed PostgreSQL + object storage ≈ $50–60/month; staging adds a second Droplet and database. Write the real numbers into `docs/adr/` when provisioned and revisit quarterly.

**Accepted risks, named:** Droplet failure means redeploy or restore (RTO below). No CDN means a traffic spike can saturate one Droplet's bandwidth; a 30–80 MB build × unexpected virality is the scenario. Accepted for 0.1; revisit if `/play/` traffic makes it real.

## Repository Layout

```text
observatory/
├── apps/
│   ├── game-unity/                 # Unity project (The Lost Observatory)
│   │   ├── Assets/_Game/{Art,Audio,Materials,Prefabs,Scenes,Scripts,ScriptableObjects,Tests}/
│   │   ├── Assets/ThirdParty/
│   │   ├── Packages/
│   │   └── ProjectSettings/
│   ├── web/                        # React + TypeScript (feedback, admin); static landing
│   └── api/                        # FastAPI (one image; roles api / celery-worker / celery-beat)
├── packages/
│   ├── api-contracts/              # OpenAPI + generated clients
│   └── game-config/                # Public, versioned configuration only
├── infrastructure/
│   ├── compose/                    # compose files; profile `jobs`
│   ├── nginx/                      # host Nginx site configs (edge only)
│   ├── web-image/                  # Dockerfile + inner nginx.conf for the `web` image (React + Unity Web)
│   ├── keycloak/                   # realm export JSON (as code) + KC Dockerfile
│   ├── scripts/                    # deploy, rollback, registry cleanup
│   └── backup/
├── tools/
│   ├── unity/                      # CI build entry points, smoke mode
│   ├── blender/
│   └── python/
├── docs/
│   ├── adr/
│   ├── architecture/
│   ├── devops/                     # hosting program (findings, general plan, operations)
│   ├── game-design/
│   ├── runbooks/
│   └── security/
├── .agent/  .cursor/  AGENTS.md  .cursorrules
├── Makefile
└── README.md
```

`apps/admin/` and `packages/web-ui/` are created only when repeated real usage exists.

## Unity Project Standards

From the first commit:

```text
Version Control Mode: Visible Meta Files
Asset Serialization Mode: Force Text
Editor version: 6000.3.x LTS, pinned in ProjectSettings/ProjectVersion.txt and CI

**Agent-friendly scene structure:** gameplay and data live in C# classes and `ScriptableObject` assets so they are diffable, reviewable, and mergeable. Scenes are thin wiring: placed objects with component attach points, light groups, and interaction marker GameObjects. Inspector-only logic, especially on prefab instances, is avoided — it cannot be reviewed by an agent or by Bugbot/Revy. Prefabs should carry their own configuration; scenes reference them, not override them.

**Blender version** is pinned in `tools/blender/BLENDER_VERSION`. Asset pipeline: `docs/game-design/asset-pipeline.md`.
```

Track source assets with their `.meta` files. Git LFS for:

```text
*.blend *.fbx *.glb *.gltf *.png *.jpg *.jpeg *.tga *.psd *.wav *.mp3 *.ogg *.mp4 *.mov
```

Never commit:

```text
Library/ Temp/ Obj/ Logs/ Build/ Builds/ UserSettings/
```

Built game output is a versioned release artifact, not a source input.

## Web Build Budgets (release gate, CI-enforced)

The riskiest technical decision in this plan is delivering a Blender-authored 3D atmospheric game through Unity Web. Serving policy alone does not make it load. These budgets are **design inputs** for the game creator, and CI fails the build when they regress.

| Budget line | Target for game one | Notes |
|:---|:---|:---|
| Initial download (compressed) | ≤ 50 MB, aim for 30 MB | Brotli |
| Total build | ≤ 250 MB, ≤ 1,500 files | |
| Time-to-playable | ≤ 20 s on mid-tier desktop | Measured by smoke mode, see below |
| Heap | ≤ 2 GB, wasm32 (`Maximum Memory Size = 2048`) | Keeps Safari |
| Threading | Off | Avoids COOP/COEP; revisit only with a measured CPU-bound need |
| First scene | Near-empty loader; content streamed via Addressables | |
| Compression / stripping | Brotli; Managed Stripping High; LTO release builds only | LTO is slow — release only |
| Device matrix | Desktop Chrome, Firefox, Safari, Edge — release gate. Mobile browsers — best effort, not a gate for game one | |
| CI build time | Budgeted; `Library/` cached between runs | Unity Web builds are slow and fragile |
| Audio (music stems, compressed) | ≤ 6 MB per episode (≤ 6 stems, Vorbis, joint-stereo 44.1 kHz) | Ambient loops ≤ 1 MB; tones synthesised at runtime; voice clips ≤ 3 MB per episode |
| Audio (voice) | Natural recorded voice, Sofi and Pluto; one voice session per episode or batch | Text boxes alongside voice; player can click through; mute supported; subtitles on by default |

Texture budgets, mesh LOD policy, and scene partitioning are decided in game design, not after the build.

**Smoke mode:** a `?smoke=1` build flag auto-plays to the main playable state and beacons success to `/api/v1/telemetry`. Used in CI and post-deploy verification.

**Hedge:** a desktop build (Windows/macOS) is produced as a secondary artifact once the Unity project exists. It is nearly free and covers the case where Web budgets cannot be met for a scene.

## Web Delivery Standards

Two Nginx layers with distinct duties. **Host Nginx** is the public edge: TLS and renewal, hostnames and routing, security headers, rate limits, staging access gate, access and error logs. It serves no application files. **The `web` container** (pinned `nginx:alpine`) holds the React build and the Unity Web build for exactly one release and owns everything file-specific: Unity content types and `Content-Encoding`, cache policy, SPA fallback, `release.json`. Host Nginx proxies `/` to it on loopback and must not re-compress or strip its headers (`gzip_proxied off`, default).

Release = one `web` image:

```text
registry.digitalocean.com/observatory/observatory-web:0.1.1     # release version
registry.digitalocean.com/observatory/observatory-web:<git-sha> # same image
  /usr/share/nginx/html/            React build (landing, /privacy/, /feedback/, /admin/)
  /usr/share/nginx/html/play/       Unity Web build (Brotli, hashed filenames)
  /usr/share/nginx/html/release.json
```

Every release is a new image tag; the running release is the `WEB_TAG` in the Compose env file; rollback is the previous tag. The `api` image follows the same rule (`API_TAG`). One artifact type, one registry, one rollback verb.

Caching (set inside the `web` image): HTML entry points and `*.loader.js` no-cache; hashed Unity `Build/` files and hashed Vite assets long-lived immutable; correct `Content-Type` for `.wasm`; Brotli with correct `Content-Encoding` and `Vary`; **Name Files As Hashes** on in Unity Player Settings so filenames change per release. Unity's own data caching only covers `.data`, so the image's Nginx policy carries `.wasm` and `.js`.

COOP/COEP headers are **not** set (threading off). Record as ADR; enabling later affects all cross-origin embeds.

**Release retention:** registry keeps all release-version tags and the last N (default 10) SHA tags; monthly garbage collection. The Droplet keeps the current and previous image pulled. Storage does not grow forever.

## Container Policy

Compose on the Droplet: `web`, `api`, `redis`; profile `identity`: `keycloak`; profile `jobs`: `redis-broker`, `celery-worker`, `celery-beat`. Both profiles are defined in the file and off until a named feature turns them on.

Host: Nginx, Certbot, SSH and host hardening, Docker Engine, DO monitoring agent, UFW.

Every container: pinned image tag (never `latest` alone), `restart: unless-stopped`, log rotation (`json-file` with `max-size` / `max-file`), memory limit (Keycloak 2 GB), no ports published on public interfaces — only loopback or the Compose network.

Keycloak: `KC_HOSTNAME=auth.createit.digital` (mandatory in production mode), admin console on a separate hostname or path restricted by Nginx allow-list. Realm configured from a versioned JSON export in `infrastructure/keycloak/`, imported at startup. Staging and production realms differ only by URLs and secrets. Hand-editing a realm in the console without exporting it back is a drift bug.

## Security Baseline

- SSH keys only; no password login; SSH restricted by fixed IP or VPN.
- Public exposure: HTTP/HTTPS through Nginx only. Redis, FastAPI, Keycloak, PostgreSQL never public.
- VPC / private connectivity to Managed PostgreSQL where available; TLS on database connections.
- Secrets: env files on the host outside the repo, root-owned `0600`; `docs/security/SECRETS.md` lists each secret, owner, storage location, rotation procedure. Includes Unity CI activation credentials.
- Least-privilege PostgreSQL roles; separate credentials per service and per environment.
- Keycloak admin access separate from public login endpoints and IP-restricted.
- Authorization and server-side validation for sensitive game API actions.
- Public API rate-limited (Redis). Feedback form additionally protected against automated abuse (proof-of-work or CAPTCHA — decide before public launch).
- Dependency update cadence and vulnerability response documented; Keycloak patch cadence explicitly owned.

## Privacy and Feedback Baseline

Before the first public release define: anonymous vs contactable feedback; whether IP and user agent are logged and for how long; retention for feedback, logs, and beacons; who can read feedback (`/admin/`, operator role); deletion request handling; spam handling; which device and build metadata is stored. State that Web saves are device-local and losable.

Collect only what is needed to understand and operate the release.

## Authentication and Identity

Keycloak is part of the foundation design from the start — realm as code, clients, validation rules, and the `auth.` hostname are specified and the cert SAN exists — but it **runs only when something uses it**. The first consumer is `/admin/` with operator login; until then the `identity` profile is off and pre-launch access is Nginx basic auth. Player-facing authentication is enabled only when a game feature requires stable identity (cross-device progress, cloud saves, leaderboard identity, purchases, entitlements, moderation). Offline play stays in force.

Standards: `https://auth.createit.digital/`, OAuth 2.0 / OIDC, Authorization Code + PKCE in the React shell, public clients hold no secrets, FastAPI validates issuer / signature / expiry / audience / roles, separate clients per surface, optional account linking preferred over mandatory sign-in.

Realm: `createit`. Launch clients: `observatory-web`, `observatory-api`. Launch roles: `operator`. Identity proves who is calling; it never proves that a submitted score, inventory, purchase, or game state is valid.

## Observability and Telemetry

### Baseline

DO Monitoring and alerts for Droplet health; Managed PostgreSQL alerts; DO Uptime HTTPS checks for staging and production; Nginx logs on host; container logs with rotation; Sentry for Unity client, React, FastAPI (and Celery when enabled); deploy logs, release metadata, smoke results.

### Telemetry contract — beacons, not Sentry

Sentry on Unity Web cannot see tab kills, has no IL2CPP line numbers, and reports "crash-free" misleadingly. It is the error tracker, not the funnel. The launch questions are answered by **privacy-minimal beacons** to `/api/v1/telemetry`, version-stamped, no personal data:

- Unity Web build loaded
- Main playable state reached
- Ending reached
- Fatal client error (with release version and browser family)
- Which API endpoint failed; which task failed (when jobs enabled)
- Deployment correlated with error increase (release version on every event)

### Initial alert categories

Droplet CPU / memory / disk / bandwidth; Managed PostgreSQL resource or availability; Uptime failure; health-check failure; Sentry error-rate spike; failed deploy or smoke; failed backup or restore verification; Redis memory pressure; Keycloak health; Celery queue growth (when enabled).

## Backup and Recovery

- Managed PostgreSQL automated backups and point-in-time recovery.
- Independent logical export (`pg_dump`) to object storage on a schedule.
- **Weekly Droplet backups** enabled (no IaC means the host itself must be recoverable); pre-deploy snapshot before risky changes.
- Keycloak realm export in git plus database backup.
- Release artifacts and previous known-good release always available for rollback.
- Redis cache not backed up; broker Redis AOF only when jobs profile is on.

**Targets (fill with real numbers at provisioning; drill quarterly):**

| Target | Initial |
|:---|:---|
| RPO database | ≤ 24 h via logical export; PITR where enabled |
| RTO public site + game | ≤ 4 h (pull `web` + `api` images to a fresh Droplet, restore env files, reload Nginx) |
| RTO Droplet rebuild | ≤ 1 working day |
| Backup retention | 4 weeks Droplet; 30 days logical exports |
| Restore drill | Quarterly, logged in `docs/runbooks/restore.md` |

## CI/CD and Release Process

```text
Feature branch → review → merge → CI checks → staging deploy → smoke (?smoke=1) + manual play → versioned release → production deploy → post-deploy smoke
```

Checks as applicable: React lint/type/test; Python lint/type/test; API contract validation; Unity EditMode/PlayMode tests; Unity Web build with **budget enforcement**; container build and vulnerability scan; Nginx config validation.

### Unity CI requirement

The project builds from a clean checkout in batch mode. The plan names the activation mechanism: **Unity account credentials + authenticator (TOTP) secret in CI secrets**, registered in `SECRETS.md`, with an activation-failure runbook entry. This is the most fragile link in the pipeline. `Library/` is cached between runs; Git LFS bandwidth in CI is measured and budgeted.

### Release artifacts

Every build records `game_id`, `version`, `git_sha`, `unity_version`, `build_target`, `build_timestamp_utc`, `artifact_checksum`, and the budget measurements. The game shows its version in a non-intrusive place.

### Deployment rules

Immutable versioned images only (`web`, `api`); the same image digest goes from staging to production; at least one prior known-good tag kept and pulled; never `latest` alone; migrations as controlled, logged steps; host Nginx config validated before reload; post-deploy HTTP and `?smoke=1` verification; rollback documented for `web` images, `api` images, migrations, configuration.

## Milestones

| Milestone | Definition of done |
|:---|:---|
| **M0 — Playable, gated** | Unity Web build meets budgets; served from the production Droplet at `observatory.createit.digital/play/` behind basic auth; landing + synchronous feedback endpoint work; `web`/`api` deployed and rolled back once each by tag. **No further platform work starts until M0 is green.** |
| **M1 — Public release 0.1** | Second Droplet (staging) live and used for the release candidate; gate removed from production; beacons flowing; restore drilled once. `/admin/` with operator login (and therefore the `identity` profile) ships in M1 **only if** feedback volume makes reading it in the database impractical — otherwise it is the first post-launch feature. |
| **M2 — Second creator** | A second person ships a playable web build on the documented path in under one week. Reuse gate opens; plan v3 (creator platform) is written from what actually happened. |

Enable the `jobs` profile only when M1 or M2 produces a real task. Enable the `identity` profile only with `/admin/`.

## First Product: The Lost Observatory

A never-ending episodic exploration series about space and engineering optimism. The player is Sofi, a young, curious girl, and her companion Pluto, a quicksilver being that can take any form.

**Full design: `docs/game-design/`.** See `vision.md` for general decisions, `world.md` for characters and the tonal language, `episode-01/GDD.md` for the Episode 1 release contract.

**Episode 1 release contract (0.1):** Sofi and Pluto arrive at a big telescope (real location: VIRAC, Latvia). Sofi saw aliens in a cartoon and wants to find one. She restores the power, opens the dome, wakes the telescope, and discovers a signal the previous observer never answered. One place, roughly 10–15 minutes; runs from `https://observatory.createit.digital/play/`; Unity 6.3 LTS; deployable and rollback-able through the platform process; no login, payments, or backend dependency; local save; offline play; landing, privacy, feedback; **meets the Web Build Budgets including audio**.

**Out of scope per episode:** mandatory login, cloud save, leaderboards, payments, advertising, multiplayer, chat, UGC, in-game economy, analytics platform, combat, procedural worlds, dialogue trees, inventory, showing the source of the signal, explaining Pluto's origin, more than one location per release.

## Distribution

Canonical home is the self-hosted domain. That is the educational point. Game one is education and portfolio; it is not designed for ad-portal economics and will not be bent toward them. itch.io as a secondary free listing is optional and cheap. Portal submission, feature flags per build target, and monetization design are **out of scope** until a game exists whose shape fits them; if the creator-platform hypothesis passes, its model is education/club, not ad share.

## Reuse Policy

Extract low-risk reusable assets immediately: deploy scripts, runbooks, Nginx snippets, CI conventions, Unity standards, Compose profiles, realm export pattern. Extract application services and multi-game APIs only after a second game demonstrates the same requirement. Do not force future games into the first game's domain model.

## Documentation Requirements

```text
README.md                         Local setup and primary commands
AGENTS.md                         Agent and AI collaboration rules
docs/adr/                         Unity 6.3 LTS; WebGL2 now / WebGPU later; wasm32 + threading off;
                                  production Droplet first, staging second; web image not host files;
                                  Keycloak on-box as profile `identity`; Celery as profile `jobs`;
                                  identity in React shell; sizing + cost
docs/architecture/                Diagrams and service boundaries
docs/devops/                      Hosting program: findings, general plan, one file per operation
docs/runbooks/deploy.md           Deployment procedure
docs/runbooks/rollback.md         Rollback procedure
docs/runbooks/restore.md          Database and Droplet recovery + drill log
docs/runbooks/incident.md         Incident response basics
docs/security/SECRETS.md          Secrets register: name, owner, location, rotation
docs/game-design/                 Per-game design documents
```

Runbooks are written when the operation is real and updated when it changes. Empty stubs are not documentation.

## Operational Ownership

One person owns operations at this scale. Write it down so it is a decision, not an omission.

| Item | Owner | Expectation |
|:---|:---|:---|
| Deploy to production | Platform owner | Via documented process only |
| Failed deploy / rollback review | Platform owner | Same day |
| Sentry alert review | Platform owner | Weekly, or on spike alert |
| DO infrastructure and PostgreSQL alerts | Platform owner | Best effort, 48 h |
| Database restore | Platform owner | Quarterly drill |
| Secret rotation | Platform owner | Per `SECRETS.md` |
| OS, dependency, Keycloak patches | Platform owner | Monthly checklist |
| Unity CI failures | Game creator first; platform owner for activation issues | |
| Public release approval | Both | |
| Privacy / deletion requests | Platform owner | 30 days |
| Production failure response | Platform owner | Best effort, 48 h; game stays playable offline regardless |

## Agent Collaboration Rules

- Preserve offline play unless a change explicitly modifies the product contract.
- Propose a plan before broad cross-project changes.
- Prefer small, reviewable, reversible changes.
- Do not change identity, production networking, secrets, deployment, or database schema without explicit review.
- Do not introduce client-side secrets or trust client-submitted competitive, financial, or entitlement state.
- Do not enable the `jobs` profile or player-facing login without a named feature that requires it.
- Do not add multi-tenant or generic multi-game abstractions before M2.
- Keep generated code readable and consistent with project conventions.
- Update tests, documentation, runbooks, and release notes when behavior or operations change.
- Never overwrite a working scene, asset, or deployment configuration without a Git commit or explicit review point.

## Definition of a Stable Foundation

The foundation is stable when a new game can:

1. Start from the Unity project conventions and repository structure.
2. Build a versioned Unity Web artifact through CI that passes the Web Build Budgets.
3. Deploy to staging and production through documented procedures.
4. Serve from a dedicated `*.createit.digital` domain through host Nginx.
5. Use FastAPI, Managed PostgreSQL, Redis, and Keycloak according to these conventions, enabling jobs and identity only when a feature needs them.
6. Be monitored through DO Monitoring, Uptime, beacons, and Sentry.
7. Roll back to a prior known-good release.
8. Remain playable without application backend services.
9. Reuse runbooks, security controls, and release conventions.
10. **Reach a deployed playable build by a second creator in under one week** — the measure that the capacity, not just the game, exists.

## Change log v1.1 → v2.1

- Purpose ranked; tiebreaker stated. Creator platform named as hypothesis with gate.
- Launch capability: Keycloak running but operator-gated (`/admin/`, staging); Celery/Beat as Compose profile, off; launch schema minimal; clients reduced to `observatory-web` + `observatory-api`.
- Identity flow corrected: PKCE in React shell, token to Unity via JS bridge.
- Unity pinned to 6.3 LTS (6000.3.x); WebGL 2; wasm32; threading off; COOP/COEP off — as ADRs.
- New: Web Build Budgets (CI gate), smoke mode, desktop hedge, milestones M0–M2.
- New: sizing, cost model, accepted-risk statements, release retention, Redis cache/broker split with eviction and AOF policy, container restart/log/memory rules, realm as code, `KC_HOSTNAME`, secrets mechanism, Unity CI activation named, LFS budget, Droplet backups, RPO/RTO table with drill cadence, ownership table with expectations.
- Telemetry moved from Sentry-implied to explicit beacons; DO Uptime named as a separate product.
- Removed: portal/monetization strategy (out of scope for game one); `observatory-admin` / `observatory-mobile` clients at launch; pre-modeled leaderboard/entitlement schema.
- "Production-grade" reworded to state single-Droplet as a scoped, revisitable decision.
- **2026-09-09 (DevOps program):** static delivery moved from host-Nginx files under `/srv/game-platform` to a versioned `web` image (`nginx:alpine` + React + Unity Web). Host Nginx is edge-only. One artifact type (images), one rollback verb (tag). Reason: no second release mechanism; every deployable is a SHA-tagged image in the registry. ADR to be written at provisioning.
- **2026-09-09 (scale-down):** one Droplet first — production-named, owns `observatory.createit.digital`, basic-auth gated until launch; staging Droplet added before the first public release. Keycloak moved from "running, operator-gated" to Compose profile `identity`, off, because it has no relying party until `/admin/` exists; `/admin/` + operator login is the named feature that enables it. Initial Droplet size reduced to 2 GB accordingly. Two-Droplet and Keycloak designs are postponed, not dropped — specs stay complete.
