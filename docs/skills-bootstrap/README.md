# docs/skills-bootstrap/README.md

# Skills bootstrap — program index

Install the sibling **agent-workflow** pack into this product repo (The Lost Observatory / game-platform-base), after stripping kp-platform leftovers that were copied in with the folders.

**Pack SSOT:** `~/projects/agent-workflow` (`main` @ `d0f8027`). No pack remote.

| Doc | Role |
|:---|:---|
| [SKILLS_BOOTSTRAP_FINDINGS.md](./SKILLS_BOOTSTRAP_FINDINGS.md) | Baseline — inventory, skill audit, leftover trees, locked decisions |
| [SKILLS_BOOTSTRAP_GENERAL_PLAN.md](./SKILLS_BOOTSTRAP_GENERAL_PLAN.md) | Phases P0–P3 — git safety, strip, materialize, verify |
| [game-platform-base-plan_v2.1.md](../../game-platform-base-plan_v2.1.md) | Target product stack (not executed by this program) |

**Status: done (2026-09-09).** P0–P3 were executed directly in one session (no per-phase execution files — the program was small enough that the general plan served as the contract). Verification items 1–7 pass; item 7 (fresh history) was completed by an orphan `main` with the kp-platform refs kept under `refs/backup/` for 90 days of safety.

**Re-audit triggers** — run `bootstrap-workflow` against `../agent-workflow` when any of these appear: `apps/*` trees (fill `test_commands`, switch `default_scope`), a Sentry MCP (`sentry-fix-issues`), or a pack version bump.

**Hosting (2026-09-09):** Q2 (`hosting.kind = none`) was superseded by private GitHub `raimondskrauklis/rocky-observatory`. Q6 (Revy off) was superseded the same day: `integrations.revy: true`, skill `babysit-revy-pr`, SSOT `.revy/review-context.json`. Consumer GitHub steps: [docs/runbooks/github-revy.md](../runbooks/github-revy.md). The findings file below is the bootstrap-time baseline.
