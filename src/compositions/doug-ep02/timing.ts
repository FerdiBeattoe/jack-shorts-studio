export interface KenBurnsConfig {
  scaleStart?: number;
  scaleEnd?: number;
  translateXStart?: number;
  translateXEnd?: number;
  translateYStart?: number;
  translateYEnd?: number;
}

export interface Beat {
  id: string;
  startSeconds: number;
  endSeconds: number;
  image: string;
  caption: string;
  kenBurns?: KenBurnsConfig;
}

// Source: assets/.../09_pipeline_specs/doug_episode_02_timing_map.json
// Beat 3 uses jack_01 as V1 fallback — see docs/missing_assets.md
export const BEATS: Beat[] = [
  {
    id: "beat_01",
    startSeconds: 0.0,
    endSeconds: 2.8,
    image: "images/jack_01_forward_calculating.png",
    caption: "Update on the Doug situation.",
    kenBurns: { scaleStart: 1.0, scaleEnd: 1.04, translateXStart: 0, translateXEnd: -8, translateYStart: 0, translateYEnd: -6 },
  },
  {
    id: "beat_02",
    startSeconds: 2.8,
    endSeconds: 6.8,
    image: "images/jack_01_forward_calculating.png",
    caption: "Very normal. Very ethical.",
    kenBurns: { scaleStart: 1.04, scaleEnd: 1.08, translateXStart: -8, translateXEnd: 8, translateYStart: -6, translateYEnd: -4 },
  },
  {
    id: "beat_03",
    startSeconds: 6.8,
    endSeconds: 11.5,
    image: "images/jack_01_forward_calculating.png",
    caption: "Email opened. Link clicked. Reply received.",
    // V1 FALLBACK: crm_monitor_closeup asset is missing. Using jack_01 still.
    // Replace with: images/crm_monitor_closeup.png when generated.
    kenBurns: { scaleStart: 1.06, scaleEnd: 1.0, translateXStart: 8, translateXEnd: 0, translateYStart: 0, translateYEnd: 8 },
  },
  {
    id: "beat_04",
    startSeconds: 11.5,
    endSeconds: 17.0,
    image: "images/jack_02_tie_fix_confident_smirk.png",
    caption: "Either Doug is interested...",
    kenBurns: { scaleStart: 1.0, scaleEnd: 1.05, translateXStart: 0, translateXEnd: -10, translateYStart: 0, translateYEnd: -5 },
  },
  {
    id: "beat_05",
    startSeconds: 17.0,
    endSeconds: 21.0,
    image: "images/jack_02_tie_fix_confident_smirk.png",
    caption: "or Doug is tracking me back.",
    kenBurns: { scaleStart: 1.05, scaleEnd: 1.08, translateXStart: -10, translateXEnd: 10, translateYStart: -5, translateYEnd: 0 },
  },
  {
    id: "beat_06",
    startSeconds: 21.0,
    endSeconds: 28.5,
    image: "images/jack_02_tie_fix_confident_smirk.png",
    caption: "Spiritually? The evidence is overwhelming.",
    kenBurns: { scaleStart: 1.02, scaleEnd: 1.07, translateXStart: 5, translateXEnd: -5, translateYStart: 0, translateYEnd: -8 },
  },
  {
    id: "beat_07",
    startSeconds: 28.5,
    // Extended to match MP3 duration: 49.791610s → ceiling at 30fps → 1494 frames → 49.8s
    // The voiceover runs past the original 38s script endpoint.
    // TODO: expand caption map to cover 28.5s–49.8s once full timing is known.
    endSeconds: 49.8,
    image: "images/jack_03_turning_to_monitor.png",
    caption: "Quietly panicking in business clothes.",
    kenBurns: { scaleStart: 1.0, scaleEnd: 1.06, translateXStart: -5, translateXEnd: 5, translateYStart: 0, translateYEnd: -6 },
  },
];

// MP3 exact duration: 49.791610s → ceil(49.791610 * 30) / 30 = 1494 frames / 30fps = 49.8s
export const TOTAL_DURATION_SECONDS = 49.8;
