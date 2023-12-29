import math


def convertToJulianDate(dateTimeStr):

    parts = dateTimeStr.split("T")
    dayParts = parts[0].split("-")
    hourParts = parts[1].split(":")
    month = int(dayParts[1])
    day = int(dayParts[2])
    year = int(dayParts[0])
    hour = int(hourParts[0])
    minutes = int(hourParts[1])
    seconds = float(hourParts[2])

    return getJulianDate(year, month, day, hour, minutes, seconds)+2400000.5


def ddd(d, min, sec):
    sign = 1.0
    if (d < 0) or (min < 0) or (sec < 0.0):
        sigm = -1.0

    d1 = abs(d)
    d2 = abs(min) / 60.0
    d3 = abs(sec) / 3600.0
    return (sign * (d1 + d2 + d3))


def getJulianDate(year, month, day, hour, minute, seconds):
    mon = month
    yy = year

    if mon <= 2:
        mon += 12
        yy -= 1

    b = 0

    if (10000 * yy + 100 * mon + day) <= 15821004:
        b = -2 + math.floor((yy + 4716) / 4) - 1179
    else:
        b = math.floor(yy / 400) - math.floor(yy / 100) + math.floor(yy / 4)

    daysForMonths = math.floor(30.6001 * (mon + 1))
    midnight = 365.0 * yy - 679004.0 + (b + daysForMonths + day)
    fracOfDay = ddd(hour, minute, seconds) / 24.0
    return midnight + fracOfDay
