# docs/game-design/art-direction-prompt.md

# Art Direction Prompt — Find Visual References

## Status

**Purpose:** Give to creative LLMs and human artists as a prompt to find or generate visual references for *The Lost Observatory*. Returned with three to five "this feels right" images and one or two "this is wrong" images. The results go into `art-direction.md` and lock the look.

**How to use:** Paste this whole document into a capable model with web/image search. Say: "Use this as your prompt. Find references. Return images with a one-sentence justification each." For a human artist, replace "find images" with "sketch or describe."

## The game (context)

*The Lost Observatory*, Episode 1. An atmospheric 3D exploration game for everyone, seen through the eyes of a seven-year-old girl named Sofi. Her companion is Pluto, a being made of living liquid metal that can take any form. Together they arrive at a giant radio telescope (RT-32, 32 metres, 600 tonnes) in a pine forest — the real VIRAC station in Irbene, Latvia. The place is dark and broken; Sofi restores it one system at a time. No combat, no menus, no HUD. Feeling first.

## The technical constraints (the LLM needs these)

- Unity 6.3 LTS, Universal Render Pipeline, **WebGL 2 as the primary target**.
- **No real-time reflections** (WebGL2, threading off). Chrome/liquid-metal looks must use baked probes, matcap shaders, or a clever unlit shader.
- **The opening download must be ≤ 50 MB compressed** (Brotli). So: stylised, low polygon count, shared texture atlases, few materials. Detail comes from shape and light, not texture resolution.
- **Two visual states:** dead (cold, dark, one light source per room, long shadows) and alive (warm, many lights, same geometry, different light groups toggled on as systems wake).
- **Sofi is about 1.1 m tall; camera at about 1.0 m.** The world is adult-sized; doors and machines loom. This is a feature, not a bug.
- **Per-asset triangle budgets:** environment modules ≤ 500 tris, set pieces ≤ 3,000, hero props ≤ 8,000, small props ≤ 300, Sofi ≤ 8,000, Pluto ≤ 4,000 per form.

## Scene references needed (what to find)

### 1. The Dish at Night

The hero shot of the episode. A 32-metre radio telescope dish on a 25-metre concrete tower, seen from the forest floor through pines at night. Cold palette: deep blue-greys, moonlight on the metal dish, one small red rim light high up. Stylised low-poly but grand. The feeling: loneliness first, then wonder. This is what Sofi sees when the trees open.

**Reference to find:** A low-poly or stylised large structure seen from a child's low angle, at night, feeling vast and quiet. A radio telescope, a satellite dish, or a similar monumental shape in a forest.

### 2. Dead Interior → Alive

A dark room with a single moonbeam through a door or window, sparse, cold — and the same room lit by many small bulbs climbing a stair, warm amber and brass tones. The transformation is in the light, not the geometry.

**Reference to find:** Two shots of the same stylised interior: one dark and lonely, one warm and lit. A workshop, a control room, or a tower stairwell. Warmth from bulbs, not from fire.

### 3. Sofi

A small girl, about seven. Active, quick, in motion. Bouncing, running, looking up at tall things. Dark hair, warm-coloured clothing that reads against both the cold dead palette and the amber alive palette. Stylised, not photoreal; readable in silhouette. No face detail at game distance.

**Reference to find:** A stylised young girl character, low-poly or cel-shaded, in motion against a dark or forest background. Adventure-game child protagonist, not a princess, not a cartoon mascot with exaggerated features.

### 4. Pluto — Liquid Metal without SSR

A being made of living liquid metal. Reflective, smooth, no hard edges. Reads as chrome or quicksilver without using real-time screen-space reflections. Can be achieved with a baked reflection probe (one per room), a matcap shader sampling a studio environment, or an unlit shader with view-space normals. Always slightly in motion — a low-amplitude surface ripple.

**Reference to find:** A stylised liquid-metal or chrome character or shape in a game or art piece that achieves a reflective look without real-time ray-tracing or SSR. The "Quicksilver" Devpost demo (procedural matcap, Fresnel rim, surface ripple) is one reference; the Argent/Glacé WebGL liquid-metal UI projects are another. Silvery, not grey.

### 5. The Transformation

A system being restored: one light turning on, then a line of lights climbing a stair, then a machine humming. The feeling of agency — I did this. Visible, audible progress without a HUD or a number.

**Reference to find:** A game or film moment where a dark machine or space wakes up step by step — lights climbing, a dial moving, something heavy turning. The lights are the progress bar.

## "This is wrong" references (what to avoid)

- Photorealistic or high-poly AAA game screenshots.
- Dark-horror palettes: gore, dread, jump scares. The game is spooky-but-kind.
- Rusted post-apocalyptic wastelands. Things are broken but repairable. The silver seam motif (Pluto repairs things and leaves a bright mark) is the visual signature.
- Adult protagonists or hero-poses. Sofi is a child exploring, not a soldier or a superhero.
- Busy HUDs, menus, inventory grids, minimaps. The game has almost no UI.

## Search terms (for agents that need them)

Try combinations of:

- `stylized low poly radio telescope night forest Unity URP`
- `dark room moonbeam ambient lighting warm bulbs transformation before after 3D`
- `stylized young girl character low poly adventure game forest`
- `liquid metal chrome character matcap shader low poly Unity WebGL`
- `machine waking up lights turning on one by one 3D game sequence`
- `Quiet Cabin itch.io low poly meditative`
- `Mistwood Cottage day night dynamic Three.js fireflies`
- `Tiny Toybox Games children 3D no reading required`

## What to deliver

Five images (or descriptions) of what feels right, labelled 1–5 in the order above. Two images of what feels wrong. A one-sentence justification per image: what about it works or doesn't.

This goes back to the creative director. When the director says yes, the look is locked and the first Astra briefs can be written.
