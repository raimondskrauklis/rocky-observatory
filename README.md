# The Lost Observatory

**A game about space and engineering optimism, built by a father and son, one real place at a time.**

Sofi is seven. Pluto is made of liquid metal and can become anything. Together they arrive at a giant radio telescope hidden in a forest and discover that someone was here before them — someone who heard a signal and never answered it.

The game is a learning engine disguised as an adventure. Sofi starts from zero: counting, shadows, "why is it dark?" Her impatience is the tutorial. Pluto is the toolset. Every puzzle is "what does Pluto need to become here?" Every place is real — the first episode is set at VIRAC in Irbene, Latvia, a genuine Cold War radio telescope that Latvian scientists rebuilt with their own hands.

There is no final answer. Each episode unlocks the next place. The journey does not end.

---

## Why this repo exists

This is my first project in C# and Unity. My son is learning alongside me. The repo is public so that if another parent, another kid, or another beginner wants to follow the same path — or build their own thing on top of it — they can see every step, every mistake, and every decision.

We are not trying to ship fast. We are trying to understand what we are building and why.

## What's here

| Folder | What it is |
|:---|:---|
| `docs/game-design/` | The creative design: vision, characters, places, episodes, and three accepted scenes for Episode 1. Start with `vision.md`. |
| `docs/initial-planning/` | The hosting and platform plan — Unity, FastAPI, Docker, DigitalOcean — for when the game is ready to go public. Not needed to just open Unity and press Play. |
| `corpus/` | Real facts about the real places. VIRAC (Latvia) is populated; Tartu and Lithuania are stubs for later episodes. |
| `apps/game-unity/` | The Unity project. Currently a scaffold with a grey-box slice spec; the first playable loop is being built. |
| `.cursor/skills/craft-scene/` | The creative producer's workflow for crafting scenes. Agents and humans can follow the same process. |

## How to start

1. **Read the game idea.** `docs/game-design/vision.md` — one sentence, then ten decisions. Five minutes.
2. **Meet the characters.** `docs/game-design/world.md` — Sofi, Pluto, the Voice, the spider.
3. **Read the first scene.** `docs/game-design/episode-01/scenes/opening.md` — Sofi and Pluto arrive at the dish.
4. **Open Unity.** `apps/game-unity/` — we're building the grey-box slice: a capsule that walks, a sphere that follows, a switch that turns on a light. That's all. When that feels right, everything else layers on top.

## What we are learning (the first few weeks)

- C# basics: classes, interfaces, MonoBehaviour, Unity events.
- Unity WebGL builds: what works, what doesn't, what costs bytes.
- How to make a character feel alive with cubes and a single point light.
- How to build a tone synthesiser from a sine wave and a float array.
- How to structure a Unity project so an AI agent can read it and contribute.

## Real places behind the fiction

- **Episode 1: VIRAC**, Irbene, Latvia. A 32-metre radio telescope hidden in pine forest, built by the Soviet navy, abandoned in 1994, rebuilt by Latvian scientists.
- **Episode 2 (candidate): LU Observatory**, Latvia. Latvijas Universitātes observatorija — a small optical observatory with a history of variable-star research.
- **Episode 3 (candidate): Tartu Observatory**, Estonia. Space research and signal processing.

Every fact in `corpus/` is sourced. Every fiction is marked.

## A note on influences

The repo is called Rocky for a reason — *Project Hail Mary* got us started. But everything here is written, drawn, and coded by us. No borrowed characters, names, or stories. We love the feeling of finding something and not knowing what it says; we just wanted to make our own version of that feeling. A licence file will arrive when the first release does.

## Links

- Platform plan: `docs/initial-planning/game-platform-base-plan_v2.1.md`
- Roadmap: `docs/game-design/roadmap.md`
- Agent entry point: `AGENTS.md`
