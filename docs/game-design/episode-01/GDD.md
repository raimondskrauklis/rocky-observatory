# docs/game-design/episode-01/GDD.md

# Episode 1 — The Lost Observatory (Game Design Document)

## Status

**Status:** Base draft — iterate. Derives from `vision.md` (v2), `world.md`, `art-direction.md`, `asset-pipeline.md`, `episodes.md`. This episode is also the platform's **M0** and **0.1** release, so it carries a second job: proving the release path.

**Decides:** the place, the restoration chain, Pluto's forms, the learning beats, the signal event, optional depth, audio plan and budget, asset list, the release contract.

**Not yet decided:** exact puzzle tuning, line-by-line script, final layout dimensions.

### Summary

Sofi saw aliens in a cartoon and wants to find one. She and Pluto arrive at a big telescope deep in a forest (VIRAC, Latvia). It is dark, dusty, and quiet except for one small ticking sound somewhere inside. She restores the power, opens the dome, wakes the telescope, and discovers that an old receiver left behind by someone before her is picking up a signal. The receiver clicks in a repeating pattern. Sofi counts it. Pluto hums it back to the sky as a tone. Silence. One clear tone comes back. Its pitch matches a number in the old notes — and the notes point to another place.

Roughly 10–15 minutes. Sofi starts knowing nothing about radio. She learns counting, shadows, and that telescopes are for looking at space. The facts underneath are real (she is at VIRAC). The wonder is hers.

## Release contract 0.1

Replaces the "First Product" section of `game-platform-base-plan_v2.1.md`.

- Runs from `https://observatory.createit.digital/play/`; hosted on owned DigitalOcean infrastructure; Unity 6.3 LTS.
- Deployable and rollback-able through the platform process as one `web` image.
- No login, payments, or backend dependency for play. Local save (IndexedDB on Web). Offline play.
- Clear beginning, restoration chain, signal event, pull forward. 10–15 minutes.
- Landing, privacy, feedback pages live alongside.
- Version shown non-intrusively. `?smoke=1` reaches the "receiver awake" state and beacons.
- Meets the Web Build Budgets, including the audio lines below.

## The place

VIRAC, Irbene, Latvia — a real radio astronomy centre deep in forest, once a secret Soviet listening post, now a working science site. For Sofi, none of that matters yet. To her, it is simply a place with a telescope. A really big one. And in cartoons, telescopes find aliens. She is here to find one.

The facts (coordinates, instruments, real history) live in `corpus/viraclatvia/`. The game starts with a girl, a quicksilver friend, and a door that won't open. The radio and the signal come later, when she is ready.

```text
Grounds        Gate → path → shed (generator) → main door (tall, heavy)
Ground floor   Entrance hall → workshop (notes, diagrams, the receiver under a cloth)
               → stair to the dome
Dome           Telescope on its mount, dome shutter closed, control desk
Roof / ledge   Reached by Pluto Ladder: the antenna the observer rigged
```

Five spaces. All geometry present from the start; light states change as systems wake (`art-direction.md`, The transformation).

## Restoration chain

**Superseded in part by Scene 0 (accepted).** VIRAC is a radio dish; there is no dome or optical telescope. The chain becomes **power → dish drive (the dish turns) → receiver → antenna**, and is re-crafted scene by scene in `scenes/`. The table below is the pre-VIRAC draft, kept until each row is replaced.

Four systems, in a fixed order the environment teaches. Each one changes the light and adds a layer to the score.

| # | System | The problem Sofi sees | Pluto's form | What wakes |
|:---|:---|:---|:---|:---|
| 1 | Power (`scenes/01-power.md`, accepted) | Generator room at the tower base; lever too high; one cut cable with a spider's web across the gap | Hand (pull the lever together), **Conductor** (pour a strand across the gap; the silver seam stays) | Lever box green; stair bulbs climb the tower one by one; one red light at the dish rim; low hum + first rhythm layer |
| 2 | Dish drive (`scenes/02-dish.md`, accepted) | Drive room (visual only) and control room; the observer's computer wants a two-digit number hidden in a magazine crossword; artefacts help or kindly don't | Ladder (the hatch to the gallery); Pluto reads aloud for the first time | The 600-tonne dish turns; gear wall walks; Sofi watches from the gallery under the sky; strings enter |
| 3 | Telescope | The telescope has no eyepiece; the observer's notes show a lens shape | Diagram (Pluto becomes the shape in the notes so Sofi understands), **Lens** (Pluto becomes the eyepiece) | Sofi sees the sky through it for the first time; the theme swells |
| 4 | Receiver | Under a cloth in the workshop; it clicks faintly; the antenna on the roof is disconnected | Ear (make the faint click loud enough to follow), Ladder (roof), Conductor (reconnect antenna) | The receiver wakes and repeats a count. Score drops to almost nothing |

The order is enforced gently: the dome crank is visible from the start but unreachable in the dark; the telescope is visible but meaningless with the shutter closed; the receiver clicks from the start, but Sofi only follows the sound once the hall is lit and quiet enough.

## Learning beats

Two basics introduced, one reinforced (`episodes.md` rule).

| Basic | Where | How it is taught (no text required) |
|:---|:---|:---|
| Dark and light | Systems 1, 2 | The same rooms, twice. Sofi names it: "It was dark. Now it's not." Shadows move when the dome opens |
| Counting | System 4, the signal | The receiver clicks in groups. Sofi counts aloud. The player repeats the count on Pluto |
| A pattern repeats (reinforced) | Signal | The count comes again. And again. Pluto: "Then it starts again." |

The Lens form quietly seeds optics for Episode 4 without teaching it.

## The signal event

