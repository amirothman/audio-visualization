import logging

import librosa
from scipy import signal
from sklearn.preprocessing import normalize
from skimage.exposure import adjust_gamma
from skimage.transform import resize
from skimage.io import imread, imsave

from utils import set_logger

logger = logging.getLogger(__name__)
set_logger(logger)

y, sr = librosa.load("data/input/bakar.mp3")

# Downsampling audio to 24 fps since we want to
# make a 24 fps video at the end
downsampled = signal.resample(y, int((24 / sr) * y.shape[0]))

# can skip if wanna go crazier and more surprising
normalized = normalize(downsampled.reshape(1, -1))
normalized = normalized[0]

input_image_ = imread("data/input/api.jpg")
input_image = resize(input_image_, (480, 640))

constant = 20

for idx, val in enumerate(normalized):
    output_frame = adjust_gamma(input_image, gain=constant * val)
    fname = f"data/output/amplitude_viz/{idx:03}.png"
    imsave(fname, output_frame)
    logger.info(f"Saved {fname}")
