# The Lost Observatory — Design Vision

## Status

**Status:** Vision captured — not yet a full game design document

**Game:** The Lost Observatory

**Platform:** Game Platform Base (`observatory.createit.digital`)

**Companion document:** `game-platform-base-plan.md`

## The Vibe

> A small abandoned observatory. A broken telescope. A signal that never got an answer.

This is a game about **space and engineering optimism**: the belief that broken things can be understood, repaired, and made to speak to the sky again.

The player is not a soldier, a racer, or a hero with a weapon. The player is the person who shows up, pays attention, and finishes the work.

## The Feeling We Are Building

The game should produce four feelings in sequence:

1. **Loneliness** — a dark, quiet, abandoned place.
2. **Curiosity** — this place was doing something important. What?
3. **Agency** — I can fix this. One system at a time.
4. **Wonder** — the sky answers.

If a feature does not serve one of these four feelings, it is out of scope.

## The Four Pillars

### 1. Science and wonder

Telescopes, stars, planets, discovery. The game treats real science as the source of magic — frequencies, optics, power systems, signals — not as a textbook. Curiosity is the reward.

### 2. Mystery and exploration

An abandoned place. Hidden logs. An unknown repeating signal. The environment itself is the story: every room answers a question and asks a new one.

### 3. Agency and restoration

Bringing something broken back to life. Every repair is visible and audible: lights flicker on, machinery hums, the dome wakes. Progress is something you *hear* and *see*, not a number on a screen.

### 4. Visual payoff

The sky. The telescope. The reveal. The game earns one great moment and builds everything toward it.

## The Pivot: The Ending Is Contact

The original design ended with power restoration. The real ending is bigger:

> **The ending is not that the telescope turns on. The ending is that the signal gets an answer.**

Gameplay chain:

```text
Restore power
  → receiver wakes
  → a strange tone pattern repeats
  → the player realizes it is structure, not noise
  → decode it (a sequence? a question? a number?)
  → transmit an answer
  → silence...
  → an answer comes back
  → END
```

The silence before the reply is the most important second in the game. Everything is built to earn it.

## The Mystery

Why was the observatory abandoned?

The logs tell the story: someone was here decades ago. They detected the signal. They tried to answer it — and gave up **one step too early**.

The player finds their notes, their calculations, their unfinished transmission. The player completes the work the previous observer could not.

This mirrors the game's own spirit: understanding, patience, and finishing what was started.

## The Tonal Language

Inspired by the idea of an alien language built from music, the game contains a small invented signal language. It must be simple enough to learn inside 10 minutes of play and structured enough to feel real.

Initial rule set (to be refined in design):

```text
Single tone        = a word / a value
Chord (2–3 tones)  = a concept
Rising pitch       = a question
Falling pitch      = a statement
Repetition         = emphasis / urgency
Number sequences   = universal handshake (e.g., primes)
```

Example first contact:

```text
Signal:      2, 3, 5, 7 ... (rising)      → "do you understand numbers?"
Player sends: 11, 13, 17 (falling)        → "yes, we understand"
Answer:      chord + new sequence          → contact established
```

The language belongs to this game. It is invented here, documented here, and owned here.

## The Alien

We do not copy anyone's character. The player of this project — its creator — designs the alien:

- Its name
- Its silhouette and world
- Its voice: which tones, which instruments, which emotional range
- What it is actually saying

The alien may never be shown. A voice made of tones and a story told through logs can be more powerful than any model — and it keeps the scope small.

Design principle: the player falls in love with something they cannot see.

## Adaptive Score

The music follows the restoration. It is the game's emotional barometer:

```text
Observatory dead      → sparse, lonely ambient / quiet piano
First system online   → a quiet rhythm enters
Power spreading       → brass and drums build, layer by layer
Telescope activates   → full triumphant theme
The answer arrives    → silence, then one clear tone
```

The player *feels* themselves getting stronger. The final tone after the answer is the release of everything the score built.

## What This Game Teaches

The game is a learning engine disguised as an adventure:

- **Frequencies and sound** — tone puzzles, signal structure, harmony
- **Patterns and sequences** — primes, progression, encoding and decoding
- **Systems thinking** — power before receiver, receiver before transmitter; dependencies as gameplay
- **Reading an environment** — logs, diagrams, physical clues
- **Optics and astronomy** — alignment, lenses, what a telescope actually does
- **Software craft** — every puzzle is a real Unity system the creator built and can explain

None of this is presented as a lesson. It is presented as a locked door.

## Scope Contract

This game stays small so it can be finished and polished.

### In scope

- One small location: the observatory and its immediate surroundings
- One player controller: walk, look, interact
- One restoration chain: power → receiver → decode → transmit
- One invented tonal language
- One mystery told through logs and environment
- One visual transformation: dark → alive → contact
- 10–15 minutes of play
- Offline play, local save, desktop and web builds

### Out of scope

```text
Combat
Multiplayer
Procedural worlds
Dialogue trees / NPCs
Inventory sprawl
Accounts, leaderboards, economy
Showing the alien (for now)
More than one location
```

## Inspiration and Ownership

This game stands in a long tradition of contact-through-signal stories, from five-tone exchanges in classic cinema to modern science fiction about optimistic engineers. We take the **ideas**: music as language, science as hope, contact as the reward for persistence.

We do not take anyone's **expression**:

- No existing character's name, design, voice, or catchphrases
- No film score or sound design
- No copied story elements, plots, or distinctive scenes
- Asset and music provenance is recorded; only original or properly licensed material ships

The rule: **inspired by the feeling, built from our own material.**

## Open Questions

To be resolved in the game design document:

- What is the exact signal chain puzzle? (How does the player decode — and how hard is it?)
- What does the tonal language sound like? (Which instruments carry the alien's voice?)
- What do the old logs reveal, and in what order?
- Does the player choose the reply, or discover the correct one?
- What is the final image after the answer arrives?
- What is the alien's name — and who names it?

## One Sentence

> A dead observatory, an unfinished message, and the person who finally answers it.
