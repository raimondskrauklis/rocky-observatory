# .revy/rules/backend.md

# Backend (`apps/api`)

FastAPI under `apps/api`. Follow runners this repo actually has — do not invent Pipenv, kp-platform paths, or `backend/` at repo root.

- No secrets in source, logs, or test fixtures.
- Do not trust client-submitted competitive, financial, or entitlement state. Authoritative writes stay on the server.
- Identity (Keycloak / JWKS) stays off until profile `identity` is a named feature. Do not add player login or webhook providers in passing.
- Database schema changes need an explicit review point. No production Postgres in Compose.
- Errors must not be swallowed or reported as success. Do not invent data to make a response look complete.
- Tests and lint: only commands in `.agent/manifest.json` `test_commands` (empty until this app documents a runner).
