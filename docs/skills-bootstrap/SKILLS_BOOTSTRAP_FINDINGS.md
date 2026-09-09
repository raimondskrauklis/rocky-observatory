# docs/skills-bootstrap/SKILLS_BOOTSTRAP_FINDINGS.md

# Skills bootstrap findings

**Status:** baseline for the general plan — no implementation steps.

**Verified against:** workspace root `/Users/raimonds.krauklis/projects/observatory`, sibling pack `/Users/raimonds.krauklis/projects/agent-workflow` (`d0f8027`), and `game-platform-base-plan.md`. There is no application tree and no database in this folder.

---

## Build principles

- **Pack is SSOT.** Materialize from `../agent-workflow`. Do not run from the pack. Do not treat `code-review/agent-workflow-pack/` as the pack.
- **Adapt, do not clone kp-platform.** Different stack, no GitHub, no Revy. Do not restore kp-platform `.cursorrules`.
- **Never mislead agents.** Manifest `test_commands`, `hosting.kind`, and `skills.installed` must match this repo, not leftovers.
- **Do not push to kp-platform.** The current `origin` is `git@github.com:raimondskrauklis/kp-platform.git`. Any commit/push here can damage that product.
- **This program is workflow only.** It does not scaffold Unity, FastAPI, React, Nginx, or CI.

---

## Terminology

| Term | Meaning here |
|:---|:---|
| **Pack** | Sibling git repo `../agent-workflow` (`pack_version` 2). |
| **Consumer** | This folder, intended as the game-platform / Observatory product repo. |
| **Materialize** | Copy pack `templates/` + write adapted `.agent/manifest.json` into the consumer. |
| **kp leftover** | Files copied from kp-platform that describe procurement analytics, Revy, Pipenv, `backend/`+`frontend/`. |
| **hosting.kind** | Agent ship/PR behavior (`none` / `github` / …). Independent of a future product CI remote. |

---

## What exists vs genuinely new

### Git identity — hazard (**verified**)

This directory is **not** a new git repo.

| Signal | Value |
|:---|:---|
| Path | `/Users/raimonds.krauklis/projects/observatory` |
| Branch | `feat/ur-etl-weekly-ckan` tracking `origin/feat/ur-etl-weekly-ckan` |
| `origin` | `git@github.com:raimondskrauklis/kp-platform.git` |
| HEAD | `686b29d8` — `fix(ur-etl): reject empty live CKAN resource_name in YAML` |
| Working tree | Mass delete of kp-platform `backend/`, `frontend/`, `.cursorrules`, `Pipfile`, `.gitignore`, plus copied `.agent` / `.cursor` / `code-review` / `.revy` |

User intent: **this product is not on GitHub.** Current remotes contradict that. Treat `origin` as a leftover, not as hosting.

### Pack (**verified**)

| Signal | Value |
|:---|:---|
| Path | `~/projects/agent-workflow` |
| HEAD | `d0f8027` — Initial agent-workflow pack |
| Remote | none — skip `git pull` |
| Entry | `skills/bootstrap-workflow/SKILL.md` |
| Adapt / audit | `patterns/ADAPT.md`, `patterns/skills-audit.md` |
| Catalog | `skills.catalog.json` `pack_version` 2 |

### Consumer agent surface today (**verified**)

Present and still **kp-platform-shaped**:

- `.agent/manifest.json` — `project_name: "kp-platform"`, `hosting.kind: github`, `pr_tool: gh`, `review_bot: revy`, `backend_dir: backend`, `frontend_dir: frontend`, Pipenv/npm `test_commands`, `review_context.ssot: .revy/review-context.json`, `flows.revy-babysit.enabled: true`, `pack_source.path: ../agent-workflow` (already pointed at sibling)
- `.agent/skills.catalog.json` — older catalog (extra `requires_*` fields; `babysit-revy-pr` `default_install: true`)
- `.agent/flows/ship.json` — text still says push → PR
- `.cursor/skills/` — 33 skill dirs, including kp product-local corpus / line-count / `lv-en-project-planning`
- `.cursor/skills/bootstrap-workflow/SKILL.md` — **kp-platform copy** (keep corpus/line-count; `hosting.kind` github)
- `.cursor/skills/ship-changes/SKILL.md` — Pipenv ruff, Revy gate, `gh pr create`
- `.cursor/BUGBOT.md` — points at `.revy/review-context.json` and deleted `.cursorrules`; leftover `ur-etl`
- `.cursor/rules/` — kp domain: color tokens, deep-investigation, scope calculators, `git-quick.md` (auto-push)
- `.revy/` — `review-context.json` program `ur-etl`; rule packs platform/backend/frontend
- `.github/workflows/deploy.yml` — `name: CI/CD - kp-platform` (DigitalOcean kp images, Celery queues)
- `code-review/` — full starter-pack + **legacy** `agent-workflow-pack` + `product/revy`
- `.cursorrules` — **already deleted** (do not restore the kp file)

