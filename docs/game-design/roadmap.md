# docs/game-design/roadmap.md

# Roadmap — From Vision to First Playable

## Status

**Status:** Active. Derives from `vision.md` (v2). No dates, no deadlines. Sequence and dependencies only. Decisions locked during each phase become the base for the next. Decisions held open are revisited when a downstream phase needs them.

## Philosophy

We are not building a minimum viable product. We are building a long-horizon creative platform where the first game is also the proof that the system works. The creative layer is not secondary; it drives the technical choices.

Every step in this roadmap is chosen so that the feeling of the thing arrives as early as possible, and the platform costs arrive only when the game needs them.

Decisions are locked as they arrive. If a later discovery needs something unlocked, the doc that holds the decision is updated first, then the downstream doc. The rule is in `README.md`.

## Phase 0 — Lock the World

The characters are the entire design. Nothing else moves until they feel right.

### What we lock

- Sofi's voice: a handful of real lines the creator writes or speaks, accepted by the creator. These are the reference for every line she ever says.
- Pluto's voice: same process. Fewer words. Calmer.
- The Voice's name. Chosen by the creator. Pronounceable by a six-year-old. Not from existing fiction. A word Sofi can shout.
- Voice policy confirmed: natural recorded voice for Sofi and Pluto, not synthetic. A child voice actor or a talented adult doing a young voice. Recorded once, processed cleanly, reused across episodes. Reserve ElevenLabs for prototyping or the Voice itself.

### What we decide but may revisit

