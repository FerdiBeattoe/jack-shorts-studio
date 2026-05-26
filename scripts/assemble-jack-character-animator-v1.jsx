// ============================================================================
// assemble-jack-character-animator-v1.jsx
// Adobe Photoshop ExtendScript (ES3-compatible)
//
// Jack V1 Character Animator Puppet — PSD Assembly Script
//
// PURPOSE
//   Imports all validated PNG puppet layer assets into a new layered PSD
//   using the group/layer naming required by Adobe Character Animator.
//   The PSD is saved to: assets/puppet/jack_character_animator_v1.psd
//
// BEFORE RUNNING
//   Confirm all V1-required assets are present:
//     node scripts/validate-jack-puppet-pack.mjs
//
// HOW TO RUN
//   In Photoshop: File > Scripts > Browse
//   Navigate to: scripts/assemble-jack-character-animator-v1.jsx
//   Click Open.
//
// OUTPUT
//   assets/puppet/jack_character_animator_v1.psd
//   Canvas: 1920 x 1920 px, RGB, 72 ppi, transparent background
//
// AFTER RUNNING
//   See: docs/animation/psd_assembly_runbook_v1.md
// ============================================================================

#target photoshop

(function () {

    // ── Guard: must be running in Photoshop ──────────────────────────────────
    if (typeof app === "undefined" || !(app instanceof Application)) {
        alert("ERROR: This script must be run from within Adobe Photoshop.\nFile > Scripts > Browse");
        return;
    }

    // ── Suppress dialogs during import to avoid profile/colour prompts ───────
    var origDialogs = app.displayDialogs;
    app.displayDialogs = DialogModes.NO;

    // ── Derive project root from this script's location ──────────────────────
    // Script lives at: <project>/scripts/assemble-jack-character-animator-v1.jsx
    // Project root is one level up from scripts/
    var jsxFile = new File($.fileName);
    var projectRoot = jsxFile.parent.parent.fsName.replace(/\\/g, "/");
    // e.g. C:/Users/ferdi/Desktop/jack-shorts-studio

    // Helper: resolve a project-root-relative path to an absolute path
    function abs(rel) {
        return projectRoot + "/" + rel;
    }

    // ── Canvas configuration ─────────────────────────────────────────────────
    var CANVAS_W   = 1920;
    var CANVAS_H   = 1920;
    var CANVAS_RES = 72;   // PPI (screen — pixel count is what matters)

    // ── Output PSD path ───────────────────────────────────────────────────────
    var PSD_OUTPUT = abs("assets/puppet/jack_character_animator_v1.psd");

    // =========================================================================
    // ASSET DEFINITIONS
    // =========================================================================
    //
    // Each entry describes one PNG → PSD layer mapping.
    //
    //   file       - absolute path to the source PNG
    //   layerName  - the name the layer will have inside the PSD
    //   groupPath  - array of group names from document root inward.
    //                [] = place at document root (unused here).
    //   visible    - initial visibility. false = hidden (swap-set members).
    //   required   - if true, abort if file is missing.
    //
    // IMPORT ORDER NOTE:
    //   Within any group, each import lands at the TOP of that group.
    //   To achieve the desired top→bottom stacking, import BOTTOM layers first.
    //   The desired final order is documented next to each group block below.
    //
    // CHARACTER ANIMATOR NAMING RULES:
    //   - Mouth group sublayer names MUST match CA phoneme map exactly.
    //     See: docs/animation/character_animator_layer_naming_v1.md
    //   - "Left" and "Right" are from the CHARACTER's perspective (mirrored
    //     from the viewer's perspective).
    //
    // =========================================================================

    var ASSETS = [

        // ── ENVIRONMENT (separate top-level group — NOT inside Jack puppet) ──
        // Final order in Environment group (top→bottom): Chair | Office Background
        // Import bottom-first: Office Background, then Chair.
        {
            file: abs("assets/puppet/layers/environment/office_background_clean.png"),
            layerName: "Office Background",
            groupPath: ["Environment"],
            visible: true,
            required: true
        },
        {
            file: abs("assets/puppet/layers/environment/office_chair.png"),
            layerName: "Chair",
            groupPath: ["Environment"],
            visible: true,
            required: true
        },

        // ── JACK > BODY ───────────────────────────────────────────────────────
        // Final order in Body (top→bottom): Right Arm | Left Arm | Tie | Torso
        // Import bottom-first: Torso, then Tie, Left Arm, Right Arm last.
        {
            file: abs("assets/puppet/layers/body/jack_torso_front.png"),
            layerName: "Torso",
            groupPath: ["Jack", "Body"],
            visible: true,
            required: true
        },
        {
            file: abs("assets/puppet/layers/body/jack_tie_straight.png"),
            layerName: "Tie Straight",
            groupPath: ["Jack", "Body", "Tie"],
            visible: true,
            required: true
        },
        {
            file: abs("assets/puppet/layers/body/jack_arm_left_resting.png"),
            layerName: "Left Arm Resting",
            groupPath: ["Jack", "Body", "Left Arm"],
            visible: true,
            required: true
        },
        // Right Arm swap set: Arm Resting (default visible), Arm Tie Fix (hidden)
        {
            file: abs("assets/puppet/layers/body/jack_arm_right_tie_fix.png"),
            layerName: "Right Arm Raised",
            groupPath: ["Jack", "Body", "Right Arm", "Arm Tie Fix"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/body/jack_arm_right_resting.png"),
            layerName: "Right Arm Resting",
            groupPath: ["Jack", "Body", "Right Arm", "Arm Resting"],
            visible: true,
            required: true
        },

        // ── JACK > HEAD > HEAD BASE ───────────────────────────────────────────
        // Head Base sits at the BOTTOM of the Head group (below Face).
        // It is imported first here; Face group (pre-created) stays above it.
        {
            file: abs("assets/puppet/layers/head/jack_head_front_base.png"),
            layerName: "Head Base",
            groupPath: ["Jack", "Head"],
            visible: true,
            required: true
        },

        // ── JACK > HEAD > FACE > MOUTH ────────────────────────────────────────
        // CA Auto Mouth maps phonemes to sublayer names. Names are EXACT strings.
        // Final order (top→bottom): Neutral | Smile | Smirk | Open | Ee | Oh |
        //   Ooh | M B P | F V | L | S
        // Import bottom-first: S → L → F V → M B P → Ooh → Oh → Ee → Open →
        //   Smirk → Smile → Neutral (last = ends on top = default visible).
        // Only Neutral is visible on open.
        {
            file: abs("assets/puppet/layers/mouth/jack_mouth_s_dtn.png"),
            layerName: "S",
            groupPath: ["Jack", "Head", "Face", "Mouth"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/mouth/jack_mouth_l.png"),
            layerName: "L",
            groupPath: ["Jack", "Head", "Face", "Mouth"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/mouth/jack_mouth_fv.png"),
            layerName: "F V",
            groupPath: ["Jack", "Head", "Face", "Mouth"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/mouth/jack_mouth_mbp.png"),
            layerName: "M B P",
            groupPath: ["Jack", "Head", "Face", "Mouth"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/mouth/jack_mouth_oo_w.png"),
            layerName: "Ooh",
            groupPath: ["Jack", "Head", "Face", "Mouth"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/mouth/jack_mouth_oh.png"),
            layerName: "Oh",
            groupPath: ["Jack", "Head", "Face", "Mouth"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/mouth/jack_mouth_ee.png"),
            layerName: "Ee",
            groupPath: ["Jack", "Head", "Face", "Mouth"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/mouth/jack_mouth_ah.png"),
            layerName: "Open",
            groupPath: ["Jack", "Head", "Face", "Mouth"],
            visible: false,
            required: true
        },
        // Smirk is a trigger-based override — NOT used by CA Auto Mouth lip sync.
        // It sits in the Mouth group for swap-set access but is hidden by default.
        {
            file: abs("assets/puppet/layers/mouth/jack_mouth_smirk.png"),
            layerName: "Smirk",
            groupPath: ["Jack", "Head", "Face", "Mouth"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/mouth/jack_mouth_smile.png"),
            layerName: "Smile",
            groupPath: ["Jack", "Head", "Face", "Mouth"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/mouth/jack_mouth_neutral.png"),
            layerName: "Neutral",
            groupPath: ["Jack", "Head", "Face", "Mouth"],
            visible: true,   // DEFAULT — CA falls back to Neutral for silence
            required: true
        },

        // ── JACK > HEAD > FACE > LEFT EYE ─────────────────────────────────────
        // "Left Eye" in Photoshop = Jack's anatomical left = RIGHT side of the screen.
        // Left Upper Lid sub-group: CA uses this for blink warp.
        //   Place the eye-open layer inside Left Upper Lid.
        // Import bottom-first into Left Eye: Pupil (bottom), Closed, Half,
        //   then Left Eye Open goes into Left Upper Lid (separate sub-group).
        {
            file: abs("assets/puppet/layers/eyes/jack_pupil_left.png"),
            layerName: "Left Pupil",
            groupPath: ["Jack", "Head", "Face", "Left Eye"],
            visible: true,
            required: true
        },
        {
            file: abs("assets/puppet/layers/eyes/jack_eye_left_closed.png"),
            layerName: "Left Eye Closed",
            groupPath: ["Jack", "Head", "Face", "Left Eye"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/eyes/jack_eye_left_half.png"),
            layerName: "Left Eye Half",
            groupPath: ["Jack", "Head", "Face", "Left Eye"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/eyes/jack_eye_left_open.png"),
            layerName: "Left Eye Open",
            groupPath: ["Jack", "Head", "Face", "Left Eye", "Left Upper Lid"],
            visible: true,   // DEFAULT open state — lives inside Left Upper Lid for CA blink
            required: true
        },

        // ── JACK > HEAD > FACE > RIGHT EYE ────────────────────────────────────
        // "Right Eye" = Jack's anatomical right = LEFT side of the screen.
        {
            file: abs("assets/puppet/layers/eyes/jack_pupil_right.png"),
            layerName: "Right Pupil",
            groupPath: ["Jack", "Head", "Face", "Right Eye"],
            visible: true,
            required: true
        },
        {
            file: abs("assets/puppet/layers/eyes/jack_eye_right_closed.png"),
            layerName: "Right Eye Closed",
            groupPath: ["Jack", "Head", "Face", "Right Eye"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/eyes/jack_eye_right_half.png"),
            layerName: "Right Eye Half",
            groupPath: ["Jack", "Head", "Face", "Right Eye"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/eyes/jack_eye_right_open.png"),
            layerName: "Right Eye Open",
            groupPath: ["Jack", "Head", "Face", "Right Eye", "Right Upper Lid"],
            visible: true,   // DEFAULT open state — lives inside Right Upper Lid for CA blink
            required: true
        },

        // ── JACK > HEAD > FACE > LEFT EYEBROW ─────────────────────────────────
        // Swap set: one visible at a time, swapped via CA triggers.
        // Final order (top→bottom): LB Neutral | LB Concerned | LB Thinking | LB Smug
        // Import bottom-first: LB Smug → LB Thinking → LB Concerned → LB Neutral (last).
        {
            file: abs("assets/puppet/layers/eyebrows/jack_eyebrow_left_smug.png"),
            layerName: "LB Smug",
            groupPath: ["Jack", "Head", "Face", "Left Eyebrow"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/eyebrows/jack_eyebrow_left_thinking.png"),
            layerName: "LB Thinking",
            groupPath: ["Jack", "Head", "Face", "Left Eyebrow"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/eyebrows/jack_eyebrow_left_concerned.png"),
            layerName: "LB Concerned",
            groupPath: ["Jack", "Head", "Face", "Left Eyebrow"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/eyebrows/jack_eyebrow_left_neutral.png"),
            layerName: "LB Neutral",
            groupPath: ["Jack", "Head", "Face", "Left Eyebrow"],
            visible: true,   // DEFAULT
            required: true
        },

        // ── JACK > HEAD > FACE > RIGHT EYEBROW ────────────────────────────────
        {
            file: abs("assets/puppet/layers/eyebrows/jack_eyebrow_right_smug.png"),
            layerName: "RB Smug",
            groupPath: ["Jack", "Head", "Face", "Right Eyebrow"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/eyebrows/jack_eyebrow_right_thinking.png"),
            layerName: "RB Thinking",
            groupPath: ["Jack", "Head", "Face", "Right Eyebrow"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/eyebrows/jack_eyebrow_right_concerned.png"),
            layerName: "RB Concerned",
            groupPath: ["Jack", "Head", "Face", "Right Eyebrow"],
            visible: false,
            required: true
        },
        {
            file: abs("assets/puppet/layers/eyebrows/jack_eyebrow_right_neutral.png"),
            layerName: "RB Neutral",
            groupPath: ["Jack", "Head", "Face", "Right Eyebrow"],
            visible: true,   // DEFAULT
            required: true
        }

    ];

    // =========================================================================
    // HELPER: PRE-FLIGHT CHECK
    // =========================================================================
    function preflight(assets) {
        var missing = [];
        for (var i = 0; i < assets.length; i++) {
            if (assets[i].required && !new File(assets[i].file).exists) {
                missing.push(assets[i].layerName + "  ->  " + assets[i].file);
            }
        }
        if (missing.length === 0) return true;

        var msg = "PREFLIGHT FAILED — " + missing.length + " required PNG(s) are missing:\n\n";
        for (var j = 0; j < Math.min(missing.length, 12); j++) {
            msg += "  " + missing[j] + "\n";
        }
        if (missing.length > 12) {
            msg += "  ... and " + (missing.length - 12) + " more.\n";
        }
        msg += "\nFix: run node scripts/validate-jack-puppet-pack.mjs for the full list.";
        alert(msg);
        return false;
    }

    // =========================================================================
    // HELPER: GROUP CACHE + GET-OR-CREATE
    // =========================================================================
    var _groupCache = {};

    // Returns a LayerSet for the given path array, creating it if needed.
    // path [] returns the document itself.
    function getOrCreateGroup(doc, path) {
        if (path.length === 0) return doc;

        var key = path.join("|");
        if (_groupCache[key]) return _groupCache[key];

        var parentPath = path.slice(0, path.length - 1);
        var parent     = getOrCreateGroup(doc, parentPath);
        var name       = path[path.length - 1];

        // Check whether the group already exists in parent
        var collection = (parent === doc) ? doc.layerSets : parent.layerSets;
        for (var i = 0; i < collection.length; i++) {
            if (collection[i].name === name) {
                _groupCache[key] = collection[i];
                return collection[i];
            }
        }

        // Create it — new group lands at TOP of parent
        var g = collection.add();
        g.name = name;
        _groupCache[key] = g;
        return g;
    }

    // =========================================================================
    // HELPER: IMPORT ONE PNG INTO A GROUP
    // =========================================================================
    function importPNG(doc, asset) {
        var f = new File(asset.file);
        if (!f.exists) {
            // Non-required missing assets are silently skipped
            return null;
        }

        // Open source PNG as a temporary document
        var srcDoc   = app.open(f);
        var srcLayer = srcDoc.artLayers[0];

        // Convert Background layer to regular layer to preserve transparency
        if (srcLayer.isBackgroundLayer) {
            srcLayer.isBackgroundLayer = false;
        }

        // Duplicate into target document (placed at top of doc stack)
        var newLayer = srcLayer.duplicate(doc, ElementPlacement.PLACEATBEGINNING);

        // Close source without saving — source PNGs are never modified
        srcDoc.close(SaveOptions.DONOTSAVECHANGES);

        // Restore target document as active
        app.activeDocument = doc;

        // Move layer into its target group (at the top of that group)
        if (asset.groupPath.length > 0) {
            var targetGroup = getOrCreateGroup(doc, asset.groupPath);
            newLayer.move(targetGroup, ElementPlacement.PLACEATBEGINNING);
        }

        // Apply PSD layer name and initial visibility
        newLayer.name    = asset.layerName;
        newLayer.visible = asset.visible;

        return newLayer;
    }

    // =========================================================================
    // MAIN
    // =========================================================================
    function main() {
        // 1. Pre-flight
        if (!preflight(ASSETS)) {
            app.displayDialogs = origDialogs;
            return;
        }

        // 2. Create canvas
        var doc = app.documents.add(
            CANVAS_W,
            CANVAS_H,
            CANVAS_RES,
            "Jack Character Animator v1",
            NewDocumentMode.RGB,
            DocumentFill.TRANSPARENT,
            1.0   // pixel aspect ratio (square pixels)
        );
        app.activeDocument = doc;

        // Remove the default transparent layer Photoshop adds at creation.
        // We do this after group skeleton is built (PS requires >=1 layer).
        // We'll remove it at the end once real layers are imported.
        var defaultLayerName = "";
        try {
            if (doc.artLayers.length > 0) {
                defaultLayerName = doc.artLayers[0].name;
            }
        } catch (e) {}

        // 3. Build group skeleton
        //
        // Creation order within each parent = REVERSE of desired panel order.
        // Reason: each .add() pushes the new group to the TOP of its parent.
        // So: create bottom groups first; they get pushed down as more are added.
        //
        // Desired final panel order (top → bottom):
        //   Doc root:  Jack | Environment
        //   Jack:      Head | Body
        //   Body:      Right Arm | Left Arm | Tie | Torso
        //   Right Arm: Arm Resting | Arm Tie Fix
        //   Head:      Face | Head Base  (Head Base is imported directly later)
        //   Face:      Mouth | Left Eye | Right Eye | Left Eyebrow | Right Eyebrow
        //   Left Eye:  Left Upper Lid | Left Lower Lid  (lid groups for CA blink warp)
        //   Right Eye: Right Upper Lid | Right Lower Lid

        // -- Doc root (Environment first → ends below Jack) --
        getOrCreateGroup(doc, ["Environment"]);
        getOrCreateGroup(doc, ["Jack"]);

        // -- Jack children (Body first → ends below Head) --
        getOrCreateGroup(doc, ["Jack", "Body"]);
        getOrCreateGroup(doc, ["Jack", "Head"]);

        // -- Body children (Torso first → ends at bottom) --
        getOrCreateGroup(doc, ["Jack", "Body", "Tie"]);
        getOrCreateGroup(doc, ["Jack", "Body", "Left Arm"]);
        getOrCreateGroup(doc, ["Jack", "Body", "Right Arm"]);

        // -- Right Arm swap set (Arm Tie Fix first → ends below Arm Resting) --
        getOrCreateGroup(doc, ["Jack", "Body", "Right Arm", "Arm Tie Fix"]);
        getOrCreateGroup(doc, ["Jack", "Body", "Right Arm", "Arm Resting"]);

        // -- Head children (Face only — Head Base is imported as a layer, not a group) --
        getOrCreateGroup(doc, ["Jack", "Head", "Face"]);

        // -- Face children (Right Eyebrow first → ends at bottom) --
        getOrCreateGroup(doc, ["Jack", "Head", "Face", "Right Eyebrow"]);
        getOrCreateGroup(doc, ["Jack", "Head", "Face", "Left Eyebrow"]);
        getOrCreateGroup(doc, ["Jack", "Head", "Face", "Right Eye"]);
        getOrCreateGroup(doc, ["Jack", "Head", "Face", "Left Eye"]);
        getOrCreateGroup(doc, ["Jack", "Head", "Face", "Mouth"]);

        // -- Eye lid sub-groups for Character Animator blink warp --
        // Lower Lid first → ends below Upper Lid (Upper Lid is CA's blink target)
        getOrCreateGroup(doc, ["Jack", "Head", "Face", "Left Eye",  "Left Lower Lid"]);
        getOrCreateGroup(doc, ["Jack", "Head", "Face", "Left Eye",  "Left Upper Lid"]);
        getOrCreateGroup(doc, ["Jack", "Head", "Face", "Right Eye", "Right Lower Lid"]);
        getOrCreateGroup(doc, ["Jack", "Head", "Face", "Right Eye", "Right Upper Lid"]);

        // Hide the Arm Tie Fix swap group by default (only Arm Resting should show)
        var armTieFix = _groupCache["Jack|Body|Right Arm|Arm Tie Fix"];
        if (armTieFix) { armTieFix.visible = false; }

        // 4. Import all PNG assets
        var imported = 0;
        var skipped  = 0;
        for (var i = 0; i < ASSETS.length; i++) {
            var result = importPNG(doc, ASSETS[i]);
            if (result !== null) { imported++; } else { skipped++; }
        }

        // 5. Clean up default empty layer (now safe since real layers exist)
        try {
            var rootLayers = doc.artLayers;
            for (var ri = 0; ri < rootLayers.length; ri++) {
                var ln = rootLayers[ri].name;
                if (ln === defaultLayerName && (ln === "Layer 1" || ln === "Background" || ln === "")) {
                    rootLayers[ri].remove();
                    break;
                }
            }
        } catch (e) { /* ignore — harmless if it fails */ }

        // 6. Save PSD
        var psdFile = new File(PSD_OUTPUT);
        var psdDir  = psdFile.parent;
        if (!psdDir.exists) { psdDir.create(); }

        var psdOpts = new PhotoshopSaveOptions();
        psdOpts.layers                = true;
        psdOpts.embedColorProfile     = true;
        psdOpts.maximizeCompatibility = true;
        psdOpts.alphaChannels         = true;

        doc.saveAs(psdFile, psdOpts, false, Extension.LOWERCASE);

        // 7. Restore dialog mode
        app.displayDialogs = origDialogs;

        // 8. Summary alert
        var done  = "✅";  // checkmark where supported
        var msg   = "Jack puppet PSD assembled.\n\n";
        msg += "Layers imported : " + imported + "\n";
        msg += "Layers skipped  : " + skipped + " (optional assets not yet generated)\n\n";
        msg += "Saved to:\n" + PSD_OUTPUT + "\n\n";
        msg += "NEXT STEPS (see runbook):\n";
        msg += "1. Open the PSD in Adobe Character Animator.\n";
        msg += "2. Run Character > Rigging > Auto-tag puppet.\n";
        msg += "3. Position each layer on the canvas (rigging step).\n";
        msg += "4. Set up Triggers panel per jack_expression_system_v1.md.\n";
        msg += "5. Test lip sync with the Episode 02 voiceover MP3.\n\n";
        msg += "Full runbook: docs/animation/psd_assembly_runbook_v1.md";
        alert(msg);
    }

    main();

})();
// End of assemble-jack-character-animator-v1.jsx
