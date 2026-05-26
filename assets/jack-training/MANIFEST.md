# Jack LoRA Training Dataset - Generation Manifest

Generated: 2026-05-26T17:26:00+02:00
Total target: 50 images
Total produced: 6/50 active

## Pre-flight check

All pre-flight checks passed: no, continued by explicit user override.

Issues:

- `jack-training-prompts.json` exists and parses cleanly.
- `prompts[]` has exactly 50 entries.
- `assets/jack-reference.png` exists and is readable.
- `assets/jack-training/` exists.
- `scripts/prepare-lora-training.mjs` is readable.
- `scripts/generate-stills.mjs` is readable.
- `codex.cmd --version` works and reports `codex-cli 0.130.0`.
- Plain `codex` is blocked by Windows PowerShell execution policy, so generation used `codex.cmd`.
- `locked_constants` is missing from `jack-training-prompts.json`.
- Many entries have `special_note: null`; user overrode the stop condition.
- Quota for 50-65 image generations cannot be confirmed from this environment.

## Existing image validation (jack_001 to jack_006)

| ID | species | suit | tie | sneakers | office | style | framing | verdict |
|---|---|---|---|---|---|---|---|---|
| jack_001 | pass | pass | pass | n/a | pass warm baseline | pass | pass | KEEP |
| jack_002 | pass | pass | pass | n/a | pass warm baseline | pass | pass | KEEP |
| jack_003 | pass | pass | pass | n/a | pass warm baseline | pass | pass | KEEP |
| jack_004 | pass | pass | pass | n/a | pass warm baseline | pass | pass | KEEP |
| jack_005 | pass | pass | pass | n/a | pass warm baseline | pass | pass | KEEP |
| jack_006 | pass | pass | pass | n/a | pass warm baseline | pass | pass | KEEP |

Regenerated: 0

Caption repair:

- Created `jack_001.txt` through `jack_006.txt` from `prompts[0..5].lora_caption`.

## Generation log (jack_007 to jack_050)

| id | pose | expression | mouth | hands | status | retry_count | failure_reason_if_any |
|---|---|---|---|---|---|---|---|
| jack_007 | front_facing_seated | surprised | wide_open_emphatic | both_paws_on_desk | FAILED_MOVED_OUT | 0 | JSON prompt generated teal open-plan office with dual monitors; diverges from approved warm wood desk/lamp/window baseline in jack_001-jack_006. |

No further images generated.

## Drift observations

Drift detected immediately at `jack_007`.

The generated image follows the JSON's older teal open-plan office wording instead of the six-image approved baseline. This would contaminate the LoRA set because the office setting diverges systematically from `jack_001` and `jack_006`.

Action taken:

- Moved failed `jack_007.png` out of the active dataset to `assets/jack-training/failed/jack_007_failed_wrong_setting.png`.
- Moved failed `jack_007.txt` to `assets/jack-training/failed/jack_007_failed_wrong_setting.txt`.
- Halted generation before producing `jack_008` through `jack_050`.

## Failures

- `jack_007`: wrong setting drift caused by JSON prompt/spec mismatch.

## Final validation

- PNG count: 6/50 active
- TXT count: 6/50 active
- Caption-image mismatches: 0 active filename-pair mismatches
- Caption identity-leak violations: not fully evaluated after halt
- Caption word-count violations: captions are longer than 30 words for some existing entries because they were copied exactly from the JSON as requested

## Costs

- gpt-image-2 calls made: 1
- Estimated quota consumed: 1 image generation
- Wall-clock duration: 00:05

## Next steps for user

1. Decide which setting is canonical:
   - the approved warm wood desk/lamp/window office in `jack_001` to `jack_006`, or
   - the older teal open-plan office described in `jack-training-prompts.json`.
2. Update `jack-training-prompts.json` so every `generation_prompt` matches the canonical setting before generating `jack_007` to `jack_050`.
3. Add or restore the missing top-level `locked_constants` block.
4. Once the JSON and baseline agree, resume from `jack_007`.
5. Once all 50 images are validated, run:
   `npm run prepare-training`
6. Then:
   `npm run hf-upload-dataset`
