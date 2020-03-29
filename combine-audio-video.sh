#!/bin/bash

# ffmpeg -i data/output/amplitude_viz/combined-images.mp4 -i data/input/drum-break.wav -c:v copy -c:a aac data/output/amplitude_viz/combined-with-audio.mp4

ffmpeg -i $1 -i $2 -c:v copy -c:a aac $3
