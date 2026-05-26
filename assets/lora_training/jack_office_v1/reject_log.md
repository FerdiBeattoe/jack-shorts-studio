# Jack Office LoRA V1 Reject Log

## 2026-05-26 - Batch 01 Wrong Setting

Rejected generated candidates:

- `qc_rejects/wrong_setting_batch_01/jack_office_v1_001.png`
- `qc_rejects/wrong_setting_batch_01/jack_office_v1_002.png`
- `qc_rejects/wrong_setting_batch_01/jack_office_v1_003.png`
- `qc_rejects/wrong_setting_batch_01/jack_office_v1_004.png`

Reason:

- Jack was close enough in some frames, but the setting drifted into a generic warm executive office instead of the exact Episode 1A office layout.
- These images must not be used for LoRA training.

Correction:

- Future generation must use the six Episode 1A frames as the setting lock.
- Generate one test image at a time and reject immediately if desk/window/shelf/layout continuity changes.
