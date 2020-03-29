#!/bin/bash

# ffmpeg -r 24 -f image2 -i data/output/amplitude_viz/%03d.png data/output/amplitude_viz/combined-images.mp4

ffmpeg -r 24 -f image2 -i $1 $2
