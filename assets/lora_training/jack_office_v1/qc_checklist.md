# Jack Office LoRA V1 QC Checklist

Use this before accepting any generated image into `images/`.

## Per-Image Decision

- `PASS`: strong Jack likeness, usable for LoRA training.
- `FIX_MINOR`: good core image, but needs crop/caption or one targeted regeneration.
- `REJECT_DRIFT`: Jack identity changed too much.
- `REJECT_STYLE`: wrong medium, too realistic, too vector, too generic.
- `REJECT_TECHNICAL`: broken hands/paws, warped face, unreadable/mangled text, bad composition, duplicate.

## Checks

- Does Jack match the master character sheet?
- Is Jack in the Episode 1A office world?
- Is the suit black, shirt white, tie black and skinny?
- Are the paws cartoon dog paws, not human hands?
- Are the eyes, eyebrows, muzzle, ears, nose, and fur silhouette consistent?
- Is the shot meaningfully different from the existing accepted images?
- Does the mouth shape match the planned caption?
- Is there no readable fake text or warped logo?
- Is it useful for training, not just pretty?

## Batch Gate

Do not scale to the next batch unless at least 80 percent of the current batch passes visual QC.
