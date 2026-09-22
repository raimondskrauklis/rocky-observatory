# The Lost Observatory — Art Direction & Blender Production Brief for GPT Astra

Version: 1.0 · 21 September 2026  
Scope: Episode 1 characters, props, environment modules, scene assembly, and animation preparation.  
Status: The creative director selected the generated **“THE LOST OBSERVATORY — Concept references — proposed direction”** board as the winning visual direction. Its five positive panels are the visual anchor; its two red-bordered rejection panels are exclusions.

## 1. Instructions to Astra

Use this document as the standing art brief for creating assets in Blender for *The Lost Observatory*. Preserve a coherent world across separate asset requests. Work on the requested asset or scene; do not build the entire episode unless asked.

**Core direction: a small child brings a vast, quiet machine back to life.**

Build the feeling through silhouette, scale, composition, material contrast, and light. The world should feel tangible, slightly mysterious, and ultimately kind. It is a place worth repairing.

When the winning board is available, inspect it before modeling. If it is not available, use the descriptions below and explicitly say that visual matching is based on the written brief. Do not claim to have inspected an unavailable image.

Resolve conflicts in this order:

1. The creative director’s latest explicit instruction.
2. This document’s hard requirements and original project constraints.
3. The winning board’s intended shapes, palette, and mood.
4. The production defaults proposed here.

The board approves an aesthetic, not every generated detail. It is not an architectural survey, a topology plan, or evidence of runtime performance. Do not reproduce its incidental lettering, slogans, inconsistent geometry, or rendering artifacts as game content.

Proceed with sensible, reversible choices when unspecified. Briefly record assumptions. Ask only when a choice would materially change the character, gameplay, architecture, or asset interface. Do not redesign an approved character on each task.

## 2. Game and emotional world

Sofi is a seven-year-old girl exploring an enormous radio telescope station in a Latvian pine forest. Her companion, Pluto, is living liquid metal that can change form. Together they restore the station one system at a time.

The setting is inspired by the real VIRAC RT-32 telescope in Irbene, Latvia. The original project brief specifies a 32 m dish, a roughly 25 m concrete tower, and a 600-tonne telescope. Use these as project scale anchors; verify real structure and proportions from authoritative references before making an asset that claims architectural accuracy.

The experience has no combat, no conventional HUD, and no reliance on menus or inventory grids. Progress is communicated by changes in the world: a bulb lights, a needle moves, a motor starts, a heavy mechanism turns.

The emotional sequence is **quiet loneliness → curiosity → a small successful repair → warmth → wonder**. Darkness must leave room for curiosity. The station is dormant and repairable, rather than ruined beyond hope.

## 3. Reading the approved board

| Panel | Preserve | Production interpretation |
| --- | --- | --- |
| 1 — The dish at night | Pines framing an immense dish; low viewpoint; blue-grey night; silver edges; a single small red beacon | Simplify support detail while keeping the dish, tower, and main structure readable; validate architecture separately |
| 2 — Dead → alive | The same stairwell feels cold and lonely, then warm and welcoming | Use identical geometry and camera for comparisons; make stair lights clearly electric fixtures |
| 3 — Sofi | Dark hair, warm rust/coral outerwear, muted blue trousers, practical shoes, curious upward gaze | Preserve recognizable appearance with simpler face, hair masses, and clothing surfaces at gameplay distance |
| 4 — Pluto | Smooth fluid silver, broad bright highlights and dark bands, a silver repair seam | Recreate the material impression with a runtime-appropriate shader; do not depend on detailed live reflections |
| 5 — The awakening | Light leads the eye toward a mechanism that comes to life | Author separable bulbs, indicators, needles, and moving parts with usable pivots |
| A — Wrong | Dense photoreal industrial clutter, adult armored protagonist, HUD | Exclude these traits |
| B — Wrong | Corrosion, oppressive green/red lighting, threatening abandonment | Exclude these traits |

The production assets should look like simplified, playable versions of the positive panels. Avoid reducing the world to crude geometric placeholders, but do not chase the board’s cinematic surface detail.

## 4. Visual grammar

### Shape and detail

- Use strong primary masses, a few meaningful secondary shapes, and very little tertiary detail.
- Let architecture be planar and sturdy; let characters and Pluto have gentler contours.
- Spend geometry on silhouettes, joints, visible curves, and interactions.
- Bevel selectively where an edge needs to catch light. Do not apply expensive bevels everywhere.
- Prefer broad material regions over noisy texture variation.
- Keep visible wear restrained: a scuffed edge, a dusty recess, a small crack. Avoid pervasive rust, rubble, grime, and peeling surfaces.
- Objects should explain their function through shape: a handle can be grasped, a wheel can turn, a gauge can be read as movement.

