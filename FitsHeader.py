
import fitsio

def getFitsHeader(fname):
    return fitsio.read_header(fname)


