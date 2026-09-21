# corpus/README.md

# Corpus — Real Reference Material for Creative Agents

## Status

**Status:** Structure established. Content to be populated per place as each episode is locked.

**Purpose:** A body of real scientific and historical documentation that an agent, a creative LLM, or a human reads to understand a place before designing its game version. The corpus separates fact from fiction so that creativity builds on truth, not guesswork.

**Relationship to game design:** `docs/game-design/places.md` defines which places belong in which episodes. The corpus holds the source material for each place. A creative LLM is pointed at both: the game design doc says "this is a telescope"; the corpus says "this is the RT-32 at VIRAC: 32-metre diameter, Cassegrain focus, built by the Soviet navy, located at 57°33′N 21°51′E."

## Repository layout

```text
corpus/
├── README.md                     this file
├── INDEX.json                     machine-readable index: places, instruments, basics taught
├── _template/                     empty episode corpus template; copy to start a new episode
├── viraclatvia/                   Episode 1 place
│   ├── README.md                  summary: what VIRAC is, one paragraph
│   ├── facts.md                   factual reference: coordinates, instruments, history, science
│   ├── gallery.md                 links / file references to real images (not stored in the corpus unless public domain)
│   ├── diagrams.md                real technical diagrams, schematics, blueprints referenced
│   └── fiction-boundaries.md      exactly what is invented for the game world vs what is real
├── lyobservatory/                 Episode 2 place (candidate)
├── tartuobservatory/              Episode 3 place (candidate)
└── ...                            one folder per episode, named after the place
```

## INDEX.json — machine-readable

Kept in `corpus/INDEX.json` and updated when a new corpus folder is added. Structure:

```json
{
  "corpus_version": 1,
  "places": [
    {
      "slug": "viraclatvia",
      "episode": 1,
      "name": "VIRAC",
      "full_name": "Ventspils International Radio Astronomy Centre",
      "country": "Latvia",
      "coordinates": { "lat": 57.553, "lon": 21.855 },
      "instruments": ["RT-32 radio antenna", "RT-16 radio antenna", "LSR satellite laser ranging"],
      "basics_taught": ["counting", "dark and light"],
      "status": "locked"
    }
  ]
}
```

Agents consume this file first to know what exists and what to load next.

## Template per place ( `_template/` )

Every corpus folder follows the same structure. The template is the source of truth for what belongs and what does not.

### README.md

One paragraph. What the place is, where, and what it means to the series.

### facts.md

```markdown
## Identity
- Name, full name, location, coordinates, altitude
- Operating organisation, current status, year built

## Instruments
- Name, type, aperture / frequency range, mounting type, year operational
- Real discoveries or monitoring tasks
- Current condition (operational? decommissioned?)

## History
- Why it was built, by whom, for what purpose
- Key events: discoveries, closures, transitions
- Publicly known facts only; no speculation

## Science
- What this instrument measures and how
- Which real phenomena it has observed
- Frequency ranges, resolutions, capabilities

## Geography
- Approach, terrain, climate, seasonal conditions
- Accessibility (how Sofi would actually get there)
```

### gallery.md

Links to public images of the site. No images stored in the corpus unless public domain and small. Reference URLs preferred.

### diagrams.md

Real schematics, block diagrams, antenna patterns, control room layouts. Referenced, not drawn from memory.

### fiction-boundaries.md

A table of "this is real | this is changed | this is ours" for every major element the game uses from this place.

## Rules for the corpus

1. **Facts are real; mark fiction.** Every statement that is invented (the observer, the signal, the abandoned state) must appear in `fiction-boundaries.md` or be explicitly prefixed with "In the game world: …" in any document an agent reads.
2. **No speculation presented as fact.** "The dish was used to track Soviet satellites" is a fact if sourced. "They might have heard the signal in 1987" is fiction unless sourced. If it is ours, say so.
3. **Public sources only.** All facts must be verifiable from public astronomy databases, institutional websites, published papers, or open encyclopaedias. No private communications, no guesswork.
4. **One folder per episode place.** Add to `INDEX.json` when a folder is created. Do not populate a folder until the episode is locked.
5. **The corpus is not the game.** It is reference material for the creative process. Do not copy corpus text directly into game text; adapt it through Sofi's and Pluto's voices.

## GenAI readiness

The corpus exists so that when a creative LLM or coding agent joins the project, it has structured, factual source material to reason from. The structure is simple and consistent so an agent can:

- Read `INDEX.json` → find the right folder.
- Read `facts.md` → know the place.
- Read `fiction-boundaries.md` → know what not to change.
- Read the game design doc for the episode → know what to build.

Temperature, style, and creative voice are the human's domain. The corpus makes sure the facts underneath them are right.

## VIRAC corpus status

The folder `corpus/viraclatvia/` is created. Content to be populated as Episode 1 design progresses. See `docs/game-design/places.md` for the Episode 1 lock.