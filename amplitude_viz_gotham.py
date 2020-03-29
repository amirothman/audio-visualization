import logging

import librosa
from scipy import signal
from sklearn.preprocessing import normalize
from skimage.io import imread, imsave

from gotham import gotham
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

input_image = imread("data/input/sample.jpg")

r_boost_upper_multiplier = 15
b_adjusted_upper_multiplier = 12
blurriness_multiplier = 20
subtraction_multiplier = 0.8
amount_bluer_blacks_multpilier = 0.01

for idx, val in enumerate(normalized):
    output_frame = gotham(
        input_image,
        r_boost_upper=r_boost_upper_multiplier * val,
        b_adjusted_upper=b_adjusted_upper_multiplier * val,
        blurriness=blurriness_multiplier * val,
        # subtraction=subtraction_multiplier * val,
        # amount_bluer_blacks=amount_bluer_blacks_multpilier * val,
    )
    fname = f"data/output/gotham_amplitude_viz/{idx:03}.png"

    imsave(fname, output_frame)
    logger.info(f"Saved {fname}")
