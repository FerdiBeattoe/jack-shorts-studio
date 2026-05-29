import React from "react";
import { AbsoluteFill, Audio, Series, staticFile } from "remotion";
import { secondsToFrames } from "../../config";
import { JackScene } from "../../components/JackScene";
import { JackCaption } from "../../components/JackCaption";
import { createComposition } from "../../utils/createComposition";
import { BEATS, TOTAL_DURATION_SECONDS } from "./timing";

const DougEp02Composition: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#1a1a1a" }}>
      {/* Voiceover plays across the full 38-second composition */}
      <Audio src={staticFile("audio/doug_episode_02_voice_current.mp3")} />

      <Series>
        {BEATS.map((beat) => {
          const durationInFrames = secondsToFrames(beat.endSeconds - beat.startSeconds);
          return (
            <Series.Sequence key={beat.id} durationInFrames={durationInFrames}>
              <JackScene
                imageSrc={staticFile(beat.image)}
                durationInFrames={durationInFrames}
                kenBurns={beat.kenBurns}
              />
              <JackCaption text={beat.caption} />
            </Series.Sequence>
          );
        })}
      </Series>
    </AbsoluteFill>
  );
};

export const DougEp02 = createComposition({
  id: "DougEp02",
  component: DougEp02Composition,
  durationInSeconds: TOTAL_DURATION_SECONDS,
  preset: "Portrait-1080p",
});
