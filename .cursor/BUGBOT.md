# Bugbot — review contract

**Active program:** none (`idle`)

**SSOT:** [.revy/review-context.json](../.revy/review-context.json) (mirror: [.agent/review-context.json](../.agent/review-context.json))

Default review authority: [.cursorrules](../.cursorrules) and [AGENTS.md](../AGENTS.md). Revy packs: [.revy/rules/](../.revy/rules/).

When a LOOP is running, set `active_program` and `programs[].scope` in `.revy/review-context.json` first, copy to the `.agent/` mirror, then point this file at that program’s findings, general plan, and current execution file.
