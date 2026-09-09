# docs/devops/operations/keycloak.md

# Keycloak and the auth model

> **Status: postponed (Q16, 2026-09-09) — spec complete, not installed.** Keycloak is Compose profile `identity`, defined and off. No relying party exists until `/admin/` with operator login is built (general plan P8). Until then: no `keycloak` database, no `keycloak.env`, no `auth.` vhost installed, no realm import. The `auth.createit.digital` DNS record and cert SAN exist now (free), so enabling is Compose + vhost + DB, not DNS/TLS work. Two people developing in parallel need none of this: Unity is offline by contract and the pre-launch gate is basic auth.

**Source (verified in Revy):** `deploy/keycloak/config/{Dockerfile,docker-compose.yml,.env.example,README.md}`, `deploy/nginx/auth.*.conf`, `backend/app/core/{auth.py,jwks.py,config.py}`, `frontend/src/lib/keycloak.ts`, `frontend/src/contexts/AuthContext.tsx`, `docs/starter-pack/KEYCLOAK_DEV_CHECKLIST.md`.

**Adapted:** realm `createit`; clients `observatory-web` + `observatory-api`; realm role `operator`; operator login only — no player accounts (plan v2.1). Dropped from Revy: webhook event provider, Google IdP, workspaces/tenancy, impersonation, JIT user provisioning table.

---

## Placement and image

Keycloak 26 runs as a Compose service on the application Droplet, behind the `auth.createit.digital` vhost ([nginx.md](./nginx.md)). Custom image with `kc.sh build` baked in so restarts are fast (`start --optimized`).

`infrastructure/keycloak/Dockerfile`:

```dockerfile
FROM quay.io/keycloak/keycloak:26.0
ENV KC_DB=postgres
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true
RUN /opt/keycloak/bin/kc.sh build
ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
```

Build-time vars (`KC_DB`, health, metrics) live in the Dockerfile; **changing them requires `docker compose build --no-cache`**. Runtime vars live in `keycloak.env`.

Compose fragment (see [compose-deploy.md](./compose-deploy.md) for the full file) — under `profiles: [identity]`:

```yaml
keycloak:
  profiles: [identity]
  build: /srv/observatory/keycloak
  image: observatory-keycloak:26.0
  command: start --optimized --import-realm
  env_file: /srv/observatory/env/keycloak.env
  volumes:
    - /srv/observatory/keycloak/realm-export.json:/opt/keycloak/data/import/createit-realm.json:ro
  ports:
    - "127.0.0.1:8080:8080"
    - "127.0.0.1:9000:9000"     # health/metrics — never proxied
  mem_limit: 1g                  # Revy runs at 1g; raise to 2g if OOM-killed
  networks: { observatory-net: { aliases: [keycloak] } }
```

`keycloak.env` (0600):

```text
KC_BOOTSTRAP_ADMIN_USERNAME=admin
KC_BOOTSTRAP_ADMIN_PASSWORD=***            # first boot only; then create a named admin and remove
KC_DB_URL=jdbc:postgresql://private-<cluster>.db.ondigitalocean.com:25060/keycloak?sslmode=require
KC_DB_USERNAME=keycloak_app
KC_DB_PASSWORD=***
KC_HOSTNAME=https://auth.createit.digital
KC_HOSTNAME_STRICT=true
KC_HTTP_ENABLED=true
KC_PROXY_HEADERS=xforwarded
KC_PROXY_TRUSTED_ADDRESSES=127.0.0.1
KC_LOG_LEVEL=INFO
```

Health: `curl -sf http://127.0.0.1:9000/health/ready`. Discovery: `https://auth.createit.digital/realms/createit/.well-known/openid-configuration`.

---

## Realm as code (new — Revy configures by hand)

`infrastructure/keycloak/realm-export.json` is the source. `--import-realm` loads it on first start of an empty realm. After any console change: **export and commit**, otherwise staging and production drift.

```bash
docker compose exec keycloak /opt/keycloak/bin/kc.sh export --realm createit --file /tmp/createit.json --users skip
docker compose cp keycloak:/tmp/createit.json infrastructure/keycloak/realm-export.json
```

Secrets are **not** in the export (client secret for `observatory-api` is set per environment; the export keeps a placeholder). Staging and production exports differ only in redirect URIs / web origins.

---

## Realm `createit`

| Setting | Value |
|:---|:---|
| Login with email | On |
| Email as username | On |
| Verify email | On |
| User registration | **Off** at launch (operator accounts are created in the console) |
| Realm roles | `operator` |

### Client `observatory-web` (public SPA)

| Setting | Value |
|:---|:---|
| Client authentication | Off |
| Standard flow | On (Authorization Code + PKCE S256) |
| Direct access grants | Off |
| Valid redirect URIs | `https://observatory.createit.digital/*` (+ `http://localhost:5173/*` in staging export only) |
| Valid post logout redirect URIs | `+` |
| Web origins | `https://observatory.createit.digital` |

Revy pitfall: if *post logout redirect URIs* is empty, logout returns *Invalid redirect uri*, the SSO cookie survives, and `check-sso` silently signs the user back in.

