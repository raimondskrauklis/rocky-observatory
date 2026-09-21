# docs/game-design/asset-pipeline.md

# Asset Pipeline — Blender, Astra, Assets as Code

## Status

**Status:** Base draft — iterate. Derives from `vision.md` (v2, decisions 6 and 8) and `art-direction.md` (budgets, naming). ADR candidate: **assets as code**.

**Decides:** how 3D assets are authored, validated, imported into Unity, versioned, and traced.

**Does not decide:** what the assets look like (`art-direction.md`) or which assets an episode needs (GDDs).

## Principle: assets as code

Assets are authored by GPT Astra writing Blender Python (`bpy`) against a brief. Blender executes the script and produces the geometry. Therefore:

- **The script is the source.** It lives in git, is reviewed like code, and can be re-run.
- **`.blend` and `.glb` are build outputs.** Stored in Git LFS for convenience and provenance, regenerable from the script.
- **Budgets are inputs.** Every brief carries the asset-class budget from `art-direction.md`; the validation step measures against it.
- **Provenance is automatic.** Each asset records its brief, script hash, Blender version, and measured budgets.

This is the same posture the platform takes toward everything deployable: versioned, reproducible, rollback-able.

## Tooling

| Tool | Decision | Notes |
|:---|:---|:---|
| Blender | **Pin to the current LTS** (5.2.x at time of writing; verify at pinning) | Same version locally and in any headless run. Record in `tools/blender/BLENDER_VERSION` |
| Astra | Via Codex or ChatGPT, authoring `bpy` scripts from briefs | Astra reasons and writes; Blender builds. Astra is not a mesh generator |
| Blender MCP | Optional | Useful for interactive refinement with screenshots; scripts must still be the saved source |
| Unity import | **GLB via glTFast (proposed)**, FBX as fallback | Astra exports GLB natively; verify glTFast on Unity 6.3 Web before locking. FBX if materials or rigs misbehave |
| Git LFS | `.blend`, `.glb`, `.fbx`, textures | Already in the platform plan's LFS list |

## Repository layout

```text
tools/blender/
├── BLENDER_VERSION
├── briefs/                     # one .md per asset: the brief given to Astra
│   └── hero_telescope.md
├── scripts/                    # one .py per asset (or per family), bpy
│   └── hero_telescope.py
├── lib/                        # shared bpy helpers: materials, naming, export, validation
├── validate.py                 # headless: opens output, measures budgets, writes report
└── manifest/                   # one .json per asset: provenance record
    └── hero_telescope.json

apps/game-unity/Assets/_Game/Art/
├── Models/<class>/             # .glb outputs (LFS)
├── Textures/                   # atlases (LFS)
└── Materials/                  # Unity materials
```

Hand-edited `.blend` files are allowed but change the rules: see *Regeneration rule*.

## Brief template

Every asset starts with a brief. Astra receives the brief plus `art-direction.md` and the shared `lib/` helpers.

```text
Asset:          hero_telescope
Class:          hero prop            → triangles ≤ 8,000; textures ≤ 1×2048² or 2×1024²; materials ≤ 3
Episode:        01
Purpose:        The observatory's main instrument. Rotates on the mount (pivot at mount axis).
Silhouette:     Long tube, counterweight, fork mount. Readable from Sofi's eye height (1.0 m).
Scale:          Tube 4.5 m long, 0.6 m diameter. 1 unit = 1 m.
States:         Dead (dusty, matte) / Alive (same geometry; lighting does the change).
Parts (named):  Telescope_Tube, Telescope_Mount, Telescope_Counterweight, Telescope_Eyepiece
Origin:         At mount rotation axis.
Materials:      mat_brass_worn, mat_paint_cream, mat_glass_dark  (from lib)
Export:         GLB, +Y up, apply modifiers, no cameras/lights, no hidden geometry.
Must not:       Exceed budget; use textures outside the shared atlas without approval; include text.
Reference:      [words or image paths — inspiration, not copying]
```

## Workflow

