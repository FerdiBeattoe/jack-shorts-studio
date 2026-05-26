# Jack Office LoRA V1 Prompt Lock

## Identity Lock

Jack must always match `source_references/jack_character_sheet_master.png`:

- Adult-animation 2D illustration style.
- Golden retriever head with shaggy golden fur, floppy ears, black rounded nose, heavy black eyebrows, half-lidded expressive eyes, cheek/muzzle freckles, and slightly tired account-manager expression.
- Stocky adult proportions, not slim fashion-model proportions.
- Black suit jacket, white slightly rumpled shirt, black skinny tie, black trousers.
- Cartoon dog paws/hands, not human hands.
- Same head shape, muzzle size, ear shape, eyebrow weight, suit silhouette, and black skinny tie feel as the master sheet.

## Episode 1A Setting Lock

Use the Episode 1A anchors as the office continuity source:

- Exact Episode 1A warm office room, not a newly invented executive office.
- Jack is seated behind the same wooden desk.
- Keep the same desk language: white mug, yellow notepad/legal pad, laptop/desk items from the anchors when visible.
- Keep the same warm window/blinds light and background shelf/cabinet continuity from the anchors.
- Keep the same cozy office scale from the anchors; do not turn it into a large luxury corner office or city-window panorama.
- No alternate bookshelf layout, no abstract framed art wall, no monitor wall, no large right-side city window unless it is visible in the anchor being varied.
- No readable fake UI text unless deliberately requested.

## Style Lock

- High-quality 2D adult-animation still frame.
- Clean black linework, simple cel-shaded forms, controlled shadows.
- Do not make Jack photorealistic.
- Do not turn him into a generic dog mascot.
- Do not over-render fabric texture.
- No 3D render, anime sparkle style, painterly realism, plastic toy look, or corporate vector icon look.

## Dataset Rules

- Generate one image at a time.
- QC every image before accepting it into `images/`.
- Bad or drifting outputs go to `qc_rejects/`, never into the accepted dataset.
- Captions must use the trigger token `jack_saas`.
- Keep captions factual and consistent: character, outfit, office, shot type, pose, expression, mouth shape.
- The six Episode 1A images in `source_references/` are accepted anchors and part of the datapack.

## Hard Rejects

- Different dog breed, different face, wrong muzzle, wrong ears, missing eyebrows.
- Human hands instead of cartoon dog paws.
- Wrong outfit, colored tie, missing tie, non-black suit.
- Green/flat reference-sheet background in final office stills.
- Extra characters.
- Readable mangled text on signs, monitors, mugs, or nameplates.
- Photorealistic fabric, hyper-detailed fur, or generic stock business character.
- Severe background drift away from Jack's office.
- Any setting that does not look like it came from the six Episode 1A anchor images.
