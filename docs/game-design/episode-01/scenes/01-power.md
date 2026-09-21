# docs/game-design/episode-01/scenes/01-power.md

# Scene 1: Power

## Status

**Status:** **Accepted** by the creative director. Spider is a resident (acting deferred); Pluto's material is "liquid metal", never mercury — both recorded in `world.md`. Built deliberately simple: one room, one puzzle with two steps, three light groups, no new controller mechanics.

**Length target:** 2–3 minutes.

## What Sofi feels

Agency, for the first time. Director's words: *"metals conduct electricity and an electric circuit must be closed to work."* She learns this by doing it, in that order: first she makes the generator run and nothing happens; then she understands why; then she closes the loop and the tower wakes up around her.

## The real place

VIRAC's tower is a concrete structure about 25 m tall carrying the 600-tonne RT-32 dish; the site had its own power and technical infrastructure for a base of 2,000 people. When the army withdrew in 1994 the cables were cut and the motors were poured with acid; the antennas were left completely inoperable and were restored by Latvian engineers without documentation. Sources: `corpus/viraclatvia/facts.md` [LP][CW][EVN].

General science used: metals conduct electricity; a circuit must be closed for current to flow. Real mercury ("quicksilver") is a liquid metal that conducts, historically used in tilt switches. The game never says Pluto is mercury; see *What is invented*.

## What is invented

- A **generator room** at the base of the tower, off the corridor at the foot of the stair. The real tower's interior layout is not reproduced; ours is a single room built for a 7-year-old's eye height and a 3-minute scene.
- One cut cable between generator and fuse box. Real history had every cable cut; we use one.
- **Pluto's material.** Director's words: *"quicksilver is metal and conducts electricity. He can pour what is needed and then it grows back to him — not destructible, just changing form and self-repairing."* In the game, quicksilver is our fantasy living metal. It is never called mercury and never linked to real mercury's toxicity. The word "quicksilver" is used as a name, not a chemistry lesson.
- A spider who lives in the generator room. Not a companion (see *Flag*), a resident.

## Entry

Sofi and Pluto come down the last steps of the corridor stair into the base of the tower. Pluto is Walker; the moonbeam from the doorway is behind them now and fading. Pluto's own faint sheen is the only light. Sofi keeps one hand on Pluto's arm.

A door on the left is ajar. Through it, a shape like a sleeping animal: the generator, a big boxy machine with a wheel on its side. Sofi pushes the door. It squeaks, long and high.

> **Sofi:** "Shh. ... Okay it's a machine. Machines don't bite."

The room is small. The generator against the far wall. A grey metal box on the side wall with a big lever on it, at adult chest height, far above Sofi's head. A thick cable runs from the generator along the floor and up the wall to the box, then on out the door and up the stairwell. If Pluto stands near it, the cable glints where the beam falls, so the player can follow it with their eyes: generator → floor → wall → box → door → up.

Pluto Lens is available on the doorway; if the player uses it, moonlight comes in and the cable line is easier to read. Not required.

## The discovery

### Step 1: try, and fail kindly

Sofi goes straight for the lever (impatience). She jumps. Misses. Jumps again.

> **Sofi:** "Pluto. Up. Be a big arm."

**Pluto: Hand.** Pluto stretches one arm up the wall, wraps the lever, and the player holds interact to pull. Sofi hangs off Pluto's arm to add her weight; the lever comes down together.

The generator coughs. Turns. Catches. A low hum fills the room. The wheel spins. One dim bulb above the generator glows orange, wired directly to it.

Nothing else. The stairwell stays black. The lever box stays dead.

> **Sofi:** "It's on! ... Why is it not *on*?"

Pluto ripples once, and the beam from Pluto's sheen slides along the cable on the floor, toward the wall. Pluto is pointing without pointing.

### Step 2: find the break

Halfway up the wall, the cable is cut. Two frayed ends a hand's width apart. Between them, glinting in Pluto's light, a spider's web. The spider sits in the middle of it, very still.

> **Sofi:** "Oh. Hello. You're sitting in the hole."
> **Sofi:** "One, two, three, four, five, six, seven, eight. Eight legs. That's a lot of legs."

The web shows her the gap. (Director: *"some spider is good."* The spider found the break first.)

Sofi looks at the two cable ends. Looks at the hum coming from the generator. Looks at the dead box above. The player can hear her think it: the hum is *here*, the lever is *there*, and there's a hole between.

> **Sofi:** "The electricity can't jump. It needs a road."

### Step 3: close the loop

**Pluto: Conductor.** Player holds interact at the gap with Pluto near. Pluto lifts a finger; the spider walks calmly onto it and is set on the wall beside the box. Then Pluto pours: a thin bright strand flows from Pluto's hand across the gap and joins the two cable ends. Pluto is visibly a little smaller for a moment. Then, over about two seconds, Pluto swells back to full size. The strand stays: a silver seam in the black cable.