1. **Brief.** Write `briefs/<asset>.md` from the template. Budget line copied from `art-direction.md`.
2. **Author.** Astra writes `scripts/<asset>.py` using `lib/` helpers. Script must be runnable headless: `blender -b -P scripts/<asset>.py`.
3. **Build.** Run the script. Outputs `.blend` and `.glb` to a staging folder.
4. **Validate.** `validate.py` opens the output and checks: named parts present; triangle count; texture count and sizes; material count; scale and bounds; origin position; no hidden or loose geometry; UVs present where a texture is used; GLB re-imports cleanly into an empty scene.
5. **Review.** Renders from two fixed angles at Sofi's eye height, dead and alive lighting. Human look.
6. **Import.** Copy `.glb` to `apps/game-unity/Assets/_Game/Art/Models/<class>/`. Unity import preset per class (scale 1, read/write off, mesh compression on for Web).
7. **Record.** Write `manifest/<asset>.json`. Commit script, brief, outputs (LFS), manifest together.

## Validation checklist

Copied into `validate.py` as assertions; kept here so humans can read it.

```text
- [ ] All named parts from the brief exist; no extra top-level objects
- [ ] Triangles ≤ class budget
- [ ] Textures ≤ class budget in count and size; all power-of-two
- [ ] Materials ≤ class budget; all from lib or approved in brief
- [ ] Bounds match brief scale within 5 %
- [ ] Origin where the brief says
- [ ] No hidden objects, no loose vertices, no non-manifold edges on hero props
- [ ] UVs present on every textured mesh; no overlapping UVs on atlas users
- [ ] Modifiers applied; no cameras, lights, or empties in the export
- [ ] GLB re-imports into an empty Blender scene with identical part names and dimensions
- [ ] Two review renders produced (dead / alive)
```

## Provenance record

```json
{
  "asset": "hero_telescope",
  "class": "hero",
  "episode": "01",
  "brief": "tools/blender/briefs/hero_telescope.md",
  "script": "tools/blender/scripts/hero_telescope.py",
  "script_sha256": "…",
  "blender_version": "5.2.1",
  "authored_by": "GPT Astra via Codex, session <id or date>",
  "reviewed_by": "<name>",
  "date": "2026-…",
  "measured": { "triangles": 6120, "textures": 1, "materials": 3, "glb_bytes": 412000 },
  "hand_edited": false,
  "license": "original — this project"
}
```

The `license` field is how the ownership rule (`world.md`, Ownership checks) becomes checkable. Anything not `original — this project` needs a licence reference.

## Regeneration rule

- If `hand_edited` is `false`, the script is the source. Change the script, re-run, re-validate.
- If a `.blend` is hand-edited in Blender, set `hand_edited: true`, and the `.blend` becomes the source for that asset. The script is kept as history and no longer regenerates it. Prefer to avoid this for anything but final polish.

## Unity side

- One import preset per asset class; presets in `apps/game-unity/Assets/_Game/Art/ImportPresets/`.
- Mesh compression on; read/write off; generate lightmap UVs only for environment modules.
- Texture import: crunch-compressed for Web; max size per class from `art-direction.md`.
- Pluto's material is Unity-side (probe or matcap shader per `art-direction.md`); Pluto's GLB carries geometry only.
- Addressables group per episode; the first scene stays near-empty (`game-platform-base-plan_v2.1.md`, Web Build Budgets).

## What this pipeline does not cover yet

- Sofi's rig and animation: whether Astra can author a usable rig in `bpy` is unverified. Plan for a hand-made or purchased-and-licensed rig if not; record the licence.
- Audio: separate pipeline; tones are synthesised (`world.md`); music stems follow the audio budget in the GDD.
- Sky: star catalogue vs painted skybox (`art-direction.md`, open questions).

## Open questions

- Confirm glTFast on Unity 6.3 Web, or lock FBX.
- Confirm Blender LTS version at pinning and record it.
- Whether `validate.py` runs in CI (needs headless Blender in the runner; cost and time) or is a local pre-commit step for now. Proposed: local first, CI when the Unity build is in CI.
- Who reviews renders: creator, platform owner, or both.
