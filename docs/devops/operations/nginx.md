# docs/devops/operations/nginx.md

# Host Nginx — edge only

**Source (verified in Revy):** `deploy/nginx/revy.createit.digital.conf`, `auth.revy.createit.digital.conf`, `nginx-http.snippet`, `deploy/nginx/README.md`. Revy's shape — host Nginx proxies `/` to a container on loopback and `/api/` to the API container — is kept as-is.

**Adapted:** host Nginx serves **no application files**. `/` proxies to the `web` container ([web-image.md](./web-image.md)) which owns Unity MIME/encoding/cache rules; `/api/` proxies to `api`; `auth.` vhost proxies Keycloak with an IP-restricted `/admin`. Added over Revy: security-headers snippet, feedback rate-limit zone, staging basic auth.

---

## Files

| Repo file | Install path |
|:---|:---|
| `infrastructure/nginx/observatory.createit.digital.conf` | `/etc/nginx/sites-available/observatory.createit.digital` |
| `infrastructure/nginx/auth.createit.digital.conf` | `/etc/nginx/sites-available/auth.createit.digital` |
| `infrastructure/nginx/conf.d/observatory-http.conf` | `/etc/nginx/conf.d/observatory-http.conf` (http context: rate-limit zones, upgrade map) |
| `infrastructure/nginx/snippets/security-headers.conf` | `/etc/nginx/snippets/security-headers.conf` |
| `infrastructure/nginx/snippets/proxy-headers.conf` | `/etc/nginx/snippets/proxy-headers.conf` |

**Now (P3):** install the `observatory.` vhost with the **basic-auth gate on** — production is gated until launch (Q3). **P7:** remove the gate here, install the same files on staging with staging names and the gate on. **P8:** enable the `auth.` vhost (written now, not enabled until profile `identity` runs — otherwise it proxies to nothing and returns 502).

```bash
ln -sf /etc/nginx/sites-available/observatory.createit.digital /etc/nginx/sites-enabled/
# P8 only: ln -sf /etc/nginx/sites-available/auth.createit.digital /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
htpasswd -c /etc/nginx/.htpasswd <operator>        # apache2-utils; one entry per developer
nginx -t && systemctl reload nginx
```

---

## `conf.d/observatory-http.conf` (once, http context)

```nginx
# Rate-limit zones (from Revy)
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=30r/s;
limit_req_zone $binary_remote_addr zone=feedback_limit:10m rate=2r/m;

# Upstream keepalive: send "Connection: upgrade" only for real WebSocket upgrades,
# otherwise send no Connection header so HTTP/1.1 keepalive to the containers works.
# (Revy hard-codes "upgrade", which silently disables upstream keepalive.)
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      '';
}
```

---

## `snippets/security-headers.conf`

```nginx
add_header Strict-Transport-Security "max-age=63072000; includeSubdomains; preload" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
# COOP/COEP intentionally absent — Unity threading is off (plan v2.1 ADR).
```

Included once at `server` level. Because no proxy `location` below sets its own `add_header`, these are inherited by every response, including everything the `web` container returns. (Nginx drops parent `add_header`s in any location that adds its own — that is why cache headers live in the container and security headers live here, never both in one place.)

## `snippets/proxy-headers.conf` (from Revy, keepalive-corrected)

```nginx
proxy_set_header Host              $host;
proxy_set_header X-Real-IP         $remote_addr;
proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Forwarded-Host  $host;
proxy_set_header X-Forwarded-Port  $server_port;
proxy_http_version 1.1;
proxy_set_header Upgrade           $http_upgrade;
proxy_set_header Connection        $connection_upgrade;   # see map in conf.d/observatory-http.conf
```

---

## `observatory.createit.digital.conf`

```nginx
upstream observatory_web { server 127.0.0.1:8081; keepalive 16; }
upstream observatory_api { server 127.0.0.1:8000; keepalive 16; }

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name observatory.createit.digital;

    ssl_certificate     /etc/letsencrypt/live/observatory.createit.digital/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/observatory.createit.digital/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    include snippets/security-headers.conf;

    access_log /var/log/nginx/observatory.access.log;
    error_log  /var/log/nginx/observatory.error.log;

    client_max_body_size 2m;          # feedback payloads only; Revy's 320m is not needed here

    # Do not touch what the web container already encoded (Brotli .br) or cached.
    gzip off;
    proxy_buffering on;
    proxy_max_temp_file_size 0;       # stream large .wasm/.data instead of spooling to disk

    # Pre-launch gate (Q3). ON in production until P7 moves it to staging. Remove by editing, not by forgetting.
    auth_basic "observatory";
    auth_basic_user_file /etc/nginx/.htpasswd;

    # Feedback: tight rate limit, then API
    location = /api/v1/feedback {
        limit_req zone=feedback_limit burst=5 nodelay;
        limit_req_status 429;
        proxy_pass http://observatory_api;
        include snippets/proxy-headers.conf;
    }

    # Telemetry beacon must bypass the basic-auth gate (smoke mode posts here)
    location = /api/v1/telemetry {
        auth_basic off;
        limit_req zone=api_limit burst=60 nodelay;
        proxy_pass http://observatory_api;
        include snippets/proxy-headers.conf;
    }

    location /api/ {
        limit_req zone=api_limit burst=60 nodelay;
        limit_req_status 429;
        limit_req_log_level warn;
        proxy_pass http://observatory_api;
        include snippets/proxy-headers.conf;
        proxy_read_timeout 60s;
        proxy_send_timeout 60s;
    }

    # Everything else — landing, /privacy/, /feedback/, /admin/, /play/, release.json — is the web image
    location / {
        proxy_pass http://observatory_web;
        include snippets/proxy-headers.conf;
        proxy_read_timeout 60s;
    }
}
```

