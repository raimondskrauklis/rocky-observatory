# docs/game-design/art-direction.md

# Art Direction — Look, Light, Quicksilver, Budgets

## Status

**Status:** Base draft — needs references from the creator before it can be accepted. Derives from `vision.md` (v2). The budgets here are inputs to `asset-pipeline.md` and to every Astra brief.

**Decides:** the visual language, the dark-to-alive transformation, how Pluto's quicksilver reads on WebGL2, scale conventions, and per-asset-class budgets.

**Does not decide:** how assets are produced (`asset-pipeline.md`) or what is in an episode (GDDs).

## Intent

Two pictures, one place. The same room dead and alive. Everything in the art serves that transformation and the moment the instrument wakes.

The look should feel handmade, warm once alive, and readable at a glance by a six-year-old and by an adult who has never seen a telescope. Not photoreal: photoreal costs bytes, fights the Web budgets, and makes quicksilver look wrong.

## Stylisation level (proposed)

**Proposed:** stylised low-poly with clean silhouettes, flat or lightly gradiented materials, strong shape language, few textures. Detail comes from shape and light, not from texture resolution.

Why: it fits Web budgets by construction; it is the style Astra-authored `bpy` geometry produces most reliably; it makes Pluto's forms readable in silhouette; and it ages well.

**Alternative to weigh:** stylised with hand-painted textures. Warmer, more expensive in bytes and in production time. Decide after references.

## The two states

### Dead

- Palette: cold. Deep blue-greys, dusty slate, near-black shadows. One or two cold accents (moonlight, a status LED that still blinks).
- Light: a single source per space, low, directional. Long shadows. Dust in the beam.
- Sound cue for art: silence with one small mechanical tick somewhere.
- Surfaces: matte, dusty, desaturated.

### Alive

- Palette: warm. Amber, brass, warm white. Cold blues retreat to the windows and the sky.
- Light: many sources, each one tied to a system Sofi restored. Lights come on in the order systems wake.
- Surfaces: the same geometry, now lit; dust reads as texture, not dirt.
- The sky: when the dome opens, the sky is the most saturated thing in the game. It is the payoff.

### The transformation

Every restored system changes light, not geometry. The rule keeps the asset count flat: one set of models, two lighting states, per-system light groups toggled as the chain progresses.

## Quicksilver: how Pluto reads on WebGL2

Real-time reflections are not available on our target (WebGL2, no screen-space reflections at budget). Pluto must look like liquid metal anyway. Options, in order of preference:

1. **Baked reflection probe + high smoothness metallic material (URP).** Cheap, works on WebGL2, looks right in still shots. One probe per room, baked.
2. **Matcap shader.** Cheapest possible; very stable; slightly "painted" look that suits the stylisation. Loses environment-specific reflections.
3. **Hybrid:** matcap base with a subtle baked-probe tint from the room.

**Proposed:** start with option 1; fall back to 3 if probes cost too much in build size or bake time.

Pluto's shape language: smooth, no hard edges, always slightly in motion (a low-amplitude surface ripple in the vertex shader). Form changes are morphs or fast dissolves, not cuts. Pluto's forms must be readable in silhouette against both the dead and alive palettes.

## Scale and camera

- 1 Unity unit = 1 metre. Enforced in the pipeline.
- Sofi is about 1.1 m tall. Camera height follows her eyes (about 1.0 m). Doors, desks, switches, and machines are built for adults, so they loom. This is intended.
- Pluto's default Walker form is about Sofi's height. Reach forms (Ladder, Bridge) scale to the gap.
- Interaction highlights are readable from Sofi's eye height, not an adult's.

## Asset budgets per class

Inputs to every Astra brief. CI enforces the total build budgets (`game-platform-base-plan_v2.1.md`, Web Build Budgets); these per-asset lines exist so the total is met by construction rather than by trimming later.

| Class | Examples | Triangles (max) | Textures | Materials (max) |
|:---|:---|---:|:---|---:|
| Environment module | Wall, floor, ceiling section, stair | 500 | Shared atlas, ≤ 1024² | 1 |
| Set piece | Generator, control desk, telescope mount, dome ring | 3,000 | Shared atlas or 1 × 1024² | 2 |
| Hero prop | The telescope tube, the receiver, the transmitter | 8,000 | 1 × 2048² or 2 × 1024² | 3 |
| Small prop | Switch, lever, note, lamp, mug | 300 | Shared atlas | 1 |
| Sofi | Character with simple rig | 8,000 | 1 × 1024² | 2 |
| Pluto | Base form; per-form variants are morphs or separate low meshes | 4,000 per form | None (material-driven) | 1 |
| Vegetation / exterior | Rocks, grass patches, trees | 400 | Shared atlas | 1 |

Whole-episode ceiling (Episode 1 target): ≤ 400k triangles on screen worst case, ≤ 24 MB of textures compressed, ≤ 40 materials, ≤ 12 real-time lights active at once (baked otherwise).

## Naming and organisation

```text
env_<place>_<part>_<variant>       env_obs_wall_a
set_<place>_<object>                set_obs_generator
hero_<object>                       hero_telescope
prop_<object>_<variant>             prop_switch_a
chr_sofi, chr_pluto_<form>          chr_pluto_ladder
mat_<atlas|object>                  mat_obs_atlas
```

Origins at the base centre for anything placed on a floor; at the pivot for anything that rotates (dome, telescope).

## UI

Almost none. No HUD in normal play. Interaction prompts are diegetic where possible (a glowing edge, Pluto's attention). Text appears only for the version tag, the pause menu, and accessibility options. Font: one, large, high contrast.

## Open questions

- References from the creator: three to five images or words that feel right, and one or two that feel wrong.
- Stylisation choice: low-poly clean vs hand-painted.
- Sofi's design: hair, clothes, colour accent. She must read against both palettes.
- How much exterior is visible in Episode 1 (affects the vegetation and sky budget).
- Whether the sky uses a real star catalogue for constellations (cheap, and honest to decision 6) or a painted skybox.
