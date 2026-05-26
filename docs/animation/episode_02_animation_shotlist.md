# Episode 02 Animation Shotlist

**Episode:** Doug Episode 02 — "The Doug Situation"  
**Total duration:** 49.8s (49.791610s audio, 1494 frames at 30fps)  
**Version:** 1.0  
**Date:** 2026-05-19

---

## Shot Reference

All shots map directly to beats in `src/compositions/doug-ep02/timing.ts`.  
Exported clips land in `public/animation/shot_exports/shot_0N.mp4`.  
Remotion will replace `<Img>` with `<Video>` per shot — see `remotion_animation_integration_plan.md`.

---

## Shot 01 — "Update on the Doug situation."

| Field | Value |
|-------|-------|
| Shot ID | `shot_01` |
| Start | 0.0s |
| End | 2.8s |
| Duration | 2.8s (84 frames) |
| Script line | "Update on the Doug situation." |
| Required expression | `concerned` (brow slightly furrowed, eyes open, forward gaze) |
| Camera angle | Front-facing. Framing: bust shot, head centred. |
| Performance notes | Jack is addressing the audience directly. This is a status update. His tone is controlled but the brow betrays minor stress. No smile. Lip sync: clean open voiceover. |
| Trigger timing | `concerned` fires on frame 1. Hold for full shot. |
| Remotion integration | Replaces `jack_01_forward_calculating.png` in `JackScene`. Ken Burns disabled when video active. |
| Export path | `public/animation/shot_exports/shot_01.mp4` |
| Status | ⬜ Not started |

---

## Shot 02 — "Very normal. Very ethical."

| Field | Value |
|-------|-------|
| Shot ID | `shot_02` |
| Start | 2.8s |
| End | 6.8s |
| Duration | 4.0s (120 frames) |
| Script line | "I sent one follow-up email this morning. Very normal. Very ethical." |
| Required expression | `thinking` into brief `concerned` — the "very normal" delivery is slightly too emphatic |
| Camera angle | Front-facing. Same framing as shot 01. |
| Performance notes | Jack is protesting slightly too much. "Very normal. Very ethical." are two flat, declarative sentences spoken with the energy of a man who has replayed this in his head four times. Brief blink between the two sentences. |
| Trigger timing | `thinking` at 0.0s. Brief blink at "normal." Hold `concerned` from "Very ethical." |
| Remotion integration | Replaces `jack_01_forward_calculating.png`. Same JackScene slot as shot 01 image. |
| Export path | `public/animation/shot_exports/shot_02.mp4` |
| Status | ⬜ Not started |

---

## Shot 03 — CRM reaction beat

| Field | Value |
|-------|-------|
| Shot ID | `shot_03` |
| Start | 6.8s |
| End | 11.5s |
| Duration | 4.7s (141 frames) |
| Script line | "Then the CRM lit up. Email opened. Link clicked. Reply received." |
| Required expression | `paranoid` — controlled shock disguised as professionalism |
| Camera angle | Front-facing with possible slow push-in (Ken Burns zoom-in on face). OR: cut to CRM monitor insert for the "Email opened / Link clicked / Reply received" lines, then back to Jack. |
| Performance notes | The words are delivered with increasing intensity: three short statements building to a crescendo. Jack's pupils should track very slightly toward the monitor on each beat. A suppressed micro-blink between each statement. |
| Trigger timing | `concerned` at 0.0s → `paranoid` on "CRM lit up" → hold through all three sub-beats. |
| Camera / Remotion note | **V1 fallback:** Shot 03 uses `jack_01` still due to missing CRM asset. When `crm_monitor_closeup.png` is available, this shot may be split into 03a (Jack) and 03b (CRM insert). |
| Export path | `public/animation/shot_exports/shot_03.mp4` |
| Status | ⬜ Not started |

---

## Shot 04 — "Either Doug is interested..."

| Field | Value |
|-------|-------|
| Shot ID | `shot_04` |
| Start | 11.5s |
| End | 17.0s |
| Duration | 5.5s (165 frames) |
| Script line | "Which means one of two things. Either Doug is interested..." |
| Required expression | Transition from `paranoid` → `smug`. The tie-fix happens at the top of this shot or just before it. |
| Camera angle | Front or slight 3/4 angle. Jack leans back. The tie-fix is a physical gesture — right arm raises to tie, adjusts, returns. |
| Performance notes | This is the pivot shot. Jack has processed the data. He is now reframing. The tie-fix is his power move — his way of reasserting control. He doesn't rush it. One deliberate tie adjustment, then the statement. |
| Trigger timing | `tie_fix` arm trigger at 0.0s. `smug` expression at approximately 2.0s (after tie settled). |
| Remotion integration | Replaces `jack_02_tie_fix_confident_smirk.png`. This image was specifically the "tie fix" pose — this shot is its animated equivalent. |
| Export path | `public/animation/shot_exports/shot_04.mp4` |
| Status | ⬜ Not started |