Host Nginx `gzip off` here is deliberate: the `web` container compresses text on the fly and serves Unity `.br` pre-encoded; the edge must pass `Content-Encoding` through untouched. Revy's `location = /silent-check-sso.html` inline HTML is gone — the file ships inside the `web` image (`apps/web/public/`).

---

## Does the proxy hop slow the game?

No, and this section exists so nobody re-opens the question without numbers.

- **In-game latency** is browser-local. After load, the Unity WebAssembly does not talk to the server (offline play is a product contract; the telemetry beacon is fire-and-forget). Topology cannot affect frame time or input latency.
- **Load time** is dominated by transferring 30–80 MB to the player: TLS handshake (~50–100 ms), player↔Droplet RTT (20–100 ms by geography — identical in every topology without a CDN), and downlink throughput (seconds). The loopback hop host Nginx → `web` container costs ~0.05–0.1 ms per request; a Unity load is 6–10 requests, so **under 1 ms in total**, on a process measured in seconds.
- Throughput is bounded by the player's link and the Droplet NIC, not by two event-driven Nginx processes on one host. Revy's SPA and every Kubernetes ingress→pod setup run through this exact hop.

What keeps it that way (all in this file or [web-image.md](./web-image.md)): `gzip off` on the proxied vhost (no double encoding), `proxy_max_temp_file_size 0` (no spooling large `.wasm` to disk), `sendfile on` inside the image, `keepalive 16` upstreams with an empty `Connection` header for non-WebSocket requests (otherwise every request opens a new TCP connection to the container), HTTP/2 to the client at the edge.

What actually decides perceived load time is upstream of hosting and already in plan v2.1: the Web Build Budgets, Brotli, immutable caching on hashed files (second load ≈ instant), and the accepted no-CDN risk.

---

## `auth.createit.digital.conf` (from Revy, renamed) — written now, enabled in P8

Do not symlink into `sites-enabled` until `docker compose --profile identity up -d` has Keycloak answering on `127.0.0.1:8080`; an enabled vhost with no upstream returns 502 on a public hostname.

```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name auth.createit.digital;

    ssl_certificate     /etc/letsencrypt/live/observatory.createit.digital/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/observatory.createit.digital/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    client_max_body_size 20m;

    # Keycloak health/metrics live on 9000 inside the network; never proxy them
    location ~ ^/(health|metrics)(/|$) { return 404; }

    # Admin console: operator IPs only (new — Revy exposes it publicly)
    location ~ ^/admin(/|$) {
        allow <ADMIN_IP>/32;
        deny all;
        proxy_pass http://127.0.0.1:8080;
        include snippets/proxy-headers.conf;
        proxy_read_timeout 3600s;
    }

    location / {
        proxy_pass http://127.0.0.1:8080;
        include snippets/proxy-headers.conf;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }
}
```

Keycloak sets its own `X-Frame-Options`/CSP for its pages; do not include `security-headers.conf` on this vhost, it would double-emit and can break the account console.

---

## Verification

```bash
nginx -t
curl -sI https://observatory.createit.digital/ -o /dev/null -w '%{http_code}\n'                             # 401 while gated
curl -sI -u <operator>:<pw> https://observatory.createit.digital/ | grep -iE 'strict-transport|x-frame|cache-control'   # headers from both layers present
curl -s -o /dev/null -w '%{http_code}\n' -X POST https://observatory.createit.digital/api/v1/telemetry -d '{}'         # not 401 — gate exempt
curl -sI https://observatory.createit.digital/play/index.html | grep -i cache-control                          # no-cache
curl -sI https://observatory.createit.digital/play/Build/<hash>.wasm.br | grep -iE 'content-(type|encoding)|cache'   # wasm, br, immutable — proves pass-through
curl -s  https://observatory.createit.digital/release.json | jq .version
# P8 only:
curl -s  https://auth.createit.digital/realms/createit/.well-known/openid-configuration | head -c 200
curl -sI https://auth.createit.digital/admin/ -o /dev/null -w '%{http_code}\n'                              # 403 from a non-admin IP
for i in $(seq 1 10); do curl -s -o /dev/null -w '%{http_code}\n' -X POST https://observatory.createit.digital/api/v1/feedback; done   # 429 after burst
```

Runbook to write when this ships: `docs/runbooks/nginx.md` (edit a vhost, validate, reload, add/remove admin IP, toggle staging basic auth).
