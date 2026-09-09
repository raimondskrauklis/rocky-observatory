# docs/skills-bootstrap/SKILLS_BOOTSTRAP_GENERAL_PLAN.md

# Skills bootstrap — general plan

**Findings:** [SKILLS_BOOTSTRAP_FINDINGS.md](./SKILLS_BOOTSTRAP_FINDINGS.md)

**Not execution.** Per-phase files come from `create-execution-plan`.

Locked decisions Q1–Q14 in findings travel unchanged. This program materializes `../agent-workflow` @ `d0f8027` into Observatory and strips kp-platform leftovers. It does not scaffold the game, API, or hosting.

---

## Cross-cutting (every phase)

- **Lineage:** `pack_source.path` stays `../agent-workflow`. Do not bootstrap from `code-review/agent-workflow-pack/`.
- **Honesty:** `hosting.kind`, `test_commands`, and `skills.installed` match this repo. Empty test commands until runners exist.
- **Coverage:** skill audit table in findings is the install/remove set. Do not resurrect corpus, Revy, or Pipenv.
- **i18n:** agent files stay English. Product EN+LV is out of scope.
- **Tests:** no application test runner yet. Verification is the findings pass/fail list (remotes, manifest, skill dirs, leftover trees).
- **Push:** `hosting.kind = none`. Local commits only. Never `git push` to the current kp-platform `origin`.
- **LOOP SSOT (Q14):** while this program runs, `active_program` is `skills-bootstrap` with scope `.agent/**`, `.cursor/**`, `docs/skills-bootstrap/**`, plus `AGENTS.md` / `.gitignore` / `.cursorrules`. P3 returns idle (`null`, empty `programs`).

---

## P0 — Git safety

**Goal:** This folder cannot update kp-platform, and it has a product `.gitignore`.

**Scope:**

- **In:** detach `origin` (remove remote or equivalent no-push guarantee); prefer orphan / fresh history so Observatory does not carry kp-platform commits and UR-ETL branch name; add `.gitignore` from the game plan (Unity `Library/` etc. + `.env` / `.DS_Store`).
- **Out:** adding a GitHub remote for Observatory or for the pack; rewriting kp-platform history on GitHub.

**Deliverables:** no `origin` pointing at `kp-platform.git`; working tree is a new product history (or an explicit orphan); `.gitignore` present; documented “do not push” until that is true.

**Depends on:** nothing.

---

## P1 — Strip leftovers

**Goal:** Agents have one instruction set: this product + the pack, not kp-platform / Revy / starter-pack.

**Scope:**

- **In:** remove `code-review/`; `.revy/`; `.github/workflows/deploy.yml` (and empty `.github` if nothing remains); kp `.cursor/rules/` listed in findings; kp product-local skills; `babysit-revy-pr`; `sentry-fix-issues`.
- **Out:** deleting `game-platform-base-plan.md`; deleting this `docs/skills-bootstrap/` folder; copying starter-pack into `apps/`.

**Deliverables:** leftover trees from findings catalog B–E gone; `.cursor/skills/` no longer contains corpus / line-count / lv-en / Revy / Sentry.

**Depends on:** P0 (so a strip commit cannot be pushed to kp-platform).

---

## P2 — Materialize pack and adapt

**Goal:** Consumer matches pack install layout, adapted to Unity + FastAPI + React + no GitHub.

**Scope:**

- **In:** copy pack catalog → `.agent/skills.catalog.json`; write `.agent/manifest.json` to the locked shape (Q10); flows without revy-babysit; `.agent/review-context.json` for **this** LOOP (Q14 — not `ur-etl`, not idle yet); copy/upgrade the findings audit **install** set from pack `templates/.cursor/skills/` (full folders when `copy_scripts`); `docs/agents/` + `docs/utils/CURSOR_AGENT_WORKFLOW.md`; root `AGENTS.md`; `.cursor/BUGBOT.md` pointing at this program’s contract; thin `.cursorrules` from game-plan agent collaboration rules. After P1 deleted `.revy/`, this phase must create the new SSOT in the same LOOP.
- **Out:** inventing Unity/pytest/npm commands; creating `.cursor/mcp.json`; enabling Revy; writing product CI; restoring kp `.cursorrules`.

**Deliverables:** pack verify checklist green for a no-GitHub, no-app-yet repo; `AGENTS.md` skills table = `skills.installed`; review SSOT is `.agent/review-context.json`.

**Depends on:** P1 (upgrade into a clean skill tree, not a merge with corpus skills).

---

## P3 — Verify

**Goal:** Findings verification list is true on disk.

**Scope:**

- **In:** walk findings “Experiment / verification” items 1–7; fix gaps that are still leftover or mis-adapted; leave `active_program` null when idle.
- **Out:** starting `phase-execution` on the game platform itself; pack remote setup.

**Deliverables:** verification list all pass; short note in this folder or `docs/agents/` that re-audit happens when apps, Sentry MCP, or a remote appear.

**Depends on:** P2.

---

## Open item / next step

**Done 2026-09-09.** P0–P3 executed directly (see [README.md](./README.md) for status and re-audit triggers). Calibration later: `test_commands` and `default_scope` when `apps/` exists.
