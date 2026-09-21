# docs/game-design/episodes.md

# Episodes — The Series Map

## Status

**Status:** Base draft — iterate. Derives from `vision.md` (v2, decisions 4 and 5) and `world.md`. The map is a candidate; the rules for adding an episode are the durable part.

**Decides:** the arc of the series, what each episode contributes, the learning ladder mapping, and how new episodes are added.

**Does not decide:** episode internals (each episode's GDD).

## The arc

No final answer. Each episode: arrive, wake, hear, learn, answer, follow (`vision.md`, the episode template). The Voice gives one more piece of structure per episode; the pieces accumulate into a language. Sofi grows a little each time: more words, more patience, more of the sky.

Three slow threads run under the episodes and are never resolved quickly:

1. **The language.** From counting to a grammar the player can partly read.
2. **The previous observer.** From "they gave up" to "they left a trail on purpose". The turn belongs to a middle episode.
3. **Pluto.** Held open. Small moments that fit both readings (friend / connected to the signal). No episode closes it without a decision in `vision.md`.

## Candidate episode map

See `places.md` for the real-world source of truth on each place. Only Episode 1 (VIRAC) is locked; the rest are candidates.

| Ep | Real place | What wakes | Sofi learns | Pluto's new forms | The Voice gives | The pull |
|:---|:---|:---|:---|:---|:---|:---|
| 1 | **VIRAC, Latvia** | Power, dome, telescope, old receiver | Dark and light; counting; a pattern repeats | Puddle, Walker, Ladder, Hand, Conductor, Lens, Ear, Tuning fork, Diagram | A count; one returning tone on a pitch | The tone matches a frequency written in the observer's notes next to a direction: Lithuania |
| 2 | LY Observatory, Lithuania (candidate) | The telescope drive, the feed, the recorder | Sound and frequency; the same signal heard differently | Flyer, Drum, Mirror | A rhythm: the count now has a beat | A recording that cannot be decoded here; a label pointing to where it could |
| 3 | Tartu Observatory, Estonia (candidate) | Cooling, power, racks, one job left unfinished | Storing, sorting, decoding; what a computer does | Wheel, Map, Key | Structure: the signal is a message with parts | The decoded part is a direction in the sky, too faint for any ground instrument |
| 4 | Mountain observatory, TBD (candidate) | Mirrors, alignment, the sky at altitude | Optics; why bigger sees further; stars vs planets | Chord (first), Bridge (long) | An image: something at the direction | Something is there, but the atmosphere blurs it |
| 5 | Space telescope, TBD (candidate) | Its instruments and pointing (how Sofi gets there is a design question) | Orbits, gravity, distance, old light | Forms in weightlessness | A question, rising: the Voice asks something | To answer, we have to go |
| … | Starbase, TBD (candidate) | | Travel | | | The horizon of the series |

Real-world grounding per episode is listed in `world.md`, Real artefacts.

## Learning ladder, mapped

| Basic | Introduced | Reinforced |
|:---|:---|:---|
| Counting, comparing | 1 | 2, 3 |
| Patterns that repeat | 1 | 2 |
| Dark, light, shadow | 1 | 4 |
| Sound, pitch, rhythm | 2 | 3, 4 |
| Signal vs noise | 2 | 3 |
| Storing, sorting, decoding | 3 | 5 |
| Lenses, mirrors, focus | 1 (Lens form) | 4 |
| What a star is; what a planet is | 4 | 5 |
| Distance and old light | 5 | … |
| Orbits and gravity | 5 | ship |

Rule: an episode introduces at most two basics and reinforces at most two more. If a draft GDD needs more, it is two episodes.

## The language across episodes

| Ep | The player hears | The player does | Grammar unlocked |
|:---|:---|:---|:---|
| 1 | A count, repeated | Counts; Pluto hums it back | Counting |
| 2 | The count with rhythm | Repeats the rhythm on Pluto's Drum | Pause = word end |
| 3 | A message with parts | Sorts the parts | Long pause = message end |
| 4 | Two tones together | Answers with Pluto's Chord | Chord = concept; rising = question |
| 5 | A question | Chooses an answer from what has been learned | First "choose" moment |

The "choose" path (composing freely) appears no earlier than Episode 5, and only over the grammar the player has actually learned. Before that, every answer is discovered.

## Rules for adding an episode

1. One real place, named and located. The place is chosen from `places.md` and given a corpus folder before design begins.
2. One restoration chain, three to five systems.
3. At most two new basics, at most two reinforced.
4. Two to four new Pluto forms, each solving a puzzle in this episode.
5. Exactly one new piece from the Voice, and exactly one pull forward (ideally a real geographical direction).
6. Fits the Web Build Budgets as one release; audio has its own lines.
7. Playable offline; local save; no login.
8. Passes the ownership checks in `world.md`; fiction boundaries per `places.md` and the corpus.

## Reuse gate (platform rule applied to the game)

Sofi's controller, Pluto's form system, the tone synthesiser, the restoration-chain framework, and the light-state system are built for Episode 1. They are extracted into shared packages only when Episode 2 repeats the need, per the platform's reuse policy. Do not build "the episode framework" before Episode 1 exists.

## Open questions

- Confirm or reorder the map. The dish-before-computer order is chosen so "hearing" precedes "decoding"; it could flip.
- The observer's turn: which episode reveals the trail was deliberate.
- How Sofi reaches the space telescope (Episode 5) without breaking the tone. Options: a control room on the ground; a dream; a real launch. This is the series' first big fiction decision.
- Whether episodes share a hub (Sofi's home, a map) or open directly at the next place.