### Client `observatory-api` (confidential, audience)

| Setting | Value |
|:---|:---|
| Client authentication | On |
| Standard flow / direct grants | Off |
| Purpose | Appears in `aud` of tokens issued to `observatory-web` via an **audience mapper** on the `observatory-web` client; API validates against it |

No `observatory-admin` client, no `observatory-mobile` until a mobile build exists (plan v2.1).

---

## Token validation in FastAPI (from Revy `auth.py` / `jwks.py`)

Rules that Revy enforces and Observatory keeps:

1. **RS256** only; signing key resolved by `kid` from the realm JWKS (`/realms/createit/protocol/openid-connect/certs`), cached 1 h, force-refreshed once on unknown `kid`, stale cache served if Keycloak is briefly down.
2. **Issuer split.** Inside Docker the API talks to `http://keycloak:8080`, but browser tokens carry `iss = https://auth.createit.digital/realms/createit`. Config needs both:

    ```text
    KEYCLOAK_URL=http://keycloak:8080
    KEYCLOAK_REALM=createit
    KEYCLOAK_ISSUER=https://auth.createit.digital/realms/createit
    KEYCLOAK_CLIENT_ID=observatory-api
    KEYCLOAK_FRONTEND_CLIENT_ID=observatory-web
    ```

3. **Audience allowlist** `{observatory-api, observatory-web}`: `azp` must be in it; `aud` may be absent, a string in it, or a list intersecting it. `aud: account` alone → 401 *Invalid token audience* (Revy's most common misconfiguration; fix with the audience mapper above).
4. Expired → 401; JWKS unreachable with no cache → 503 *Authentication service unavailable* (not 401).
5. Roles read from `realm_access.roles`; `require_operator()` dependency guards `/admin/` and `/api/v1/admin/*`.

What Observatory **drops** from Revy's `get_current_user`: workspace resolution, impersonation, JIT provisioning into a `users` table. Launch has no player accounts; the `operator` role is enough. Add a users table when the first player-identity feature arrives.

---

## Browser flow (from Revy `keycloak.ts` + `AuthContext.tsx`)

```ts
const kc = new Keycloak({ url: VITE_KEYCLOAK_URL, realm: 'createit', clientId: 'observatory-web' });
await kc.init({
  onLoad: 'check-sso',
  pkceMethod: 'S256',
  checkLoginIframe: false,
  silentCheckSsoRedirectUri: `${window.location.origin}/silent-check-sso.html`,
});
```

- `check-sso`, not `login-required`: the public site never forces login. Only `/admin/` routes call `kc.login()`.
- `silent-check-sso.html` lives in `apps/web/public/` and ships inside the `web` image (see [web-image.md](./web-image.md)). Revy inlines it in host Nginx; not needed when the image carries it.
- Logout uses `post_logout_redirect_uri` back to the site root.
- `VITE_KEYCLOAK_*` are **build-time**; changing them means a new `web` image. Staging and production `web` images therefore differ in these values only.

**Unity never does OAuth.** If a game feature ever needs identity, the React shell passes a short-lived access token into the Unity instance via a JS bridge; Unity sends it as `Authorization: Bearer` to `/api/v1/...` and never stores refresh tokens. This is the v2.1 correction to the v1.1 diagram.

---

## Enabling the profile (P8 checklist)

1. Managed PG: `keycloak` database + `keycloak_app` user, grants ([managed-postgres.md](./managed-postgres.md)).
2. `/srv/observatory/env/keycloak.env` (0600) as above.
3. Resize the Droplet to 4 GB / 2 vCPU (Q17).
4. Install `auth.createit.digital` vhost ([nginx.md](./nginx.md)); `nginx -t && systemctl reload nginx`.
5. `docker compose --profile identity build && docker compose --profile identity up -d`; wait for `/health/ready`.
6. Realm `createit` imports on first start; set the `observatory-api` client secret; create the first operator user; remove `KC_BOOTSTRAP_ADMIN_*`.
7. Rebuild the `web` image with `VITE_KEYCLOAK_*` set; deploy `api` with `KEYCLOAK_*` in `api.env`.
8. Verify per the section below. Then repeat on staging.

## Access gate before `identity` is on

Production `/` (which includes `/play/`) is behind host Nginx basic auth until launch (P7 removes it). Once `identity` is on, `/admin/` is Keycloak-gated regardless of the basic-auth state; the staging Droplet may keep basic auth at the edge or use the `operator` role for the whole site — decide in the P7 execution file.

---

## Verification

```bash
curl -sf http://127.0.0.1:9000/health/ready
curl -s https://auth.createit.digital/realms/createit/.well-known/openid-configuration | jq .issuer
# after operator login in the browser, decode the access token: iss ends /realms/createit, azp = observatory-web, aud includes observatory-api, realm_access.roles includes operator
curl -s -H "Authorization: Bearer $TOKEN" https://observatory.createit.digital/api/v1/admin/feedback | head -c 200
```

Runbook to write when this ships: `docs/runbooks/keycloak.md` (upgrade KC version, export/import realm, reset operator password, rotate `observatory-api` secret).
