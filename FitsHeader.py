from astropy.io import fits


def getFitsHeader(name):
    return fits.getheader(name)

