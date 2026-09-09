# Game Platform Base Plan

## Status

**Status:** Production foundation specification — implementation in progress

**First game:** The Lost Observatory

**Primary product domain:** `observatory.createit.digital`

**Platform identity domain:** `auth.createit.digital`

## Purpose

Build a reusable, self-hosted production platform for Unity-based games and interactive real-time experiences.

The platform has three purposes:

1. **Product:** deliver a complete, publicly hosted first game, starting with *The Lost Observatory*.
2. **Learning:** expose real production concepts through the construction and operation of a real product.
3. **Foundation:** provide reusable delivery, hosting, API, identity, data, background-processing, and operations conventions for future games.

The first game is not a throwaway prototype. It is a constrained, complete product built on a production-grade foundation.

The platform is production-grade from day one. There are no temporary architectural choices that must be replaced later. Operational scope is controlled: Terraform, CDN, multi-node availability, Kubernetes, and enterprise analytics are intentionally out of the current scope because there is no requirement for them. They can be added later without replacing the architecture.

## Core Intent

The platform should allow a game creator to focus on:

- Game ideas and player experience
- Unity scenes, interactions, visuals, audio, and gameplay
- Meaningful iteration and release
- Understanding production systems through concrete platform capabilities

The production foundation exists from the start, but it is used progressively. A game creator does not need to solve infrastructure details before seeing a playable result. When a new capability is needed, the platform exposes the real architecture and documentation for that capability.

The platform should make simple work simple, while making real architecture available when a feature requires it.

## Why Not a Web-Only or Managed Web Platform

A web-only AI coding workflow or a managed deployment service can be useful for rapid experiments. It can also become a dead end when the product requires:

- A game engine and native runtime workflow
- Unity scenes, assets, physics, animation, and platform builds
- Controlled self-hosted deployment
- Private network and database architecture
- Custom security and identity decisions
- Versioned game releases and rollback
- Direct ownership of player data and product behavior
- A stack that can evolve into desktop, web, mobile, console, or XR products

This project intentionally keeps stack ownership and operational control.

It does not reject managed services entirely. It uses them where they provide clear operational value, such as Managed PostgreSQL, DigitalOcean Monitoring, and Sentry. It avoids making a third-party development or deployment abstraction the entire product architecture.

## Production Scope

The foundation is production-grade and small-scale.

### Included from day one

- Unity 6 LTS game client using C#
- Blender asset workflow
- Git + Git LFS source control
- Self-hosted public delivery on `observatory.createit.digital`
- Host-level Nginx for TLS, routing, static assets, Unity Web builds, and reverse proxying
- Docker Compose for application services
- DigitalOcean Droplet runtime
- DigitalOcean Managed PostgreSQL
- Redis container
- FastAPI application service
- Celery worker and Celery Beat
- Keycloak as the platform identity provider at `auth.createit.digital`
- DigitalOcean Monitoring
- Sentry error tracking
- Staging and production environments
- Versioned release artifacts
- CI/CD and controlled deployment
- Backup, restore, incident, security, deployment, and rollback runbooks
- Privacy and data-handling rules for the public release

### Intentionally out of current scope

These are not architectural placeholders. They are deferred platform capabilities that can be added later without changing the core architecture.

- Terraform or other infrastructure-as-code
- CDN
- Multi-node high availability
- Kubernetes
- Full PLG/product analytics stack
- Large-scale log aggregation
- Multi-region delivery
- Console or mobile store automation
- Real-time multiplayer infrastructure
- Payment and entitlement systems
- User-generated content moderation platform

## Architectural Principles

1. **The game is independently playable.** Core gameplay, rendering, audio, interaction, and local saves must not depend on backend availability.
2. **Production discipline starts immediately.** Use version control, reproducible builds, CI/CD, staging, deployment runbooks, monitoring, error tracking, backups, and rollback from the first release.
3. **Production-grade does not require production-scale complexity.** A controlled single-Droplet deployment with managed data, backups, security, monitoring, and rollback is production-grade for the current product scope.
4. **All selected platform capabilities are implemented to production standard.** Redis, Celery, FastAPI, PostgreSQL, and Keycloak are not temporary services. They are durable parts of the foundation.
5. **The game client is untrusted.** A Unity Web, desktop, or mobile client can be inspected and modified. The server validates all data that affects other players, durable progress, competition, entitlement, or money.
6. **Use standards at boundaries.** Use HTTPS, OpenAPI, OAuth 2.0/OpenID Connect, PostgreSQL, Docker images, and versioned release artifacts.
7. **Keep ownership clear.** Unity owns game runtime behavior. FastAPI owns public server APIs. PostgreSQL owns durable business data. Redis owns ephemeral coordination, cache, and queue state. Keycloak owns identity.
8. **Use small, coherent releases.** Each release is versioned, deployable, testable, observable, and reversible.
9. **Avoid premature generalization.** The first game does not define platform-wide APIs. Shared platform abstractions are extracted only after repeated real usage.
10. **Keep simple paths simple.** A game creator can open Unity, press Play, and iterate without running application containers locally.

