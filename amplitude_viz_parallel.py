import logging
from threading import Thread
import librosa
from scipy import signal
from sklearn.preprocessing import normalize
from skimage.exposure import adjust_gamma
from skimage.transform import resize
from skimage.io import imread, imsave

from utils import set_logger

logger = logging.getLogger(__name__)
set_logger(logger)


def build_image(input_image, constant, val, idx):
    output_frame = adjust_gamma(input_image, gain=constant * val)
    fname = f"data/output/amplitude_viz/{idx:04}-c.png"
    imsave(fname, output_frame)
    logger.info(f"Saved {fname}")


y, sr = librosa.load("data/output/audio/bass_only.wav")

# Downsampling audio to 24 fps since we want to
# make a 24 fps video at the end
downsampled = signal.resample(y, int((24 / sr) * y.shape[0]))

# can skip if wanna go crazier and more surprising
normalized = normalize(downsampled.reshape(1, -1))
normalized = normalized[0]

input_image_ = imread("data/input/api.jpg")
input_image = resize(input_image_, (480, 640))

constant = 5

joins = []

for idx, val in enumerate(normalized):
    th = Thread(target=lambda: build_image(input_image, constant, val, idx))
    th.start()
    joins.append(th)
    if idx > 0 and idx % 6 == 0:
        for thread in joins:
            thread.join()
        joins = []

if len(joins):
    for thread in joins:
        thread.join()
