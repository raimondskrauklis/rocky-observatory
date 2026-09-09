# Game Platform Base Plan — Independent Review

**Reviewer:** Perplexity (AI assistant, deep-research review pass)
**Date:** 2026-09-09
**Source document:** `game-platform-base-plan.md` — Game Platform Base Plan, status "production foundation specification — implementation in progress"
**First game:** The Lost Observatory — `observatory.createit.digital`
**Review type:** validation, devil's advocate, market/distribution reality check
**Author-provided context for this pass:** game-building *capacity* is the primary value; education is the main purpose with monetization on the long horizon; web is the first direction, with mobile/offline games possible later; the author is experienced with Keycloak and PostgreSQL and does not consider their operation a burden.

---

## 1. Verdict

**Approve with amendments.** The architecture is coherent, the trust model and service boundaries are stated better than most professional platform documents, and the deferred-scope list is genuinely deferrable. Three classes of issues require action:

1. **Unbudgeted Web platform risk.** Unity Web is the riskiest technical decision in the plan, and the plan contains no size, memory, load-time, or device budgets for it. Fix by adopting the Web Performance Budget (Section 4) as a CI-enforced release gate.
2. **Missing distribution and monetization model.** The plan defines domains and routes but no channel strategy. For web games, distribution is the market: self-hosted domains have zero discovery, and portal constraints feed back into build architecture. A new plan section is required (Section 5).
3. **Operational and versioning omissions.** Unity 6.0 LTS reaches end of support in October 2026 (weeks from review date); Redis eviction policy is unspecified on an instance shared with the Celery broker; droplet sizing, host-level backups, staging topology, and secrets mechanics are undefined (Section 6).

Under the author's reframing — platform capability as the product — keeping the full stack from day one is defensible given demonstrated operational skill, subject to the "exercised or marked as staging" condition in Section 3.

---

## 2. What holds up (unchanged from first pass)

- Trust model (Principle 5) and ownership boundaries (Principle 7) are correct and durable.
- Single Celery Beat instance; idempotent task effects; PostgreSQL constraints as the correctness layer; Redis locks as optimization only — all consistent with Celery's at-least-once delivery semantics on a Redis broker.
- Nginx caching policy for Unity Web artifacts (immutable versioned paths, short/no-cache HTML) matches how Unity Web builds behave; note Unity's IndexedDB Data Caching only caches `.data` files, so Nginx policy carries `.wasm`/`.js` caching.
- Gating player-facing auth behind a real feature need; extracting platform-wide APIs only after a second game demonstrates repeated requirements.
- The deferred list (Terraform, CDN, HA, Kubernetes, analytics) blocks nothing in the chosen stack.

---

## 3. Strategic review: capacity as the product

The author's clarification — *"maybe not game but game-building capacity is the actual value"* — resolves the goal tension identified in the first pass, and changes what the plan should optimize for.

### Accepted

- If the platform is the product and the game is the forcing function, day-one Keycloak/PostgreSQL/Celery is not over-engineering; it is the curriculum. The author's existing operational mastery of these systems removes the maintenance-cost objection.
- The education purpose is best served exactly where the plan is already strong: ADRs, runbooks, CI conventions, and real production failure modes.

### Conditions

1. **Unexercised capability rots.** A Keycloak realm deployed months before its first real auth feature will drift, be upgraded without testing, and accumulate fictional runbooks. Resolution (pick one, write it into the plan):
   - Wire one real identity-gated feature into release 0.2 (optional account, cloud-synced settings, authenticated feedback thread — anything small but real), **or**
   - Formally mark Keycloak/Celery as "platform staging-ground — deployed, monitored, not production-exercised" so the plan does not claim demonstrated capability it does not have.
   - The current gate — "enabled when the first feature requires it," with no feature scheduled — has no forcing function and will slip indefinitely.
2. **Redefine the success metric.** If capacity is the value, the Definition of a Stable Foundation should be measured by *"a second game reaches a deployed playable build in under one week"*, not by first-game delivery alone.
3. **The game still matters as validation.** A platform that never produces a finished game is an unvalidated platform. Milestone discipline (Section 7) remains necessary.

---

## 4. Unity Web: validated as the top technical risk

The author's assertion — *"Unity WebGL is your riskiest decision, and the plan never budgets for it"* — is confirmed by evidence.

### 4.1 Hard technical constraints (as of Unity 6.x, September 2026)

