# docs/game-design/places.md

# Real Places — The Observatory Network

## Status

**Status:** Base draft — iterate. Derives from `vision.md` (v2, decision 6) and `world.md`. Episode 1 is locked: VIRAC, Latvia.

**Decides:** which real places each episode visits, the approach for the series as a journey through real European and world observatories.

**Does not decide:** what happens inside each place (GDDs).

## Approach

Every episode is set at a real place. The place is named, its geography is real, its instrument is a real type, and the facts about it are real. The story — why it is abandoned, who worked there, what the signal means — is ours.

A creative LLM or agent fed the corpus (`corpus/`) should be able to understand each place before designing its game version. Facts are facts; fiction is clearly marked.

## Episode 1 is locked: VIRAC, Latvia

**VIRAC** (Ventspils International Radio Astronomy Centre) in Irbene, Latvia. A former Soviet military installation turned scientific research centre. It houses two fully steerable parabolic antennas (RT-32 and RT-16), a radio telescope complex, and a satellite laser ranging station. The site is surrounded by forest, remote, and genuinely atmospheric.

In the game: "the observatory" is VIRAC. It is named VIRAC. The geography — the forest, the approach road, the dish silhouettes on the horizon — is real. The interior is our invention based on real antenna control rooms, receiver racks, and Soviet-era scientific workspace.

The corpus for VIRAC goes in `corpus/viraclatvia/`.

## Candidate map (real places)

Only Episode 1 is locked. The rest are candidates the creator ranks, reorders, or replaces.

| Ep | Place | Real instrument | Country | Why it fits the journey |
|:---|:---|:---|:---|:---|
| 1 | **VIRAC** | RT-32 radio antenna + optical | Latvia | A remote forest site with Cold War history; the game's origin |
| 2 | **LY Observatory** (candidate) | Optical telescope, variable star research | Lithuania | A small, historically significant optical site; neighbour to Latvia; the next logical stop |
| 3 | **Tartu Observatory** (candidate) | Old optical + modern instruments; space research | Estonia | The Baltic chain continues; Tartu has a long astronomy tradition and real signal-processing work |
| 4 | **A major mountain observatory** (candidate) | Large optical reflector | TBD | Altitude and atmosphere become the lesson; candidate: Calar Alto (Spain), La Silla (Chile), or another European site |
| 5 | **A space telescope** (candidate) | Orbiting optical / infrared / radio instruments | Space | The horizon: Hubble, JWST, Gaia, or our own invented next-generation instrument |
| — | **Starbase** (candidate) | Launch complex | TBD | The ship; the real place where humanity launches |

Europe-first by default (the series starts in Latvia), opening outward as the signal points further.

## Place categories

Not every real place needs a full episode. Some are referenced, studied, or dreamed about.

- **Playable episode.** Full location, Sofi visits, restoration chain. One per episode.
- **Reference in notes.** Mentioned in the observer's documents. "They built a bigger one in Spain." "The Americans heard it too, in Puerto Rico."
- **Dream / virtual visit.** Reached through a screen, a telescope feed, or Pluto's Diagram form. A way to include NASA, ESA, or a space telescope without Sofi physically travelling there (yet).

## Real facts we use

Every episode draws on public-domain scientific and historical facts about the place:

- What instrument is there (type, aperture, frequency range)
- What it discovered or monitored
- When it was built, by whom, for what purpose
- Its coordinates, altitude, geography
- Real images and diagrams (corpus)

Facts become puzzles. A real dish's actual frequency range becomes the number the Voice transmits on. A real site's latitude becomes the angle Sofi must align the mirror. The game is more honest when the numbers are real.

## Fiction boundaries per episode

| Layer | Real | Ours |
|:---|:---|:---|
| Place name and geography | Real | — |
| Instrument type and capability | Real | — |
| Specific scientific facts used as puzzle meat | Real | — |
| Why it is abandoned in the game world | — | Ours |
| The interior layout (specific rooms, items) | Based on real reference | Ours |
| The previous observer, their notes, their story | — | Ours |
| The signal, the Voice, Pluto | — | Ours |
| Sofi's presence and story | — | Ours |

When a fact is used, source it in the corpus. When something is invented, state it clearly. An agent or creative LLM must never confuse which is which.

## The learning ladder tied to real instruments

Each place teaches what its real instrument actually does, from the very basics.

| Basic | Real instrument that teaches it | Episode |
|:---|:---|:---|
| Counting, patterns | Any receiver counting pulses | 1 |
| Dark and light; lenses | Optical telescope; a dark dome | 1 |
| Sound, frequency, rhythm | Radio dish; the receiver's audio output | 2 |
| Storing, sorting, what a computer does | Data centre / supercomputing cluster | 3 |
| Stars vs planets; galaxies | Large optical reflector; star catalogue | 4 |
| Orbits, gravity, distance | Space telescope data; tracking | 5 |
| Travel | Launch vehicle; orbital mechanics | — |

## Open questions

- Confirm LY Observatory as Episode 2, or replace with another candidate.
- Confirm or reorder the Baltic chain (VIRAC → LY → Tartu) before locking Episode 2.
- Decide which mountain observatory. European (cheaper to visit for reference photos) or world.
- How Sofi reaches Episode 5: a control room on the ground, or a real launch. If a launch, where.
- Whether the series ever leaves Europe, or if the map turns back for reasons the story finds.