## Technology Decisions

| Area | Decision | Role |
|---|---|---|
| Game engine | Unity 6 LTS | Primary game client, scenes, rendering, interaction, physics, UI, exports |
| Game language | C# | Unity gameplay and editor code |
| 3D assets | Blender | Source modelling, scene assets, asset preparation |
| Public web product | React + TypeScript | Landing, player, and admin surfaces |
| Public API | FastAPI | Game platform APIs, feedback, player services, integrations |
| Durable data | DigitalOcean Managed PostgreSQL | System of record for application and game-service data |
| Cache and broker | Redis container | Celery broker, caching, rate limits, short-lived state, coordination |
| Background jobs | Celery worker + Celery Beat | Asynchronous and scheduled work |
| Identity | Keycloak | OAuth 2.0/OpenID Connect identity and access management |
| Reverse proxy | Host-level Nginx | TLS, routing, static files, Unity Web delivery, reverse proxy to application containers |
| Runtime | DigitalOcean Droplets + Docker Compose | Containerized application services and controlled deployment |
| Monitoring | DigitalOcean Monitoring | Droplet and infrastructure metrics and alerts |
| Error tracking | Sentry | Client, API, worker, and scheduler error reporting |
| Source control | Git + Git LFS | Source history and large binary asset management |
| CI/CD | Repository-hosted CI plus self-managed build/deploy workflow | Tests, Unity builds, artifact publishing, staging and production deployment |

## Domain Model

### Public product domain

```text
https://observatory.createit.digital/
```

Routes:

```text
/             Landing page and product information
/play/        Unity Web build
/privacy/     Privacy information
/feedback/    Feedback page
/status/      Optional public status surface
/api/v1/      FastAPI public API
/admin/       Internal administration UI when introduced
```

### Platform identity domain

```text
https://auth.createit.digital/
```

Keycloak is hosted as a reusable platform identity service. It is not coupled to one game URL path.

Future games may use independent product domains while sharing the same identity domain.

## Runtime Architecture

```text
Browser
  |
  v
observatory.createit.digital
  |
  v
Host-level Nginx on DigitalOcean Droplet
  |-------------------------------|
  |                               |
  v                               v
React web application             Unity Web release artifacts
                                  /play/
  |
  v
/api/v1/ reverse proxy
  |
  v
FastAPI container
  |-------------------------------|
  |                               |
  v                               v
DigitalOcean Managed PostgreSQL   Redis container
Durable system of record          Cache, rate limits, Celery broker
                                  |
                                  v
                         Celery worker and Celery Beat containers
```

Identity:

```text
Unity/Web client
  |
  | Authorization Code Flow with PKCE
  v
Keycloak at auth.createit.digital
  |
  v
FastAPI validates access tokens and applies API authorization
```

## Service Boundaries

### Unity game client

The Unity client owns:

- Gameplay logic
- Scenes, prefabs, UI, physics, input, audio, visuals, and local saves
- Offline play
- Client-side presentation of remote data when remote features exist

The Unity client must not contain:

- Database credentials
- Keycloak administrator credentials
- Payment-provider secrets
- Privileged API keys
- Trust assumptions for player-submitted scores, inventory, currency, or purchases

The game must work when FastAPI, Redis, Celery, or Keycloak is unavailable. Only optional online features may be disabled by a service outage.

### React web application

The web application owns:

- Public landing pages
- Game information and release notes
- Feedback user interface
- Future player account pages
- Future administration interface

### FastAPI service

The API owns:

- Public HTTP API contracts
- Request validation and authorization
- Server-side validation of sensitive game actions
- Platform integrations
- Feedback endpoints
- Future cloud-save, leaderboard, entitlement, and account-linking capabilities