The heart of the episode. Every earlier system exists to make this room quiet enough.

```text
1. Receiver wakes. Clicks in a group: · · ·   (three). Pause. · · · again.
2. Sofi counts. "One, two, three! Three!"  Pluto: "Then it starts again."
3. Player interaction: ask Pluto to become the Tuning fork and hum the count.
   The player taps three times (or holds and releases three times). Wrong counts are simply not answered;
   the receiver keeps repeating, patiently. No fail state.
4. Pluto hums three tones to the antenna. 
5. Silence. The score is gone. Room tone only. Long enough to feel it (target 4–6 s).
6. One clear tone returns. Different timbre from Pluto. The dome lights respond faintly.
7. Sofi: "It heard us."  Pluto, quietly: "Someone was here before us. They heard it too."
8. The tone's pitch matches a number circled in the observer's notes on the desk, next to a direction: south.
9. Sofi: "Where does it go? Can we go there?"  Cut to the version card. Episode ends.
```

The count is three in the base version. Tuning decides if it is three or four; never more than five for a six-year-old.

## Optional depth (solving gives more)

None of this is required to finish. All of it rewards the patient player.

- **Notes.** Six notes are placed. Pluto reads each aloud. Finding all six unlocks a seventh under the receiver cloth: the observer's last line.
- **The scratched count.** Somewhere a wall has tally marks. A player who notices can count them before the receiver ever wakes; Sofi reacts if the player already knows the number.
- **The second pattern.** After the returning tone, if the player waits instead of leaving, a second, longer count comes: a taste of Episode 2. Most players will never hear it. That is fine.
- **Sky.** With the Lens, the player can look at the sky before the receiver is fixed. Nothing is required there; the constellations are simply there.

## Pluto forms in this episode

Puddle, Walker, Hand, Ladder, Conductor, Wheel, Lens, Ear, Tuning fork, Diagram. Ten forms is the ceiling for Episode 1; if the puzzle design wants more, cut a puzzle.

Form selection is contextual: at an interaction point, Pluto offers the one or two forms that could apply. There is no inventory or radial menu of ten forms.

## Controls

- Move, look, interact. One interact button. Hold to ask Pluto.
- Gamepad and keyboard/mouse. Touch is not a gate for Episode 1 (`game-platform-base-plan_v2.1.md`, device matrix).
- No jump, no crouch, no run toggle (Sofi already runs).

## Audio plan and budget

The score follows restoration (`vision.md`, Audio is a design input).

| Layer | Enters at | Notes |
|:---|:---|:---|
| Room tone / ambient | Start | Loop, mono, low bitrate |
| Quiet piano motif | Start | Sparse; the loneliness |
| Low hum + rhythm | Power | |
| Strings | Dome | |
| Full theme | Telescope | |
| Silence | Signal event step 5 | Score stops; only room tone |
| One clear tone | Step 6 | Synthesised, not a file |
| Unresolved phrase | Ending | Short; the pull |

**Budget lines (Episode 1):** ≤ 6 music stems, Vorbis, mono or joint-stereo, 44.1 kHz, ≤ 6 MB compressed total; ambient loops ≤ 1 MB; all tones synthesised at runtime; Sofi and Pluto lines ≤ 40 short clips, ≤ 3 MB total, or text-with-tone if voice recording is not in scope for 0.1. Music streams from Addressables after the first scene.

## Asset list (first Astra briefs)

Per class budgets from `art-direction.md`; pipeline from `asset-pipeline.md`.

| Class | Assets |
|:---|:---|
| Environment modules | Wall, floor, ceiling, stair, dome ring segment, dome shutter segment, path, gate, ground |
| Set pieces | Generator, control desk, workbench, telescope mount, receiver, antenna rig |
| Hero props | Telescope tube |
| Small props | Switch, lever, hand-crank, cable ends, cloth, lamp, notes (6 + 1), mug, tally marks decal |
| Characters | Sofi; Pluto base + 10 form meshes or morphs |
| Sky | Skybox or star field (decision in `art-direction.md`) |

About 45 assets. This is the first real test of the pipeline; expect to revise the briefs after the first ten.

## Technical notes for the Unity project

- Gameplay logic in C# and ScriptableObjects; scenes thin (systems, light groups, interaction points as data). Keeps the project reviewable and agent-friendly.
- The restoration chain is data: a list of systems with prerequisites, light group, score layer, and Pluto forms allowed.
- The light-state system toggles per-system light groups and swaps a small set of emissive materials. No geometry changes.
- Tones from a small synthesiser (`AudioSource` + generated clips or a procedural `OnAudioFilterRead`). Owned by the game, reused by every episode.
- Save: which systems are awake, which notes found, position. Small JSON in `PlayerPrefs`/IndexedDB.
- `?smoke=1`: auto-plays to "receiver awake" and beacons to `/api/v1/telemetry`.
- Beacons (no personal data): episode loaded, each system woke, signal answered, ending reached, fatal error with version and browser family.

## Out of scope for Episode 1

```text
Flyer, Drum, Chord, Mirror, Map, Key forms
Any second location or exterior beyond the grounds
Naming the Voice; explaining Pluto
Voice acting beyond short lines (may be text + tone for 0.1)
Touch controls as a gate
Anything the count-and-answer puzzle does not need
```

## Open questions

- Three or four clicks in the base count.
- Voice lines recorded, or text plus tone, for 0.1.
- Whether the dome opens before or after the telescope gets its Lens (current order: dome first, so moonlight motivates looking).
- How Sofi arrived: shown in a short opening, or simply present at the gate.
- Whether the seventh note reveals anything about Pluto (proposed: no; keep it about the observer).
