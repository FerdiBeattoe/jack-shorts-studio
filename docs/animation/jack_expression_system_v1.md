# Jack Expression System v1

**Version:** 1.0  
**Date:** 2026-05-19

Jack's emotional range is narrow by design. He is a professional who is barely containing it. Every expression exists on the spectrum between "I have this under control" and "I absolutely do not have this under control."

---

## Expression States

### 1. Neutral
**Trigger key:** default (no trigger)  
**Use case:** Transitions between expressions, brief pauses, professional composure mask.

| Feature | Description |
|---------|-------------|
| Eyebrows | Flat, horizontal, resting. No tension. |
| Eyes | Fully open, looking forward. |
| Mouth | `Neutral` (closed, flat line or very slight downward curve). |
| Notes | Jack's "neutral" reads as slightly tired to the audience. There is no actual rest for Jack. |

---

### 2. Concerned / Calculating
**Trigger key:** `concerned`  
**Episode 02 use:** Shots 01–03 ("Update on the Doug situation." / CRM beat)

| Feature | Description |
|---------|-------------|
| Eyebrows | Both inner brows raised and drawn together, creating a slight furrow between them. |
| Eyes | Wide open. Pupils centered or very slightly upward. |
| Mouth | `Neutral` or `Ee` during speech. Transitions through lip sync. |
| Notes | Jack's default professional expression. Concerned, but professionally so. The face of a man who has sent four follow-up emails and is monitoring the situation. |

---

### 3. Thinking / Problem-Solving
**Trigger key:** `thinking`  
**Episode 02 use:** Shot 01 ("I sent one follow-up email this morning.")

| Feature | Description |
|---------|-------------|
| Eyebrows | Right brow (viewer's left) slightly higher than left. Asymmetric. |
| Eyes | Slightly narrowed. Pupils tracking slightly up-left (looking at mental data). |
| Mouth | `Neutral` baseline. Lip sync as normal during speech. |
| Notes | The face of a man tabulating evidence. Smart-paranoid, not dumb-paranoid. |

---

### 4. Quietly Paranoid
**Trigger key:** `paranoid`  
**Episode 02 use:** Shot 03 (CRM lit up beat — "Email opened. Link clicked. Reply received.")

| Feature | Description |
|---------|-------------|
| Eyebrows | Both brows raised but held steady. Controlled panic. |
| Eyes | Pupils shifted slightly toward the monitor (right from character's perspective). |
| Mouth | Speaking through controlled tension. Normal lip sync, slightly tighter jaw. |
| Notes | Jack has noticed something. He is not reacting visibly to anyone watching. He is reacting internally at maximum volume. |

---

### 5. Controlled Confident Smirk
**Trigger key:** `smug`  
**Episode 02 use:** Shot 04 ("Either Doug is interested...") — building toward punchline

| Feature | Description |
|---------|-------------|
| Eyebrows | Right brow (viewer's left) arched slightly higher. One brow raised. |
| Eyes | Half-open. Controlled. Slightly lidded. |
| Mouth | `Smile` baseline. `Smirk` for emphasis. |
| Notes | Jack has reframed the situation in his favour. Confidence is regained. This is a lie he is telling himself, and it is working. |

---

### 6. Smug Recovery
**Trigger key:** `smug` (same trigger, held expression)  
**Episode 02 use:** Shot 05 ("or Doug is tracking me back.")

| Feature | Description |
|---------|-------------|
| Eyebrows | Same as Controlled Smirk. |
| Eyes | More lidded — approaching half-blink confidence. |
| Mouth | `Smirk` into full `Smile` on punchline delivery. |
| Notes | The punchline landing expression. Jack knows this line is good. He is savouring it. He has rehearsed this observation in the car. |

---

### 7. Side-Eye Toward Monitor
**Trigger key:** `side_eye`  
**Episode 02 use:** Shot 07 ("Jack turns toward monitor.")

| Feature | Description |
|---------|-------------|
| Eyebrows | Neutral, but right brow (viewer's left) very slightly elevated. |
| Eyes | Pupils rotated toward the monitor (character's right / screen left). |
| Mouth | `Neutral` or very gentle `Smile`. |
| Notes | Jack has made a decision. He is done narrating. He is returning to the work. Or he is checking the CRM again. Probably the CRM. |

---

### 8. Blink
**Trigger key:** `blink`  
**Episode 02 use:** Punctuation moments, natural idle behaviour, punchline beats

| Feature | Description |
|---------|-------------|
| Eyebrows | Unchanged from current expression. |
| Eyes | Both upper lids descend to fully closed. Duration: 3–5 frames. |
| Mouth | Unchanged from current lip sync. |
| Notes | Blink should feel natural, not mechanical. Character Animator handles auto-blink from the `Left Upper Lid` / `Right Upper Lid` warp layers. A deliberate slow blink on punchlines reads as withering disdain, which is correct for Jack. |

---

## Expression Transition Map

| From | To | Trigger moment | Feel |
|------|----|---------------|------|
| Neutral | Concerned | Shot 01 open | Immediate, no ease |
| Concerned | Thinking | "I sent one follow-up email" | Subtle 2-frame transition |
| Thinking | Concerned | CRM lights up (shot 03) | Snaps back to concerned |
| Concerned | Smug | "Either Doug is interested" | Deliberate slow ease-in |
| Smug | Smug (held) | Through shots 05, 06 | Hold throughout |
| Smug | Side-eye | Shot 07 turn | Gradual with head turn |

---

## Design Constraint

Jack's expressions are **all in the same territory**. He is a professional. He does not:
- Scream
- Grin wildly
- Cry
- Look directly surprised

All emotions are filtered through the professional mask. The comedy comes from the gap between the surface composure and the internal chaos that is bleeding through the eyebrows.
