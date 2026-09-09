# .revy/rules/platform.md

# Platform (shared)

Check the **whole file** for each path in the diff (unchanged lines count). Comment on violations. Soft line-count / taste is out of scope.

- Priority when goals conflict: capacity, then foundation, then game.
- Offline play is a product contract. Do not make the game require the API to start unless the change is explicitly that contract.
- Do not enable player login, Compose profile `identity` (Keycloak), profile `jobs` (Celery/Beat), or multi-tenant abstractions without a named feature.
- No secrets, credentials, or `.env` values in diffs. None in the Unity client.
- Do not trust client-submitted competitive, financial, or entitlement state.
- Do not change identity, production networking, secrets, deployment, or database schema without an explicit review point in the PR.
- Host Nginx is edge-only. Application files ship in `web` / `api` images. Do not add a second release mechanism (host files under `/srv`).
- Do not overwrite a working Unity scene, asset, or deployment configuration without a Git commit or explicit review point.
