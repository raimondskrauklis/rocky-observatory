# docs/devops/operations/droplet-host.md

# Droplet host — users, SSH, firewall, Docker

**Source (verified in Revy):** `docs/utils/deploy-user-migration.md`, `docs/utils/CERTBOT_DIGITALOCEAN_DNS_RENEWAL.md` §11–13, `deploy.yml` (Docker network, loopback ports).

**Adapted:** **one Droplet first** — production-named, owns `observatory.createit.digital`, gated by Nginx basic auth until launch (Q3). Staging is a second Droplet added in P7 with this same file. Env/config root `/srv/observatory`. No application files on the host — the site and game ship as the `web` image.

---

## Droplets

| Env | When | Initial size | Notes |
|:---|:---|:---|:---|
| production | **now** (P1) | 2 GB / 1 vCPU, Ubuntu LTS (Q17) | api + redis + web (~10 MB) + host Nginx. Resize to 4 GB / 2 vCPU when profile `identity` is enabled (Keycloak ~1 GB). Resize is a reboot, not a rebuild. |
| staging | P7, before first public release | 2 GB / 1 vCPU | Same layout; separate DB, secrets; `staging.*` names (Q10) |

Configure the first box as `production` in every file. It is production with a gate, not staging — the public name never moves off it.

Enable **weekly Droplet backups**. Take a snapshot before risky host changes. Attach to the DO **VPC** in the same region as Managed PostgreSQL. Record final size and monthly cost in `docs/adr/`.

**Two firewall layers exist.** DigitalOcean Cloud Firewall (control panel) and UFW on the host. Both must allow `443`. Keep them in sync.

---

## Users and SSH

Root login over SSH is **disabled** (`PermitRootLogin no`). Revy learned this the hard way: CI as `root` failed with `no supported methods remain`. Use a dedicated non-root `deploy` user for automation; use your own key-only user for interactive admin.

```bash
adduser --disabled-password --gecos "" deploy
usermod -aG docker deploy
install -d -m 700 -o deploy -g deploy /home/deploy/.ssh
install -m 600 -o deploy -g deploy /dev/null /home/deploy/.ssh/authorized_keys
```

Key generation happens **as `deploy`**, ed25519, no passphrase; the public half goes into `authorized_keys`, the private half into the deploy secret store (CI secret or operator machine), then the private file is **deleted from the Droplet**.

```bash
su - deploy
ssh-keygen -t ed25519 -f ~/.ssh/observatory_deploy -N "" -C "observatory-deploy"
cat ~/.ssh/observatory_deploy.pub >> ~/.ssh/authorized_keys
# copy ~/.ssh/observatory_deploy out, then:
shred -u ~/.ssh/observatory_deploy
```

Verify from outside before wiring any automation: `ssh -i <key> deploy@<ip> docker ps`. Group membership takes effect only on a fresh login.

`/etc/ssh/sshd_config` baseline: `PasswordAuthentication no`, `PermitRootLogin no`, `PubkeyAuthentication yes`.

---

## UFW

Final public surface is **22 (restricted) + 443**. Port 80 is not needed because TLS renewal uses DNS-01 (see [dns-certbot.md](./dns-certbot.md)).

```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow from <ADMIN_IP>/32 to any port 22 proto tcp
ufw allow 443/tcp
ufw enable
ufw status numbered
```

Do **not** open 8000, 8080, 9000, 6379. Containers publish only to `127.0.0.1` (below), so UFW never sees them, but keep the rule anyway.

Mirror the same in the DO Cloud Firewall: inbound TCP 443 from anywhere, TCP 22 from admin IPs only. Remove TCP 80 once Certbot DNS-01 dry-run passes.

---

## Docker

```bash
apt-get install -y docker.io docker-compose-plugin
systemctl enable --now docker
docker network create observatory-net
```

Rules carried from Revy:

- Every container that Nginx proxies publishes on **loopback only**: `-p 127.0.0.1:8000:8000`. Never `0.0.0.0`.
- Redis and Keycloak health ports are reachable only inside `observatory-net` / loopback.
- `restart: unless-stopped` on all long-running containers.
- Log rotation on every service (`json-file`, `max-size: 10m`, `max-file: 3`) — Revy did not set this; Observatory does.

---

## Filesystem layout (per Droplet)

```text
/srv/observatory/
├── env/
│   ├── api.env             # 0640 deploy:deploy — FastAPI, Redis, Keycloak validation vars
│   └── keycloak.env        # 0600 — KC_* runtime vars
├── compose/
│   ├── docker-compose.yml  # copied from repo infrastructure/compose/
│   └── .env                # WEB_TAG / API_TAG of the running release (written by deploy)
├── keycloak/
│   ├── Dockerfile          # KC 26 optimized image
│   └── realm-export.json   # realm as code, imported at startup
└── redis-data/             # owned by uid 999 (redis container user); used only by profile jobs
```

Ownership:

```bash
install -d -o deploy -g deploy /srv/observatory/{env,compose,keycloak}
install -d -o 999 -g 999 -m 750 /srv/observatory/redis-data
```

`deploy` cannot `chown` to another uid later (root-only), so set container-owned directories **once, as root, now** — Revy's Redis data dir bug.

There is no release directory on the host. Releases are images in the registry; the host holds only env files, the Compose file, and the Keycloak build context. Rebuilding a Droplet = restore these files + pull tags.

---

## Host-level extras

- DO monitoring agent: `curl -sSL https://repos.insights.digitalocean.com/install.sh | sudo bash` (verify script source before running).
- Unattended security upgrades on; reboot window documented.
- `certbot`, `python3-certbot-dns-digitalocean` via APT (not Snap) — see [dns-certbot.md](./dns-certbot.md).

---

## Verification

```bash
ssh deploy@<ip> 'id; docker ps; ufw status'          # from admin IP
ss -lntp | grep -E ':(80|443|8000|8081|8080|6379)\b' # only 443 public; others 127.0.0.1
docker network ls | grep observatory-net
```

Runbook to write when this ships: `docs/runbooks/host-access.md` (add/remove admin IP, rotate deploy key, rebuild from snapshot).