### PostgreSQL

Managed PostgreSQL is the durable system of record for:

- Feedback and operational records
- Player and account-linked application records
- Cloud-save metadata and durable game-service data
- Leaderboard records
- Entitlements and payment-related records when introduced
- Audit records and durable job business state

Use separate database users and clear ownership boundaries. Keycloak must use a separate database or a clearly isolated schema and user.

### Redis

Redis is used for:

- Celery message broker
- Cache
- Rate limiting
- Short-lived sessions or temporary state
- Idempotency keys
- Distributed coordination where appropriate

Redis is not the authoritative store for accounts, purchases, entitlements, permanent game progress, or permanent leaderboard data.

### Celery

Celery provides:

- Background task processing through Celery workers
- Scheduled dispatch through one Celery Beat instance

All durable task effects must be idempotent. PostgreSQL constraints and transactions protect correctness. Redis locks may optimize coordination but do not establish business correctness.

Only one Celery Beat instance runs in production unless a deliberate scheduler leader-election mechanism is introduced.

## Environments

Maintain separate local, staging, and production environments.

| Environment | Purpose | Required behavior |
|---|---|---|
| Local | Fast development and automated tests | Unity can run without Docker or backend services |
| Staging | Integration, deploy validation, tester access | Mirrors production routes and deployment process with separate secrets and database |
| Production | Public stable release | Versioned artifacts, monitoring, backups, error tracking, documented rollback |

Use separate environment configuration and secrets. Do not share production databases, credentials, OAuth clients, or signing materials with staging.

## Initial Production Availability Posture

The initial production topology is:

```text
Single application Droplet
DigitalOcean Managed PostgreSQL
Host-level Nginx
Docker Compose application services
Controlled object storage for backups and artifacts where required
```

This provides a controlled, recoverable production environment. It is not a high-availability architecture.

A Droplet failure may require redeploy or restore. Planned maintenance may cause downtime. These limitations are acceptable because release artifacts, configuration, database backups, and restore procedures are complete and tested.

High availability, multiple application nodes, container orchestration, and distributed systems are deferred until there is a concrete availability or scale requirement.

## Repository Layout

```text
game-platform-base/
├── apps/
│   ├── game-unity/                 # Unity project: first game is The Lost Observatory
│   │   ├── Assets/
│   │   │   ├── _Game/
│   │   │   │   ├── Art/
│   │   │   │   ├── Audio/
│   │   │   │   ├── Materials/
│   │   │   │   ├── Prefabs/
│   │   │   │   ├── Scenes/
│   │   │   │   ├── Scripts/
│   │   │   │   ├── ScriptableObjects/
│   │   │   │   └── Tests/
│   │   │   └── ThirdParty/
│   │   ├── Packages/
│   │   └── ProjectSettings/
│   ├── web/                        # React + TypeScript web application
│   ├── api/                        # FastAPI application
│   └── admin/                      # Internal administration UI when needed
├── packages/
│   ├── api-contracts/              # OpenAPI contract and generated clients
│   ├── web-ui/                     # Shared web UI package when repeated usage exists
│   └── game-config/                # Public, versioned configuration only
├── infrastructure/
│   ├── compose/
│   ├── nginx/
│   ├── scripts/
│   └── backup/
├── tools/
│   ├── unity/                      # CI build entry points and build helpers
│   ├── blender/                    # Source asset tooling
│   └── python/                     # Data and asset tooling
├── docs/
│   ├── adr/
│   ├── architecture/
│   ├── game-design/
│   ├── runbooks/
│   └── security/
├── .github/workflows/
├── .cursor/
├── AGENTS.md
├── Makefile
└── README.md
```

## Unity Project Standards

Configure Unity from the first commit:

```text
Version Control Mode: Visible Meta Files
Asset Serialization Mode: Force Text
```

Track Unity source assets and their `.meta` files together.

Use Git LFS for large binary assets, including:

```text
*.blend
*.fbx
*.glb
*.gltf
*.png
*.jpg
*.jpeg
*.tga
*.psd
*.wav
*.mp3
*.ogg
*.mp4
*.mov
```

Do not commit generated Unity directories:

```text
Library/
Temp/
Obj/
Logs/
Build/
Builds/
UserSettings/
```

