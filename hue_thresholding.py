import logging

import librosa
import numpy as np
from scipy import signal
from skimage import img_as_uint
from skimage.color import rgb2hsv
from skimage.io import imread, imsave

from utils import set_logger


def hue_threshold(input_image, threshold):
    hsv_img = rgb2hsv(input_image)
    hue_img = hsv_img[:, :, 0]

    return hue_img > threshold


logger = logging.getLogger("hue_thresholding")
set_logger(logger)

y, sr = librosa.load("data/input/drum-break.wav")

# Downsampling audio to 24 fps since we want to
# make a 24 fps video at the end
downsampled = signal.resample(y, int((24 / sr) * y.shape[0]))

# can skip if wanna go crazier and more surprising
min_value = np.max(np.abs(downsampled.reshape(1, -1)))
normalized = downsampled / min_value

input_image = imread("data/input/sample.jpg")

for idx, val in enumerate(normalized):
    output_frame = hue_threshold(input_image, abs(val))
    fname = f"data/output/hue_thresholding/{idx:03}.png"
    imsave(fname, img_as_uint(output_frame))
    logger.info(f"Saved {fname} threshold: {val}")
