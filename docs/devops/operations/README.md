# docs/devops/operations/README.md

# Operations — distilled from Revy, adapted for Observatory

Source of truth for how each hosting component is set up **here**. Distilled from the working Revy deployment (`~/projects/revy`, `bf39ce5`) and rewritten for the Observatory topology in [game-platform-base-plan_v2.1.md](../../../game-platform-base-plan_v2.1.md).

Every file marks **verified in Revy** (running today) vs **new for Observatory** (Unity Web delivery, `web` image, Compose profiles, operator-only realm). Do not copy Revy hostnames, container names, or the `revy` realm.

**Rule of the program:** everything deployable is a SHA/version-tagged image in the registry — `web`, `api`, and (built on-box, profile `identity`) `keycloak`. Host Nginx is edge-only and serves no application files. One artifact type, one rollback verb.

**Scale-down (2026-09-09, Q3/Q16/Q17):** one Droplet first — production-named, gated by basic auth, 2 GB. Compose runs `web`, `api`, `redis`; profiles `identity` (Keycloak) and `jobs` (Celery) are defined and off. Staging Droplet = P7; Keycloak + `/admin/` = P8. Every spec below states what is installed now and what waits.

| Operation | File | Revy source | Delta for Observatory |
|:---|:---|:---|:---|
| Droplet, deploy user, SSH, UFW, Docker | [droplet-host.md](./droplet-host.md) | `docs/utils/deploy-user-migration.md`, Certbot doc §11–13 | One production Droplet now (2 GB), staging in P7; `/srv/observatory` holds env + Compose + KC build context only |
| DNS + TLS (Certbot DNS-01) | [dns-certbot.md](./dns-certbot.md) | `docs/utils/CERTBOT_DIGITALOCEAN_DNS_RENEWAL.md` | Names `observatory.` + `auth.createit.digital`; same DO zone |
| Host Nginx (edge) | [nginx.md](./nginx.md) | `deploy/nginx/*.conf`, `nginx-http.snippet` | Proxies `/` → `web`, `/api/` → `api`; security headers, rate limits, **basic-auth gate on production until P7**; `auth.` vhost written, enabled in P8 |
| `web` image | [web-image.md](./web-image.md) | `frontend/Dockerfile`, `deploy.yml` Vite build | `nginx:alpine` instead of Node `serve`; carries the Unity Web build; owns Brotli/wasm/cache rules |
| Managed PostgreSQL | [managed-postgres.md](./managed-postgres.md) | `docs/utils/DATABASE_CONNECTION_GUIDE.md`, `deploy/sql/postgres-extensions.sql` | No pgvector; separate Keycloak DB/user |
| Container registry | [container-registry.md](./container-registry.md) | `.github/workflows/deploy.yml`, `github-actions.secrets.example` | Two images; SHA + semver tags; `-staging` web tags; prune script |
| Keycloak + auth model | [keycloak.md](./keycloak.md) | `deploy/keycloak/config/*`, `backend/app/core/auth.py`, `jwks.py`, `frontend/src/lib/keycloak.ts`, `AuthContext.tsx`, `KEYCLOAK_DEV_CHECKLIST.md` | **Postponed to P8** (profile `identity`). Realm `createit`; clients `observatory-web` / `observatory-api`; `operator` role; no webhook provider, no workspaces |
| Compose deploy | [compose-deploy.md](./compose-deploy.md) | `deploy.yml` deploy job, `deploy/keycloak/config/docker-compose.yml`, `deploy/env-examples/*` | Compose instead of `docker run`; `web` + `api` via `WEB_TAG` / `API_TAG`; profiles `identity` + `jobs` off |

## What Revy proves

- DO Droplet + host Nginx + Certbot DNS-01 (port 80 closed) + Docker containers on loopback ports works in production.
- Host Nginx proxying `/` to a static-site container and `/api/` to the API container.
- Keycloak 26 `start --optimized` custom image at ~1 GB behind a dedicated `auth.` vhost, with FastAPI validating RS256 JWTs against JWKS, issuer split (internal URL vs public issuer), `azp`/`aud` allowlist.
- React + `keycloak-js`, `check-sso`, PKCE S256, `silent-check-sso.html`.
- DOCR login as `doctoken`; images tagged by git SHA; migrations run on the Droplet from the deployed image.

## What Revy does not have (new here)

- A production-grade static container: Revy's is Node `serve` with no cache headers; Observatory's is pinned `nginx:alpine`.
- Unity Web in the image: Brotli `.br` content types, `application/wasm`, immutable cache on hashed `Build/` files, `release.json`.
- Compose with a `jobs` profile that is off.
- Staging as a separate Droplet.

## Order of operations

Now: `droplet-host` → `dns-certbot` → `nginx` (stub 404 vhost first, then gated) → `managed-postgres` → `container-registry` → `web-image` → `compose-deploy`. Later: staging (P7, all files again with staging names) → `keycloak` (P8). Matches [DEVOPS_GENERAL_PLAN.md](../DEVOPS_GENERAL_PLAN.md).