**Missing** (pack install expects these):

- Root `AGENTS.md`
- `.agent/review-context.json`
- `docs/agents/`
- `docs/utils/CURSOR_AGENT_WORKFLOW.md`
- `.cursor/mcp.json`
- Application lockfiles (`Pipfile`, `package.json`, `pyproject.toml`, `go.mod`)
- `.gitignore` (deleted with the kp tree)

`docs/skills-bootstrap/` exists (this program). `game-platform-base-plan.md` is the product spec.

### Target stack (**from plan, not from code**)

No `apps/` tree exists yet. Planned layout (`game-platform-base-plan.md` Repository Layout):

- `apps/game-unity/` — Unity 6 LTS, C#, Git LFS
- `apps/web/` — React + TypeScript
- `apps/api/` — FastAPI
- `apps/admin/` — later
- `infrastructure/` — Compose, Nginx, backup
- Identity Keycloak at `auth.createit.digital`; product at `observatory.createit.digital`

Pack `patterns/ADAPT.md` does not mention Unity/C#. Manifest must declare `apps/game-unity/**` as an available scope without inventing test commands.

---

## Catalog — leftover classes

### A. Keep / replace from pack (workflow)

Core LOOP, planning, docs-export skills, `.agent/` wiring, `docs/agents/`, root `AGENTS.md`, idle `BUGBOT.md`.

### B. Strip — kp product-local skills (not “keep”)

Pack audit says **keep** skills absent from the catalog when they belong to **this** product. These belong to kp-platform, not Observatory:

- `author-corpus`, `corpus-program`, `author-system-corpus`, `author-platform-corpus`, `author-lot-indicator-corpus`, `author-market-screen-corpus`, `author-scope-screen-corpus`, `author-community-group-corpus`
- `line-count-hardening`, `count-lines-backend`, `count-lines-frontend`, `assess-oversized-file`, `split-file-backend`, `split-file-frontend`
- `lv-en-project-planning`

### C. Strip — integrations this repo does not have

- `babysit-revy-pr`, `.revy/`, `flows.revy-babysit`
- `sentry-fix-issues` until `.cursor/mcp.json` exists (rule `.cursor/rules/sentry-mcp.mdc` currently references a missing file)
- `.github/workflows/deploy.yml` (kp CI/CD)

### D. Strip — domain rules

`.cursor/rules/color-tokens.mdc`, `deep-investigation-*.mdc`, `scope-calculator-pattern.mdc`, `git-quick.md` (conflicts with `hosting.kind = none`).

### E. Out of this program — `code-review/`

| Path | Why it is here | Action |
|:---|:---|:---|
| `code-review/agent-workflow-pack/` | Stale in-tree pack; pack README says prefer sibling | Delete from this repo. Never bootstrap from it. |
| `code-review/product/revy/` | Revy SaaS overlay | Delete. |
| `code-review/starter-pack/` | FastAPI/React/Keycloak scaffold | Delete from this repo. Useful later as a **sibling reference**, not as in-tree agent instructions (`starter-pack/AGENTS.md` would compete with root `AGENTS.md`). |
| `code-review/_archive/` | Old drafts | Delete. |

Product scaffold (copying starter-pack patterns into `apps/api` / `apps/web`) is a **later** program. Bootstrap must not copy that SaaS layout (pack `Not in scope`: product SaaS scaffold).

---

## Skill audit (required before materialize)

Evaluate against pack `skills.catalog.json` + `patterns/skills-audit.md` + user: not on GitHub; phased docs work; docs export yes; no Sentry MCP; no staging-validation memos.

| Skill | Now | Action |
|:---|:---|:---|
| `bootstrap-workflow` | kp copy | **upgrade** from pack `templates/` |
| `phase-execution` | installed | **upgrade** |
| `ship-changes` | GitHub/Revy/Pipenv body | **upgrade** |
| `chunk-execution` | installed | **upgrade** |
| `create-findings` | installed | **upgrade** (planning: this folder) |
| `create-general-plan` | installed | **upgrade** |
| `create-execution-plan` | installed | **upgrade** |
| `architecture-peer-review` | installed | **upgrade** |
| `execution-peer-review` | installed | **upgrade** |
| `devils-advocate` | installed | **upgrade** |
| `post-finish-gap-pass` | installed | **upgrade** |
| `md-formatting` | installed | **upgrade** |
| `mermaid-diagrams` | KP-flavoured copy | **upgrade** |
| `md-docx-export` | installed | **upgrade** (`copy_scripts: true`) |
| `docx-md-export` | installed | **upgrade** (`copy_scripts: true`) |
| `babysit-revy-pr` | installed | **remove** |
| `sentry-fix-issues` | installed | **remove** (re-install when MCP exists) |
| `staging-validation` | absent | **skip** |
| corpus / line-count / `lv-en-*` | installed | **remove** |

