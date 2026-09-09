# docs/devops/operations/web-image.md

# `web` image — React shell + Unity Web build

**Source (verified in Revy):** `frontend/Dockerfile` (static build baked into an image, container on loopback, host Nginx proxies `/`), `deploy.yml` (Vite build in CI with `VITE_*` baked, image tagged by SHA).

**Adapted:** Revy's image runs Node `serve` (dev static server, no cache headers). Observatory's image is **pinned `nginx:alpine`** and also carries the Unity Web build, so the file-specific rules (Unity MIME/encoding, immutable caching, SPA fallback) live **inside the image** and ship with the release. Host Nginx stays edge-only ([nginx.md](./nginx.md)).

---

## Contents of one image

```text
registry.digitalocean.com/observatory/observatory-web:<version>    e.g. 0.1.0
registry.digitalocean.com/observatory/observatory-web:<git-sha>    same digest

/usr/share/nginx/html/
├── index.html, assets/*.<hash>.{js,css}, privacy/, feedback/, admin/   ← Vite build (apps/web)
├── silent-check-sso.html                                               ← keycloak-js (apps/web/public)
├── play/
│   ├── index.html
│   ├── Build/<hash>.loader.js, <hash>.framework.js.br, <hash>.wasm.br, <hash>.data.br
│   ├── StreamingAssets/
│   └── TemplateData/
└── release.json                                                        ← game_id, version, git_sha, unity_version, budgets
```

One image = one release of the whole public surface. The React shell and the game move together; `release.json` is served at `/release.json` and its `version` is what `/api/v1/version` and the in-game version label must agree with.

**Unity Player Settings required:** Compression = Brotli, **Name Files As Hashes = on**, Decompression Fallback = off (Nginx serves `.br` natively).

---

## `infrastructure/web-image/Dockerfile`

```dockerfile
FROM nginx:1.27-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY site/     /usr/share/nginx/html/
COPY play/     /usr/share/nginx/html/play/
COPY release.json /usr/share/nginx/html/release.json
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://127.0.0.1:8080/healthz || exit 1
```

Build context is assembled by CI (or the operator script) from `apps/web/dist` → `site/`, the Unity Web output → `play/`, and the generated `release.json`. Nginx runs as the image's default `nginx` user on an unprivileged port; no root in the container.

Pin the `nginx` tag; bump it deliberately and record the change.

---

## `infrastructure/web-image/nginx.conf`

```nginx
worker_processes auto;
error_log /dev/stderr warn;
pid /tmp/nginx.pid;

events { worker_connections 1024; }

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    types { application/wasm wasm; }

    access_log /dev/stdout;
    sendfile on;
    tcp_nopush on;

    # Vite/React text assets: compress on the fly. Unity .br files are excluded by their own locations.
    gzip on;
    gzip_types text/plain text/css application/javascript application/json image/svg+xml;
    gzip_min_length 1024;
    gzip_vary on;

    server {
        listen 8080;
        server_name _;
        root /usr/share/nginx/html;
        index index.html;

        # Trust X-Forwarded-* from host Nginx only (loopback)
        set_real_ip_from 127.0.0.1;
        real_ip_header X-Forwarded-For;

        location = /healthz { access_log off; return 200 "ok\n"; }
        location = /release.json { add_header Cache-Control "no-cache"; }

        # ---- Unity Web: Brotli-precompressed, hashed, immutable ----
        location ~ ^/play/.+\.wasm\.br$ {
            gzip off;
            types {} default_type application/wasm;
            add_header Content-Encoding br;
            add_header Vary Accept-Encoding;
            add_header Cache-Control "public, max-age=31536000, immutable";
        }
        location ~ ^/play/.+\.js\.br$ {
            gzip off;
            types {} default_type application/javascript;
            add_header Content-Encoding br;
            add_header Vary Accept-Encoding;
            add_header Cache-Control "public, max-age=31536000, immutable";
        }
        location ~ ^/play/.+\.(data|symbols\.json)\.br$ {
            gzip off;
            types {} default_type application/octet-stream;
            add_header Content-Encoding br;
            add_header Vary Accept-Encoding;
            add_header Cache-Control "public, max-age=31536000, immutable";
        }
        # Uncompressed fallback if a build is ever exported without Brotli
        location ~ ^/play/.+\.wasm$ {
            add_header Cache-Control "public, max-age=31536000, immutable";
        }
        # Entry points: always revalidate
        location ~ ^/play/.+\.loader\.js$ { add_header Cache-Control "no-cache"; }
        location = /play/index.html      { add_header Cache-Control "no-cache"; }
        location /play/ {
            try_files $uri $uri/ /play/index.html;
        }

        # ---- React shell ----
        location ~* \.(js|css|woff2|png|jpg|svg|ico)$ {
            try_files $uri =404;
            add_header Cache-Control "public, max-age=31536000, immutable";   # Vite hashes filenames
        }
        location = /silent-check-sso.html { add_header Cache-Control "public, max-age=300"; }
        location / {
            try_files $uri $uri/ /index.html;
            add_header Cache-Control "no-cache";
        }
    }
}
```

Security headers (`HSTS`, `X-Frame-Options`, `nosniff`, `Referrer-Policy`) are **not** set here; host Nginx adds them at the server level for every proxied response so they cannot be lost in an inner `location`.

---

## Build (CI or operator machine)

```bash
VERSION=0.1.0; SHA=$(git rev-parse --short=12 HEAD)
CTX=$(mktemp -d)
cp infrastructure/web-image/{Dockerfile,nginx.conf} "$CTX/"
cp -R apps/web/dist            "$CTX/site"           # VITE_* baked here
cp -R build/WebGL              "$CTX/play"           # Unity output, passed Web Build Budgets
tools/unity/write_release_json.sh "$VERSION" "$SHA" > "$CTX/release.json"

IMG=registry.digitalocean.com/observatory/observatory-web
docker build -t $IMG:$SHA -t $IMG:$VERSION "$CTX"
docker push $IMG:$SHA && docker push $IMG:$VERSION
```

`VITE_API_BASE_URL` is build-time now; `VITE_KEYCLOAK_URL`, `VITE_KEYCLOAK_REALM=createit`, `VITE_KEYCLOAK_CLIENT_ID=observatory-web` join it in P8 (the React shell must render every public route with them unset). Changing any of them is a new image. Staging and production therefore build **the same image** only if those values are identical — they are not (staging URLs differ), so CI produces `observatory-web:<sha>-staging` and `observatory-web:<sha>` from the same source, and the Unity `play/` payload is byte-identical between them (verify with the checksum in `release.json`).

---

## Local check before pushing

```bash
docker run --rm -p 8081:8080 $IMG:$SHA &
curl -sI localhost:8081/play/index.html | grep -i cache-control                       # no-cache
curl -sI localhost:8081/play/Build/*.wasm.br | grep -iE 'content-(type|encoding)|cache' # wasm, br, immutable
curl -s  localhost:8081/release.json | jq .version
curl -s  localhost:8081/healthz
```

Runbook to write when this ships: `docs/runbooks/web-release.md` (build, push, promote staging → production, roll back `WEB_TAG`).
