# .revy/rules/README.md

# Revy rule packs — Observatory

Short, checkable principles for PR review. Not `.cursorrules` (that file is agent chat + LOOP). Revy reviews **whole files the diff touches**; these packs are what it checks against.

Do not copy kp-platform packs. Do not ingest `.cursorrules` or `AGENTS.md`.

| Id | File | When |
|:---|:---|:---|
| `platform` | [platform.md](./platform.md) | Any `apps/`, `infrastructure/`, or `packages/` path in `scope` |
| `backend` | [backend.md](./backend.md) | Any `apps/api/` path in `scope` (including tests) |
| `frontend` | [frontend.md](./frontend.md) | Any `apps/web/` path in `scope` |

`apps/game-unity/**` uses **platform** only until a Unity pack exists.

**Include:** P0.0 writes `programs[].rule_packs` from `scope`. Do not ask in chat. Docs-only scope (`docs/**`) → `[]`.

**Catalog:** `.revy/review-context.json` → `rule_packs_catalog`. GitHub App setup: [docs/runbooks/github-revy.md](../../docs/runbooks/github-revy.md).
