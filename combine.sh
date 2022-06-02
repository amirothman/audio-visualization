#!/bin/bash

ffmpeg -r 24 -f image2 -i $1/frame-%04d.png $1/combined-images.mp4
ffmpeg -i $1/combined-images.mp4 -i $2 -c:v copy -c:a aac $1/combined-with-audio.mp4
