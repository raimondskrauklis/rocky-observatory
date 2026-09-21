# docs/game-design/README.md

# Game Design — The Lost Observatory

Design documentation for *The Lost Observatory*, an episodic exploration series about space and engineering optimism. The platform that delivers it is specified in `docs/initial-planning/game-platform-base-plan_v2.1.md`; that plan's "First Product" section defers to this folder.

## Source of truth

`vision.md` holds the general decisions (audience, no final answer, one place per episode, Pluto as interface, real artefacts, own material). Every other document here derives from it. If a downstream document needs a general decision changed, change it in `vision.md` first, then propagate.

## Documents

| # | Document | Purpose | Status |
|:---|:---|:---|:---|
| 0 | [vision.md](vision.md) | Creative direction and general decisions | v2 — accepted |
| 1 | [world.md](world.md) | Sofi, Pluto, the previous observer, the Voice, the tonal language, real artefacts | Base draft — iterate |
| 2 | [art-direction.md](art-direction.md) | Look, palette, dark-to-alive lighting, quicksilver on Web, asset budgets | Base draft — needs references |
| 3 | [asset-pipeline.md](asset-pipeline.md) | Blender + Astra as assets-as-code; validation; Unity import; provenance | Base draft — iterate |
| 4 | [places.md](places.md) | Real places per episode; Episode 1 = VIRAC locked; fiction boundaries | Base draft — iterate |
| 5 | [episodes.md](episodes.md) | Series arc, episode map, learning ladder, rules for adding an episode | Base draft — iterate |
| 6 | [episode-01/GDD.md](episode-01/GDD.md) | Episode 1, the observatory: layout, restoration chain, signal event, audio, assets, release contract | Base draft — iterate |
| — | [episode-01/scenes/](episode-01/scenes/README.md) | Per-scene breakdown of Episode 1, crafted by the creative producer | Opening scene not started |
| — | [roadmap.md](roadmap.md) | Phased sequence from vision through first playable; no dates | Active |

### Corpus (parallel track)

| Folder | Purpose | Status |
|:---|:---|:---|
| [corpus/](../corpus/README.md) | Real reference material per place; machine-readable INDEX.json; genAI-ready | Structure created — populate per episode |

## Reading order

1. `vision.md` — always first.
2. `world.md` — who and what.
3. `art-direction.md` then `asset-pipeline.md` — how it looks and how assets are made. Both precede the first Astra brief.
4. `places.md` then `episodes.md` — where each episode is and where the series goes.
5. `episode-01/GDD.md` then `episode-01/scenes/` — what gets built first, scene by scene.
6. `roadmap.md` — the overall sequence.

## Creative producer workflow

The `.cursor/skills/craft-scene/` skill defines the scene-crafting process. Read `SKILL.md` for the full workflow. Start with `task-opening-scene.md` — the first assignment.

## Iteration rule

Each document carries a **Status** line and an **Open questions** section. Iterate one document at a time; when a document's open questions are resolved, update its status. Do not start Unity scene work for an episode until its GDD status is *accepted*.

## History

`docs/story/the-lost-observatory-vision.md` is vision v1, superseded and kept for history.
