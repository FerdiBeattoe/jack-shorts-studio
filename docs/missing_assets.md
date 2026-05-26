# Missing Assets — Jack Shorts Studio

## Beat 3 (6.8s–11.5s): CRM Monitor Close-up

**Required path:** `public/images/crm_monitor_closeup.png`

**V1 status:** Missing. Beat 3 currently uses `jack_01_forward_calculating.png` as a fallback.

**What this asset should show:** A close-up of Jack's CRM monitor displaying the Doug account timeline — email opened, link clicked, reply received. Matches the script line: "Then the CRM lit up."

**Generation prompt:** See `assets/jack_saas_design_asset_pack_v0_1/.../08_prompts/image_generation/missing_asset_generation_prompts.md`

**To activate when ready:**
1. Generate the image and save to `public/images/crm_monitor_closeup.png`
2. In `src/compositions/doug-ep02/timing.ts`, change beat_03 `image` from:
   `"images/jack_01_forward_calculating.png"`
   to:
   `"images/crm_monitor_closeup.png"`
3. Re-render.

---

## Other V1 Missing Assets (not blocking current render)

These are listed in `assets/.../09_pipeline_specs/asset_manifest.json` as required for future episodes:

- Transparent bust PNGs (5 expressions) — for compositing over backgrounds
- Office background plate (no Jack) — for layered composition
- Desk/monitor foreground plate — for depth layering
- Sales dashboard insert — for B-roll beats
- Caption style templates — for branded caption variants
- Hook card / punchline card / thumbnail templates — for episode branding

None of these are required for the Doug Episode 02 V1 render.

---

## TODO: Caption Map Needs Expansion to Full Voiceover Length

**Issue:** The voiceover MP3 (`doug_episode_02_voice_current.mp3`) is **49.8s** (49.791610s exact, 1494 frames at 30fps). The current caption beat map covers only 0.0s–38.0s. The final visual beat (beat_07) has been extended to 49.8s as a V1 hold, but the caption text "Quietly panicking in business clothes." was written for the 28.5s–38.0s window only.

**Required action:** Transcribe or review the voiceover from 38.0s onwards and add new caption beats in `src/compositions/doug-ep02/timing.ts` to cover the full 49.8s runtime.

**Steps:**
1. Listen to `public/audio/doug_episode_02_voice_current.mp3` from 38s to end.
2. Identify any spoken lines after "Quietly panicking in business clothes."
3. Add new `Beat` entries to `BEATS` array in `timing.ts` with correct `startSeconds`/`endSeconds`.
4. Ensure the last beat's `endSeconds` equals `TOTAL_DURATION_SECONDS` (49.8).
5. Re-render.