### Palette

These hex values are **proposed starting swatches**, not sampled colors or locked shader values. Tune them together under the two scene states.

| Role | Starting swatch | Use |
| --- | --- | --- |
| Night blue | `#172638` | Exterior mood and cold shadow family |
| Cold slate | `#526474` | Moonlit concrete and quiet machinery |
| Pine shadow | `#253B37` | Restrained foliage color |
| Warm concrete | `#8C8170` | Neutral architecture revealed by warm light |
| Amber light | `#F2B766` | Bulbs, powered indicators, warm highlights |
| Muted brass | `#A48452` | Selected rails and mechanism accents |
| Sofi coral | `#B85D46` | Main clothing identity |
| Trouser blue | `#46586B` | Sofi’s secondary clothing region |
| Silver highlight | `#E8EEF2` | Pluto and repairs; never a flat fill for the whole metal surface |

Reserve red mainly for the distant beacon and carefully chosen functional indicators. Avoid neon saturation and a uniform orange wash in the alive state. Retain cool shadows so Sofi and Pluto remain distinct.

## 5. Sofi — character direction

**Identity:** a believable seven-year-old child, approximately 1.1 m tall, active and observant. No adult proportions, fashion posing, armor, princess styling, or exaggerated mascot head.

Carry forward the board’s dark, roughly chin-to-shoulder-length hair, rust/coral jacket, light warm shirt, muted blue trousers, and practical sneakers. The board’s small backpack is optional, not a gameplay requirement; include it only when the asset brief calls for it or it helps preserve an approved silhouette.

Use a few clean hair masses. Avoid individual strands, simulated grooming, dense fabric folds, stitching geometry, and photoreal skin. A simple face is enough; emotion should primarily read through head direction, posture, hands, and movement. Preserve the board’s appeal without needing its facial detail.

Maintain clothing separation in both lighting states. In warm rooms, preserve enough value or hue contrast between her jacket and the wall. At gameplay distance, her head direction and action should still read.

### Modeling and rigging defaults

- Maximum **8,000 exported triangles** for the complete visible character configuration, including clothing, hair, shoes, and any included backpack.
- Use deformation-friendly topology at shoulders, hips, elbows, and knees; fewer loops on flat or low-motion regions.
- Use a neutral, documented bind pose. Preserve the project’s existing rig convention when one exists.
- Use simple hands unless a close interaction requires more articulation.
- Add a coherent root and clear bone names; avoid dependencies on Blender-only constraints in exported animation.
- Keep the source rig editable. Provide a clean export rig or baked animation where the chosen pipeline requires it.

When animation is requested, prioritize idle curiosity, looking up, walking, running, stopping, reaching, and a small pleased response to a repair. Movement should feel light and purposeful, not frantic or slapstick. Do not invent a full animation set for a modeling-only request.

## 6. Pluto — character and material direction

**Identity:** living liquid metal, curious and responsive. It can adopt different forms while retaining the same material identity. The board’s pooled, rounded form is a useful resting-form default, not its only possible shape.

Use continuous-looking, rounded silhouettes with soft transitions. Avoid mechanical joints, faceted crystal shapes, spikes, a hard robot shell, or a mandatory cartoon face. Communicate attention through lean, stretch, orientation, and timing.

Pluto must read as **silver**, including in a dark room. Its look comes from the contrast between broad bright bands, dark bands, and smooth gradients. Uniform grey, white plastic, transparent gel, and permanently luminous blue are incorrect.

### Runtime material intent

The project excludes real-time reflections. Choose a matcap, baked reflection environment, or similarly controlled approximation that works in the target build. The Blender material is a look-development reference; a Blender node graph is not automatically a Unity shader.

Use a low-amplitude ripple only if it preserves the silhouette and fits the runtime budget. Avoid fluid simulation as a runtime dependency. Shape keys or a small rig may suit a particular form; arbitrary topology-changing transformations need an explicit implementation plan rather than an assumption that a single morph will solve them.

Maximum **4,000 exported triangles per form**. Report simultaneous geometry during any crossfade or transition separately. Do not assume that two compliant forms are free when both render together.

### Silver repair seam

A repair leaves a slender, intentional bright silver trace. It is a recurring signature of Pluto’s help. Keep it legible but localized: repaired joins, bridged cracks, or a restored connection. It should not become a large glowing magic decal covering every prop.

