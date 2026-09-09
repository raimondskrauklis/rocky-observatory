# OpenAI review: game-building capacity, not the first game

Status: review note. Not a change to `game-platform-base-plan_v1.1.md`.
Date: 2026-09-09
Project: The Lost Observatory / createit.digital

## Reviewed claim

The earlier read treated *The Lost Observatory* as the thing of value, and treated shipping it as the onboarding win.

That is too small.

The asset is **game-building capacity**: a person who can take a small idea to a public, versioned, playable build, watch someone else fail at it, and do the next one without starting the stack from zero.

The first game is the proof that the capacity exists. It is not the product that pays, and it is not the curriculum.

## What this does not change

The first public release contract stays:

- `https://observatory.createit.digital/play/`
- Unity 6 LTS, about 10 to 15 minutes, beginning / progress / ending
- Playable with no login, no ads, no payments
- Playable if FastAPI, Redis, Celery, or Keycloak is down
- Landing, privacy, feedback, version, monitoring, rollback

Those deferred features stay deferred: mandatory login, cloud save, leaderboards, payments, advertising, multiplayer, chat, user-generated content, in-game economy, large analytics.

## Keycloak, PostgreSQL, and the rest of the foundation

Earlier wording could be read as "cut the backend because it is too much."

That is not the point.

Raimonds can implement and maintain Keycloak, Managed PostgreSQL, Redis, Celery, Nginx, and the droplet. That is not the constraint. He already owns that class of work.

They are later for a different reason: the first release does not need them for play, and the son's first job is not operating them. They stay in the architecture as real pieces, used when a real feature needs them (cross-device progress, purchases, moderation). They are not temporary toys, and they are not the first lesson.

Father owns ops. Son owns the playable loop and the public link. Backend seams, one at a time, when the game asks for them.

## Why the first game is not the money

A 10 to 15 minute atmospheric web puzzle does not match the shape of games that pay.

- Q4 2025, Steam, indie launches: 1,712 titles, 24 cleared $2M net (1.4%). None of those hits had under 2 hours average playtime. Pricing under $10 was a negative signal. Source: Turbine Games, 27 May 2026, Q4 2025 set.
- 2025 Steam release cohort: mean gross about $358,900, median about $249 (a December 2025 read put the median near $318). The often-quoted "$5,000 to $15,000 median" is a synthesis of survivor-shaped sources, not that full-year cohort. Source: reporting of Gamalytic's 2025 Steam release analysis.
- Same title on itch.io is typically 1 to 5% of its Steam take. itch.io is the right shelf for a free short piece and a jam, not the cash register.
- Unity Web: Unity staff have said WebGL is not supported by Unity Ads or by Unity IAP direct-to-consumer payments (those target iOS and Android). A self-hosted `/play/` page does not have a built-in cash path.
- Browser portals (CrazyGames and similar) can pay later from ads, but they do not publish a fixed revenue split in the main developer docs. A 2026 jam terms sheet listed 60% of ad revenue to the developer. Payouts need volume. That channel wants session length and repeat play, not a one-sitting atmosphere piece. It is a later option, not the launch model.

First-game revenue also does not predict who ships again. About 80% of first Steam releases have no follow-up within three years. Developers whose first game missed, middled, or hit continue at roughly the same rate. Persistence is a trait, not a reward for the first cheque. Sources: a327ex.com on Steam follow-up; Game Oracle figure cited by Turbine (about 4 in 5 first-game failures never ship a second).

So: do not put a price, a login wall, or ads on this release to "make it real." That fights the learning and the offline contract, and the numbers say it would not pay anyway.

## What can pay, on a long horizon

Ranked by fit with this project. None of these are a forecast for *The Lost Observatory*.

1. **Later games, paid where the shape fits.** A game people finish and recommend, long enough to sit on Steam or a store (hours, not 15 minutes), priced like a real indie (the Q4 2025 hit set clustered at $10 to $20). Second games sell better on average because scope, marketing, and audience carry, not because the first title was a hit. This is the cleanest money path, and it is years out.
2. **createit as a studio, not a platform product.** Paid interactive work, education pieces, client jobs, using the same habits: versioned build, staging, rollback, owned hosting. The buyer pays for a finished experience and a reliable delivery, not for your Keycloak realm.
3. **A short web title on a portal, after it is fun.** Ads, SDK, their traffic. Optional. Do not bend the observatory into a portal game to chase this.
4. **Selling the platform.** Weakest. Nobody buys a private game backend. Shared APIs wait until a second game repeats a need. The plan already says this. Keep it.

## What the son should actually get

Not a tour of the droplet.

The capacity, in order:

1. A loop he can press Play on, without containers.
2. A public URL someone else can open, and a broken moment he sees with his own eyes.
3. A version number, a rollback, and a reason those exist.
4. A second small game that reuses the release path, not a new religion.
5. Identity, cloud save, and money only when a feature cannot exist without them.

The production stack is the father's instrument. It becomes his instrument when he has already shipped and the next feature needs a seam. Starting him on Keycloak teaches the wrong craft first.

## Lock

- Value = game-building capacity. First game = proof, free, offline, public.
- Keycloak and PostgreSQL: Raimonds can build and keep them. They wait for a feature, not for courage.
- Son's first job: the playable loop and the public link. Father's job: ops.
- No platform product. No paywall on v1.
- Money waits for a later game that matches a store, or for studio work under createit. Not for this foundation.

## Sources used

- Turbine Games, "What Separates Steam Indie Winners From Losers", 27 May 2026. Q4 2025, 1,712 indie launches, 24 over $2M net, playtime and price splits.
- Gamalytic 2025 Steam release cohort, as reported (mean vs median). Treat the $249 to $318 median as the full-cohort figure. Treat $5k to $15k medians as a different, softer cut.
- a327ex.com, "What predicts indie success, tested against all of Steam." Follow-up rates; first-game outcome does not predict a second ship.
- Unity Discussions, Unity staff on IAP 5.4 / D2C: WebGL not supported; D2C targets mobile.
- CrazyGames developer docs: Tipalti payouts, €100 minimum, no fixed split in the main docs. 2026 jam terms are the nearest published share, not a general contract.
