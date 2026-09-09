# docs/devops/operations/compose-deploy.md

# Compose deploy and release

**Source (verified in Revy):** `.github/workflows/deploy.yml` deploy job (pull by SHA, migrate on Droplet from the deployed image, stop/rm/run, loopback ports, `--env-file`), `deploy/keycloak/config/docker-compose.yml`, `deploy/env-examples/*`.

**Adapted:** Revy uses ad-hoc `docker run` per container from GitHub Actions. Observatory uses **one Compose file** with two profiles, `identity` and `jobs`, both off at launch. Everything deployable is an image: `web` ([web-image.md](./web-image.md)) and `api` from the registry, `keycloak` built on the Droplet when its profile is enabled. One artifact type, one rollback verb (change a tag). No GitHub until this repo has a remote; the same steps run from a deploy script.

**First deployment target is the single production Droplet** (Q3). Staging receives the same file later (P7).

---

## What gets deployed

| Service | Image | Tag var | Profile |
|:---|:---|:---|:---|
| `web` — React shell + Unity Web build | `observatory-web` (DOCR) | `WEB_TAG` | default |
| `api` — FastAPI | `observatory-api` (DOCR) | `API_TAG` | default |
| `redis` — cache | `redis:7-alpine` | pinned in file | default |
| `keycloak` | built from `/srv/observatory/keycloak` | pinned in file | `identity` — **off** (Q16, P8) |
| `redis-broker`, `celery-worker`, `celery-beat` | `redis:7-alpine`, `observatory-api` | `API_TAG` | `jobs` — **off** |

Nothing is served from the host filesystem. Host Nginx proxies to `web` (8081) and `api` (8000) on loopback. `docker compose ps` on the launch box shows exactly three services.

---

## `infrastructure/compose/docker-compose.yml`

```yaml
name: observatory

x-logging: &logging
  logging: { driver: json-file, options: { max-size: "10m", max-file: "3" } }

services:
  web:
    image: registry.digitalocean.com/observatory/observatory-web:${WEB_TAG:?set WEB_TAG to a release version or git sha}
    restart: unless-stopped
    ports: ["127.0.0.1:8081:8080"]
    read_only: true
    tmpfs: ["/tmp", "/var/cache/nginx", "/var/run"]
    mem_limit: 128m
    networks: [observatory-net]
    <<: *logging

  api:
    image: registry.digitalocean.com/observatory/observatory-api:${API_TAG:?set API_TAG to a git sha or version}
    restart: unless-stopped
    env_file: /srv/observatory/env/api.env
    environment: { SENTRY_RELEASE: "${API_TAG}" }
    ports: ["127.0.0.1:8000:8000"]
    depends_on: [redis]
    networks: [observatory-net]
    <<: *logging

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: ["redis-server", "--maxmemory", "128mb", "--maxmemory-policy", "allkeys-lru", "--save", ""]
    networks: [observatory-net]
    <<: *logging

  # ---- profile identity: defined, not started, until /admin/ with operator login exists (Q16, P8) ----
  keycloak:
    profiles: [identity]
    build: /srv/observatory/keycloak
    image: observatory-keycloak:26.0
    restart: unless-stopped
    command: start --optimized --import-realm
    env_file: /srv/observatory/env/keycloak.env
    volumes:
      - /srv/observatory/keycloak/realm-export.json:/opt/keycloak/data/import/createit-realm.json:ro
    ports: ["127.0.0.1:8080:8080", "127.0.0.1:9000:9000"]
    mem_limit: 1g
    networks: { observatory-net: { aliases: [keycloak] } }
    <<: *logging

  # ---- profile jobs: defined, not started, until a real task exists (plan v2.1) ----
  redis-broker:
    profiles: [jobs]
    image: redis:7-alpine
    restart: unless-stopped
    command: ["redis-server", "--maxmemory-policy", "noeviction", "--appendonly", "yes", "--appendfsync", "everysec"]
    volumes: ["/srv/observatory/redis-data:/data"]
    networks: [observatory-net]
    <<: *logging

  celery-worker:
    profiles: [jobs]
    image: registry.digitalocean.com/observatory/observatory-api:${API_TAG}
    restart: unless-stopped
    env_file: /srv/observatory/env/api.env
    environment: { SENTRY_RELEASE: "${API_TAG}" }
    command: celery -A app.workers.celery_app worker --loglevel=info --concurrency=2 -Q default
    depends_on: [redis-broker]
    networks: [observatory-net]
    <<: *logging

  celery-beat:
    profiles: [jobs]
    image: registry.digitalocean.com/observatory/observatory-api:${API_TAG}
    restart: unless-stopped
    env_file: /srv/observatory/env/api.env
    command: celery -A app.workers.celery_app beat --loglevel=info
    depends_on: [redis-broker]
    networks: [observatory-net]
    <<: *logging

networks:
  observatory-net:
    external: true
```

No `:latest`. `WEB_TAG` and `API_TAG` live in `/srv/observatory/compose/.env`, written by the deploy step and committed to nothing — the registry is the history. Redis and the broker are not published on any host port (Revy published `127.0.0.1:6379`; not needed here).

