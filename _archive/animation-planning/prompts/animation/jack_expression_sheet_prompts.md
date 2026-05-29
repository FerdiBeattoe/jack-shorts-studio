# Jack Expression Sheet Prompts

**Version:** 1.0  
**Date:** 2026-05-19  
**Purpose:** Prompts for generating Jack's facial expression reference sheets.

---

## Base Character Description

Include this in every expression prompt:

```
Humanoid golden retriever, adult male, professional account manager character.
Front-facing head and neck portrait. Golden/amber fur. Black round nose.
Dark thick expressive eyebrows. Dark almond-shaped eyes with warm golden irises.
Floppy golden ears. Anthropomorphic muzzle — readable but not exaggerated.
Black slim-fit suit jacket, white dress shirt, black skinny tie.
Flat 2D illustration style, clean linework, cel shading.
Soft lighting from upper-left. Transparent or clean white background.
```

---

## Warnings

1. **No extreme expressions.** Jack operates in a narrow professional band. Even his most emotional face is filtered through the professional mask.
2. **Same head angle for all expressions.** Front-facing in all cases unless specified.
3. **Mouth is neutral in expression sheets.** The mouth is handled separately by viseme layers. Expression sheets show the eyebrows and eye state only.
4. **Consistency is more important than perfect expression.** It is better to have eight slightly imperfect but stylistically consistent expressions than eight inconsistent ones.

---

## Prompt E1 — Neutral Expression

**File target:** (component of expression reference sheet)

```
[BASE]
Expression: NEUTRAL.
Eyebrows: flat, horizontal, resting. No tension, no raise, no furrow.
Eyes: fully open, pupils centred, looking forward.
Mouth: closed, neutral line (mouth handled separately).
Feel: professional composure. Slightly tired but not showing it.
This is Jack's default state. It reads as professional to colleagues 
and as slightly exhausted to anyone who is paying attention.
```

---

## Prompt E2 — Concerned / Calculating

**File target:** (component of expression reference sheet)

```
[BASE]
Expression: CONCERNED / CALCULATING.
Eyebrows: inner brows raised and drawn slightly together, creating a slight
furrow between them. Not a deep frown — a professional's concern.
Eyes: fully open, slightly widened. Pupils centred.
Mouth: closed (handled by viseme system separately).
Feel: the face of a man reviewing data he did not want to see.
Actively processing information while maintaining professional composure.
This is NOT panic. This is managed concern.
```

---

## Prompt E3 — Thinking / Problem-Solving

**File target:** (component of expression reference sheet)

```
[BASE]
Expression: THINKING / PROBLEM-SOLVING.
Eyebrows: asymmetric — right brow (character's right, viewer's left) 
slightly higher than left. One brow raised, one neutral.
Eyes: very slightly narrowed. Pupils angled very slightly upward-left 
(looking at mental imagery).
Mouth: closed (handled separately).
Feel: active cognition. The face of a man running a mental calculation.
Subtle asymmetry is the key marker — one eyebrow doing more work than the other.
```

---

## Prompt E4 — Quietly Paranoid

**File target:** (component of expression reference sheet)

```
[BASE]
Expression: QUIETLY PARANOID.
Eyebrows: both raised and held there. The raise is controlled — this is not shock, 
this is heightened vigilance being professionally suppressed.
Eyes: slightly wider than normal. Pupils very slightly off-centre — 
fractionally toward the character's right (toward where the monitor would be).
Mouth: closed (handled separately).
Feel: a man who has noticed something and is performing not noticing it.
The internal alarm is at maximum volume. The external display is 3% elevated.
```

---

## Prompt E5 — Controlled Confident Smirk (building)

**File target:** (component of expression reference sheet)

```
[BASE]
Expression: CONTROLLED CONFIDENT SMIRK — building phase.
Eyebrows: right brow (character's right, viewer's left) arched slightly higher — 
a single elevated arch, the other brow resting lower.
Eyes: slightly lidded — the early stage of the "I know something" expression.
Not fully half-lidded yet. Transitional.
Mouth: closed (handled separately — mouth smirk is a separate trigger).
Feel: Jack has reframed the situation in his favour and is about to say something.
```

---

## Prompt E6 — Smug Recovery (held)

**File target:** (component of expression reference sheet)

```
[BASE]
Expression: SMUG RECOVERY — full held smug.
Eyebrows: right brow (character's right, viewer's left) arched high and confident.
Left brow lower, slightly amused.
Eyes: clearly lidded — half-open, deliberate. The gaze of someone choosing 
to be unruffled.
Mouth: closed (handled separately by smirk trigger).
Feel: complete. Jack has delivered the line. He is not breaking character.
This is the expression of a man who made the observation, knew it was good, 
and is now waiting for the reaction.
```

---

## Prompt E7 — Side-Eye Toward Monitor

**File target:** (component of expression reference sheet)

```
[BASE]
Expression: SIDE-EYE TOWARD MONITOR.
Eyebrows: right brow (character's right, viewer's left) very slightly elevated.
Left brow neutral. Asymmetric but subtle.
Eyes: pupils shifted to character's right (viewer's left — toward the monitor).
Not turned dramatically — just a clear leftward glance without moving the head.
White of eye more visible on the left side of each eye.
Mouth: closed (handled separately).
Feel: Jack has decided something. He is redirecting attention to the CRM.
Or he is checking it again. Almost certainly checking it again.
```

---

## Prompt E8 — Blink (mid-blink state)

**File target:** (component of expression reference sheet)

```
[BASE]
Expression: BLINK — mid-blink state (for reference only).
Both upper eyelids descended to approximately 70% closed.
Lower lids unchanged — only upper lids move in a blink.
Eyebrows: unchanged from whatever expression was active before the blink.
For this reference sheet, use neutral brow position.
Mouth: closed (handled separately).
Note: In Character Animator, blink animation is handled automatically 
by the Left Upper Lid and Right Upper Lid warp groups. This image 
is for reference only, not for a puppet layer.
```

---

## Full Expression Reference Sheet Prompt

**File target:** `assets/puppet/refs/jack_expression_reference_sheet.png`

```
A professional character expression reference sheet for an animated character.
Character: humanoid golden retriever, adult male, business professional.
Golden fur, dark eyebrows, black suit. 2D flat illustration style.

Layout: 4×2 grid, 8 expression panels.
Panel labels (left to right, top to bottom):
1. Neutral
2. Concerned
3. Thinking
4. Quietly Paranoid
5. Controlled Smug (building)
6. Smug (held)
7. Side-Eye
8. Blink (mid-blink)

Each panel: same head angle (front-facing), same lighting.
Mouth is neutral/closed in all panels — only eyebrows and eyes change.
Clean sheet background (white or light grey). Professional reference sheet format.
Label each panel with the expression name in small text beneath.
```

---

## QC Checklist

After generating expression layers:
- [ ] All 8 expressions are front-facing at the same angle
- [ ] Eyebrows are the primary differentiator between expressions
- [ ] Eye state (open/lidded/wide) is consistent with the spec
- [ ] No expression has a mouth shape baked in (mouth system is separate)
- [ ] Fur colour matches existing keyframes
- [ ] Style is consistent with existing keyframe assets
