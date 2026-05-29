# Jack LoRA Training Dataset - Generation Manifest

Completed: 2026-05-30T01:08:27+02:00
Trigger word: `jacksaas`
Total target: 50 images
Total generated and accepted: 50/50 active
Minimum accepted score: 9.5/10

## Final Validation

- Active PNG count: 50
- Active TXT count: 50
- Active score JSON count: 50
- Every PNG has a matching TXT: yes
- Every PNG has a matching `.score.json`: yes
- Every TXT starts with `jacksaas`: yes
- Active captions containing `hand`, `hands`, `finger`, or `fingers`: 0
- `npm run prepare-training`: pass
- Package written: `dist/jack-training.zip` (161.28 MB)

## Strict Gate

The active dataset now uses the 9.5+ scoring system in `SCORING.md`.

Reject gates applied:

- Wrong character/species or wardrobe
- Office drift, including wrong bookshelf/laptop placement
- Brown paw pads or dark marks on the outside/top of digits
- Human-hand anatomy where dog paws are required
- Wrong target pose, mouth, expression, or action
- Wrong format, text, watermark, UI, or non-9:16 framing

Future generation prompts append the paw lock at generation time:

`Paws: golden fur on all visible surfaces, brown pad markings only on underside when visible, zero nail-like markings.`

## Nail-Defect Fixes

- Known defect fixed: `jack_020`
- Rejected original: `jack_020_REJECTED_reject-gate-brown-paw-pads-rendered-on-outside-of-digits-like-nails.png`
- Accepted replacement: `jack_020.png`, score 9.6
- Additional nail/paw-risk rejections: `jack_008`, `jack_014`, `jack_017`, `jack_018`, `jack_040`, `jack_041`

## Regenerations And Rejections

- Rejected PNG records kept in `_rejected/`: 31
- Review scratch retained in `_generated_review/` for audit only; active training uses root `jack_*.png/.txt/.score.json`.
- User manual candidates below 9.5 were quarantined, not counted.
- Mouth renders that pass are retained under `_mouth-renders/` and are not part of the 50-image requirement.

Notable retries:

- `jack_001`: rejected smirk candidate; accepted closed-neutral deadpan replacement.
- `jack_004`: rejected tired expression; accepted engaged mid-sentence replacement.
- `jack_005`: rejected two sleepy/tired attempts; accepted confident lecture replacement.
- `jack_011`: accepted candidate was pulled back after user caught laptop placement drift; replacement accepted with laptop restored to lower-right foreground.
- `jack_020`: repaired known nail-defect slot.
- `jack_025`: rejected wrong profile direction; replacement accepted.

## Drift Observations

- Canonical office locked to warm wood executive office: golden blinds/window on camera-left, bookshelf on camera-right, dark wood desk, amber lighting, mug/legal pad, and laptop in lower-right foreground when visible.
- Teal/open-plan office and globe/fancy-library variants were rejected.
- Laptop placement was tightened in the generator prompt after `jack_011`.

## Costs

- Estimated image generations/retries consumed: approximately 65-75 image calls, including rejected candidates and timeout completions.
- Wall-clock duration: multi-hour controlled generation and review session ending 2026-05-30T01:08:27+02:00.

## Next Steps

1. `npm run hf-upload-dataset`
2. `npm run train-lora-runpod`
3. Copy `LORA_URL` to `.env`
4. `npm run generate-stills-lora -- --episode=cut_1a`
