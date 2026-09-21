# docs/game-design/greybox-slice.md

# Grey-Box Slice — The First Playable Loop

## Status

**Phase 2 of `roadmap.md`.** The smallest possible Unity Web build that proves every technical seam before any art exists. If Sofi and Pluto do not feel right as capsules, nothing else matters and we fix them here.

## What it contains

- One grey-box room in Unity (a floor plane, four walls in crude cubes, a doorway through to a smaller room — the tower base, the generator room, and the stairwell as three connected boxes).
- **Sofi**: a capsule (or cube) that walks (WASD), looks (mouse), and interacts (press E on a switch/object). Moves with a slight bounce in the step. The camera is at exactly 1.0 m above the capsule's feet; it looks up at a tall ceiling.
- **Pluto**: a sphere that smoothly follows Sofi at a small offset. Changes colour or sheen when near an interactable. No form changes yet (sphere only — Puddle/Walker/Lens/Hand/Conductor/Ladder all come when the form system exists).
- **One switch**: a cube on the wall at adult chest height (too high for Sofi's capsule). Pressing E near it does nothing (Sofi is too short).
- **Pluto assist**: when Pluto is near the switch, pressing E causes Pluto to rise to the switch height (a smooth lerp), the switch to flip, and Pluto to return to following position. This is the grey-box version of Pluto-Hand.
- **One light**: a point light in the room, off by default. Flipping the switch turns it on. The room is dark, then lit.
- **The generator room**: a second room behind a doorway. A dark box (generator) and a cable line (line renderer) on the floor. The cable has a visible gap. Walking near the gap with Pluto causes Pluto to stretch across it (Pluto-Conductor grey-box: a stretched sphere or short cylinder). The gap closes (line renderer joins), and a second light turns on in the stairwell.
- **Stairwell**: a tall narrow box with three point lights spaced vertically. They come on bottom-to-top, 0.5 s apart, when the circuit closes. The player sees lights climb.
- **One tone**: an AudioSource that plays a single synthesised tone when the stair lights are all on. A pure sine wave, 440 Hz, 0.5 s, gentle attack/release. This proves the tone synthesiser works.
- **Smoke mode**: append `?smoke=1` to the URL. The game auto-runs: walks to the switch, waits for Pluto assist, flips it, walks to the generator room, waits for Pluto stretch, then walks into the stairwell until the tone plays. Then beacons success to `/api/v1/telemetry` (mock: log to console). If any step times out (5 s per step), it beacons failure.

## What this proves

| Seam | Proved by |
|:---|:---|
| Unity 6.3 project builds for Web | The build. If it doesn't build, nothing else matters. |
| Player controller works at child scale | Sofi capsule moves, the camera is at 1.0 m, the switch is out of reach. |
| Interaction system | E press, proximity check, switch state toggle. |
| Companion system | Pluto follows, reacts to interactable proximity. |
| Pluto assist (form system seed) | Pluto rises to switch, returns. Simple lerp; no forms yet. |
| Pluto stretch (Conductor seed) | Pluto stretches across the cable gap. Line renderer join. |
| Light-state system group | Three groups: room, stairwell. Toggled by events, not by the switch directly. Stair lights have a delayed sequence. |
| Tone synthesis | One tone generates and plays. `AudioSource` + generated `AudioClip` or `OnAudioFilterRead`. |
| Telemetry beacon | HTTP POST fires on smoke completion or timeout. Mock endpoint. |
| Web build budgets baseline | Actual compressed size of a cube scene. Compare to the 30 MB target. |
| The dark → light feeling | It's cubes and a single light, but it should already feel like something. |

## What this does NOT do

- No art assets. No textures. No Blender, no Astra, no GLB import.
- No Pluto forms beyond a stretched/lerped sphere. No Lens, no Puddle, no Ladder.
- No voice. No music stems. The tone is the only audio.
- No real telemetry endpoint. The beacon hits a mock (or a localhost endpoint if available).
- No save/load. No pause menu. No UI beyond the version text (non-intrusive, bottom corner).
- No story. No voice lines. No spider.
- No CI. Local build only. The platform plan's CI build is Phase 5.
- No Docker. No Droplet. No real deploy.

## Files needed (all in `apps/game-unity/Assets/_Game/`)

| File | Type | What it does |
|:---|:---|:---|
| `Scenes/Greybox.unity` | Scene | The grey-box room, switch, light, generator, cable, stairwell, Sofi capsule, Pluto sphere, camera, one AudioSource |
| `Scripts/Player/SimpleController.cs` | MonoBehaviour | WASD movement, mouse look, E interact. Rigidbody + capsule collider. |
| `Scripts/Player/Interactor.cs` | MonoBehaviour | Raycast or trigger check on E press. Calls `IInteractable.Interact()`. |
| `Scripts/Core/IInteractable.cs` | Interface | `void Interact(GameObject actor)`. Switch, generator gap, and any future interactable implement this. |
| `Scripts/Systems/Switch.cs` | MonoBehaviour, IInteractable | Has a `requiresPluto` bool. If true and Pluto not near, no-op. If Pluto near (or not required), toggles a `UnityEvent`. |
| `Scripts/Pluto/PlutoFollower.cs` | MonoBehaviour | Smoothly follows Sofi at an offset. Exposes `isNear(Vector3 target, float range)`. |
| `Scripts/Pluto/PlutoAssist.cs` | MonoBehaviour | On interact near a Pluto-required switch: lerps to switch position, flips it, lerps back. |
| `Scripts/Pluto/PlutoStretch.cs` | MonoBehaviour | On proximity to the cable gap: stretches a mesh (sphere → cylinder) to bridge it. Calls an event on bridge complete. |
| `Scripts/Systems/LightGroup.cs` | MonoBehaviour | Exposes a `TurnOn()` method (and optionally `TurnOff()`). Turns on a list of lights. |
| `Scripts/Systems/LightSequence.cs` | MonoBehaviour | Exposes a `PlaySequence()` method. Turns on lights in a list with configurable delay between each. |
| `Scripts/Audio/TonePlayer.cs` | MonoBehaviour | `PlayTone(float frequency, float duration)`. Generates a sine wave AudioClip at runtime. |
| `Scripts/Core/GameEvents.cs` | ScriptableObject | A shared event bus: `SwitchFlipped`, `CircuitClosed`, `TonePlayed`, `SmokeSuccess`, `SmokeFailure`. One instance, referenced by every script. |
| `Scripts/Telemetry/Beacon.cs` | MonoBehaviour, ISmokeStep | Sends HTTP POST to telemetry endpoint. Mock implementation that logs to console. |
| `Scripts/Core/SmokeRunner.cs` | MonoBehaviour | Reads `?smoke=1` from URL. Runs a list of `ISmokeStep` in sequence. Reports success/failure on timeout. |
| `Scripts/Core/ISmokeStep.cs` | Interface | `IEnumerator RunSmokeStep()`. Each step (walk to switch, flip, walk to gap, bridge, walk to stairwell) is one implementation. |
| `Scripts/Core/VersionDisplay.cs` | MonoBehaviour | Shows version text in bottom corner. Reads from a `version.txt` or hardcoded constant. |

## The scene YAML (rough layout)

```yaml
--- !u!1 &Greybox
GameObjects:
  - name: Room
    children:
      - Floor (Cube, scale 10,0.1,10, dark grey material)
      - Wall_North (Cube, scale 10,3,0.1)
      - Wall_South (Cube, scale 10,3,0.1, with doorway gap)
      - Wall_East (Cube, scale 0.1,3,10)
      - Wall_West (Cube, scale 0.1,3,10)
      - Ceiling (Cube, scale 10,0.1,10)  # optional
  - name: GeneratorRoom
    children:
      - GeneratorBox (Cube, scale 2,1,1, position (3, 0.5, -4))
      - CableLine (LineRenderer from generator along floor to wall, then up)
      - CableGap (empty marker at gap position)
  - name: Stairwell
    children:
      - StairLights (3 point lights at y=1, y=2.5, y=4)
  - name: Sofi
    components: [SimpleController, Interactor, CapsuleCollider, Rigidbody]
    position: (0, 1.0, 5)
  - name: Pluto
    components: [PlutoFollower, PlutoAssist, PlutoStretch]
    position: (1, 1.0, 5)
  - name: Switch
    components: [Switch, BoxCollider (trigger)]
    position: (0, 2.0, -3)  # high on the wall
  - name: MainLight
    components: [Light (Point, off)]
    position: (0, 2.5, 0)
  - name: Managers
    children:
      - GameEvents (ScriptableObject ref)
      - LightGroup_Main (LightGroup, list: MainLight)
      - LightSequence_Stair (LightSequence, list: StairLights)
      - TonePlayer
      - Beacon
      - SmokeRunner
      - VersionDisplay
  - name: Camera
    position: child of Sofi, local (0, 1.0, 0)
```

## Smoke mode steps

1. Move Sofi to Switch position. Wait.
2. Move Pluto to Switch position. Wait.
3. Trigger Switch interact. Wait for SwitchFlipped event.
4. Move Sofi to CableGap position. Wait.
5. Wait for CircuitClosed event.
6. Move Sofi to Stairwell centre. Wait for TonePlayed event.
7. Fire SmokSuccess beacon.

Each step has a 5 s timeout; timeout fires SmokeFailure.

## Tone synthesis approach

Simplest path: `AudioClip.Create` with a generated `float[]` buffer of sine wave samples. A `TonePlayer` MonoBehaviour exposes `PlayTone(float frequency, float duration)`. For the grey-box slice, a single hardcoded call on CircuitClosed: 440 Hz, 0.5 s. Later, a `ToneSynth` ScriptableObject holds the tonal language rules from `world.md` and can play sequences.

## Success criteria

- The scene builds to WebGL and loads in Chrome on the local machine.
- Sofi moves and looks. Pluto follows.
- Approaching the switch with Pluto near, pressing E: Pluto rises, switch flips, room light turns on.
- Walking to the generator room with Pluto: Pluto stretches across the gap, stairwell lights climb bottom to top, tone plays.
- `?smoke=1` in the URL: the whole sequence runs without input and beacons success.
- The whole build compressed is under 10 MB (cubes and a few scripts should be < 2 MB; if it's over 5 MB something is wrong with build settings).

## Open questions

- Unity version: exactly which 6000.3.x patch is installed. Pinned in `ProjectSettings/ProjectVersion.txt`.
- Whether to use URP or Built-in for the grey-box. URP is the plan; if it complicates the Web build, revert to Built-in and note it as a finding.
- Whether the sphere-stretch approach for Pluto bridge is good enough or needs a cylinder mesh swap.