Installed set after bootstrap (catalog + extras: none):

```text
bootstrap-workflow
phase-execution, ship-changes, chunk-execution
create-findings, create-general-plan, create-execution-plan
architecture-peer-review, execution-peer-review, devils-advocate, post-finish-gap-pass
md-formatting, mermaid-diagrams, md-docx-export, docx-md-export
```

---

## Advice — adapted manifest (locked shape)

Fill from pack `project.manifest.template.json` + `patterns/ADAPT.md`. Do not copy kp values.

| Field | Value |
|:---|:---|
| `project_name` | `observatory` |
| `pack_source` | `kind: sibling`, `path: ../agent-workflow`, `url: null`, `pack_version: "2"` |
| `hosting.kind` | `none` — `pr_tool: null`, `review_bot: null` |
| `backend_dir` | `apps/api` (planned; directory may not exist yet) |
| `frontend_dir` | `apps/web` (planned) |
| `default_scope` | `["docs/**"]` until an application tree exists, then one primary app glob |
| `scopes.available` | `docs/**`, `apps/api/**`, `apps/web/**`, `apps/game-unity/**`, `apps/admin/**`, `infrastructure/**` |
| `test_commands` | `{}` — fill when each app has a real runner; **never** leave Pipenv ruff |
| `review_context.ssot` | `.agent/review-context.json` |
| `integrations.revy` | `false` |
| `flows.revy-babysit.enabled` | `false` |

`scopes.note` must say: Unity is a first-class tree; pack ADAPT has no C# recipe; do not invent `dotnet test` / Unity batch commands until the project documents them.

**LOOP vs idle SSOT:**

- **While this program runs:** `active_program: "skills-bootstrap"` with `programs[].scope` covering `.agent/**`, `.cursor/**`, `docs/skills-bootstrap/**`, `AGENTS.md`, `.gitignore`, `.cursorrules` (paths to this findings + general + execution). Do not use idle `docs/**` as LOOP scope — P1/P2 change `.cursor` and `.agent`.
- **When idle (after the LOOP):** `active_program: null`, `programs: []`. Do not invent `ur-etl`.

Thin product rules (new, not kp):

- Root `AGENTS.md` from pack template, filled with Observatory / Unity+FastAPI+React+Keycloak one-liner.
- Optional thin `.cursorrules` from `game-platform-base-plan.md` § Agent Collaboration Rules (offline play, no client secrets, no unreviewed identity/deploy/schema). File headers only if this repo adopts them later — pack says do not invent stack.
- New `.gitignore`: Unity generated dirs + LFS patterns from the game plan, plus pack ignores (`.DS_Store`, `.env`).

---

## Data scope & exclusions

**In:** agent workflow files, leftover inventory, git-safety, skill audit, planned layout fields in the manifest.

**Out (compute-time — do not do in this program):**

- Unity project, web app, API, Compose, Nginx, Keycloak realm, DigitalOcean
- Writing product CI (plan’s `.github/workflows/` is future; **not** keeping kp `deploy.yml`)
- Adding a GitHub remote for this product or for the pack
- Installing Sentry MCP
- Copying `code-review/starter-pack` into `apps/`
- Translating or porting kp corpus / line-count programs

**Coverage:** skill audit table above is the install set. Hosting stays `none` until the user asks to re-audit after a remote exists.

---

## Edge cases

1. **Push to current origin** — would update kp-platform’s `feat/ur-etl-weekly-ckan` with a gutted tree. Forbidden.
2. **Pack “keep product-local”** — would retain corpus/line-count if followed blindly. Override: those skills are another product’s.
3. **`hosting.kind` vs plan CI** — the game plan describes PRs and `.github/workflows/`. That is future product hosting. Agent `hosting.kind` stays `none` until a real remote exists and the user re-runs bootstrap.
4. **Empty `test_commands`** — better than fake Pipenv. Ship/LOOP must skip lint that does not exist.
5. **`create-findings` pack text** still mentions `docs/DATABASE_CONNECTION_GUIDE.md` (kp). Copy pack as-is; product `AGENTS.md` notes there is no that guide here.
6. **Two AGENTS.md** if `code-review/starter-pack` remains — agents will follow the wrong one.

---

## Decisions registry

