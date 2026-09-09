# .revy/rules/frontend.md

# Frontend (`apps/web`)

React + TypeScript under `apps/web`. `/admin/` lives here when it exists. Unity Web is a build artifact in the `web` image, not a second static tree on the host.

- No secrets, tokens, or Keycloak client secrets in the bundle.
- Do not trust browser-submitted competitive, financial, or entitlement state.
- Preserve offline play in the shell unless the PR explicitly changes that contract.
- Do not invent npm scripts. Use what `package.json` actually defines once it exists.
- Identity UI (PKCE, `silent-check-sso.html`) ships only with a named `/admin/` (or other) consumer — not as an unused login wall.
- Hashed assets may be immutable; HTML and Unity loaders stay `no-cache`. Do not flatten cache policy to `max-age=0` on everything.
