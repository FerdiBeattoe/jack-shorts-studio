import React from "react";
import { Img, interpolate, useCurrentFrame } from "remotion";

interface KenBurnsParams {
  scaleStart: number;
  scaleEnd: number;
  translateXStart: number;
  translateXEnd: number;
  translateYStart: number;
  translateYEnd: number;
}

interface JackSceneProps {
  imageSrc: string;
  durationInFrames: number;
  kenBurns?: Partial<KenBurnsParams>;
}

const DEFAULT_KEN_BURNS: KenBurnsParams = {
  scaleStart: 1.0,
  scaleEnd: 1.06,
  translateXStart: 0,
  translateXEnd: 0,
  translateYStart: 0,
  translateYEnd: -10,
};

export const JackScene: React.FC<JackSceneProps> = ({
  imageSrc,
  durationInFrames,
  kenBurns = {},
}) => {
  const frame = useCurrentFrame();
  const params: KenBurnsParams = { ...DEFAULT_KEN_BURNS, ...kenBurns };

  // progress 0→1 over the beat
  const progress = durationInFrames > 1 ? frame / (durationInFrames - 1) : 0;

  const scale = interpolate(progress, [0, 1], [params.scaleStart, params.scaleEnd], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  const translateX = interpolate(
    progress,
    [0, 1],
    [params.translateXStart, params.translateXEnd],
    { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
  );

  const translateY = interpolate(
    progress,
    [0, 1],
    [params.translateYStart, params.translateYEnd],
    { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
  );

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        overflow: "hidden",
        backgroundColor: "#1a1a1a",
      }}
    >
      <Img
        src={imageSrc}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale}) translate(${translateX}px, ${translateY}px)`,
          transformOrigin: "center center",
          display: "block",
        }}
      />
    </div>
  );
};
