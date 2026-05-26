import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

interface JackCaptionProps {
  text: string;
}

export const JackCaption: React.FC<JackCaptionProps> = ({ text }) => {
  const frame = useCurrentFrame();

  // Slide up + fade in over first 6 frames
  const opacity = interpolate(frame, [0, 6], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  const translateY = interpolate(frame, [0, 6], [14, 0], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        // 360px from the bottom keeps captions above the TikTok UI safe-zone (bottom 300px)
        bottom: 360,
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
        paddingLeft: 100,
        paddingRight: 100,
        opacity,
        transform: `translateY(${translateY}px)`,
        zIndex: 10,
      }}
    >
      <div
        style={{
          backgroundColor: "rgba(0, 0, 0, 0.72)",
          borderRadius: 18,
          paddingTop: 28,
          paddingBottom: 28,
          paddingLeft: 44,
          paddingRight: 44,
          maxWidth: 880,
        }}
      >
        <p
          style={{
            margin: 0,
            color: "#ffffff",
            fontSize: 66,
            fontWeight: 800,
            lineHeight: 1.22,
            textAlign: "center",
            fontFamily: "'Arial Black', Arial, sans-serif",
            letterSpacing: -0.5,
            textShadow: "0 2px 10px rgba(0,0,0,0.55)",
          }}
        >
          {text}
        </p>
      </div>
    </div>
  );
};
