import React from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import type { Episode1AKeyframe } from "../compositions/episode-1a/keyframes";

interface MasterKeyframeSceneProps {
  keyframe: Episode1AKeyframe;
  durationInFrames: number;
  visualSteps: number;
}

export const MasterKeyframeScene: React.FC<MasterKeyframeSceneProps> = ({
  keyframe,
  durationInFrames,
  visualSteps,
}) => {
  const frame = useCurrentFrame();
  const rawProgress = durationInFrames > 1 ? frame / (durationInFrames - 1) : 0;
  const steppedProgress =
    visualSteps > 1 ? Math.round(rawProgress * (visualSteps - 1)) / (visualSteps - 1) : rawProgress;

  const scale = interpolate(
    steppedProgress,
    [0, 1],
    [keyframe.scaleStart, keyframe.scaleEnd],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  const translateX = interpolate(steppedProgress, [0, 1], [0, keyframe.focusX], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const translateY = interpolate(steppedProgress, [0, 1], [0, keyframe.focusY], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const rotate = interpolate(
    steppedProgress,
    [0, 1],
    [keyframe.rotateStart, keyframe.rotateEnd],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#111111", overflow: "hidden" }}>
      <Img
        src={staticFile(keyframe.image)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `translate(${translateX}px, ${translateY}px) scale(${scale}) rotate(${rotate}deg)`,
          transformOrigin: "center center",
        }}
      />
    </AbsoluteFill>
  );
};
