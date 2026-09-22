# The Lost Observatory

**A game about space and engineering optimism, built by a father and son, one real place at a time.**

**Status:** Early learning project. Design docs and the real-world corpus are ahead of code; the first playable grey-box slice is in development.

Sofi is seven. Pluto is made of liquid metal and can become anything. Together they arrive at a giant radio telescope hidden in a forest and discover that someone was here before them — someone who heard a signal and never answered it.

The game is a learning engine disguised as an adventure. Sofi starts from zero: counting, shadows, "why is it dark?" Her impatience is the tutorial. Pluto is the toolset. Every puzzle is "what does Pluto need to become here?" Every place is real — the first episode is set at VIRAC in Irbene, Latvia, a genuine Cold War radio telescope that Latvian scientists rebuilt with their own hands.

There is no final answer. Each episode unlocks the next place. The journey does not end.

## Why this repo exists

This is my first project in C# and Unity. My son is learning alongside me. The repo is public so that if another parent, another child, or another beginner wants to follow the same path — or build their own thing on top of it — they can see every step, every mistake, and every decision.

Over the long term, the aim is to help children explore science, technology, engineering, and mathematics through playful stories rooted in real places and real scientific work.

We are not trying to ship fast. We are trying to understand what we are building and why.

## Where we are

The roadmap runs lock the world → lock the look → grey-box slice → art and episodes. We are between the first two: the characters have base drafts and sample lines waiting to be accepted, the art direction is being pinned, and the grey-box slice is specified but not yet built.

## What's here

| Folder | What it is |
|:---|:---|
| [`docs/game-design/`](docs/game-design/) | The creative design: vision, characters, places, episodes, art direction, and three accepted scenes for Episode 1. Start with [`vision.md`](docs/game-design/vision.md). |
| [`corpus/`](corpus/) | Real facts about the real places, fact and fiction kept apart. VIRAC (Latvia) is populated; LU Observatory and Tartu Observatory are stubs for later episodes. |
| [`apps/game-unity/`](apps/game-unity/) | The Unity project. Folder scaffold and the [grey-box slice spec](docs/game-design/greybox-slice.md); scripts are not committed yet. |
| [`docs/initial-planning/`](docs/initial-planning/) | The hosting and platform plan — Unity, FastAPI, Docker, DigitalOcean — for when the game goes public. Not needed to open Unity and press Play. |
| [`docs/devops/`](docs/devops/) | Hosting operations: droplet, DNS, TLS, Nginx, registry, deploy. |
| [`docs/agents/`](docs/agents/) | How agents and humans work in this repo. |
| [`.cursor/skills/craft-scene/`](.cursor/skills/craft-scene/) | The creative producer's workflow for crafting scenes. Agents and humans follow the same process. |

## What's not here yet

- No playable build.
- No C# scripts; the Unity folder is structure only.
- No recorded voice or audio.
- No licence file. One arrives with the first release.

## How to start

1. **Read the game idea.** [`docs/game-design/vision.md`](docs/game-design/vision.md) — one sentence, then ten decisions. Five minutes.
2. **Meet the characters.** [`docs/game-design/world.md`](docs/game-design/world.md) — Sofi, Pluto, the Voice, the spider.
3. **Read the first scene.** [`docs/game-design/episode-01/scenes/opening.md`](docs/game-design/episode-01/scenes/opening.md) — Sofi and Pluto arrive at the dish.
4. **Open Unity.** [`apps/game-unity/`](apps/game-unity/) — the grey-box slice is a capsule that walks, a sphere that follows, a switch that turns on a light. That's all. When that feels right, everything else layers on top.

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

The repo is called Rocky for a reason — *Project Hail Mary* got us started. But everything here is written, drawn, and coded by us. No borrowed characters, names, or stories. We love the feeling of finding something and not knowing what it says; we just wanted to make our own version of that feeling.

## Links

- Platform plan: [`docs/initial-planning/game-platform-base-plan_v2.1.md`](docs/initial-planning/game-platform-base-plan_v2.1.md)
- Roadmap: [`docs/game-design/roadmap.md`](docs/game-design/roadmap.md)
- Agent entry point: [`AGENTS.md`](AGENTS.md)

## Contact

- Open a GitHub issue.
- Email: raimonds.krauklis [at] gmail.com
