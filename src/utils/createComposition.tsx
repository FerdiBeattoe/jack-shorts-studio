import React from "react";
import { Composition } from "remotion";
import { secondsToFrames } from "../config";
import { VIDEO_PRESETS, type PresetName } from "../presets";

interface CreateCompositionOptions {
  id: string;
  component: React.ComponentType;
  durationInSeconds: number;
  preset: PresetName;
}

export const createComposition = ({
  id,
  component,
  durationInSeconds,
  preset,
}: CreateCompositionOptions) => {
  const { fps, width, height } = VIDEO_PRESETS[preset];
  return () => (
    <Composition
      id={id}
      component={component}
      durationInFrames={secondsToFrames(durationInSeconds, fps)}
      fps={fps}
      width={width}
      height={height}
    />
  );
};
