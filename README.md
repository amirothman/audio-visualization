# Audio Visualization Experiments

* Requeirements:
    - python
    - librosa
    - scikit-image
    - ffmpeg (working and in the path)

* Analyze audio with librosa to get audio features
* Downsample the audio to match the video frame rate
    - Can use scipy.signal.resample
* Feed that data as an argument in a scikit-image method
    - normalize/preprocess as necessary according to the arguments requirement
* The output images are then merged into a silent video
    - [Refer here](https://hamelot.io/visualization/using-ffmpeg-to-convert-a-set-of-images-into-a-video/)
    - example:
    
        ffmpeg -r 24 -f image2 -i output/frame_%03d.png test-2.mp4

* The silent video is then merged back with the original audio
    - [Refer here](https://superuser.com/questions/277642/how-to-merge-audio-and-video-file-in-ffmpeg)
    - example:

        ffmpeg -i test.mp4 -i drum-break.wav -c:v copy -c:a aac combined.mp4