Use source assets, scripts, scenes, prefabs, packages, project settings, and infrastructure configuration as version-controlled inputs. Treat built game output as a versioned release artifact.

## Web Delivery Standards

Nginx runs on the Droplet host and is the public edge.

Nginx responsibilities:

- TLS termination and certificate renewal
- Host and route configuration
- Static delivery of web and Unity Web release artifacts
- Reverse proxy to private FastAPI ports
- Correct Unity Web content types, compression headers, and cache policy
- Security headers appropriate to the product
- Access logging and error logging

Unity Web release layout:

```text
/srv/game-platform/
├── releases/
│   ├── the-lost-observatory-0.1.0/
│   │   ├── site/
│   │   └── play/
│   └── the-lost-observatory-0.1.1/
├── current -> releases/the-lost-observatory-0.1.0
└── shared/
```

Caching policy:

- HTML entry points use short-cache or no-cache behavior.
- Versioned Unity build assets use long-lived immutable caching.
- Unity WebAssembly files use the correct `Content-Type`.
- Brotli or gzip build output uses the correct `Content-Encoding` and `Vary` headers.
- New releases use unique, versioned artifact paths to prevent mixed old/new browser caches.

## Container Policy

Use Docker Compose for application services.

Containerize:

- FastAPI
- Celery worker
- Celery Beat
- Redis
- Keycloak
- Future application-specific workers

Keep on the host:

- Nginx
- TLS certificate management
- SSH and host security controls
- Docker Engine
- DigitalOcean monitoring agent
- Host firewall configuration

PostgreSQL is provided by DigitalOcean Managed PostgreSQL and is not run in a Droplet container for production.

## FastAPI and Worker Layout

Use one application image with separate runtime roles:

```text
api                 FastAPI HTTP service
celery-worker       Celery worker process
celery-beat         Celery Beat scheduler process
redis               Redis broker/cache
keycloak            Identity provider
```

Use pinned application image tags. Do not deploy only `latest`.

Use a single production Celery Beat instance.

Use UTC for scheduled tasks and stored timestamps unless a documented product requirement says otherwise.

## Security Baseline

- SSH key authentication only; no password login.
- Restrict SSH access by fixed IP, VPN, or bastion policy.
- Expose only HTTP/HTTPS publicly through Nginx.
- Do not expose Redis, FastAPI, Keycloak container ports, or PostgreSQL publicly.
- Use DigitalOcean VPC/private connectivity for application-to-database traffic where available.
- Use TLS for public traffic and database connections.
- Store secrets outside the repository and rotate them through documented procedures.
- Use least-privilege PostgreSQL roles and separate service credentials.
- Keep Keycloak administration access separate from public login endpoints and restrict administrative access.
- Require authorization and server-side validation for sensitive game API actions.
- Rate-limit public API endpoints.
- Maintain dependency update and vulnerability-response practices.
- Maintain a documented list of secrets, their owners, rotation procedure, and storage location.

## Privacy and Feedback Baseline

The first public release includes a feedback capability and must define:

- Whether feedback is anonymous or may include contact information
- Whether IP addresses and user-agent information are logged
- Retention period for feedback and logs
- Who can access submitted feedback
- How deletion requests are handled
- How spam and abusive submissions are addressed
- Which player device and build metadata is stored for troubleshooting

Do not collect more data than is needed to understand and operate the release.

## Authentication and Identity

Keycloak is part of the production platform from the start. Player-facing authentication is enabled only when a product feature uses it.

Keycloak standards:

- Available at `https://auth.createit.digital/`.
- Uses OAuth 2.0/OpenID Connect.
- Browser and native/mobile clients use Authorization Code Flow with PKCE.
- Public clients do not hold client secrets.
- FastAPI validates token issuer, signature, expiry, audience, and applicable authorization claims.
- Separate Keycloak clients exist for web game, mobile game, API, and administration surfaces.
- Optional account linking is preferred over mandatory sign-in before first play.
- If Keycloak or the API is unavailable, offline gameplay still works and only online features are disabled.

Initial platform realm:

```text
createit
```

Initial client concept:

```text
observatory-web
observatory-mobile
observatory-api
observatory-admin
```

Identity proves the caller identity. It does not prove a submitted score, inventory, purchase, or game state is valid.

## Observability Baseline

### Required baseline

