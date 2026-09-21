# docs/game-design/vision.md

# The Lost Observatory — Vision v2

## Status

**Status:** Vision v2 — stage-setting document, not a game design document. Captures the creative direction and the general decisions made on 2026-09-21. Execution planning comes later.

**Supersedes:** `docs/story/the-lost-observatory-vision.md` (v1). What changed is listed at the end.

**Platform companion:** `docs/initial-planning/game-platform-base-plan_v2.1.md`. The platform half of that plan stands. Its "First Product" section describes the v1 game and will become a pointer to this folder.

**Next documents (in order):** `docs/game-design/world.md` (characters, places, the signal language), `docs/game-design/episodes.md` (the episode map), then a GDD for Episode 1.

## One sentence

> A small girl, a quicksilver friend, and a dead observatory that still hears something. Every place they fix points to the next one. The journey does not end.

## What this is

A never-ending exploration series about space and engineering optimism, told one real place at a time. The player is Sofi, a very young, very curious girl. Her companion is Pluto, a being of quicksilver that can take any form. Together they wake abandoned scientific instruments, learn how the universe works from the very basics, and follow a signal that says we are not alone.

It is a learning engine disguised as an adventure. Nothing is presented as a lesson; everything is presented as a locked door, a dark room, or a sound nobody has explained yet.

## The characters

### Sofi

Small, young, active, curious. About seven, first grade; the game never says so. Smart enough to start exploring anything, too impatient to wait for the answer. Enthusiastic, easily excited, talks to Pluto constantly.

Sofi is the player's excuse to start from zero. When she asks "why is it dark?" or "what is that sound?", the game gets to answer from the basics without ever talking down to an adult. Most adults do not know the basics either. Sofi asking is the mechanism that lets everyone learn.

Her impatience is a design tool. She rushes; the player rushes. The game does not punish that. It simply rewards the player who stops and listens with more.

### Pluto

Made of quicksilver. Can take any form: flow through a pipe, walk beside Sofi, fly, become a lens, a bridge, a key, an antenna, a tuning fork that hums a signal back. Pluto is the game's verb set. Most puzzles are some version of "what does Pluto need to become here?"

Pluto is also the patient one. Where Sofi rushes, Pluto waits, listens, and shows. Pluto reads the old notes aloud, turns a diagram into a shape Sofi can walk around, becomes the thing the previous observer was describing. Pluto is how the game explains without text.

Pluto's origin is a held mystery. The early episodes do not explain where Pluto came from. Two readings are kept open on purpose: Pluto is simply Sofi's friend, or Pluto has something to do with the signal. Decide only when a later episode needs it.

### The previous observer

Someone was here decades ago. They heard the signal, tried to answer it, and stopped one step too early. Their notes, calculations, and unfinished work are scattered through every place Sofi visits. Sofi finishes what they started, one instrument at a time.

They are never met. They are the game's second voice, spoken through Pluto.

### The Voice

The source of the signal. Unnamed here. It is never shown. It never gives a final answer. What it gives, each episode, is one more piece of structure: a pattern, a number, a direction, a place to look next.

The Voice is ours. It has its own name (to be chosen by the creator), its own sound, and its own logic. It is not any character from any book or film.

## The feeling loop

Every episode produces the same five feelings, in order:

1. **Loneliness.** A dark, quiet, abandoned place.
2. **Curiosity.** This place was doing something important. What?
3. **Agency.** I can fix this. One system at a time. Every repair is seen and heard.
4. **Wonder.** The instrument wakes. The sky, or the signal, answers with something.
5. **The pull.** The answer points somewhere else. We have to go there.

Feeling five is what v1 did not have. It is what makes the series never-ending instead of finished.

## General decisions

These are the decisions that shape everything downstream. Change them here, not in an episode.