---

## Shot 05 — "or Doug is tracking me back."

| Field | Value |
|-------|-------|
| Shot ID | `shot_05` |
| Start | 17.0s |
| End | 21.0s |
| Duration | 4.0s (120 frames) |
| Script line | "or Doug is tracking me back." |
| Required expression | `smug` — confident, leaning into the absurdity with controlled delivery |
| Camera angle | Same framing as shot 04. Jack is still in the lean-back posture. |
| Performance notes | The pause before this line is important. Jack considers this possibility genuinely. He is not ruling it out. His expression says "I have considered this possibility and I respect it." |
| Trigger timing | `smug` held from shot 04. Brief eyebrow micro-raise at "tracking me back." |
| Remotion integration | Replaces `jack_02_tie_fix_confident_smirk.png` (same image as shot 04 in current stills version). |
| Export path | `public/animation/shot_exports/shot_05.mp4` |
| Status | ⬜ Not started |

---

## Shot 06 — "Spiritually? The evidence is overwhelming."

| Field | Value |
|-------|-------|
| Shot ID | `shot_06` |
| Start | 21.0s |
| End | 28.5s |
| Duration | 7.5s (225 frames) |
| Script line | "Can I prove that legally? No. Spiritually? The evidence is overwhelming." |
| Required expression | `smug` → beat pause on "No." → full `smirk` on "Spiritually? The evidence is overwhelming." |
| Camera angle | Front-facing. The "No." pause deserves a full blink — slow, deliberate. |
| Performance notes | This is the joke. The "legally / spiritually" pivot is the central comedic beat of the episode. "Spiritually" deserves a slight eyebrow raise and the `smirk` mouth shape override. The delivery should be unhurried. Jack knows this. |
| Trigger timing | `smug` at 0.0s. `blink` at "No." (slow blink — 8-10 frames). `smirk` trigger at "Spiritually". Hold smirk through "overwhelming." |
| Remotion integration | Replaces `jack_02_tie_fix_confident_smirk.png`. This is the longest held expression in the episode. |
| Export path | `public/animation/shot_exports/shot_06.mp4` |
| Status | ⬜ Not started |

---

## Shot 07 — "Quietly panicking in business clothes."

| Field | Value |
|-------|-------|
| Shot ID | `shot_07` |
| Start | 28.5s |
| End | 49.8s |
| Duration | 21.3s (639 frames) |
| Script line | "So I'm staying calm. Making no sudden movements. And pretending this pipeline isn't negotiating with my nervous system. Account management is mostly trust, timing... and quietly panicking in business clothes." |
| Required expression | Transition from `smug` → `side_eye` toward monitor → gradual return to `neutral` / tired acceptance |
| Camera angle | This shot covers the turn-toward-monitor moment. Physical action: Jack's head or body orientation gradually shifts toward the monitor. |
| Performance notes | The final shot is the longest. It covers the episode conclusion. The punchline "quietly panicking in business clothes" should land on a controlled expression — not laughter, not distress. Just the truth. Delivered professionally. Possibly the saddest and funniest moment of the episode at the same time. |
| Trigger timing | `side_eye` fires at the "turn toward monitor" moment. Final line delivers on near-neutral expression. `blink` optionally on the final beat. |
| Remotion integration | Replaces `jack_03_turning_to_monitor.png`. Extended to 49.8s to match full audio. Caption map needs expansion — see `docs/missing_assets.md`. |
| Export path | `public/animation/shot_exports/shot_07.mp4` |
| Status | ⬜ Not started |

---

## Shot Completeness Summary

| Shot | Status | Fallback Still | Duration |
|------|--------|---------------|----------|
| shot_01 | ⬜ Missing | jack_01_forward_calculating.png | 2.8s |
| shot_02 | ⬜ Missing | jack_01_forward_calculating.png | 4.0s |
| shot_03 | ⬜ Missing | jack_01_forward_calculating.png | 4.7s |
| shot_04 | ⬜ Missing | jack_02_tie_fix_confident_smirk.png | 5.5s |
| shot_05 | ⬜ Missing | jack_02_tie_fix_confident_smirk.png | 4.0s |
| shot_06 | ⬜ Missing | jack_02_tie_fix_confident_smirk.png | 7.5s |
| shot_07 | ⬜ Missing | jack_03_turning_to_monitor.png | 21.3s |

All shots are missing. Current renderer uses fallback stills. This is the intended V1 state.
