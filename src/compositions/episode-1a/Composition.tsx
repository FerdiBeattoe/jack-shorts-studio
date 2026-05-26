import React from "react";
import { AbsoluteFill, Audio, Series, staticFile } from "remotion";
import { JackCaption } from "../../components/JackCaption";
import { MasterKeyframeScene } from "../../components/MasterKeyframeScene";
import { secondsToFrames } from "../../config";
import { createComposition } from "../../utils/createComposition";
import {
  EPISODE_1A_DURATION_SECONDS,
  EPISODE_1A_KEYFRAMES,
  EPISODE_1A_VISUAL_STEPS_PER_SEGMENT,
} from "./keyframes";

const Episode1AComposition: React.FC = () => {
  const segmentDurationSeconds = EPISODE_1A_DURATION_SECONDS / EPISODE_1A_KEYFRAMES.length;

  return (
    <AbsoluteFill style={{ backgroundColor: "#111111" }}>
      <Audio src={staticFile("episode-1a/audio/episode_1a_voice.mp3")} />

      <Series>
        {EPISODE_1A_KEYFRAMES.map((keyframe, index) => {
          const isLast = index === EPISODE_1A_KEYFRAMES.length - 1;
          const durationInFrames = isLast
            ? secondsToFrames(
                EPISODE_1A_DURATION_SECONDS - segmentDurationSeconds * index,
              )
            : secondsToFrames(segmentDurationSeconds);

          return (
            <Series.Sequence key={keyframe.id} durationInFrames={durationInFrames}>
              <MasterKeyframeScene
                keyframe={keyframe}
                durationInFrames={durationInFrames}
                visualSteps={EPISODE_1A_VISUAL_STEPS_PER_SEGMENT}
              />
              <JackCaption text={keyframe.caption} />
            </Series.Sequence>
          );
        })}
      </Series>
    </AbsoluteFill>
  );
};

export const Episode1A = createComposition({
  id: "Episode1A",
  component: Episode1AComposition,
  durationInSeconds: EPISODE_1A_DURATION_SECONDS,
  preset: "Portrait-1080p",
});