Director's words, as the rule: *"he can pour what is needed and then it grows back to him."*

This is the visual motif of the whole episode: **every repair leaves a silver seam.** By the end, the observatory has Pluto's marks all over it.

The loop is closed. Current runs.

## The change

Three light groups, sequenced, all driven by the light-state system with delays. Nothing here needs new code beyond "toggle group N after t seconds".

1. **The lever box** clacks and a green lamp on it lights. The hum deepens.
2. **The stairwell.** Through the door, the bulbs up the spiral stair come on one at a time, bottom to top, about half a second apart. A line of light climbing the tower. Sofi runs to the doorway to watch it go up.
3. **The dish.** Faint, through the tower's outer door at the far end of the corridor: one small red light comes on at the rim of the dish, high up in the dark.

> **Sofi:** "Pluto. Pluto, look. It's got a *light*. It's awake a little bit."

Score: the first layer enters. Low hum pad plus a quiet rhythm, per the GDD plan ("Power: low hum + rhythm"). The loneliness is over; the place has a pulse.

## Pluto's forms

**Hand** (the lever), **Conductor** (the bridge). Both from the Episode 1 catalogue. Lens available but optional.

## Optional depth

- **The spider stays.** It is now on the wall by the box, and it reappears somewhere in every later Episode 1 scene, never with a mechanic, always findable. A player who spots it in every scene gets a line from Sofi at the end. (Name held for the director; Sofi's placeholder is "Eight".)
- **The second cut.** A short dead-end cable in the corner, also cut, going nowhere. Pluto can bridge it; nothing happens; Sofi: "That one didn't need a road." Teaches that a loop has to *go somewhere*, for the player who tries.
- **The observer's second note**, pinned inside the lever box door: a hand-drawn loop — generator, box, lights — with an X where the break is. The observer found this gap too. Pluto cannot read yet; Sofi pockets it.
- **The cable up the stair** is the same one Sofi will follow to the drive room in Scene 2. Seen now, followed later.

## Audio

- Door squeak (long, high, a little funny).
- Generator: cough, catch, idle hum. Hum is a loop that deepens on circuit close.
- Pluto pour: a soft liquid-metal shimmer, synthesised from Pluto's ripple tone.
- Lever box clack. Each stair bulb: a tiny tick. Red dish light: nothing, silence, it is far away.
- Score: first layer enters on the lever-box clack — low hum pad + quiet rhythm.

## Out

Sofi stands in the doorway looking up the lit stair, then back down the corridor at the red dot on the dish.

> **Sofi:** "The lights go up. So we go up."

Pull: the line of bulbs climbing the tower. Scene 2 is the drive room and the dish turning.

## Assets this scene adds

Within `art-direction.md` budgets.

- Set: generator (set piece, ≤ 3,000 tris), lever box with lever and green lamp.
- Small props: cable segments (floor, wall, stair; straight and corner variants), cut cable ends ×2, silver seam (appears), spider web (alpha plane), observer's note.
- Creature: spider (small prop budget, ≤ 300 tris, one idle animation, one walk-onto-finger). First rigged creature in the project; keep it minimal.
- Lights: stair bulbs (one prefab, instanced), red rim light on the dish (emissive swap on the hero asset).
- Pluto forms: Hand, Conductor (the strand as a separate small mesh).

## Flag for the director: the spider as companion

Director's words: *"maybe even a new companion."*

The vision (decision 7, and the scope contract: one companion) makes Pluto the only companion with mechanics; that is what keeps the game free of inventory and menus. I have written the spider as a **recurring resident**: a character, findable in every scene, no mechanics, one payoff line at the end. That gives the warmth of a second friend without a second system.

If you want the spider to *do* things (carry a thread across a gap, show the way), that is a vision change; say so and we update `vision.md` first. My recommendation is resident for Episode 1 and revisit in Episode 2 when we know what Pluto's forms cost to build.

## Checklist

- [x] Director's words used verbatim for the lesson and Pluto's material
- [x] Real facts cited (tower, 1994 cables and acid; metals conduct)
- [x] "What is invented" stated, including the mercury boundary
- [x] Pluto's forms from the catalogue (Hand, Conductor; Lens optional)
- [x] Pluto's origin not shown; the Voice not shown or named
- [x] No held mystery closed
- [x] "The change" and "Out" written; the flow continues without a jump (corridor → generator room → stair)
- [x] Optional depth filled
- [x] Audio matches the GDD score plan (first rhythm layer at Power)
- [x] Asset classes referenced; one new creature flagged as the first rig
