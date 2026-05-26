export const DEFAULT_FPS = 30;

export const secondsToFrames = (seconds: number, fps: number = DEFAULT_FPS): number =>
  Math.round(seconds * fps);

export const framesToSeconds = (frames: number, fps: number = DEFAULT_FPS): number =>
  frames / fps;
