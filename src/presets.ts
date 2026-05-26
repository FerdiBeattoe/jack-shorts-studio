export const VIDEO_PRESETS = {
  "Portrait-1080p": {
    width: 1080,
    height: 1920,
    fps: 30,
  },
} as const;

export type PresetName = keyof typeof VIDEO_PRESETS;
