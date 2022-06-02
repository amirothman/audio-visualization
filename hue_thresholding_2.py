import logging
from threading import Thread

import librosa
import numpy as np
from scipy import signal
from skimage import img_as_uint
from skimage.color import rgb2hsv, hsv2rgb
from skimage.io import imread, imsave
from skimage.transform import resize

from utils import set_logger


logger = logging.getLogger("hue_thresholding")
set_logger(logger)


def hue_level(input_image, level=0.3):
    hsv_img = rgb2hsv(input_image)
    saturation_img = hsv_img[:, :, 1]
    saturation_adjusted = saturation_img + level

    hsv_img[:, :, 1] = saturation_adjusted
    return hsv2rgb(hsv_img)


def build_image(input_image, val, idx):

    if val < 0.2:
        level = val * 0.2 * 0.7
    else:
        level = min(float(np.exp(val)) * 0.1 + 0.5, 1.0) * 0.7

    output_frame = hue_level(input_image, level=level)
    fname = f"data/output/hue_leveling/{idx:03}-b.png"
    imsave(fname, img_as_uint(output_frame))
    logger.info(f"Saved {fname} level: {level}")


y, sr = librosa.load("data/output/audio/bass_only.wav")

# Downsampling audio to 24 fps since we want to
# make a 24 fps video at the end
downsampled = signal.resample(y, int((24 / sr) * y.shape[0]))

# can skip if wanna go crazier and more surprising
min_value = np.max(np.abs(downsampled.reshape(1, -1)))
normalized = downsampled / min_value

# input_image = imread("data/input/sample.jpg")
input_image_ = imread("data/input/api.jpg")
input_image = resize(input_image_, (480, 640))

joins = []

for idx, val in enumerate(normalized):
    th = Thread(target=lambda: build_image(input_image, val, idx))

    th.start()
    joins.append(th)
    if idx > 0 and idx % 6 == 0:
        for thread in joins:
            thread.join()
        joins = []

if len(joins):
    for thread in joins:
        thread.join()
