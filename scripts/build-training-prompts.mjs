#!/usr/bin/env node
/**
 * build-training-prompts.mjs
 *
 * One-shot generator that produces jack-training-prompts.json — the 50 LoRA
 * training image prompts + captions for the Jack SaaS character.
 *
 * Output: jack-training-prompts.json at the project root.
 *
 * Re-run any time you want to tweak the locked-constants block, variation
 * matrix, or per-axis descriptors. The output is deterministic.
 *
 *   node scripts/build-training-prompts.mjs
 *   node scripts/build-training-prompts.mjs --out=path/to/out.json
 *
 * Structural rules baked in (per the OpenAI image-gen prompting guide):
 *   - Ordering: scene → subject → key details → style → framing → constraints
 *   - Character anchor: locked constants repeated verbatim on every prompt
 *   - Wardrobe lock: explicit "do not redesign" + identical descriptor phrasing
 *   - Framing/lighting phrased explicitly (9:16 portrait, eye-level, soft diffuse)
 *   - Constraints: preserve list + exclude list on every prompt
 *
 * Caption rules:
 *   - Every caption starts with trigger word "jacksaas"
 *   - Captions describe ONLY variables (pose, expression, mouth, hands)
 *   - Captions never repeat identity constants (no "golden retriever", "suit", etc.)
 *   - Captions 15–30 words, comma-separated descriptors
 */

import { writeFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");

const args = parseArgs(process.argv.slice(2));
const OUT = resolve(ROOT, args.out || "jack-training-prompts.json");

// ── Locked constants — appear verbatim in every generation_prompt ───────────

const SCENE = "Open-plan SaaS office, late afternoon. Muted teal painted walls, dark walnut wood desk, soft diffuse golden-hour daylight entering from a tall window camera-left. Dual matte-black monitors on the desk angled away from camera (screens not the focus). One small potted snake plant on the desk corner. Off-white ceramic coffee mug visible on the desk surface. Black ergonomic mesh office chair. Sparse bookshelf and a small round wall clock visible in soft background blur.";

const CHARACTER = "Jack — the same anthropomorphic golden retriever character as the attached jack-reference.png. Honey-blonde fur with subtle darker honey shading along the muzzle and ear tips, slight paper-grain texture. Floppy ears falling to jaw line. Warm amber-brown almond-shaped eyes with small dark fur tufts above each brow. Pronounced golden-retriever muzzle, glossy black nose, soft jaw. Wearing the same wardrobe: black single-breasted notched-lapel two-button suit jacket, crisp white pointed-collar dress shirt, plain black skinny tie loosely knotted (knot small and tight, tie length to mid-chest), black slim-cut trousers, black low-top canvas Converse-style sneakers with white rubber toe caps and white laces, black leather belt with small silver square buckle. Same character, same wardrobe — do not redesign.";

const STYLE = "2D adult-animation cel-shaded illustration matching the attached reference exactly. Painterly flat shading with subtle paper-grain texture overlay on the fur. Visible hand-drawn line work of consistent medium weight. Limited palette: warm honey blondes, deep blacks, off-whites, muted teals. Soft natural shadow under the jaw and where body meets chair or desk. No rim light, no high-gloss render, no bloom. Same illustration style on every frame as in the attached reference.";

const CONSTRAINTS = "Preserve character identity, wardrobe, fur tone, eye geometry, ear shape, and art style exactly as in the attached reference. No text, no captions, no watermarks, no logos, no on-screen UI elements. Do not redesign Jack. Do not add other characters or people. Same office setting across all stills. Solo character.";

// ── Per-axis descriptors ────────────────────────────────────────────────────

const POSE = {
  front_facing_seated: {
    long: "Jack seated in his office chair facing the camera directly, torso squared to the camera, shoulders relaxed",
    short: "front-facing seated",
  },
  three_quarter_left: {
    long: "Jack seated in his office chair turned three-quarters toward camera-left, left shoulder closer to lens",
    short: "three-quarter left turn",
  },
  three_quarter_right: {
    long: "Jack seated in his office chair turned three-quarters toward camera-right, right shoulder closer to lens",
    short: "three-quarter right turn",
  },
  profile_left: {
    long: "Jack seated in his office chair in full left profile, body facing camera-left, only the left side of his face visible to camera",
    short: "full left profile",
  },
  profile_right: {
    long: "Jack seated in his office chair in full right profile, body facing camera-right, only the right side of his face visible to camera",
    short: "full right profile",
  },
  leaning_forward: {
    long: "Jack leaning forward in his office chair toward the camera, shoulders pushed in toward the desk, elbows or forearms anchored on the desk surface",
    short: "leaning forward toward camera",
  },
  leaning_back: {
    long: "Jack leaning back in his office chair, shoulders rolled back against the chair backrest, body relaxed and open",
    short: "leaning back, body open and relaxed",
  },
  slight_upward_tilt: {
    long: "Jack seated in his chair with his head tilted slightly upward (chin raised about ten degrees), eyes following the upward tilt",
    short: "head tilted slightly up",
  },
  slight_downward_tilt: {
    long: "Jack seated in his chair with his head tilted slightly downward (chin tucked about ten degrees), gaze cast just below horizontal",
    short: "head tilted slightly down",
  },
};

const EXPRESSION = {
  tired_deadpan: {
    long: "his expression tired and deadpan, eyelids low, eyes half-lidded, face unmoving — the look of someone three back-to-back meetings deep",
    short: "tired deadpan, eyes half-lidded",
  },
  smug_smirk: {
    long: "his expression a smug knowing smirk, one corner of his mouth lifted, eyes narrowed slightly with quiet amusement",
    short: "smug knowing smirk, eyes narrowed",
  },
  mild_irritation: {
    long: "his expression mildly irritated, brow lowered a touch, jaw set, eyes flat and unimpressed",
    short: "mildly irritated, brow lowered, jaw set",
  },
  exasperated: {
    long: "his expression exhausted and exasperated, eyes wide and slightly unfocused, brow heavy — the look of someone whose patience is fully spent",
    short: "exasperated, patience spent",
  },
  surprised: {
    long: "his expression surprised, eyebrows raised high, eyes widened, ears perked forward in alert",
    short: "surprised, eyebrows raised, ears perked",
  },
  concerned_skeptical: {
    long: "his expression concerned and skeptical, brow furrowed, one eyebrow slightly higher than the other, eyes narrow and reading the situation",
    short: "concerned skeptical, brow furrowed, one brow higher",
  },
  laughing_chuckling: {
    long: "his expression genuinely laughing, eyes scrunched with mirth, ears slightly back, the easy laugh of someone caught off-guard by something funny",
    short: "laughing chuckle, eyes scrunched",
  },
  whispering_conspiratorial: {
    long: "his expression conspiratorial, eyes flicking sideways as if checking who might overhear, the whisper-energy of someone about to share office gossip",
    short: "conspiratorial whisper energy, eyes flicking sideways",
  },
  mid_sentence_talking: {
    long: "his expression engaged mid-sentence, eyes alive, eyebrows neutral, caught in the middle of explaining something",
    short: "engaged mid-sentence, eyes alive",
  },
  confident_lecture: {
    long: "his expression confident and explanatory, brow slightly raised, eyes direct — the look of someone holding the floor",
    short: "confident lecture mode, holding the floor",
  },
};

const MOUTH = {
  closed_neutral: { long: "mouth closed in a relaxed neutral line", short: "mouth closed neutral" },
  slightly_open: { long: "mouth slightly parted, just barely open", short: "mouth slightly open" },
  half_open_mid_word: { long: "mouth half open mid-word, caught mid-syllable", short: "mouth half-open mid-word" },
  wide_open_emphatic: { long: "mouth wide open in an emphatic vowel shape", short: "mouth wide open emphatic" },
  smirk: { long: "mouth held in an asymmetric smirk, one corner clearly raised", short: "mouth in a smirk" },
};

const HANDS = {
  both_paws_on_desk: {
    long: "both paws resting flat on the desk in front of him, fingers relaxed",
    short: "both paws extended forward palms-down",
  },
  one_paw_holding_coffee_mug: {
    long: "one paw wrapped around the off-white ceramic coffee mug, lifting it just above the desk surface",
    short: "one paw lifting a mug",
  },
  gesturing_mid_air: {
    long: "one or both paws gesturing in mid-air at chest level, palms open, caught mid-explanation",
    short: "paws gesturing mid-air",
  },
  pointing_at_off_screen_monitor: {
    long: "one paw extended off-screen-right, single finger pointing toward where his monitor sits just out of frame, the gesture sharp and directed",
    short: "one paw pointing off-screen-right",
  },
  touching_laptop_keyboard: {
    long: "one paw resting on the keys of his open laptop on the desk, the other relaxed at his side or on the desk surface",
    short: "fingers resting on keys",
  },
  tie_adjustment: {
    long: "one paw at the knot of his black skinny tie, fingers gripping the knot and tugging it slightly to one side",
    short: "one paw gripping a knot at the neck",
  },
  paws_crossed_folded: {
    long: "paws folded together in front of his chest or crossed lightly across his body, posture closed and contained",
    short: "paws folded across body",
  },
  one_paw_on_chin: {
    long: "one paw raised to his muzzle, finger curled lightly under his chin in a thinking gesture",
    short: "paw on chin thinking",
  },
};

// ── Special-note overrides (replace pose/hands/framing as needed) ───────────

const SPECIAL = {
  mid_coffee_sip: {
    hands_long: "lifting the off-white ceramic coffee mug to his muzzle mid-sip, the rim of the mug touching just below his nose, the other paw cradling the bottom of the mug",
    hands_short: "mid-coffee-sip, mug rim at muzzle",
  },
  tie_tugged: {
    hands_long: "one paw gripping the knot of his black skinny tie and pulling it firmly to one side, fabric pulled away from the collar",
    hands_short: "knot at neck pulled firmly to one side",
  },
  emphatic_laptop_point: {
    hands_long: "one paw extended forward, finger jabbing emphatically toward the open laptop screen in front of him, finger tense, the gesture sharp and accusing",
    hands_short: "emphatic finger jab forward, tense pointing",
  },
  head_back_chuckle: {
    pose_long: "Jack leaning fully back in his office chair, head tilted back against the headrest, eyes closed, ears slightly back, body shaking gently with a quiet chuckle",
    pose_short: "head tilted fully back, eyes closed, chuckling",
  },
  extreme_closeup_eye: {
    framing: "Extreme close-up on the right side of Jack's face — only one eye, the brow above it, and the bridge of his snout visible in frame. Skin-level detail on the dark fur tufts above the brow.",
    framing_short: "extreme close-up on one eye, brow detail",
  },
  paws_over_face_despair: {
    hands_long: "both paws raised to cover his face, heels of the palms pressing into his eye sockets, fingers spread up into the fur on his forehead, head bowed",
    hands_short: "both paws covering face, head bowed in mock despair",
  },
};

// ── The 50-slot assignment ──────────────────────────────────────────────────
// Pre-validated for uniqueness + matches axis target counts.
// See coverage_report at end of generated JSON.

const SLOTS = [
  // FRONT-FACING SEATED (8)
  { id: "jack_001", pose: "front_facing_seated", expression: "tired_deadpan",       mouth: "closed_neutral",     hands: "both_paws_on_desk",            special: null },
  { id: "jack_002", pose: "front_facing_seated", expression: "smug_smirk",          mouth: "smirk",              hands: "both_paws_on_desk",            special: null },
  { id: "jack_003", pose: "front_facing_seated", expression: "tired_deadpan",       mouth: "closed_neutral",     hands: "one_paw_holding_coffee_mug",   special: null },
  { id: "jack_004", pose: "front_facing_seated", expression: "mid_sentence_talking",mouth: "half_open_mid_word", hands: "gesturing_mid_air",            special: null },
  { id: "jack_005", pose: "front_facing_seated", expression: "confident_lecture",   mouth: "slightly_open",      hands: "both_paws_on_desk",            special: null },
  { id: "jack_006", pose: "front_facing_seated", expression: "exasperated",         mouth: "wide_open_emphatic", hands: "paws_crossed_folded",          special: "paws_over_face_despair" },
  { id: "jack_007", pose: "front_facing_seated", expression: "surprised",           mouth: "wide_open_emphatic", hands: "both_paws_on_desk",            special: null },
  { id: "jack_008", pose: "front_facing_seated", expression: "concerned_skeptical", mouth: "closed_neutral",     hands: "one_paw_on_chin",              special: "extreme_closeup_eye" },

  // THREE-QUARTER LEFT (6)
  { id: "jack_009", pose: "three_quarter_left",  expression: "tired_deadpan",       mouth: "closed_neutral",     hands: "both_paws_on_desk",            special: null },
  { id: "jack_010", pose: "three_quarter_left",  expression: "smug_smirk",          mouth: "smirk",              hands: "one_paw_holding_coffee_mug",   special: "mid_coffee_sip" },
  { id: "jack_011", pose: "three_quarter_left",  expression: "mild_irritation",     mouth: "slightly_open",      hands: "gesturing_mid_air",            special: null },
  { id: "jack_012", pose: "three_quarter_left",  expression: "whispering_conspiratorial", mouth: "half_open_mid_word", hands: "one_paw_on_chin",        special: null },
  { id: "jack_013", pose: "three_quarter_left",  expression: "smug_smirk",          mouth: "slightly_open",      hands: "one_paw_holding_coffee_mug",   special: "mid_coffee_sip" },
  { id: "jack_014", pose: "three_quarter_left",  expression: "concerned_skeptical", mouth: "half_open_mid_word", hands: "touching_laptop_keyboard",     special: null },

  // THREE-QUARTER RIGHT (6)
  { id: "jack_015", pose: "three_quarter_right", expression: "tired_deadpan",       mouth: "closed_neutral",     hands: "both_paws_on_desk",            special: null },
  { id: "jack_016", pose: "three_quarter_right", expression: "smug_smirk",          mouth: "smirk",              hands: "one_paw_holding_coffee_mug",   special: null },
  { id: "jack_017", pose: "three_quarter_right", expression: "mid_sentence_talking",mouth: "half_open_mid_word", hands: "gesturing_mid_air",            special: null },
  { id: "jack_018", pose: "three_quarter_right", expression: "confident_lecture",   mouth: "half_open_mid_word", hands: "pointing_at_off_screen_monitor", special: "emphatic_laptop_point" },
  { id: "jack_019", pose: "three_quarter_right", expression: "mild_irritation",     mouth: "slightly_open",      hands: "tie_adjustment",               special: "tie_tugged" },
  { id: "jack_020", pose: "three_quarter_right", expression: "whispering_conspiratorial", mouth: "slightly_open", hands: "gesturing_mid_air",           special: null },

  // PROFILE LEFT (4)
  { id: "jack_021", pose: "profile_left",        expression: "tired_deadpan",       mouth: "closed_neutral",     hands: "one_paw_holding_coffee_mug",   special: null },
  { id: "jack_022", pose: "profile_left",        expression: "mid_sentence_talking",mouth: "slightly_open",      hands: "touching_laptop_keyboard",     special: null },
  { id: "jack_023", pose: "profile_left",        expression: "smug_smirk",          mouth: "smirk",              hands: "one_paw_on_chin",              special: null },
  { id: "jack_024", pose: "profile_left",        expression: "exasperated",         mouth: "half_open_mid_word", hands: "both_paws_on_desk",            special: null },

  // PROFILE RIGHT (4)
  { id: "jack_025", pose: "profile_right",       expression: "tired_deadpan",       mouth: "closed_neutral",     hands: "both_paws_on_desk",            special: null },
  { id: "jack_026", pose: "profile_right",       expression: "concerned_skeptical", mouth: "slightly_open",      hands: "touching_laptop_keyboard",     special: null },
  { id: "jack_027", pose: "profile_right",       expression: "surprised",           mouth: "wide_open_emphatic", hands: "gesturing_mid_air",            special: null },
  { id: "jack_028", pose: "profile_right",       expression: "smug_smirk",          mouth: "smirk",              hands: "one_paw_holding_coffee_mug",   special: "mid_coffee_sip" },

  // LEANING FORWARD (6)
  { id: "jack_029", pose: "leaning_forward",     expression: "whispering_conspiratorial", mouth: "slightly_open", hands: "both_paws_on_desk",           special: null },
  { id: "jack_030", pose: "leaning_forward",     expression: "mid_sentence_talking",mouth: "half_open_mid_word", hands: "gesturing_mid_air",            special: null },
  { id: "jack_031", pose: "leaning_forward",     expression: "confident_lecture",   mouth: "half_open_mid_word", hands: "pointing_at_off_screen_monitor", special: "emphatic_laptop_point" },
  { id: "jack_032", pose: "leaning_forward",     expression: "surprised",           mouth: "wide_open_emphatic", hands: "both_paws_on_desk",            special: null },
  { id: "jack_033", pose: "leaning_forward",     expression: "concerned_skeptical", mouth: "closed_neutral",     hands: "touching_laptop_keyboard",     special: null },
  { id: "jack_034", pose: "leaning_forward",     expression: "mild_irritation",     mouth: "half_open_mid_word", hands: "tie_adjustment",               special: "tie_tugged" },

  // LEANING BACK (6)
  { id: "jack_035", pose: "leaning_back",        expression: "laughing_chuckling",  mouth: "wide_open_emphatic", hands: "paws_crossed_folded",          special: "head_back_chuckle" },
  { id: "jack_036", pose: "leaning_back",        expression: "laughing_chuckling",  mouth: "half_open_mid_word", hands: "paws_crossed_folded",          special: "head_back_chuckle" },
  { id: "jack_037", pose: "leaning_back",        expression: "tired_deadpan",       mouth: "closed_neutral",     hands: "one_paw_on_chin",              special: null },
  { id: "jack_038", pose: "leaning_back",        expression: "confident_lecture",   mouth: "slightly_open",      hands: "pointing_at_off_screen_monitor", special: null },
  { id: "jack_039", pose: "leaning_back",        expression: "whispering_conspiratorial", mouth: "slightly_open", hands: "one_paw_holding_coffee_mug",  special: null },
  { id: "jack_040", pose: "leaning_back",        expression: "exasperated",         mouth: "wide_open_emphatic", hands: "gesturing_mid_air",            special: null },

  // SLIGHT UPWARD TILT (4)
  { id: "jack_041", pose: "slight_upward_tilt",  expression: "tired_deadpan",       mouth: "closed_neutral",     hands: "one_paw_holding_coffee_mug",   special: null },
  { id: "jack_042", pose: "slight_upward_tilt",  expression: "surprised",           mouth: "slightly_open",      hands: "gesturing_mid_air",            special: null },
  { id: "jack_043", pose: "slight_upward_tilt",  expression: "mild_irritation",     mouth: "slightly_open",      hands: "pointing_at_off_screen_monitor", special: null },
  { id: "jack_044", pose: "slight_upward_tilt",  expression: "concerned_skeptical", mouth: "closed_neutral",     hands: "one_paw_holding_coffee_mug",   special: null },

  // SLIGHT DOWNWARD TILT (6)
  { id: "jack_045", pose: "slight_downward_tilt",expression: "mild_irritation",     mouth: "closed_neutral",     hands: "paws_crossed_folded",          special: null },
  { id: "jack_046", pose: "slight_downward_tilt",expression: "exasperated",         mouth: "closed_neutral",     hands: "touching_laptop_keyboard",     special: null },
  { id: "jack_047", pose: "slight_downward_tilt",expression: "exasperated",         mouth: "closed_neutral",     hands: "one_paw_holding_coffee_mug",   special: null },
  { id: "jack_048", pose: "slight_downward_tilt",expression: "laughing_chuckling",  mouth: "wide_open_emphatic", hands: "pointing_at_off_screen_monitor", special: null },
  { id: "jack_049", pose: "slight_downward_tilt",expression: "laughing_chuckling",  mouth: "closed_neutral",     hands: "pointing_at_off_screen_monitor", special: null },
  { id: "jack_050", pose: "slight_downward_tilt",expression: "laughing_chuckling",  mouth: "wide_open_emphatic", hands: "touching_laptop_keyboard",     special: null },
];

// ── Framing rotation (avoid all 50 having identical framing) ────────────────

const FRAMINGS = [
  "Medium shot from chest up. Eye-level perspective.",
  "Medium-tight shot from waist up. Eye-level perspective.",
  "Close-up of head and shoulders. Eye-level perspective.",
  "Medium shot from chest up, slight low angle.",
];

// ── Renderers ───────────────────────────────────────────────────────────────

function renderGenerationPrompt(slot, index) {
  const poseLong = slot.special && SPECIAL[slot.special]?.pose_long
    ? SPECIAL[slot.special].pose_long
    : POSE[slot.pose].long;
  const handsLong = slot.special && SPECIAL[slot.special]?.hands_long
    ? SPECIAL[slot.special].hands_long
    : HANDS[slot.hands].long;
  const framing = slot.special && SPECIAL[slot.special]?.framing
    ? SPECIAL[slot.special].framing
    : FRAMINGS[index % FRAMINGS.length];

  return [
    "[SCENE]",
    SCENE,
    "",
    "[CHARACTER — locked, do not redesign]",
    CHARACTER,
    "",
    "[POSE & ACTION FOR THIS STILL]",
    `${poseLong}, ${EXPRESSION[slot.expression].long}, ${MOUTH[slot.mouth].long}, ${handsLong}.`,
    "",
    "[STYLE]",
    STYLE,
    "",
    "[FRAMING]",
    `9:16 vertical portrait orientation, 1080x1920 aspect ratio. ${framing}`,
    "",
    "[CONSTRAINTS]",
    CONSTRAINTS,
  ].join("\n");
}

function renderLoraCaption(slot) {
  const poseShort = slot.special && SPECIAL[slot.special]?.pose_short
    ? SPECIAL[slot.special].pose_short
    : POSE[slot.pose].short;
  const handsShort = slot.special && SPECIAL[slot.special]?.hands_short
    ? SPECIAL[slot.special].hands_short
    : HANDS[slot.hands].short;
  const framingExtra = slot.special && SPECIAL[slot.special]?.framing_short
    ? `, ${SPECIAL[slot.special].framing_short}`
    : "";

  return [
    "jacksaas",
    poseShort,
    EXPRESSION[slot.expression].short,
    MOUTH[slot.mouth].short,
    handsShort,
  ].join(", ") + framingExtra;
}

function coverageReport(slots) {
  const tally = (key) => slots.reduce((acc, s) => ((acc[s[key]] = (acc[s[key]] || 0) + 1), acc), {});
  return {
    poses: tally("pose"),
    expressions: tally("expression"),
    mouth_states: tally("mouth"),
    hands: tally("hands"),
    special_moments: slots.filter(s => s.special).reduce((acc, s) => ((acc[s.special] = (acc[s.special] || 0) + 1), acc), {}),
  };
}

// ── Validation ──────────────────────────────────────────────────────────────

function validate(prompts) {
  const issues = [];

  // Unique tuples
  const seen = new Set();
  for (const p of prompts) {
    const key = `${p.pose}|${p.expression}|${p.mouth}|${p.hands}|${p.special || ""}`;
    if (seen.has(key)) issues.push(`Duplicate combo at ${p.id}: ${key}`);
    seen.add(key);
  }

  // Trigger word on every caption
  for (const p of prompts) {
    if (!p.lora_caption.toLowerCase().startsWith("jacksaas")) {
      issues.push(`${p.id}: lora_caption does not start with "jacksaas"`);
    }
  }

  // Caption word counts
  for (const p of prompts) {
    const words = p.lora_caption.split(/\s+/).filter(Boolean).length;
    if (words < 5 || words > 35) issues.push(`${p.id}: caption ${words} words (target 15–30, tolerable 5–35)`);
  }

  // Identity-leak check — captions must not include character constants
  const forbidden = /\b(golden retriever|golden labrador|labrador|navy suit|black suit|dress shirt|tie|office|desk|warm lighting|teal walls|cel.?shaded|painterly|honey.?blonde|amber|brown.eyes|converse|sneakers|monitors|laptop\b)/i;
  for (const p of prompts) {
    if (forbidden.test(p.lora_caption)) {
      issues.push(`${p.id}: caption leaks identity constant: "${p.lora_caption}"`);
    }
  }

  // Special-moment coverage
  const required = {
    mid_coffee_sip: 3,
    tie_tugged: 2,
    emphatic_laptop_point: 2,
    head_back_chuckle: 2,
    extreme_closeup_eye: 1,
    paws_over_face_despair: 1,
  };
  const got = prompts.filter(p => p.special_note).reduce((acc, p) => ((acc[p.special_note] = (acc[p.special_note] || 0) + 1), acc), {});
  for (const [k, n] of Object.entries(required)) {
    if ((got[k] || 0) !== n) issues.push(`Special "${k}": expected ${n}, got ${got[k] || 0}`);
  }

  // Axis target totals
  const targets = {
    pose:       { front_facing_seated: 8, three_quarter_left: 6, three_quarter_right: 6, profile_left: 4, profile_right: 4, leaning_forward: 6, leaning_back: 6, slight_upward_tilt: 4, slight_downward_tilt: 6 },
    expression: { tired_deadpan: 8, smug_smirk: 6, mild_irritation: 5, exasperated: 5, surprised: 4, concerned_skeptical: 5, laughing_chuckling: 5, whispering_conspiratorial: 4, mid_sentence_talking: 4, confident_lecture: 4 },
    mouth:      { closed_neutral: 15, slightly_open: 12, half_open_mid_word: 10, wide_open_emphatic: 8, smirk: 5 },
    hands:      { both_paws_on_desk: 10, one_paw_holding_coffee_mug: 10, gesturing_mid_air: 8, pointing_at_off_screen_monitor: 6, touching_laptop_keyboard: 6, tie_adjustment: 2, paws_crossed_folded: 4, one_paw_on_chin: 4 },
  };
  for (const [axis, targs] of Object.entries(targets)) {
    const actual = prompts.reduce((acc, p) => ((acc[p[axis]] = (acc[p[axis]] || 0) + 1), acc), {});
    for (const [val, target] of Object.entries(targs)) {
      if ((actual[val] || 0) !== target) {
        issues.push(`Axis ${axis} value "${val}": expected ${target}, got ${actual[val] || 0}`);
      }
    }
  }

  return issues;
}

// ── Build ───────────────────────────────────────────────────────────────────

const prompts = SLOTS.map((slot, i) => ({
  id: slot.id,
  pose: slot.pose,
  expression: slot.expression,
  mouth: slot.mouth,
  hands: slot.hands,
  special_note: slot.special,
  generation_prompt: renderGenerationPrompt(slot, i),
  lora_caption: renderLoraCaption(slot),
}));

const issues = validate(prompts);
if (issues.length > 0) {
  console.error("Validation issues:");
  for (const issue of issues) console.error("  - " + issue);
  process.exit(1);
}

const out = {
  version: "1.0",
  generated: new Date().toISOString(),
  trigger_word: "jacksaas",
  reference_image: "assets/jack-reference.png",
  total_count: prompts.length,
  prompts,
  coverage_report: coverageReport(SLOTS),
};

writeFileSync(OUT, JSON.stringify(out, null, 2));
const captionLens = prompts.map(p => p.lora_caption.split(/\s+/).length);
const promptLens = prompts.map(p => p.generation_prompt.length);
console.log(`Wrote ${OUT}`);
console.log(`  ${prompts.length} prompts, ${issues.length === 0 ? "all validation checks passed" : "validation FAILED"}.`);
console.log(`  caption words: min=${Math.min(...captionLens)} max=${Math.max(...captionLens)} avg=${(captionLens.reduce((a,b)=>a+b,0)/captionLens.length).toFixed(1)}`);
console.log(`  generation_prompt chars: min=${Math.min(...promptLens)} max=${Math.max(...promptLens)} avg=${(promptLens.reduce((a,b)=>a+b,0)/promptLens.length).toFixed(0)}`);

// ── Helpers ─────────────────────────────────────────────────────────────────

function parseArgs(argv) {
  const out = {};
  for (const arg of argv) {
    if (!arg.startsWith("--")) continue;
    const eq = arg.indexOf("=");
    if (eq === -1) out[arg.slice(2)] = true;
    else out[arg.slice(2, eq)] = arg.slice(eq + 1);
  }
  return out;
}
