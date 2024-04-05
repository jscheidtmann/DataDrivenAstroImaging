import math

from astropy.coordinates import (EarthLocation, AltAz)
from astropy.coordinates import get_sun, get_body
from astropy.time import Time


def getTime(jd):
    return Time(jd, None, 'jd')


def getLocalTime(jd, loc):
    return Time(jd, location=loc, format='jd')


def formatTime(jd):
    time = getTime(jd)
    time.precision = 0
    return time.iso


def frac(d):
    return d - math.floor(d)


def formathms(secs):
    if secs < 60.0:
        return str(secs) + " seconds"
    else:
        mins = secs / 60.0
        if mins < 60.0:
            sec = int(frac(mins) * 60.0)
            min = math.floor(mins)

            if sec == 0:
                return str(min).zfill(2) + " min "

            return str(min).zfill(2) + " min " + str(int(sec)).zfill(2) + " sec"
        else:
            hours = mins / 60.0
            min = frac(hours) * 60.0
            sec = int(frac(mins) * 60.0)

            if sec == 0:
                return str(int(hours)).zfill(2) + " hours " \
                    + str(int(min)).zfill(2) + "min "

            return str(int(hours)).zfill(2) + " hours " \
                + str(int(min)).zfill(2) + "min " \
                + str(int(sec)).zfill(2) + " sec"


def formatDMS(angle):
    sign = '+'
    if angle < 0.0:
        sign = '-'

    angle = abs(angle)
    deg = math.floor(angle)
    mins = 60.0 * (angle - deg)
    min = math.floor(mins)
    secs = round(60.0 * (mins - min), 2)

    return sign + str(deg).zfill(2) + "° " + str(min).zfill(2) + "' " + '{:04.1f}'.format(secs)


def formatDMSLow(angle):
    sign = '+'
    if angle < 0.0:
        sign = '-'

    angle = abs(angle)
    deg = math.floor(angle)
    mins = 60.0 * (angle - deg)

    return sign + str(deg).zfill(2) + "° " + '{:04.2f}'.format(mins) + "'"


def formatAngle(angle):
    dms = angle.signed_dms
    sign = '+'
    if dms.sign < 0.0:
        sign = '-'

    return sign + "{0:02.0f}° {1:02.0f}' {2:04.1f}".format(dms.d, dms.m, dms.s)


def formatHMS(angle):
    sign = '+'
    if angle < 0.0:
        sign = '-'

    angle = abs(angle)
    deg = math.floor(angle)
    mins = 60.0 * (angle - deg)
    min = math.floor(mins)
    secs = round(60.0 * (mins - min), 2)

    return sign + str(deg).zfill(2) + "h " + str(min).zfill(2) + "' " + '{:04.1f}'.format(secs)


def getEarthLocation(lon, lat):
    return EarthLocation.from_geodetic(lon, lat)


def getMoonAltAz(jd, lon, lat):
    loc = getEarthLocation(lon, lat)
    time = getLocalTime(jd, loc)
    coord = get_body("moon", time)
    aa = AltAz(location=loc, obstime=time)
    return coord.transform_to(aa)


def getSunAltAz(jd, lon, lat):
    loc = getEarthLocation(lon, lat)
    time = getLocalTime(jd, loc)
    coord = get_sun(time)
    aa = AltAz(location=loc, obstime=time)
    return coord.transform_to(aa)


def getAltAz(coord, jd, lon, lat):
    loc = getEarthLocation(lon, lat)
    time = getLocalTime(jd, loc)
    aa = AltAz(location=loc, obstime=time)
    return coord.transform_to(aa)