1. **Everyone is the audience. Sofi is the lens.** The game is for anyone who wants to learn something new about space. Sofi's age lets it start from the basics without embarrassment. Text is never required to progress; Pluto shows, the environment shows, sound shows.
2. **Discover from basics.** Counting before primes. Light and shadow before optics. Sound before frequency. Each episode teaches one or two real things properly and assumes nothing.
3. **Solving gives more. Not solving does not punish.** The critical path is always passable. A patient player who decodes, listens, and finishes the observer's work earns more: more notes, more of the language, a fuller sky, a clearer hint about the next place. Difficulty is tuned later; this principle is not.
4. **No final answer.** The Voice is never fully understood. Each episode discovers some knowledge and finds the next instance: a bigger telescope, a radio array, a supercomputer, a space telescope, and someday a ship. The journey is the product.
5. **One place per episode. One episode per release.** Each episode is a small, complete, self-contained location with its own beginning, restoration, and pull forward. This is what keeps the series impressive in scope and small in bytes.
6. **Real science, real artefacts, invented places.** The instruments Sofi wakes are modelled on real ones and the facts are real. The specific place, its story, and its people are ours. Real history is the mystery's raw material; nothing from fiction is.
7. **Pluto is the interface.** Companion, tool, translator, hint system, and narrator. If a mechanic can be expressed as a Pluto form, it should be. This is what keeps the game free of inventory sprawl, dialogue trees, and menus.
8. **Own material only.** Inspired by the feeling of contact stories; built from our own characters, names, sounds, and language. Anything recognisably from a specific book or film is renamed and redesigned before it ships.
9. **Episode 1 is a dream.** Sofi is seven and alone at night because she is dreaming. The frame is not shown in the opening; the ending reveals it when she wakes. One small thing crosses over into the waking world (she is humming the count; "south" is in her notebook in her own handwriting). Pluto is not in her room. Whether Pluto was only a dream is a held question for the series. Later episodes do not replay the frame; the player already understands.
10. **Artefacts are the learning.** Every place is full of things to look at: notes, magazines, plates, charts, mugs. Each one gives a fact or a feeling in one line. Some are keys (a fact opens a lock); most are not, and that is fine. Exploring is never punished and never required; a player who reads everything learns more and gets there first, a player who reads nothing still gets there (Pluto points, eventually). Puzzles have an escape-room flavour: gentle locks, no lockouts, no failure sounds. The facts in artefacts are real; the artefacts are ours.

## The structure: a journey in episodes

### Why episodes

Sofi's story has many scenes and no end. The platform delivers Unity Web builds under a 30–50 MB initial download. Those two facts are reconciled by structure: each episode is one location, one build, one release. Ambition lives in the series; bytes live in the episode.

An episode is also exactly what the platform plan needs to exercise: a versioned artefact, deployed and rolled back by tag, many times. Every episode shipped proves the capacity again.

### The episode template

```text
Arrive         Sofi and Pluto reach a dead place. Something about it is wrong or interesting.
Wake it        Restore one system at a time. Power, then the instrument, then the thing it measures.
Hear it        The instrument catches the signal, or a piece of it. It is structure, not noise.
Learn it       One or two basics, discovered through the place itself. Pluto shows; Sofi tries.
Answer it      Send something back. Silence. Then one more piece of structure comes in.
Follow it      The piece points to the next place. The pull.
```

### Candidate episode map

Not fixed. The order and the places will move as the learning ladder settles.

| Episode | Place (modelled on real artefacts) | What wakes | What Sofi learns |
|:---|:---|:---|:---|
| 1 | A small abandoned optical observatory | Power, dome, telescope, an old receiver | Dark and light; counting; patterns repeat |
| 2 | A radio telescope dish, long silent | The dish, the feed, the recorder | Sound and frequency; the same signal, heard differently |
| 3 | A shut-down supercomputing centre | Cooling, racks, one job left unfinished | Storing, sorting, decoding; what a computer actually does |
| 4 | A great mountain observatory | Mirrors, alignment, the sky at altitude | Optics; why bigger sees further; what stars are |
| 5 | A space telescope, reached somehow | Its instruments, its pointing | Orbits, gravity, distance; light that is very old |
| ... | A ship | | Space travel. The horizon of the series. |

### The learning ladder

Basics first, always. A rough ladder the episodes climb:

- Counting, comparing, patterns that repeat
- Light and dark, shadows, lenses
- Sound, pitch, rhythm, frequency
- Signals: structure versus noise
- Storing and sorting; what computers do
- Optics and telescopes; what a star, a planet, a galaxy is
- Radio; the invisible sky
- Distance, time, and old light
- Orbits and gravity
- Travel

## The signal and the tonal language

The Voice speaks in tones. The language is invented here and belongs to this game.

Basics-first rules, to be refined in `world.md`:

```text
One tone            = one thing / one count
Same tone repeated  = a number (Episode 1: count them)
Rising pitch        = a question
Falling pitch       = a statement
Chord (2–3 tones)   = a concept (later episodes)
Number patterns     = the handshake (counting first; primes when Sofi is ready)
```

Pluto is the tuning fork: Pluto can become a shape that hums a tone, and Sofi can ask Pluto to hum it back to the sky. The player's first "transmission" is Sofi counting out loud and Pluto answering in tone.

Tones are synthesised at runtime, not shipped as audio files. This is thematically right (the Voice is a signal, not a recording) and keeps the language nearly free in bytes.

## Audio is a design input

The adaptive score is the emotional barometer of every episode:

