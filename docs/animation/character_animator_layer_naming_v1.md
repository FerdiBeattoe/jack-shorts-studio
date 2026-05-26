# Character Animator Layer Naming v1

**Version:** 1.0  
**Target software:** Adobe Character Animator (2022 or later)  
**Date:** 2026-05-19

---

## Naming Rules

1. Group names are case-sensitive. Use exact names as listed — Character Animator recognises specific strings.
2. Spaces in group names are supported. Use them as shown below.
3. Square brackets `[ ]` are used for Character Animator behaviour tags. Include them exactly.
4. All layers inside a tagged group inherit that group's behaviour unless overridden.
5. Every layer and group should have a unique descriptive name — duplicate names cause rigging bugs.
6. Merge duplicate-content layers before importing to Photoshop.

---

## Full PSD Layer Tree

The complete recommended layer order from top to bottom in Photoshop:

```
[Group] Jack                            ← Puppet root. Name this after the character.
│
├── [Group] Head                        ← Face-tracked head group (tag: Face)
│   │
│   ├── [Group] Face                    ← Inner face container
│   │   │
│   │   ├── [Group] Mouth               ← Mouth swap group (CA: Auto Mouth)
│   │   │   ├── [Layer] Neutral         ← Rest / closed
│   │   │   ├── [Layer] Smile           ← Closed smile
│   │   │   ├── [Layer] Smirk           ← One-sided smirk (trigger)
│   │   │   ├── [Layer] Open            ← Wide open (ah/aw)
│   │   │   ├── [Layer] Ee              ← Horizontal wide (ee/ih)
│   │   │   ├── [Layer] Oh              ← Rounded open (oh)
│   │   │   ├── [Layer] Ooh             ← Pursed (oo/w)
│   │   │   ├── [Layer] M B P           ← Lips together
│   │   │   ├── [Layer] F V             ← Lower lip tucked
│   │   │   ├── [Layer] L               ← Tongue tip (l sounds)
│   │   │   └── [Layer] S               ← Teeth together (s/d/t/n)
│   │   │
│   │   ├── [Group] Left Eye            ← CA: left eye group
│   │   │   ├── [Group] Left Upper Lid  ← CA: blink warp target
│   │   │   ├── [Group] Left Lower Lid  ← CA: blink warp target
│   │   │   └── [Layer] Left Pupil      ← CA: eye direction warp layer
│   │   │
│   │   ├── [Group] Right Eye           ← CA: right eye group
│   │   │   ├── [Group] Right Upper Lid ← CA: blink warp target
│   │   │   ├── [Group] Right Lower Lid ← CA: blink warp target
│   │   │   └── [Layer] Right Pupil     ← CA: eye direction warp layer
│   │   │
│   │   ├── [Group] Left Eyebrow        ← CA: warp layer for brow movement
│   │   │   ├── [Layer] LB Neutral      ← Default brow position
│   │   │   ├── [Layer] LB Concerned    ← Furrowed inner brow
│   │   │   ├── [Layer] LB Thinking     ← Raised calculating brow
│   │   │   └── [Layer] LB Smug         ← Arched confident brow
│   │   │
│   │   ├── [Group] Right Eyebrow       ← CA: warp layer for brow movement
│   │   │   ├── [Layer] RB Neutral
│   │   │   ├── [Layer] RB Concerned
│   │   │   ├── [Layer] RB Thinking
│   │   │   └── [Layer] RB Smug
│   │   │
│   │   └── [Layer] Nose                ← Jack's black nose, subtle warp
│   │
│   └── [Layer] Head Base               ← Golden retriever head, ears, fur base
│
├── [Group] Body                        ← Body group (CA: independent physics)
│   │
│   ├── [Group] Right Arm               ← Right arm with tie-fix swap set
│   │   ├── [Group] Arm Resting         ← Default arm position (trigger: arm_rest)
│   │   │   └── [Layer] Right Arm Resting
│   │   └── [Group] Arm Tie Fix         ← Raised tie-fix position (trigger: tie_fix)
│   │       ├── [Layer] Right Arm Raised
│   │       └── [Layer] Right Hand Tie
│   │
│   ├── [Group] Left Arm                ← Left arm (resting only for V1)
│   │   └── [Layer] Left Arm Resting
│   │
│   ├── [Group] Tie                     ← Tie as physics-enabled group
│   │   ├── [Layer] Tie Straight        ← Default, swap for resting
│   │   └── [Layer] Tie Adjusted        ← Post-tie-fix variant (optional)
│   │
│   └── [Layer] Torso                   ← Suit jacket + shirt base
│
└── [Group] Environment                 ← Background (non-puppet, locked)
    ├── [Layer] Desk Foreground         ← Foreground desk layer (optional)
    ├── [Layer] Monitor                 ← Monitor prop layer
    ├── [Layer] Chair                   ← Office chair (behind Jack)
    └── [Layer] Office Background       ← Full office background plate
```

