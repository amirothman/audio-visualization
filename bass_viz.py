import logging

import librosa
from scipy.signal import butter, lfilter, resample
from sklearn.preprocessing import normalize
from skimage.exposure import adjust_gamma
from skimage.io import imread, imsave

# import soundfile as sf

from utils import set_logger

logger = logging.getLogger("bass_viz")
set_logger(logger)

# A bunch of these code came from
# here https://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter/12233959#12233959


def get_lowpass_filter(lowcut, sample_rate, order):
    # Nyquist frequenz. Erinnerst du noch
    # an Digitale Signalverarbeitung ?? Hahahaha..
    nyq_freq = 0.5 * sample_rate
    low = lowcut / nyq_freq
    b, a = butter(order, low, btype='lowpass')
    return b, a


def lowpass(data, lowcut, sample_rate, order=5):
    b, a = get_lowpass_filter(lowcut, sample_rate, order)
    y = lfilter(b, a, data)
    return y


signal, sample_rate = librosa.load("data/input/drum-break.wav")
lowcut = 200
filtered_signal = lowpass(signal, lowcut, sample_rate)
logger.info(f"Filter signal with lowpass filter at {lowcut} Hz")

downsampled = resample(signal, int((24 / sample_rate) * signal.shape[0]))
normalized = normalize(downsampled.reshape(1, -1))
normalized = normalized[0]

input_image = imread("data/input/sample.jpg")
constant = 10

for idx, val in enumerate(normalized):
    output_frame = adjust_gamma(input_image, gain=constant * val)
    fname = f"data/output/bass_viz/{idx:03}.png"
    imsave(fname, output_frame)
    logger.info(f"Saved {fname}")
