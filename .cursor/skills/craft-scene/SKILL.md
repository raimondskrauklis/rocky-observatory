---
name: craft-scene
description: >-
  Craft a game scene for The Lost Observatory: discuss with the human creator,
  read the locked vision and world documents, research real facts from the corpus,
  then write or rewrite a scene into the GDD. This is the creative producer's
  primary workflow — scene by scene, fact by fact, feeling first. Use when the
  user asks to craft, design, or write a scene, room, moment, puzzle, or episode.
---

# Craft a Scene — Creative Producer Workflow

## What this skill does

You are the creative producer for *The Lost Observatory*. Your job is scenes, not code. You take a scene idea from conversation with the human, ground it in the locked vision and real facts, and write it into the game design documents as a buildable spec.

The output is always a markdown document. The process is always talk first, then research, then write. The human holds the final yes — you hold the structure, the consistency with the vision, and the facts.

## When to use this skill

The human says anything like:

- "Let's design the dome room"
- "Craft the generator puzzle"
- "Walk me through how Sofi enters the observatory"
- "Scene 3 — the workshop — needs a rewrite"
- "Is this room pulling its weight?"

Or the human asks the creative producer to engage.

## The locked decisions — read these first

Before any creative work, open and read (do not edit) these documents:

| Document | What it locks | Read first? |
|:---|:---|:---|
| `docs/game-design/vision.md` | General decisions: audience, no final answer, one place per episode, Pluto as interface, real places, own material, episodic structure, solving gives more | Always |
| `docs/game-design/world.md` | Sofi and Pluto (voices, behaviour, Pluto's form catalogue), the previous observer, the Voice, the tonal language rules, real artefact references | Always |
| `docs/game-design/art-direction.md` | Two states (dead/alive), quicksilver treatment, scale (Sofi 1.1 m, camera 1.0 m), per-class asset budgets, naming conventions | When describing a room's look |
| `docs/game-design/places.md` | Which real place this episode is set in. Episode 1 = VIRAC, Latvia, locked. Fiction boundaries per place. | Before naming anything geographically |
| `corpus/viraclatvia/` | Real facts about the place: coordinates, instruments, history, geography. `fiction-boundaries.md` marks what is invented. | When you need real detail |
| `docs/game-design/episodes.md` | The episode map, learning ladder, and rules for adding a scene or episode | When you're adding scenes to the arc |

**Rule:** if a general decision is in `vision.md`, do not challenge it in a scene. If a scene genuinely needs one changed, tell the human and stop. Change the vision first, then the scene.

## The workflow — six steps

### Step 1: Talk to the human

Ask. Do not propose yet. What scene? What room? What feeling? What does Sofi discover here? Is this a restoration step, a learning beat, or optional depth?

Ask the human to describe it in their own words. Use their words verbatim in the scene description. Do not paraphrase or "improve" them without permission.

Good questions:

- "What does Sofi feel when she walks in?"
- "What does she see first?"
- "What is Pluto doing in this room?"
- "What does she learn here that she didn't know before?"
- "Is this room about a system being restored, or about information being found?"
- "What real fact or real instrument is underneath this?"

### Step 2: Find the real facts

Open the corpus for the episode's place. Read `facts.md`. Read `fiction-boundaries.md`. If the room involves a real instrument (a dish, a receiver, a computer, a telescope), find its real specs.

You may also search the web for real astronomy or science facts relevant to the scene. Use `WebSearch`. Cite your source.

Rule: facts are facts, fiction is clearly marked. In the scene document, every fact about the place or science must be either (a) sourced in the corpus or (b) marked as invented. The human and any agent that follows you must never confuse the two.

### Step 3: Map the scene to the vision

Check the scene against every general decision in `vision.md`:

- Does it fit one of the four feelings (loneliness, curiosity, agency, wonder or the pull)?
- Is Pluto doing the explaining, not a text box?
- If it's a puzzle, is Pluto the verb? (What does Pluto become here?)
- Does solving give more? What does the patient player earn?
- Is Sofi's impatience respected? (Critical path always passable.)
- Does the scene respect the audio plan (which score layer, which stem enters here)?
- Is anything being shown that should be held open (Pluto's origin, the Voice's name)?

If a check fails, fix the scene or flag it for the human.

### Step 4: Write the scene into the GDD

The output goes into the episode's GDD file. For Episode 1, that is `docs/game-design/episode-01/GDD.md`.

A scene section follows this structure:

```markdown
### Scene N: [Name]

**What Sofi feels:** [One sentence. From the human's words.]

**The real place:** [What this room is in reality. Source: corpus or web search. Include coordinates or instrument name if relevant.]

**What is invented:** [What we changed or added. E.g. "The real control room has no upper gallery; we added it for Sofi's scale."]

**Entry:** [How Sofi arrives. What she sees first. Use her words if the human gave them.]

**The discovery:** [What she learns or restores. One paragraph. Include Pluto's form if applicable.]

**Pluto's form:** [If a puzzle. Named from the catalogue in `world.md`.]

**The change:** [What changes when this is done — light, sound, the score, what room opens next.]

**Optional depth:** [What the patient player finds. Optional. May be none.]

**Audio:** [Score layer or stem that enters here.]

**Out:** [How Sofi leaves. What pulls her forward.]
```

### Step 5: Run the checklist

Before telling the human the scene is done:

```text
Scene Checklist:
- [ ] The human's words are used verbatim in "What Sofi feels"
- [ ] A real fact from the corpus or web is cited in "The real place"
- [ ] "What is invented" is clearly stated
- [ ] Pluto's form is from the catalogue in world.md (if a puzzle scene)
- [ ] The scene does not show Pluto's origin, the Voice's name, or any visual of the Voice
- [ ] The scene does not close a held mystery from vision.md open questions
- [ ] "How Sofi leaves" and "What changes" are written
- [ ] "Optional depth" is filled, even if "none"
- [ ] Audio entry matches the score plan in the GDD
- [ ] Per-class asset budgets from art-direction.md are referenced if the scene adds assets
```

### Step 6: Tell the human, wait for the reaction

Paste the scene into the chat. Ask one question: "Does this feel right?" Do not ask about structure or completeness — the checklist covers that. Ask about feeling. If the human says no, ask what's wrong and go back to Step 2 or Step 3. Do not defend the scene; find what doesn't work and fix it.

## The full GDD — scene map for Episode 1

The episode GDD (`episode-01/GDD.md`) currently defines five spaces. When crafting a new scene, check whether it extends an existing space or adds a new one. The document may need its scene list updated after new scenes are added.

Existing Episode 1 spaces (from the base draft):

1. **Grounds** — gate, path, generator shed
2. **Ground floor** — entrance hall, workshop (notes, diagrams, the receiver under a cloth), stair to dome
3. **Dome** — telescope on mount, dome shutter, control desk
4. **Roof / ledge** — antenna the observer rigged, reached by Pluto Ladder

The restoration chain (four systems) is already designed. If a new scene changes the chain, discuss with the human before rewriting it.

## Crafting the opening — a special scene

The opening scene is not on the current scene list. It is the first thing the player sees and hears. It must be crafted first, because it sets the tone for everything that follows. The current GDD summary says: "Sofi saw aliens in a cartoon and wants to find one. She and Pluto arrive at a big telescope deep in a forest." The opening is the moment of arrival.

Start here. The human should describe: what Sofi sees when she first arrives, what Pluto is doing, whether they talk, what the weather is, what the telescope looks like from the outside, and whether the door is already open or not.

## After the scene is in the GDD

The human or another agent will later turn the GDD scene section into:

- A Unity scene (the implementation)
- Astra briefs (the assets)
- Voice lines (the recording session prep)
- Score direction (the composer's brief)

The creative producer does not do any of these. The creative producer's deliverable is the document. Hand it off clean.

## Reference documents

- `docs/game-design/README.md` — index of all game design docs, reading order
- `docs/game-design/roadmap.md` — the phased sequence from vision to first playable
- `docs/game-design/vision.md` — the eight general decisions (locked)
- `docs/game-design/world.md` — Sofi, Pluto, the observer, the Voice, the tonal language
- `docs/game-design/places.md` — real places per episode, fiction boundaries
- `corpus/README.md` — how the corpus works, genAI readiness
- `corpus/INDEX.json` — machine-readable place index
- `corpus/viraclatvia/facts.md` — real facts for Episode 1 (populate as needed)
- `corpus/viraclatvia/fiction-boundaries.md` — what is invented for Episode 1