- DigitalOcean Monitoring and alerts for Droplet health.
- Managed PostgreSQL monitoring and alerts.
- Nginx access and error logs on the host.
- Docker container logs for application services.
- Sentry for Unity client, React web, FastAPI, Celery worker, Celery Beat, and Keycloak-adjacent integration errors.
- HTTPS uptime checks for production and staging.
- Deployment logs, release metadata, and smoke-test results.

### Launch telemetry contract

The platform must answer these questions without unnecessary personal data:

- Did the Unity Web build load?
- Did the game reach the main playable state?
- Did a fatal client error occur?
- Which release version failed?
- Which browser/device family failed?
- Did the player reach the ending?
- Which API endpoint failed?
- Which Celery task failed?
- Did a deployment correlate with an error increase?

A full product-led-growth analytics stack is not part of the current scope.

### Initial alert categories

- High CPU, memory, disk, load, or bandwidth usage on the Droplet.
- Managed PostgreSQL resource, connection, or availability alert.
- HTTPS availability failure.
- Application health-check failure.
- Repeated Sentry exceptions or elevated error rate.
- Failed deployment or smoke test.
- Failed backup or restore-verification job.
- Redis memory pressure or failed Redis health check.
- Celery queue growth or task failure pattern.
- Keycloak startup or health failure.

## Backup and Recovery

- Use DigitalOcean Managed PostgreSQL automated backups and point-in-time recovery capabilities.
- Maintain an independent logical database export strategy to controlled object storage when data value requires provider-independent recovery.
- Keep release artifacts and previous deployable versions available for rollback.
- Back up persistent Redis data only when loss of the selected Redis workload is operationally material; Redis remains non-authoritative.
- Test database restore procedures periodically.
- Document recovery objectives, restore ownership, and recovery runbooks.

The production baseline must define:

- Target RPO for database data
- Target RTO for the public site and game
- Target RTO for rebuilding the Droplet
- Backup retention periods
- Ownership of restore testing

## CI/CD and Release Process

### Build pipeline

```text
Feature branch
  -> Pull request
  -> Automated checks
  -> Merge to main
  -> Staging deployment
  -> Smoke test and manual gameplay verification
  -> Versioned release
  -> Production deployment
```

Automated checks include as applicable:

- React linting, type checking, and tests
- Python linting, type checking, and tests
- API contract validation
- Unity EditMode and PlayMode tests where suitable
- Unity command-line Web build
- Container image build and vulnerability checks
- Infrastructure configuration validation

### Unity CI requirement

The Unity project must build in CI from a clean checkout.

This verifies:

- Unity editor version is pinned and reproducible.
- CI license/activation is documented and controlled.
- The project opens in batch mode without unexpected manual steps.
- Required packages and settings are present in the repository.
- Unity Web output is produced as a versioned artifact.
- Build logs and artifact checksums are captured.
- A staging deployment serves the artifact correctly.
- The game reaches a defined smoke-test state.

### Release artifacts

Every deployable game build records:

```text
game_id
version
git_sha
unity_version
build_target
build_timestamp_utc
artifact_checksum
```

The game displays a build version in a non-intrusive place such as a settings or pause screen.

### Deployment rules

- Deploy immutable, versioned artifacts; do not deploy untracked working directories.
- Deploy the same verified artifact from staging to production.
- Keep at least one known-good prior static release available.
- Use image tags, never only `latest`, for application containers.
- Run database migrations as controlled, logged deployment steps.
- Validate Nginx configuration before reload.
- Run post-deploy HTTP and Unity Web smoke tests.
- Document rollback for static releases, API images, database migrations, and configuration changes.

## First Product: The Lost Observatory

### Product definition

The Lost Observatory is a short, atmospheric 3D exploration and puzzle game.

### Initial release contract

The first public release must:

- Run from `https://observatory.createit.digital/play/`.
- Be hosted on owned DigitalOcean infrastructure.
- Use Unity 6 LTS and C# for gameplay.
- Be deployable through the platform CI/CD process.
- Work without mandatory login, payments, or required gameplay backend availability.
- Support a clear beginning, progression, and ending.
- Be playable in approximately 10 to 15 minutes.
- Include a public landing page, privacy information, and feedback capability.
- Include release versioning, monitoring, error tracking, and rollback procedures.

### Initial gameplay scope

