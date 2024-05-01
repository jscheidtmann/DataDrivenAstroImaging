from astropy.io import fits
import logging
import sys


def createMinimalFits(column, dest):
    # Create a minimal header
    header = fits.Header()
    header['SIMPLE'] = True  # Required keyword
    header['BITPIX'] = 8     # Required keyword, set to 8-bit per pixel
    header['NAXIS'] = 0      # No data, set NAXIS to 0
    header[column] = 1

    # Create an empty Primary HDU with the header
    hdu = fits.PrimaryHDU(header=header)

    # Write to a FITS file
    hdu.writeto(dest, overwrite=True)


def dropPictureData(src, dest):
    h = fits.getheader(src)

    hdu = fits.PrimaryHDU(header=h)
    hdu.writeto(dest, overwrite=True)


def showHeader(src):
    h = fits.getheader(src).cards
    for item in h:
        print(item)

if __name__ == "__main__":
    chdlr = logging.StreamHandler()
    logging.getLogger().addHandler(chdlr)
    logging.getLogger().info("Test")
    logging.getLogger().setLevel(logging.DEBUG)  

    showHeader(sys.argv[1])

    # createMinimalFits('AAA', 'fits/A.fits')
    # createMinimalFits('BBB', 'fits/B.fits')
    # createMinimalFits('CCC', 'fits/C.fits')

    # LIGHT
    # dropPictureData("d:\Bilder\\astroupload\\2024-01-10\M 81 M 82\LIGHT\\2024-01-10_20-40-01_NoFilter_-14.80_180.00s_0000.fits", "fits/LIGHT.fits")

    # FLAT
    # dropPictureData("d:\Bilder\\astroupload\\2024-01-09\FLAT\\2024-01-10_08-50-21__-14.10_0.08s_0009.fits", "fits/FLAT.fits")

    # DARK
    # dropPictureData("d:\Bilder\\astroupload\\2024-01-09\DARK\\2024-01-10_09-03-26__-14.80_180.00s_0100.fits", "fits/DARK.fits")

