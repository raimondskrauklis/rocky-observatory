# docs/devops/operations/dns-certbot.md

# DNS and TLS — DigitalOcean DNS + Certbot DNS-01

**Source (verified in Revy):** `docs/utils/CERTBOT_DIGITALOCEAN_DNS_RENEWAL.md` — production cert for `revy.createit.digital` + `auth.revy.createit.digital` renews via DNS-01 with port 80 closed.

**Adapted:** names `observatory.createit.digital` and `auth.createit.digital`; staging names per Q10 (findings).

---

## Zone

`createit.digital` is hosted on **DigitalOcean DNS** (authoritative `ns1–3.digitalocean.com`, verified in Revy). Revy and Observatory share this zone. Records for Observatory:

| Name | Type | Target | When |
|:---|:---|:---|:---|
| `observatory.createit.digital` | A / AAAA | production Droplet | P2 |
| `auth.createit.digital` | A / AAAA | production Droplet | P2 — record + cert SAN now; vhost only when profile `identity` is on (P8) |
| `staging.observatory.createit.digital` *(Q10 default)* | A | staging Droplet | P7 |
| `auth.staging.observatory.createit.digital` *(Q10 default)* | A | staging Droplet | P7 |

`auth.createit.digital` is the **platform** identity host (shared across future games). `auth.revy.createit.digital` is a different Keycloak — do not merge realms. Creating the `auth.` record and SAN now costs nothing and means enabling Keycloak later is not a DNS/TLS operation.

Check: `dig +short observatory.createit.digital` before requesting certificates.

---

## Why DNS-01

HTTP-01 needs public port 80. DNS-01 creates a temporary `_acme-challenge.<name>` TXT record via the DO API, so **port 80 stays closed** in UFW and the Cloud Firewall. Wildcards become possible later.

---

## Install (APT, not Snap)

Plugins must match the Certbot install. Revy's Certbot is `/usr/bin/certbot` (APT), so:

```bash
apt-get install -y certbot python3-certbot-dns-digitalocean
certbot plugins | grep dns-digitalocean
```

---

## DO API token

Create a token scoped to **DNS only** (read + write on domains). One token per Droplet. Store:

```bash
install -d -m 700 /etc/letsencrypt/secrets
printf 'dns_digitalocean_token = %s\n' '<TOKEN>' > /etc/letsencrypt/secrets/digitalocean.ini
chown root:root /etc/letsencrypt/secrets/digitalocean.ini
chmod 600 /etc/letsencrypt/secrets/digitalocean.ini
```

Register in `docs/security/SECRETS.md`: name, scope, Droplet, rotation.

---

## Issue one SAN certificate per Droplet

Production:

```bash
certbot certonly \
  --dns-digitalocean \
  --dns-digitalocean-credentials /etc/letsencrypt/secrets/digitalocean.ini \
  --dns-digitalocean-propagation-seconds 30 \
  --cert-name observatory.createit.digital \
  -d observatory.createit.digital \
  -d auth.createit.digital
```

Staging (P7): same with `--cert-name staging.observatory.createit.digital` and the two staging names.

Result paths used by every Nginx vhost on that Droplet:

```text
/etc/letsencrypt/live/observatory.createit.digital/fullchain.pem
/etc/letsencrypt/live/observatory.createit.digital/privkey.pem
```

---

## Reload hook and timer

```bash
tee /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh >/dev/null <<'EOF'
#!/bin/sh
nginx -t && systemctl reload nginx
EOF
chmod 755 /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh
systemctl enable --now certbot.timer
```

---

## Verify

```bash
certbot renew --cert-name observatory.createit.digital --dry-run --run-deploy-hooks
grep -E '^(authenticator|dns_digitalocean)' /etc/letsencrypt/renewal/observatory.createit.digital.conf
systemctl list-timers certbot.timer
echo | openssl s_client -connect observatory.createit.digital:443 -servername observatory.createit.digital 2>/dev/null \
  | openssl x509 -noout -dates -ext subjectAltName
```

Only after the dry-run succeeds: remove TCP 80 from UFW and the Cloud Firewall, and delete any `listen 80` server blocks.

---

## Pitfalls carried from Revy

- A `return 301 https://$host$request_uri;` inside a **443** block loops forever. Stub vhosts must `return 404;` until the real proxy exists.
- With port 80 closed, `http://observatory.createit.digital` does not redirect — it times out. Publish only `https://` links.
- If renewal fails: `journalctl -u certbot.service --since "24 hours ago"`, check token validity, file mode 600, plugin still installed, zone still on DO DNS.

Runbook to write when this ships: `docs/runbooks/tls.md` (force renew, rotate DO token, add a SAN).
