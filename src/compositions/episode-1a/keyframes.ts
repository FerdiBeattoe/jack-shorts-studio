export const EPISODE_1A_DURATION_SECONDS = 38.244;
export const EPISODE_1A_VISUAL_STEPS_PER_SEGMENT = 6;

export interface Episode1AKeyframe {
  id: string;
  image: string;
  caption: string;
  focusX: number;
  focusY: number;
  scaleStart: number;
  scaleEnd: number;
  rotateStart: number;
  rotateEnd: number;
}

export const EPISODE_1A_KEYFRAMES: Episode1AKeyframe[] = [
  {
    id: "master_01",
    image: "episode-1a/frames/master_01.png",
    caption: "Update on the Doug situation.",
    focusX: 0,
    focusY: 0,
    scaleStart: 1.0,
    scaleEnd: 1.035,
    rotateStart: 0,
    rotateEnd: -0.2,
  },
  {
    id: "master_02",
    image: "episode-1a/frames/master_02.png",
    caption: "Very normal.",
    focusX: -8,
    focusY: -4,
    scaleStart: 1.025,
    scaleEnd: 1.055,
    rotateStart: -0.15,
    rotateEnd: 0.15,
  },
  {
    id: "master_03",
    image: "episode-1a/frames/master_03.png",
    caption: "Very ethical.",
    focusX: 8,
    focusY: -8,
    scaleStart: 1.03,
    scaleEnd: 1.065,
    rotateStart: 0.15,
    rotateEnd: -0.1,
  },
  {
    id: "master_04",
    image: "episode-1a/frames/master_04.png",
    caption: "Email opened. Link clicked.",
    focusX: -5,
    focusY: 3,
    scaleStart: 1.02,
    scaleEnd: 1.06,
    rotateStart: 0,
    rotateEnd: 0.2,
  },
  {
    id: "master_05",
    image: "episode-1a/frames/master_05.png",
    caption: "Reply received.",
    focusX: 6,
    focusY: -5,
    scaleStart: 1.025,
    scaleEnd: 1.07,
    rotateStart: 0.1,
    rotateEnd: -0.15,
  },
  {
    id: "master_06",
    image: "episode-1a/frames/master_06.png",
    caption: "Quietly panicking in business clothes.",
    focusX: 0,
    focusY: -10,
    scaleStart: 1.0,
    scaleEnd: 1.055,
    rotateStart: -0.1,
    rotateEnd: 0.1,
  },
];
