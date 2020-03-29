import logging

import librosa
from scipy import signal
from skimage.filters import gaussian
from skimage.io import imread, imsave
from sklearn.preprocessing import normalize


from utils import set_logger

logger = logging.getLogger(__name__)
set_logger(logger)

y, sr = librosa.load("data/input/drum-break.wav")

# Downsampling audio to 24 fps since we want to
# make a 24 fps video at the end
downsampled = signal.resample(y, int((24 / sr) * y.shape[0]))

# can skip if wanna go crazier and more surprising
normalized = normalize(downsampled.reshape(1, -1))
normalized = normalized[0]
normalized = normalized + min(normalized)

input_image = imread("data/input/sample.jpg")
multiplier = 20

for idx, val in enumerate(normalized):
    sigma = abs(val) * multiplier

    output_frame = gaussian(input_image, sigma=sigma)
    fname = f"data/output/amplitude_blur/{idx:03}.png"

    imsave(fname, output_frame)
    logger.info(f"Saved {fname} with Sigma {sigma}")