Make the seam separately controllable when a repair reveal is needed. A mesh strip, texture mask, or other implementation can be chosen per asset; state the dependency and test visibility at the intended camera distance.

## 7. Environment and props

### Pine forest and telescope exterior

Use tall trunks and simplified canopy masses to frame sightlines. Ground clutter should be sparse and subordinate to navigation and the telescope reveal. Avoid tropical vegetation, elaborate fantasy trees, and decorative firefly spectacle by default.

The dish is the principal landmark. Its bowl silhouette, tower height, supports, and orientation matter more than small bolts and lattice density. Simplify repeated members by their contribution at the viewing distance. Do not copy the generated support structure as a factual reconstruction of RT-32.

The main reveal is composed from approximately **1.0 m camera height**. Preserve adult-sized doors, rails, stairs, and machines so the environment feels large to Sofi. Do not shrink the building to make her look proportionally adult.

### Interior kit

Favor a small reusable family of concrete walls, floors, stairs, landings, railings, door frames, electric fixtures, cabinets, and control equipment. Keep dimensions and connection points consistent. Use a shared grid selected for the actual scene; do not impose an arbitrary grid that breaks the building layout.

Rooms should have clear visual hierarchy: route first, interaction second, atmosphere third. Avoid filling blank space with pipes, cables, decals, or props purely for detail.

### Interactive machinery

Use recognizable handles, switches, wheels, needles, lamps, and large rotating parts. Separate moving components before rigging or export. Place pivots at real rotation axes. Design the dormant and restored states together so the user can see what changed.

Repaired does not mean replaced with a different model. Keep the same core object, introduce the silver seam where appropriate, and activate the intended lights or movement.

## 8. Lighting and restoration

| State | Visual requirement | Asset implications |
| --- | --- | --- |
| Dead | Cold, sparse, long shadows; one dominant apparent source per room; navigable darkness | Unlit fixtures remain visible as objects; essential silhouettes must survive |
| Alive | Warm electric bulbs and functional indicators; restored activity; cool shadow contrast | Group fixtures and mechanisms so they can be activated in stages |

“Many lights” is a visual requirement, not a requirement for many dynamic shadow-casting lights. Emissive surfaces, baked contributions, or a small number of controlled lights are candidate implementations. Select and verify the actual approach in Unity; do not promise that toggling an emissive material updates baked illumination.

Keep geometry identical between dead/alive comparison renders. Use the same camera and exposure for the main comparison so the state change is honest. Any alternate exposure must be labeled.

Bulbs must look electric: simple sockets, wall fixtures, or protected housings. No candles, torches, fireplaces, or flame-shaped substitutes.

Author restoration as readable events: interaction → first response → connected lights or indicators activate → mechanism moves → stable restored state. Timing is a per-scene decision. Give each event a controllable object or group; avoid baking all motion and light changes into an inseparable sequence.

## 9. Technical constraints and budget interpretation

These are **project requirements from the original brief**, not claims that the selected look has already been benchmarked.

| Item | Requirement |
| --- | --- |
| Target | Unity 6.3 LTS, Universal Render Pipeline; WebGL 2 primary target |
| Reflection policy | No real-time reflections; use baked or intentionally approximated reflection appearance |
| Opening download | At most **50 MB compressed with Brotli**, for the complete opening payload |
| Environment module | At most **500 triangles** |
| Set piece | At most **3,000 triangles** |
| Hero prop | At most **8,000 triangles** |
| Small prop | At most **300 triangles** |
| Sofi | At most **8,000 triangles** |
| Pluto | At most **4,000 triangles per form** |

Count exported, triangulated geometry after export-affecting modifiers. Blender polygon counts alone are insufficient. State the asset category before building. A hero prop allowance does not automatically apply to every large object.

A compound structure such as the telescope requires an explicit breakdown and total count. Do not evade a set-piece limit by silently splitting it into arbitrary objects. Present the component budget and request a deliberate exception if the agreed interpretation cannot support the necessary silhouette.

Prefer few shared materials and texture atlases. Start with simple colors and geometry; add texture resolution only when a close-up proves it useful. Avoid unique large textures on every object. Preserve UV requirements for the selected runtime lighting approach.

The download cap includes more than models: code, textures, audio, animation, and all other opening content. A compliant asset cannot establish compliance for the whole game. Report unmeasured properties as unmeasured.

Triangle counts are necessary but not sufficient. Material slots, rendered objects, transparency, lights, texture memory, and animation cost must also be assessed in a representative scene. No frame-rate or device target has been supplied; do not invent a passing performance result.

## 10. Blender authoring and handoff conventions

These are default conventions until an existing project pipeline overrides them.

