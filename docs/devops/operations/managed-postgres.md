# docs/devops/operations/managed-postgres.md

# DigitalOcean Managed PostgreSQL

**Source (verified in Revy):** `docs/utils/DATABASE_CONNECTION_GUIDE.md`, `deploy/sql/postgres-extensions.sql`, `deploy/keycloak/config/.env.example` (Keycloak on a separate DB/user in the same cluster).

**Adapted:** no `vector`; Keycloak gets its own database + user; separate cluster (or at minimum separate databases and users) per environment.

---

## Clusters and databases

| Env | When | Cluster | Databases | Users |
|:---|:---|:---|:---|:---|
| production | **now** (P5) | `observatory-prod` (PG 17, same region/VPC as Droplet) | `observatory`; `keycloak` added in P8 | `observatory_app`; `keycloak_app` added in P8 |
| staging | P7 | `observatory-staging` | same | same names, different passwords |

One cluster per environment is the clean split the game plan requires (no shared credentials). If cost forces one cluster, still use separate databases **and** users per environment — never one user across envs. The `keycloak` database is created only when profile `identity` is enabled (Q16).

**Trusted sources:** the Droplet (by VPC / private IP) and admin IPs. No `0.0.0.0/0`.

---

## Pooled vs direct (Revy rule)

| Mode | Use |
|:---|:---|
| Connection pool (port `25060`) | FastAPI runtime `DATABASE_URL` |
| Direct / session (DO console "Connection parameters") | **Alembic migrations**, extensions, DDL |

Migrations through the pooler can *look* successful while nothing persists. Always migrate with the direct URL. Keycloak also uses the **direct** connection (it manages its own schema).

Use the **private (VPC) host** from the Droplet; the public host only from admin machines.

---

## Extensions (once per database, as `doadmin`)

```sql
-- observatory database
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pg_trgm;   -- only if search needs it
-- keycloak database: none required
```

No `vector` here (that was Revy's embeddings).

---

## App user grants (PG 15+/DO: `public` owned by `pg_database_owner`)

```sql
GRANT CONNECT ON DATABASE observatory TO observatory_app;
GRANT USAGE, CREATE ON SCHEMA public TO observatory_app;
GRANT ALL PRIVILEGES ON ALL TABLES    IN SCHEMA public TO observatory_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO observatory_app;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO observatory_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES    TO observatory_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO observatory_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO observatory_app;
SELECT has_schema_privilege('observatory_app', 'public', 'CREATE');  -- must be true
```

Repeat for `keycloak_app` on `keycloak`. `ALTER SCHEMA public OWNER` often fails on DO — not needed when `CREATE` is granted.

---

## Connection strings

```text
# api.env (runtime, pooled)
DATABASE_URL=postgresql+asyncpg://observatory_app:***@private-<cluster>.db.ondigitalocean.com:25060/observatory?ssl=require

# migrations (direct) — pass at run time, not stored in api.env
ALEMBIC_DATABASE_URL=postgresql+asyncpg://observatory_app:***@private-<cluster>.db.ondigitalocean.com:25060/observatory?ssl=require   # direct host/port from console

# keycloak.env (P8)
KC_DB=postgres
KC_DB_URL=jdbc:postgresql://private-<cluster>.db.ondigitalocean.com:25060/keycloak?sslmode=require
KC_DB_USERNAME=keycloak_app
KC_DB_PASSWORD=***
```

asyncpg quirk from Revy: with `?ssl=require` in the URL, ad-hoc scripts must strip it and pass an SSL context; the app's SQLAlchemy URL is fine as-is.

---

## Migrations

Hand-written Alembic revisions only (no `--autogenerate`), run **from the deployed API image on the Droplet**, never from a laptop against production:

```bash
docker compose -f /srv/observatory/compose/docker-compose.yml run --rm \
  -e DATABASE_URL="$ALEMBIC_DATABASE_URL" api alembic upgrade head
```

Migration is the only LOOP pause point (AGENTS.md).

---

## Backups

DO automated daily backups + PITR are on by default; confirm retention in the console. Add the independent `pg_dump` to object storage when [compose-deploy.md](./compose-deploy.md) `jobs` profile gains its first task, or as a host cron until then.

Runbook to write when this ships: `docs/runbooks/restore.md` (PITR restore to new cluster, repoint `DATABASE_URL`, verify `alembic current`).