```text
Dead place            → sparse, lonely ambient, quiet piano
First system online   → a quiet rhythm enters
Power spreading       → layers build, one per system restored
Instrument wakes      → the full theme
The answer arrives    → silence, then one clear tone
The pull              → a new, unresolved phrase
```

Layered stems are the single easiest way to break the Web download budget. Audio therefore gets its own budget lines before any music is composed: stem count per episode, format, sample rate, preload versus streamed, and the size ceiling. Sofi's and Pluto's voices are short bark lines or tones, not full voice acting, until an episode proves otherwise.

## Real artefacts, real history

The mystery does not need inventing. Real, public history already contains it:

- A 72-second narrowband signal recorded in 1977, never repeated, never explained, never answered.
- A message humanity sent to the stars in 1974 from a great dish that collapsed in 2020: a real lost observatory.
- Records and plaques sent out on probes, speaking in numbers, hydrogen, and diagrams: real attempts at a universal handshake.
- Space telescopes that see light older than the Earth.

The previous observer's notes can refer to these as facts. The places Sofi visits are inspired by them but are our own. The Voice, and what it says, is fiction of our making.

## Episode 1: what it must be

Episode 1 is the observatory. It is also the platform's M0 and 0.1 release, so it carries a second job: proving the release path.

Release contract sketch (the GDD makes it precise):

- One small location: the observatory and its immediate grounds.
- Sofi walks, looks, interacts. Pluto flows, changes form, talks.
- One restoration chain: power, dome, telescope, receiver.
- One basic or two, learned through the place: dark and light; counting; a pattern that repeats.
- The signal is heard. Sofi and Pluto count it. They answer. Silence. One clear tone comes back, and it points somewhere.
- Clear beginning, restoration, and pull. Roughly 10–15 minutes.
- No login, no payments, no backend needed to play. Local save. Works offline.
- Meets the Web Build Budgets.

The silence before the single returning tone is still the most important second in the game. Everything in Episode 1 is built to earn it. What is new is that the tone does not end the story; it starts the journey.

## Scope contract per episode

### In scope

- One location and its immediate surroundings
- One player controller: walk, look, interact
- One companion with a small set of forms for that episode
- One restoration chain
- One or two basics learned
- One signal event and one pull forward
- Adaptive score within the audio budget
- 10–20 minutes of play
- Offline play, local save, Web build; desktop build as hedge

### Out of scope, for every episode until stated otherwise

```text
Combat
Multiplayer
Procedural worlds
Dialogue trees / other NPCs
Inventory systems (Pluto's forms replace them)
Accounts, leaderboards, economy
Showing the Voice
Explaining Pluto's origin
More than one location per episode
```

## What this means for the platform

Nothing in the platform plan changes shape. A few things get sharper:

- **Episode = release.** The `web` image carries exactly one episode build. Rollback is by tag, as designed.
- **Budgets are per episode**, and audio gets its own lines.
- **Shared systems earn reuse the honest way.** Sofi's controller, Pluto's form system, the tone synthesiser, and the restoration-chain framework are built for Episode 1 and extracted when Episode 2 repeats the need. Same rule as the platform's reuse policy.
- **Offline play stays in force.** The Voice lives in the build, not on the server. Beacons report that an episode loaded, that the instrument woke, and that the tone came back; nothing personal.
- **The desktop hedge** stays. If a later episode's place cannot fit Web, desktop carries it.

## Open questions, held on purpose

Not blocking the world document or Episode 1. Decide when an episode needs them.

- The Voice's name, and who names it.
- Pluto's origin (sharpened by decision 9: was Pluto only a dream?).
- Which small thing crosses over when Sofi wakes: the hummed count, the word in the notebook, or both.
- Sofi's and Pluto's exact voices: a handful of sample lines, then a rule.
- Art style: how stylised, how dark, how the quicksilver reads on Web.
- How much of the previous observer's story is told in Episode 1 versus later.
- Whether the tonal language is ever writable by the player (the "choose" path), and in which episode it first appears.

## What changed from v1

- Protagonist and companion added: Sofi and Pluto. v1 had an unnamed player and no companion.
- The ending is no longer "contact established". There is no final answer. Each episode ends with a pull to the next place.
- Structure is now an explicit episodic series, one real-artefact place per episode, one episode per release.
- "Discover from basics" and "solving gives more, not solving does not punish" added as general decisions.
- Text is no longer the primary carrier of story. Pluto is.
- Audio named as a budget input.
- The Rocky-flavoured reference is dropped; the Voice is our own entity with its own name to come.
- Real history named as the source of the mystery.
- The tonal language starts at counting, not primes.