- Whether Pluto ever speaks in the tonal language unprompted (touches Pluto's origin; keep closed for now).
- Why Sofi is at the observatory.

### Document to iterate

`docs/game-design/world.md` — the base draft exists. Rewrite with the creator's lines, the Voice's name, and the voice production approach.

### Done when

The creator reads Sofi's and Pluto's sample lines aloud, feels them, and says yes.

## Phase 1 — Lock the Look

Art direction is the second most important emotional tool after the characters. Until the look is pinned, Astra briefs will drift.

### What we lock

- Stylisation level: low-poly clean versus hand-painted versus something else.
- Palette: the two-state language (dead / alive) from `art-direction.md`.
- Quicksilver treatment: how Pluto reads on WebGL2 without real reflections. Probe, matcap, or hybrid.
- Sofi's and Pluto's designs: silhouette, colours, how they read against both palettes.
- Per-asset-class budgets from `art-direction.md`: accepted or revised.

### What we decide

- Sky: real star catalogue or painted skybox.
- How much exterior is visible in Episode 1.
- Reference images: three to five "this feels right" and one or two "this is wrong."

### Document to iterate

`docs/game-design/art-direction.md` — the base draft exists. Rewrite with references and the confirmed decisions.

### Done when

The creator can picture the observatory in both states and can see Sofi and Pluto moving through it.

## Phase 2 — Prove the Loop (Grey-Box Slice)

Before any 3D asset is made, before any Astra brief is written, we make the smallest possible playable loop in Unity. This is not a demo. It is a validation of every technical seam.

### What it contains

- One grey-box room in Unity.
- Sofi: a simple capsule or placeholder, walks, looks.
- One switch, interactable. One light, toggles.
- Pluto: a sphere that follows Sofi and changes colour when she interacts.
- One tone: a synthesised sine wave plays when the light turns on.
- `?smoke=1`: auto-plays to the "light on + tone played" state and beacons to `/api/v1/telemetry`.

### What this proves

- Unity 6.3 project starts, builds for Web, and runs.
- The light-state system works with two states and one toggle.
- The tone synthesiser generates sound at runtime.
- The beacon fires and hits the API.
- The grey-box loop feels like something, not just a tech test. Sofi walks into a dark room, turns on a light, hears a tone, and something about it is already a little magical.

### What this does not do

- No art. No story. No release to a Droplet. No CI. No Pluto forms beyond a sphere. No voice. No music stems.

### Document created

None. This is a Unity project checkpoint, not a document. The result is a working scene in `apps/game-unity/` and knowledge of what breaks.

### Done when

The loop plays in a browser. The tone plays. The beacon arrives. The creator feels something.

## Phase 3 — Pipeline Test (One Astra Asset)

Before writing briefs for the whole episode, we make one real asset through the full pipeline and import it into Unity.

### What it contains

- One Astra brief: the telescope tube (hero prop) from `episode-01/GDD.md`.
- One `bpy` script, run headless, validated against the budget.
- One `.blend` and one `.glb` output, checked and imported into Unity.
- One provenance record in `manifest/`.

### What this proves

- The asset-pipeline brief template works.
- Astra produces usable, budget-compliant geometry from a real brief.
- Validation catches what it should.
- GLB import into Unity 6.3 works (glTFast or FBX path confirmed).
- The asset looks right at Sofi's eye height (1.0 m camera).

### Documents revised

- `docs/game-design/asset-pipeline.md` — updated with real findings.
- `docs/game-design/episode-01/GDD.md` — asset list revised based on what Astra actually produced.

### Done when

The telescope tube sits in the grey-box room from Phase 2. It is in budget, its provenance record exists, and the creator says the scale and silhouette are right.

## Phase 4 — Finish the GDD

With the world locked, the look locked, and the pipeline proven, the Episode 1 game design document becomes the blueprint, not a proposal.

### What we lock

- Restoration chain, one system at a time, with Pluto's forms per system.
- The signal event: exact count, exact timing, exact response.
- Optional depth: what the patient player earns.
- Audio budget lines: stem count, formats, compressed size ceiling. Approved.
- Voice approach: natural recorded voice, text boxes alongside, mute works, player can click through.
- Asset list: every object in Episode 1, class-tagged, budgeted per class.
- Release contract 0.1: the public promise, accepted.

### Document to iterate

`docs/game-design/episode-01/GDD.md` — the base draft exists. Rewrite into the buildable spec.

### Done when

A person who has never read any other doc can read the GDD and describe exactly what Episode 1 is, how it plays, and what it sounds like.

## Phase 5 — Platform Touch-Up

Before Episode 1 production starts, the platform plan and the game design need to agree.

### What changes

- The "First Product" section of `game-platform-base-plan_v2.1.md` becomes a one-paragraph pointer to `docs/game-design/`.
- Blender LTS version is pinned in the plan.
- Audio budget lines are added to the Web Build Budgets table.
- Unity standards note that gameplay lives in C# and ScriptableObjects; scenes are thin (agent-friendly Unity).

### Document edited

`docs/initial-planning/game-platform-base-plan_v2.1.md` — minor, surgical edits.

### Done when

The plan no longer describes a v1 game that no longer exists.

## Phase 6 — Episode 1 Production

Now the creative and technical paths merge. Episode 1 is built as the platform's M0 and 0.1 release. This is a parallel phase: the creator and the agent work on different threads that meet at the release.

### Thread A — Game content

- Astra briefs for all 45 Episode 1 assets (or however many the revised GDD calls for).
- `bpy` scripts, validation, provenance records.
- Unity import, light-state wiring, interaction points.
- Voice recording session (Sofi and Pluto lines).
- Music stems composed or sourced, within the audio budget.
- Score integration with the light-state system.
- Tone synthesiser integration with the signal event.

### Thread B — Platform

- DevOps execution plan written from the existing general plan and operations specs.
- Droplet provisioned, Compose running, host Nginx live, TLS live, basic auth on.
- `web` image built (Nginx + React landing/privacy/feedback + Unity Web build).
- `api` image built (feedback endpoint, health, version, telemetry beacon).
- Managed PostgreSQL provisioned, feedback and beacon tables created.
- Redis running with rate limiting.
- Sentry configured for API, web, and Unity client.
- First deploy to production. First rollback. Smoke passes. Beacons flow.

### Meeting point: M0

- The game is at `observatory.createit.digital/play/` behind basic auth.
- It meets the Web Build Budgets.
- `web` and `api` images have been deployed and rolled back once each by tag.

### Meeting point: 0.1

- Staging Droplet added.
- Gate removed from production.
- `/admin/` ships only if feedback volume makes reading the database impractical.
- First restore drill logged.
- Public release.

## What Does Not Happen Yet

Until M0 is green:

- No Keycloak (profile `identity` stays off).
- No Celery or scheduled jobs (profile `jobs` stays off).
- No second episode production.
- No multi-game or multi-tenant abstractions.
- No voice acting beyond Episode 1.
- No touch controls as a gate.
- No music beyond Episode 1.

## Parallel Track — The Episodes Arc

While Episode 1 is in production, the series map in `docs/game-design/episodes.md` stays draft. Iterate it as ideas arrive, but do not lock any episode beyond 1 until the pipeline and the voice have been proven on real assets and real recordings. The arc grows as the series grows.

## The Rule That Holds Everything Together

A constrained design that feels right is always better than an unconstrained design that is impressive. Every time a budget tightens, ask: does this make Sofi's experience more honest? If the answer is yes, keep the constraint. If the answer is no, change the budget.

And the most important rule of all: if Sofi and Pluto do not feel right in the grey-box slice, nothing else matters. Fix them first.