- **Single-threaded C#.** The Web platform does not support managed (C#) multithreading; only native C/C++ multithreading is available, behind COOP/COEP site-isolation headers.
- **Wasm64 XOR multithreading.** As of Unity 6.6, a build must choose between >4 GB memory addressing (wasm64) and native multithreading — not both. Wasm64 additionally excludes Safari.
- **WebGPU is newly production-ready but opt-in.** WebGPU left experimental status in Unity 6.6 (released 2026-09-01) and ships disabled; WebGL 2 remains the default renderer. Decision: stay on WebGL 2 for game one; record an ADR to evaluate WebGPU at the Unity 6.6+ upgrade.
- **Load time is the primary UX failure mode.** Unity's own manual ties slow initialization directly to player abandonment.
- **LTO release builds are slow.** "Disk Size with LTO" significantly increases build time — this is a CI-minutes and iteration-cost budget item, not merely a setting.

### 4.2 The plan's gap

The Web Delivery Standards section specifies *serving* (MIME types, compression headers, cache policy) but nothing about the *build itself*: no size budget, no memory budget, no time-to-playable target, no device test matrix, no texture/scene budgeting discipline. None of the standard mitigation set — Brotli, High managed stripping, IL2CPP "Faster (smaller) builds", WebAssembly 2023 target, exceptions off, near-empty first scene with Addressables streaming — is referenced.

### 4.3 Adopted Web Performance Budget (release gate, enforced in CI)

| Budget line | Target | Basis |
|---|---|---|
| Initial download | ≤ 50 MB (≤ 20 MB for mobile featuring) | CrazyGames hard requirement |
| Total build size | ≤ 250 MB, ≤ 1,500 files | CrazyGames hard requirement |
| Time-to-playable | ≤ 20 s on mid-tier hardware | CrazyGames QA evaluation bar for externally loaded games |
| Heap memory | ≤ 2 GB (`Maximum Memory Size = 2048`), wasm32 | Keeps Safari; avoids wasm64/threading trade-off |
| First scene | Near-empty; content via Addressables groups | Standard Unity Web load-time practice |
| Compression | Brotli; stripping High; LTO for release only | Unity community/documentation consensus |
| Threading | Off (avoids COOP/COEP requirement) | Revisit only with a measured perf need |
| Device matrix | Desktop Chrome/Firefox/Safari/Edge; mobile best-effort | Unity 6 lists iOS Safari 15+ / Android Chrome as supported, memory-constrained |

CI should fail the build on size regressions. Texture budgets, mesh LOD policy, and scene partitioning are **design inputs**, not post-build optimizations.

---

## 5. Missing section: distribution and monetization

The plan contains no distribution channel strategy. For web games this is a larger gap than any infrastructure choice.

### 5.1 Market reality (September 2026)

- **Self-hosted = zero discovery.** Web game traffic concentrates on portals (Poki reports 1B+ monthly plays; CrazyGames a 50M+ audience). A standalone domain brings no players by itself.
- **Revenue is ad-driven and retention-driven.** Portal monetization splits advertising revenue; session time and repeat play drive income.
- **Realistic earnings:** a *well-performing* casual web game typically clears roughly **$200–$3,000/month** on ad revenue share; the median first game earns close to nothing.
- **Splits:** Poki — 50% (100% on traffic the developer brings); CrazyGames — no public split, closest published terms (2026 jam) are 60% of ad revenue / 70% of IAP with a €100 payout floor; publishers offering advances typically take ~70%.
- **Exclusivity:** Poki requires web exclusivity; CrazyGames pays a rev-share bonus for ~2 months of exclusivity.

### 5.2 Genre mismatch

Portal economics punish The Lost Observatory's shape: a 10–15 minute finite narrative has no natural ad-break cadence and no replay loop. As a monetization vehicle it is structurally near-zero; as education and portfolio it is excellent. Consequences:

- Game one: self-hosted canonical home + itch.io (paid/donation fits narrative indie) + optional non-exclusive portal submission for reach, not revenue.
- Game two (if monetization remains the long horizon): design *for* portal economics — replayable, high-session-time, natural commercial-break points.

### 5.3 Architectural consequence: two build targets

Portal constraints feed back into the platform architecture:

- **Poki blocks all external requests by default.** A portal build cannot call `observatory.createit.digital` APIs or Keycloak. Online features must be feature-flagged per build target.
- **Portal packaging** is a single self-contained bundle (fonts, assets, SDK), 16:9 scaling, incognito-safe localStorage, desktop+mobile+tablet support, SDK lifecycle events (`gameLoadingFinished`, `gameplayStart/Stop`, `commercialBreak`, `rewardedBreak`).
- The platform therefore needs two release targets — **self-hosted build** (online features on) and **portal build** (self-contained) — designed now, cheaply, rather than retrofitted.

