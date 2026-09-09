# docs/devops/operations/container-registry.md

# DigitalOcean Container Registry

**Source (verified in Revy):** `.github/workflows/deploy.yml` (login, build, tag, push, pull-on-Droplet), `deploy/env-examples/github-actions.secrets.example` (`DOCR_TOKEN` derivation).

**Adapted:** two application images — `observatory-web` (React shell + Unity Web build, see [web-image.md](./web-image.md)) and `observatory-api` (FastAPI with runtime roles). Keycloak is built on the Droplet from `infrastructure/keycloak/` and is not pushed. **No `latest`-only deploys.**

---

## Registry

| Item | Value |
|:---|:---|
| Registry | `registry.digitalocean.com/observatory` (create in DO console; name is global per account) |
| Images | `observatory-web`, `observatory-api` |
| Tag policy | every push gets `<git-sha>`; a release additionally gets `<semver>` (`web`) / `<semver>` (`api`); staging `web` builds are `<git-sha>-staging` (different baked `VITE_*`); `latest` may exist for humans but is **never** referenced by Compose |

The registry is the release history. Everything deployable is here; nothing deployable is a file on the Droplet.

---

## Credentials (Revy's hard-won detail)

`DOCR_TOKEN` is the registry **password**, not the `dop_v1_` API token.

1. DO → Container Registry → Settings → *Download Docker Credentials* (read/write for CI; read-only for the Droplet).
2. In the JSON, decode `auth`: `echo '<auth>' | base64 -d` → `doctoken:<password>`.
3. Username is always `doctoken`; store only `<password>`.

```bash
echo "$DOCR_TOKEN" | docker login registry.digitalocean.com -u doctoken --password-stdin
```

Two tokens: **read-write** for whatever builds/pushes; **read-only** on each Droplet. Register both in `docs/security/SECRETS.md`.

On the Droplet, avoid persisting credentials in `~/.docker/config.json` for `deploy`; Revy passes them per-command:

```bash
DOCR_AUTH="$(printf 'doctoken:%s' "$DOCR_TOKEN_RO" | base64 -w0)"
export DOCKER_AUTH_CONFIG="{\"auths\":{\"registry.digitalocean.com\":{\"auth\":\"${DOCR_AUTH}\"}}}"
docker pull registry.digitalocean.com/observatory/observatory-api:<sha>
```

---

## Build and push (operator machine or CI)

```bash
SHA=$(git rev-parse --short=12 HEAD); REG=registry.digitalocean.com/observatory
docker build -t $REG/observatory-api:$SHA apps/api
docker push $REG/observatory-api:$SHA
# web image: context assembled from apps/web/dist + Unity output — see web-image.md
# on a tagged release:
for img in observatory-api observatory-web; do
  docker tag $REG/$img:$SHA $REG/$img:0.1.0 && docker push $REG/$img:0.1.0
done
```

Until this repo has a git remote and CI, this runs from the operator machine. When CI exists, lift Revy's `docker/login-action` + build/push steps; the `validate → deploy-production` shape is proven.

---

## Tag hygiene

Storage cost is not a concern (images elsewhere run ~1 GB; `observatory-web` is 30–80 MB). Prune for clarity, not money: keep **all semver tags** and the last 10 SHA tags per image; delete `-staging` tags older than the current staging release; run registry garbage collection monthly (DO console → Settings → *Start Garbage Collection*) so `list-tags` stays readable. `infrastructure/scripts/registry-prune.sh` implements this with `doctl registry repository delete-tag`.

---

## Verification

```bash
doctl registry repository list-tags observatory-web
doctl registry repository list-tags observatory-api
docker compose -f /srv/observatory/compose/docker-compose.yml config | grep image:   # no ':latest'
```

Runbook to write when this ships: `docs/runbooks/registry.md` (rotate tokens, GC, find the SHA running in prod).