Profiles are enabled per invocation (`docker compose --profile identity up -d`) or persistently via `COMPOSE_PROFILES=identity` in `.env`. Use the `.env` form once a profile is on for good, so a plain `docker compose up -d` during a deploy does not silently stop it.

---

## `api.env` (0640 `deploy:deploy`) — shape

```text
ENVIRONMENT=production
LOG_LEVEL=INFO
LOG_FORMAT=json
SECRET_KEY=<python -c "import secrets; print(secrets.token_urlsafe(48))">
ALLOWED_ORIGINS=https://observatory.createit.digital
APP_PUBLIC_URL=https://observatory.createit.digital

DATABASE_URL=postgresql+asyncpg://observatory_app:***@private-<cluster>...:25060/observatory?ssl=require

REDIS_URL=redis://redis:6379/0
# CELERY_BROKER_URL=redis://redis-broker:6379/0        # only when profile jobs is enabled
# CELERY_RESULT_BACKEND=redis://redis-broker:6379/1

# Identity — unset until profile identity is enabled (P8). API must start and serve public routes without these.
# KEYCLOAK_URL=http://keycloak:8080
# KEYCLOAK_REALM=createit
# KEYCLOAK_ISSUER=https://auth.createit.digital/realms/createit
# KEYCLOAK_CLIENT_ID=observatory-api
# KEYCLOAK_CLIENT_SECRET=***
# KEYCLOAK_FRONTEND_CLIENT_ID=observatory-web

SENTRY_DSN=
SENTRY_SEND_DEFAULT_PII=false
SENTRY_TRACES_SAMPLE_RATE_PROD=0.1
```

Runtime secrets live **only** on the Droplet. The `web` image has no env file: its `VITE_*` values are baked at build.

---

## Deploy procedure

Order is Revy's, proven: pull → migrate from the new API image → swap → verify. `web` and `api` may ship independently or together; the procedure is the same.

```bash
# on the Droplet as deploy
cd /srv/observatory/compose
export DOCKER_AUTH_CONFIG=...                         # read-only DOCR token, see container-registry.md

WEB=0.1.0          # release version tag of observatory-web (or a sha)
API=<sha>          # tag of observatory-api

docker pull registry.digitalocean.com/observatory/observatory-web:$WEB
docker pull registry.digitalocean.com/observatory/observatory-api:$API

# 1. migrate with the direct DB URL, from the NEW api image, before it serves traffic
docker run --rm --network observatory-net --env-file /srv/observatory/env/api.env \
  -e DATABASE_URL="$ALEMBIC_DATABASE_URL" \
  registry.digitalocean.com/observatory/observatory-api:$API alembic upgrade head

# 2. record and swap (Compose recreates only services whose image changed)
printf 'WEB_TAG=%s\nAPI_TAG=%s\n' "$WEB" "$API" > .env
docker compose up -d                                  # add --profile jobs only when jobs are enabled

# 3. verify
curl -sf http://127.0.0.1:8081/healthz
curl -sf http://127.0.0.1:8081/release.json | jq -e --arg v "$WEB" '.version == $v'
curl -sf http://127.0.0.1:8000/api/v1/health
curl -sf https://observatory.createit.digital/api/v1/version | grep "$API"
curl -sf "https://observatory.createit.digital/play/?smoke=1" >/dev/null    # smoke mode beacons to /api/v1/telemetry
```

Host Nginx does not need a reload for a `web` or `api` deploy — upstream ports are stable.

**Rollback (either service):** edit the tag in `.env`, `docker compose up -d`. Keep the previous image pulled (`docker image ls` shows it; do not prune below two per service). Migrations are forward-only; a rollback that needs a schema revert is a hand-written down-migration decision, not a script.

---

## Promotion staging → production

The Unity `play/` payload is byte-identical between the staging and production `web` images (only baked `VITE_*` URLs differ). Promotion means: staging ran `observatory-web:<sha>-staging` and passed smoke + manual play → production deploys `observatory-web:<version>` built from the same `<sha>`. Verify `release.json.artifact_checksum` matches on both.

---

## Staging (P7, later)

Same Compose file, same procedure, different `api.env`, Nginx `server_name`, and `WEB_TAG=<sha>-staging`. Until the staging Droplet exists, **production itself is gated** by host Nginx basic auth on `/`; P7 moves the gate to staging.

---

## Later: CI

When this repo has a git remote, Revy's `deploy.yml` shape lifts directly: `validate` job (lint, type, tests, Unity budget check) → `deploy` job (build/push `web` + `api`, `appleboy/ssh-action` as `deploy` user, run the procedure above). Keep runtime secrets off CI; CI holds only `DOCR_TOKEN` (rw), `DROPLET_IP`, `SSH_PRIVATE_KEY`, `VITE_*`, and Unity activation.

---

## Verification

```bash
docker compose ps                                    # web, api, redis up; no identity or jobs services
docker compose config | grep -c ':latest'            # 0
ss -lntp | grep -E ':(8000|8081)\b'                  # 127.0.0.1 only; 8080/9000 appear only with identity on
cat .env                                             # WEB_TAG / API_TAG match what release notes say
```

Runbooks to write when this ships: `docs/runbooks/deploy.md`, `docs/runbooks/rollback.md`, `docs/runbooks/web-release.md`.
