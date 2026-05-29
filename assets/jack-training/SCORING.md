# Jack LoRA Scoring System

Active LoRA slots require a score of `9.5/10` or higher. Anything lower stays in review, goes to `_mouth-renders/`, or is quarantined in `_rejected/`.

## Automatic Reject Gates

Any one of these is an immediate reject, even if the image is attractive:

- Wrong character or species: not clearly Jack, the golden retriever.
- Wrong wardrobe: missing black suit, white shirt, or black skinny tie.
- Office drift: teal/open-plan office, cold grey office, globe/fancy-library variant, wrong bookshelf/window layout, or changed lighting mood.
- Paw defect: brown/dark nail-like marks on top or outside of digits.
- Wrong target prompt: pose, expression, mouth, or paw action does not match the intended ID.
- Bad anatomy: human hands, extra digits, malformed paws, broken face, distorted muzzle.
- Wrong format or contamination: not vertical 9:16, visible watermark, text, UI, or low-quality artifacts.

## 10-Point Rubric

| Area | Points | Requirement |
|---|---:|---|
| Character identity | 2.0 | Jack matches the reference: golden retriever, fur tone, floppy ears, muzzle, eyes, brows. |
| Wardrobe | 1.0 | Black suit, white shirt, black skinny tie, consistent business look. |
| Office continuity | 2.0 | Warm wood office, left golden blinds/window, right wooden bookshelf, amber lamp, dark desk. |
| Pose/action accuracy | 1.5 | Correct ID-specific body angle, head tilt/profile, paw action, laptop/mug/pointing. |
| Expression/mouth accuracy | 1.0 | Correct emotion, eye shape, mouth open/closed/smirk/laugh. |
| Paw anatomy | 1.5 | Golden visible paw surfaces, no nail-like pads, no human fingers. |
| Style/framing/quality | 1.0 | 2D cel-shaded, paper texture, clean 9:16, no artifacts. |

## Verdicts

| Score | Verdict | Placement |
|---:|---|---|
| `9.5-10` | Accept | Counted active LoRA set. |
| `9.0-9.49` | Review only | Keep in `_generated_review/` or `_mouth-renders/`, not counted. |
| `8.0-8.99` | Reject unless useful | Usually `_rejected/`; optional reference only. |
| `<8.0` | Reject | `_rejected/`. |
| Any gate failure | Reject | `_rejected/` regardless of score. |

## Four-Agent Workflow

1. Generator Agent: creates candidates only in `_generated_review/`.
2. Visual Review Agent: checks image reality first: office, paws, anatomy, expression, pose, framing.
3. Rubric Scoring Agent: applies the 10-point rubric and writes the score/notes.
4. Dataset Clerk Agent: promotes only `>=9.5` images, writes captions, refreshes prompt status, quarantines rejects.

The generator never approves its own work. The clerk cannot promote an image without an explicit score and notes.
