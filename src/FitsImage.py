import os
from multiprocessing import shared_memory

import numpy as np
from PIL import Image, ImageEnhance
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from astropy.visualization import AsinhStretch
from colour_demosaicing import (
    demosaicing_CFA_Bayer_bilinear)
from photutils.detection import IRAFStarFinder
from scipy.optimize import root
from skimage import io, exposure
from skimage.util import img_as_float32
# from astropy.stats import mad_std


class FitsImage:
    def __init__(self):
        self.imageData = None
        self.imageStetchedData = None
        self.imageDisplay = None
        self.imageDisplaySaturated = None
        self.img_format = None
        self.fits_header = None
        self.width = 0
        self.height = 0

    def fromFile(self, directory):
        self.img_format = os.path.splitext(directory)[1].lower()

        imageData = None
        if self.img_format == ".fits" or self.img_format == ".fit" or self.img_format == ".fts":
            hdul = fits.open(directory)
            imageData = hdul[0].data
            self.fits_header = hdul[0].header
            hdul.close()

            if len(imageData.shape) == 3:
                imageData = np.moveaxis(imageData, 0, -1)

        else:
            imageData = io.imread(directory)
            self.fits_header = fits.Header()

        # Reshape greyscale picture to shape (y,x,1)
        if len(imageData.shape) == 2:
            imageData = np.array([imageData])
            imageData = np.moveaxis(imageData, 0, -1)

        # Use 32 bit float with range (0,1) for internal calculations
        imageData = img_as_float32(imageData)

        if np.min(imageData) < 0 or np.max(imageData > 1):
            imageData = exposure.rescale_intensity(imageData, out_range=(0, 1))

        self.imageData = imageData
        self.width = self.imageData.shape[1]
        self.height = self.imageData.shape[0]
        self.createDisplayImage()
        return

    def createDisplayImage(self):

        self.imageData = demosaicing_CFA_Bayer_bilinear(np.squeeze(self.imageData), self.fits_header['BAYERPAT'])

        imageDisplay = self.stretch()
        self.imageStetchedData = imageDisplay
        imageDisplay = imageDisplay * 255

        if imageDisplay.shape[2] == 1:
            self.imageDisplay = Image.fromarray(imageDisplay[:, :, 0].astype(np.uint8))
        else:
            self.imageDisplay = Image.fromarray(imageDisplay.astype(np.uint8))

        self.saturateImage()

        return

    def stretch(self):
        bg, sigma = (0.25, 3)
        return stretch(self.imageData, bg, sigma)

    def get_local_median(self, img_point):
        sample_radius = 25
        y1 = int(np.amax([img_point[1] - sample_radius, 0]))
        y2 = int(np.amin([img_point[1] + sample_radius, self.height]))
        x1 = int(np.amax([img_point[0] - sample_radius, 0]))
        x2 = int(np.amin([img_point[0] + sample_radius, self.width]))

        if self.imageData.shape[-1] == 3:
            R = sigma_clipped_stats(data=self.imageData[y1:y2, x1:x2, 0], cenfunc="median", stdfunc="std", grow=4)[1]
            G = sigma_clipped_stats(data=self.imageData[y1:y2, x1:x2, 1], cenfunc="median", stdfunc="std", grow=4)[1]
            B = sigma_clipped_stats(data=self.imageData[y1:y2, x1:x2, 2], cenfunc="median", stdfunc="std", grow=4)[1]

            return [R, G, B]

        if self.imageData.shape[-1] == 1:
            L = sigma_clipped_stats(data=self.imageData[x1:x2, y1:y2, 0], cenfunc="median", stdfunc="std", grow=4)[1]
            return L

    def saturateImage(self):
        self.imageDisplaySaturated = self.imageDisplay

        if self.imageData.shape[-1] == 3:
            self.imageDisplaySaturated = ImageEnhance.Color(self.imageDisplay)
            self.imageDisplaySaturated = self.imageDisplaySaturated.enhance(1.25)

        return

    def analyse(self):

        data = self.imageData
        # image = self.imageStetchedData #stretch(self.imageData, 0.25, 3)
        mean, median, std = sigma_clipped_stats(data, sigma=3.0)
        threshold = median + (5.0 * std)

        dao = IRAFStarFinder(threshold=threshold, fwhm=3.0)
        sources = dao.find_stars(data - median)
        print(sources)


def stretch_channel(shm_name, c, bg, sigma, shape, dtype):
    existing_shm = shared_memory.SharedMemory(name=shm_name)
    channels = np.ndarray(shape, dtype, buffer=existing_shm.buf)  # [:,:,channel_idx]
    channel = channels[:, :, c]

    try:
        indx_clip = np.logical_and(channel < 1.0, channel > 0.0)
        median = np.median(channel[indx_clip])
        mad = np.median(np.abs(channel[indx_clip] - median))

        shadow_clipping = np.clip(median - sigma * mad, 0, 1.0)
        highlight_clipping = 1.0

        midtone = MTF((median - shadow_clipping) / (highlight_clipping - shadow_clipping), bg)

        channel[channel <= shadow_clipping] = 0.0
        channel[channel >= highlight_clipping] = 1.0

        indx_inside = np.logical_and(channel > shadow_clipping, channel < highlight_clipping)

        channel[indx_inside] = (channel[indx_inside] - shadow_clipping) / (highlight_clipping - shadow_clipping)

        channel = MTF(channel, midtone)

    except:
        print("Error while stretching channel")
    finally:
        existing_shm.close()


def stretch(data, bg, sigma):
    shm = shared_memory.SharedMemory(create=True, size=data.nbytes)
    copy = np.ndarray(data.shape, dtype=data.dtype, buffer=shm.buf)
    np.copyto(copy, data)

    for c in range(copy.shape[-1]):
        stretch_channel(shm.name, c, bg, sigma, copy.shape, copy.dtype)

    copy = np.copy(copy)

    shm.close()
    shm.unlink()

    return copy


def MTF(data, midtone):
    if type(data) is np.ndarray:
        data[:] = (midtone - 1) * data[:] / ((2 * midtone - 1) * data[:] - midtone)
    else:
        data = (midtone - 1) * data / ((2 * midtone - 1) * data - midtone)

    return data


def asinh_stretch(data, bg, sigma):
    data = data / np.max(data)
    median = np.median(data)
    deviation_from_median = np.mean(np.abs(data - median))

    shadow_clipping = np.clip(median - sigma * deviation_from_median, 0, 1.0)
    highlight_clipping = 1.0

    # Use rootfinding to find correct factor a
    a = root(asinhfunc_root, 0.5, ((median - shadow_clipping) / (highlight_clipping - shadow_clipping), bg),
             method='lm')
    a = np.abs(a.x)

    data[data <= shadow_clipping] = 0.0
    data[data >= highlight_clipping] = 1.0

    indx_inside = data > shadow_clipping

    data[indx_inside] = (data[indx_inside] - shadow_clipping) / (highlight_clipping - shadow_clipping)

    asinh = AsinhStretch(a)
    data = asinh(data)

    return data


def asinhfunc_root(a, x, y):
    return np.arcsinh(x / a) / np.arcsinh(1 / a) - y
