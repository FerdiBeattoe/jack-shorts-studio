import React from "react";
import { registerRoot } from "remotion";
import { DougEp02 } from "./compositions/doug-ep02/Composition";
import { Episode1A } from "./compositions/episode-1a/Composition";

const RemotionRoot: React.FC = () => (
  <>
    <DougEp02 />
    <Episode1A />
  </>
);

registerRoot(RemotionRoot);
