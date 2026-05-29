# Manual LoRA Asset Review - 2026-05-29

Reviewed source files:

- `manual_050_candidate_A.png` from `ChatGPT Image May 29, 2026, 06_36_19 PM.png`
- `manual_050_candidate_B.png` from `ChatGPT Image May 29, 2026, 06_36_38 PM.png`
- `manual_044_candidate_A.png` from `ChatGPT Image May 29, 2026, 06_36_13 PM.png`
- `hedra_zip_01.png` through `hedra_zip_04.png` extracted from `hedra_assets_2026-05-29.zip`

## Decisions

| Source | Rating | Destination | Reason |
|---|---:|---|---|
| `manual_050_candidate_A.png` | 9/10 | `assets/jack-training/jack_050.png` | Best counted match for `jack_050`: laughing mouth, eyes scrunched, paws on laptop keys, warm office, no nail defect. |
| `manual_050_candidate_B.png` | 8/10 | `assets/jack-training/_mouth-renders/mouth_050_alt_2026-05-29_A.png` | Good passing mouth/expression render, but duplicate of the `jack_050` slot and weaker hands-on-keys match. Kept as extra mouth render, not counted toward 50. |
| `manual_044_candidate_A.png` | 6/10 | `assets/jack-training/_rejected/manual_044_candidate_A_REJECTED_globe-office-drift.png` | Pose/mug mostly useful, but background includes globe/fancy-library drift. Rejected from counted LoRA set. |
| `hedra_zip_01.png` | 8/10 | `assets/jack-training/jack_049.png` | Good `jack_049`: laughing/chuckling closed-mouth read, pointing off-screen-right, warm office, no nail defect. |
| `hedra_zip_02.png` | 9/10 | `assets/jack-training/jack_048.png` | Strong `jack_048`: laughing/chuckling wide-open mouth, pointing off-screen-right, warm office, no nail defect. |
| `hedra_zip_03.png` | 8/10 | `assets/jack-training/jack_044.png` | Pass for `jack_044`: concerned/skeptical, closed mouth, mug held, warm office, no nail defect. |
| `hedra_zip_04.png` | 8/10 | `assets/jack-training/jack_046.png` | Pass for `jack_046`: head-down exasperated feel, closed mouth, paw on laptop keys, warm office, no nail defect. |

## Dataset Status After Placement

- Counted active PNGs: 29/50
- Counted active TXTs: 29/50
- Extra passing mouth renders: 1
- Rejected manual candidates: 1