```text
Goal: Restore power to an abandoned observatory and activate its telescope.

Core actions:
- Explore a small environment.
- Interact with objects.
- Find and use required items or clues.
- Solve one connected environmental puzzle chain.
- Restore power.
- Trigger a clear visual and audio ending.
```

### Explicitly deferred product features

These are product features, not architectural shortcuts:

```text
Mandatory login
Cloud save
Leaderboards
Payments and entitlements
Advertising
Multiplayer
Chat
User-generated content
Complex in-game economy
Large-scale analytics platform
```

## Initial Capability Rollout

The production architecture is fixed. Product features activate as needed.

### Launch capability

- Unity project and playable game
- React public product site
- Self-hosted Unity Web build
- FastAPI service foundation
- Feedback API and privacy-compliant storage
- Managed PostgreSQL
- Redis, Celery worker, and Celery Beat foundation
- Keycloak service foundation and realm configuration
- Host Nginx and TLS
- Staging and production
- Versioned release directories
- Deployment and rollback
- Monitoring, Sentry, logs, and alerts

### Player account activation

Player-facing authentication is enabled when the first feature requires stable identity, such as:

- Cross-device progress
- Cloud saves
- Leaderboard identity
- Purchases
- Entitlements
- Moderation

The offline gameplay requirement remains in force.

### Reuse activation

Platform-wide APIs and shared multi-game abstractions are extracted only after a second game demonstrates repeated requirements.

Low-risk reusable assets—deployment scripts, runbooks, templates, CI conventions, Nginx snippets, and Unity standards—are extracted immediately.

## Reuse Policy

The platform is reusable, but reuse must be earned.

Rules:

- Keep the first game simple and specific.
- Keep seams clean: game client, web product, API, data, identity, and deployment are separate.
- Do not define a generic multi-game API until two games demonstrate the same requirement.
- Extract reusable scripts, documentation, and deployment patterns early because they are low-risk.
- Extract reusable application services only after repeated real usage.
- Keep per-game design data and build configuration explicit.
- Do not force future games into the first game’s domain model.

## Documentation Requirements

Maintain these documents as the platform evolves:

```text
README.md                         Local setup and primary commands
AGENTS.md                         Agent and AI collaboration rules
docs/architecture/                System diagrams and service boundaries
docs/adr/                         Architecture Decision Records
docs/runbooks/deploy.md           Deployment procedure
docs/runbooks/rollback.md         Rollback procedure
docs/runbooks/restore.md          Database and service recovery
docs/runbooks/incident.md         Incident response basics
docs/security/                    Secrets, access, and security practices
docs/game-design/                 Per-game design documents
```

## Operational Ownership

Define ownership before public launch:

- Who can deploy to production?
- Who reviews failed deploys and rollbacks?
- Who owns Sentry alert review?
- Who owns DigitalOcean infrastructure alerts?
- Who owns Managed PostgreSQL alerts?
- Who can restore the database?
- Who can rotate secrets?
- Who applies operating-system and dependency updates?
- Who reviews Unity CI build failures?
- Who approves public releases?
- Who responds to privacy or data-deletion requests?
- What is the expected response time for production failure?

## Agent Collaboration Rules

- Preserve the game’s offline-play requirement unless a change explicitly modifies the product contract.
- Propose a plan before making broad cross-project changes.
- Prefer small, reviewable, reversible changes.
- Do not change identity, production networking, secrets, deployment, or database schema without explicit review.
- Do not introduce client-side secrets or trust client-submitted competitive, financial, or entitlement state.
- Keep generated code readable and consistent with project conventions.
- Update tests, documentation, and release notes when behavior or operations change.
- Never overwrite a working scene, asset, or deployment configuration without a Git commit or explicit review point.

## Definition of a Stable Foundation

The Game Platform Base is stable when a new game can:

1. Start from the Unity project conventions and repository structure.
2. Build a versioned Unity Web artifact through CI.
3. Deploy to staging and production through documented procedures.
4. Serve from a dedicated `*.createit.digital` domain through host-level Nginx.
5. Use FastAPI, Redis/Celery, Managed PostgreSQL, and Keycloak according to production conventions.
6. Be monitored through DigitalOcean infrastructure monitoring and Sentry error tracking.
7. Roll back to a prior known-good release.
8. Remain playable without application backend services.
9. Reuse platform documentation, runbooks, security controls, and release conventions.
10. Demonstrate successful reuse by a second game before platform-wide APIs are generalized.