### 5.4 Recommendation

Add a "Distribution and Monetization" section to the plan covering: canonical self-hosted home; portal submission policy (non-exclusive while the domain strategy matters); itch.io as the paid/donation channel for narrative titles; a per-build-target feature-flag matrix; and explicit monetization expectations per game (education/portfolio vs revenue).

---

## 6. Carried-over technical findings (first pass, still open)

| # | Finding | Severity | Required action |
|---|---|---|---|
| 1 | "Unity 6 LTS" ambiguous; 6.0 LTS support ends **October 2026** | High | Pin **6000.3 LTS** (supported to Dec 2027) in plan + CI; ADR for WebGL2-now/WebGPU-later |
| 2 | One Redis container for broker + cache + rate limits + idempotency, no eviction policy specified | High | `maxmemory-policy: noeviction` on broker DB (Celery docs), separate logical DBs or second container for cache; document `visibility_timeout` rationale |
| 3 | No droplet sizing; Keycloak needs ~2 GB container limit (≈1.25 GB base) | Medium-High | 4 GB / 2 vCPU droplet (~$24/mo); document `KC_HOSTNAME` (v2 mandatory in production mode) and admin hostname separation |
| 4 | Sentry on WebGL cannot see native/tab crashes, no IL2CPP line numbers; telemetry contract overpromises | Medium | Add milestone-beacon endpoint (load → menu → playable) in FastAPI; document blind spots |
| 5 | Git LFS metered billing (10 GiB free bandwidth/mo) × clean-checkout CI | Medium | Cache LFS in CI or set an overage budget |
| 6 | Unity CI activation (GameCI email/password or serial secrets) is the pipeline's most fragile link | Medium | Name the exact mechanism; write activation-failure runbook entry |
| 7 | No host-level backup despite no IaC | Medium | Enable weekly droplet backups (+20% droplet cost, 4-week retention) + Keycloak realm export; pre-deploy snapshots |
| 8 | COOP/COEP absent from Nginx standards | Low-Medium | Record decision (off, with threading); note retroactive cross-origin impact if ever enabled |
| 9 | Staging topology undefined | Medium | Specify: second droplet + separate DB, or co-located with isolation; staging Keycloak placement |
| 10 | Secrets mechanics, Docker log rotation, restart policies unspecified | Low | Name the mechanism (e.g., SOPS/age); configure log rotation in Compose |

Estimated launch run-rate: 4 GB droplet $24 + backups ~$4.80 + managed PostgreSQL $15 + object storage ~$5 ≈ **$49/mo** before staging.

---

## 7. Amended rollout (given the capacity-value framing)

- **M0 — Playable web build shipped.** Static `/play/` artifacts + landing + synchronous feedback endpoint. Web Performance Budget enforced in CI from the first public build. This milestone validates the riskiest decision first.
- **M1 — Full stack deployed and exercised.** Redis/Celery doing real work (e.g., feedback triage/notification), Keycloak realm live with **one real identity-gated feature** (or formally marked staging-ground per Section 3).
- **M2 — Portal build variant.** Feature-flag matrix implemented; non-exclusive submission to at least one portal; itch.io listing.
- **Reuse gate (unchanged):** platform-wide abstractions only after game two demonstrates repeated requirements; success measured as second-game boot time under one week.

---

## 8. Decision log

| Decision | Outcome | Revisit trigger |
|---|---|---|
| Unity version | Pin 6000.3 LTS | Next LTS cycle (Dec 2027 horizon) |
| Renderer | WebGL 2 | After Unity 6.6+ upgrade, evaluate WebGPU ADR |
| Memory model | wasm32, ≤ 2 GB heap | Safari wasm64 support |
| Threading | Off (no COOP/COEP) | Measured CPU-bound perf need |
| Keycloak day-one | Keep (author mastery), must be exercised or marked staging | Release 0.2 scope call |
| Portal exclusivity | Decline for game one | When domain strategy is demonstrably secondary |
| Monetization expectation, game one | Education/portfolio only | Game two design brief |

## 9. What would change this review

- Monetization timeline moves closer → portal economics and genre redesign dominate every other consideration; The Lost Observatory's shape would need re-scoping or explicit acceptance as a non-revenue title.
- Game one slips past ~8 weeks of active development → strip ruthlessly to M0; the platform is unvalidated until a game ships on it.
- Second game never materializes → the reuse policy and shared identity domain should be re-scoped to single-product infrastructure.

---

*End of review. Generated by Perplexity, 2026-09-09.*