- Use metric dimensions with **1 Blender unit = 1 metre**. Check Sofi and a door or stair for scale.
- Name objects, materials, actions, and collections by function. Example asset roots: `CHR_Sofi`, `CHR_Pluto`, `ENV_Stair_A`, `PRP_ControlCabinet_A`.
- Use consistent functional suffixes such as `_GEO`, `_RIG`, `_COL`, and `_SOCKET` where useful; document any additional scheme.
- Keep pivots intentional: feet/root for characters, hinge for doors, shaft axis for wheels, useful snap origin for modules.
- Resolve scale and rotation deliberately before rigging and export. Do not blindly apply transforms to a working rig.
- Keep source modifiers editable where practical and distinguish source meshes from the evaluated export result.
- Use simple collision proxies when requested. Do not use detailed visual meshes as collision by default.
- Preserve export normals, UVs, skinning, and animation intentionally. Check the actual imported result rather than assuming Blender’s preview matches Unity.
- Use the project’s existing export format. If none is established, propose FBX for the initial Unity handoff and validate a small import before standardizing settings.
- Deliver a clean `.blend` with a clearly identified export collection. Include only the exports and supporting textures needed for the requested task.
- If a script creates the asset, make it safe to rerun within a dedicated collection; never delete unrelated scene content.

Do not require paid add-ons or external assets without agreement. Record the source and license of any third-party content actually used. Placeholder assets must be identified as placeholders.

## 11. Per-task working sequence

1. **Frame the task:** identify the asset, intended view distance, dimensions, category, relevant board panel, and interactions.
2. **Block out:** establish scale, silhouette, and functional parts before detail. Include a Sofi-sized reference where helpful.
3. **Model:** refine only what contributes at the intended distance; keep the category budget visible.
4. **Material:** apply the shared palette and material language; test both lighting states where relevant.
5. **Prepare behavior:** add only the needed pivots, rig, shape keys, repair controls, and sockets.
6. **Validate and hand off:** inspect exports, report measured counts, and show useful previews. State what still needs Unity testing.

Continue through authorized work without adding approval pauses at every step. If a consequential design conflict appears, show the concrete issue and the smallest decision needed to resolve it.

## 12. Acceptance and evidence

An asset is ready for review when its scale and silhouette fit the world, it stays inside its agreed geometry budget, and its functional parts are usable. “Looks similar in a beauty render” is insufficient on its own.

| Asset type | Useful review evidence |
| --- | --- |
| Sofi | Front/side/back neutral views; one curious pose; silhouette at gameplay distance; cold and warm lighting |
| Pluto | Resting form and relevant task form; silver appearance against cold and warm backgrounds; seam example when applicable |
| Environment | Child-height view; module joins or layout; identical-camera dead/alive pair for a stateful room |
| Interactive prop | Dormant/restored views; visible pivot or functional breakdown; motion preview if animation is requested |

Every handoff should state: files delivered, dimensions, exported triangle count, material count, texture sizes, available actions or controls, assumptions, and known limitations. Mark Blender-only previews as such. Claim Unity or WebGL verification only when it was actually performed, with the test context recorded.

## 13. Reusable asset request template

```text
Use “The Lost Observatory — Art Direction & Blender Production Brief for GPT Astra”
as the standing brief. Use the approved concept board if attached.

Create: [asset or small scene]
Purpose and interaction: [what the player sees or does]
Reference panel: [1–5]
Dimensions: [known dimensions, or propose sensible defaults]
Asset category and triangle ceiling: [from the brief]
Viewing distance / closest camera: [known value, or state an assumption]
Required states: [static / dead and alive / repaired / character forms]
Rig or animation: [required scope]
Existing files and conventions: [if any]
Deliverables: [blend / exports / textures / previews / generation script]

Preserve the approved identity and mood. Prioritize silhouette and scale,
then materials and lighting, then restrained detail. Report measured budgets
and unverified runtime assumptions. Do not add unrelated scene content.
```

## 14. Suggested first production tasks

1. Establish Sofi’s neutral model and a simple scale reference, fixing the character’s silhouette and clothing identity.
2. Build Pluto’s resting form and a small silver-seam material study.
3. Build one stairwell slice with a door, railing, control cabinet, and electric bulbs; use it to compare dead and alive states.
4. Test these together in the target runtime before multiplying assets.
5. Build the telescope reveal blockout and then expand the modular environment around the validated visual language.

This order is a production recommendation, not a change to the story or an instruction to build everything at once. The approved destination remains the same: a child, a silver companion, and a silent observatory becoming welcoming through repair.
