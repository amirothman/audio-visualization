from skimage.util import img_as_float
from skimage import io, filters

# from skimage.viewer import ImageViewer
import numpy as np


def split_image_into_channels(image):
    """Look at each image separately"""
    red_channel = image[:, :, 0]
    green_channel = image[:, :, 1]
    blue_channel = image[:, :, 2]
    return red_channel, green_channel, blue_channel


def merge_channels(red, green, blue):
    """Merge channels back into an image"""
    return np.stack([red, green, blue], axis=2)


def sharpen(image, a, b):
    """Sharpening an image: Blur and then subtract from original"""
    blurred = filters.gaussian(image, sigma=10, multichannel=True)
    sharper = np.clip(image * a - blurred * b, 0, 1.0)
    return sharper


def channel_adjust(channel, values):
    # preserve the original size, so we can reconstruct at the end
    orig_size = channel.shape
    # flatten the image into a single array
    flat_channel = channel.flatten()

    # this magical numpy function takes the values in flat_channel
    # and maps it from its range in [0, 1] to its new squeezed and
    # stretched range
    adjusted = np.interp(flat_channel, np.linspace(0, 1, len(values)), values)

    # put back into the original image shape
    return adjusted.reshape(orig_size)


def gotham(
    original_image,
    r_boost_upper=1,
    b_adjusted_upper=1,
    blurriness=1.3,
    subtraction=0.3,
    amount_bluer_blacks=0.03,
):
    original_image = img_as_float(original_image)

    r, g, b = split_image_into_channels(original_image)

    # np.linspace second argument
    r_boost_lower = channel_adjust(r, np.linspace(0, r_boost_upper))

    # amount of bluer_blacks
    bluer_blacks = merge_channels(
        r_boost_lower, g, np.clip(b + amount_bluer_blacks, 0, 1.0)
    )

    # amount blurriness, and subtraction
    sharper = sharpen(bluer_blacks, blurriness, subtraction)

    r, g, b = split_image_into_channels(sharper)
    # np.linspace second argument
    b_adjusted = channel_adjust(b, np.linspace(0, b_adjusted_upper))
    return merge_channels(r, g, b_adjusted)


if __name__ == "__main__":
    original_image = io.imread("data/input/sample.jpg")
    output = gotham(original_image, b_adjusted_upper=3)
    io.imsave("data/output/image-experiment/gotham.jpg", output)