---

## Behaviour Tags Reference

Character Animator reads these group names and applies behaviours automatically:

| Layer / Group Name | CA Behaviour Applied |
|-------------------|---------------------|
| `Head` | Face tracking origin. All face layers must be inside. |
| `Face` | Inner face group. CA applies face-tracking physics to contents. |
| `Left Eye` / `Right Eye` | Eye direction tracking (pupils follow face camera). |
| `Left Upper Lid` / `Left Lower Lid` | Blink warp — CA animates these for eye close/open. |
| `Right Upper Lid` / `Right Lower Lid` | Same, right side. |
| `Left Pupil` / `Right Pupil` | Pupil warp handles for gaze direction. |
| `Left Eyebrow` / `Right Eyebrow` | Brow raise/lower warp based on face tracking. |
| `Mouth` | Lip sync swap group. CA cycles through sublayer names. |
| `Body` | Body tracking origin, independent from face. |

---

## Mouth Layer Names

Character Animator's Auto Mouth behaviour maps phoneme audio to mouth layer names using these exact strings:

| Layer Name in PSD | Phoneme Group | Audio Examples |
|------------------|--------------|----------------|
| `Neutral` | Rest / silence | Pauses between words |
| `Smile` | Smile sound | Soft "ih" with smile |
| `Open` | Open vowels | "ah", "aw" |
| `Ee` | Front vowels | "ee", "ih" |
| `Oh` | Mid-back vowels | "oh", "aw" |
| `Ooh` | Back rounded | "oo", "w" onset |
| `M B P` | Bilabial stops | "m", "b", "p" |
| `F V` | Labiodentals | "f", "v" |
| `L` | Alveolar lateral | "l" |
| `S` | Sibilants | "s", "z", "d", "t", "n" |

> **Note:** `Smirk` is NOT a lip-sync layer — it is a trigger-based expression that overrides the Mouth group. Add it as a separate expression trigger, not inside the Mouth swap group.

---

## Eyebrow Swap Sets

Eyebrow states are trigger-based, not warp-based for V1. Each state is a swap group:

| Group Name | Trigger Key | Used In |
|-----------|------------|---------|
| `LB Neutral` / `RB Neutral` | Default (no trigger) | Shots 02, 07 |
| `LB Concerned` / `RB Concerned` | `concerned` | Shots 01, 03 |
| `LB Thinking` / `RB Thinking` | `thinking` | Shots 01, 04 |
| `LB Smug` / `RB Smug` | `smug` | Shots 04, 05, 06 |

Triggers are set up in Character Animator's Triggers panel. Keyboard shortcuts (0–9) can be assigned for live performance.

---

## Expression Trigger Groups

The following groups in the PSD represent full-face expression swap states. They live outside the standard face layers and are shown/hidden via triggers:

| Trigger Name | Keyboard | Description |
|-------------|----------|-------------|
| `concerned` | Key: 1 | Furrowed brow, eyes slightly wide |
| `thinking` | Key: 2 | One raised brow, eyes narrowed |
| `paranoid` | Key: 3 | Both brows raised, pupils left |
| `smug` | Key: 4 | Arched brow, half-smile |
| `smirk` | Key: 5 | Full smirk expression override |
| `side_eye` | Key: 6 | Eyes turned toward monitor |
| `blink` | Key: B | Full blink (instant) |

---

## Common Mistakes to Avoid

1. **Merged mouth layers** — Every viseme must be its own separate layer inside the Mouth group. If you merge them, CA cannot swap between them.
2. **Flattened eyes** — Eyes must be separate from the head base. A flattened eye becomes a permanent static marking.
3. **Wrong eye naming** — `Left Eye` in Photoshop is Jack's LEFT eye (on the right side of the screen). Character Animator mirrors naming from the character's perspective, not the viewer's.
4. **Missing Neutral mouth layer** — Without a `Neutral` layer, CA has no default mouth position and may hold the last used viseme.
5. **Environment layers inside the puppet group** — Background layers inside the puppet root will be treated as part of the character. Keep them in a separate non-puppet group or import separately.
6. **Tie on body torso** — Tie must be its own group with physics enabled. If merged to the torso, it won't animate independently.
7. **Duplicate layer names** — Any two layers with the same name in the same group will confuse CA's auto-tagging. Always check for duplicates before importing.