| Q# | Question | Status | Resolution |
|:---|:---|:---|:---|
| Q1 | Pack source | **locked** | Sibling `../agent-workflow` @ `d0f8027`. No remote → no `git pull`. Not `code-review/agent-workflow-pack/`. |
| Q2 | Hosting | **locked** | `hosting.kind = none`. User: this repo is not on GitHub. Ignore current kp `origin` as leftover. |
| Q3 | Git identity | **locked** | Detach before any product commit: remove `origin` (or never push it). Prefer a **new orphan history** or `git init` so Observatory does not carry kp-platform commits. |
| Q4 | kp `.cursorrules` | **locked** | Do not restore. Thin stub from game-plan agent rules only. |
| Q5 | kp product-local skills | **locked** | Remove (corpus, line-count, lv-en). Pack “keep” does not apply. |
| Q6 | Revy | **locked** | Remove skill, `.revy/`, revy-babysit flow. `integrations.revy: false`. |
| Q7 | Planning + docs skills | **locked** | Install/upgrade. This repo does program docs and MD/Word handoff. |
| Q8 | Sentry skill | **locked** | Remove until `.cursor/mcp.json` exists. Product will use Sentry later; MCP is separate. |
| Q9 | `staging-validation` | **locked** | Skip. |
| Q10 | Manifest layout | **locked** | Planned `apps/api`, `apps/web`, `apps/game-unity`; `test_commands` empty; default_scope `docs/**` until apps exist. |
| Q11 | `code-review/` | **locked** | Remove entire tree from this repo. Starter-pack is a later optional sibling reference, not in-tree. |
| Q12 | kp `.github` deploy | **locked** | Remove. Future CI is a different program. |
| Q13 | Pack GitHub remote | **locked** | Out of scope. User may add later; then consumers `git pull` + upgrade workflow pack. |
| Q14 | LOOP program id | **locked** | `skills-bootstrap`. Scope as in “LOOP vs idle SSOT”. P3 returns idle. |

---

## Parking lot

- **Phase-0 prerequisite:** git detach (Q3). Nothing else ships until origin cannot receive this tree.
- When apps exist: re-run `bootstrap-workflow` to fill `test_commands` and switch `default_scope`.
- When Sentry MCP is added: re-audit → install `sentry-fix-issues` + a thin MCP rule.
- When a product remote exists: re-audit `hosting.kind`.
- Starter-pack as a **sibling** checkout for later API/web conventions — not this program.
- Pack improvement (not this consumer): `create-findings` still names `DATABASE_CONNECTION_GUIDE.md`.

---

## Devil's advocate

- **Keeping kp git history** “for convenience” leaves `gh` / Revy habits and a dangerous `origin`. Agents will still see `feat/ur-etl-weekly-ckan`.
- **Keeping `code-review/starter-pack`** for Keycloak/FastAPI similarity will make bootstrap look like a SaaS copy (`backend/`+`frontend/`, Revy overlay README). The game plan forbids premature multi-game APIs and wants Unity-first offline play.
- **Setting `hosting.kind: github` because the plan has CI** reintroduces `gh pr` on a repo with no GitHub product remote — or worse, against kp-platform.
- **Leaving `test_commands` as Pipenv** makes every ship fail or lint the wrong tree.

---

## Experiment / verification

Pass when all are true (post-execution, not now):

1. `git remote -v` does not list kp-platform (or user-confirmed no-push + origin removed).
2. `.agent/manifest.json` `project_name` is `observatory`, `hosting.kind` is `none`, `pack_source.path` is `../agent-workflow`, `test_commands` is `{}` or real commands only.
3. `.agent/skills.catalog.json` `pack_version` is `"2"` and matches sibling catalog skill ids (no kp-only extras in `skills.installed`).
4. `.cursor/skills/` listing equals the installed set in the audit table (plus nothing from catalog-remove).
5. No `.revy/`, no `code-review/`, no kp `deploy.yml`, no corpus/line-count skills, no `git-quick.md`.
6. Root `AGENTS.md` skills table matches `skills.installed`. Review SSOT is `.agent/review-context.json`.
7. `git status` does not show thousands of kp `backend/` deletions as the project (orphan/new repo or those paths gone from history).

---

## References

- Pack: `~/projects/agent-workflow/skills/bootstrap-workflow/SKILL.md`, `patterns/ADAPT.md`, `patterns/skills-audit.md`, `PACK_INSTALL.md`, `project.manifest.template.json`
- Consumer: `.agent/manifest.json`, `.cursor/skills/bootstrap-workflow/SKILL.md`, `.cursor/skills/ship-changes/SKILL.md`, `.revy/review-context.json`, `.github/workflows/deploy.yml`, `code-review/README.md`
- Product: `game-platform-base-plan.md` (stack, layout, agent collaboration rules)
