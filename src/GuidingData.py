import re

from JulianDate import getJulianDate
from Parsing import parseFloat


class GuidingFrame:
    def __init__(self):
        self.frame = None
        self.time = None
        self.dx = None
        self.dy = None
        self.raRawDistance = None
        self.decRawDistance = None
        self.raGuideDistance = None
        self.decGuideDistance = None
        self.raDuration = None
        self.raDirection = None
        self.decDuration = None
        self.decDirection = None
        self.xStep = None
        self.yStep = None
        self.starMass = None
        self.snr = None
        self.settlingAfterDither = False
        self.errorCode = None


class GuidingData:
    def __init__(self):
        self.guidingStart = None
        self.guidingEnd = None
        self.maxsnr = 0.0
        self.maxStarmass = 0.0
        self.raRate = 13.5
        self.decRate = 13.5
        self.frames = []


class GuidingSessionData:
    def __init__(self):
        self.guidingData = []

    def count(self):
        count = 0
        for gd in self.guidingData:
            count += len(gd.frames)
        return count

    def getGuidingFrames(self, jd1, jd2):

        values = []
        if len(self.guidingData) > 0:
            for gd in self.guidingData:
                if gd.guidingEnd < jd1:
                    continue
                elif gd.guidingStart > jd2:
                    continue

                for frame in gd.frames:
                    if jd1 <= frame.time and jd2 >= frame.time:
                        values.append(frame)
                    elif frame.time > jd2:
                        break

        return values

    def readTime(self, str):
        # 2023-03-15 20:34:49
        print('parsing ' + str)

        parts = str.split(' ')
        date = parts[0]
        time = parts[1]
        ymd = date.split('-')
        hms = time.split(':')
        year = int(ymd[0])
        month = int(ymd[1])
        day = int(ymd[2])
        hour = int(hms[0])
        minute = int(hms[1])
        sec = int(hms[2])
        return getJulianDate(year, month, day, hour, minute, sec) + 2400000.5

    def readGuidingSessionData(self, fname):

        with open(fname, newline='\r\n') as file:
            lines = file.readlines()

            guidingRanges = []
            raRate = 13.5
            decRate = 13.5

            inBetween = False
            for i in range(0, len(lines)):
                line = lines[i]

                if line.startswith("RA Guide Speed"):
                    matches = re.findall(
                        "Guide Speed = ([0123456789.]+) a-s/s", line)

                    if len(matches) == 2:
                        raRate = parseFloat(matches[0])
                        decRate = parseFloat(matches[1])

                        print("Guiding Speed RA: " + str(raRate))
                        print("Guiding Speed DEC: " + str(decRate))

                if line.startswith('Guiding Begins at'):
                    if inBetween:
                        guidingRanges.append(i)

                    guidingRanges.append(i)
                    inBetween = True
                if inBetween and line.startswith('Guiding Ends at'):
                    guidingRanges.append(i)
                    inBetween = False

            self.guidingData.clear()

            for i in range(1, len(guidingRanges), 2):
                start = guidingRanges[i-1]
                end = guidingRanges[i]

                print('reading ' + str(start) + '-' + str(end))

                line1 = lines[start].replace('Guiding Begins at ', '')
                if len(line1) == len(lines[start]):
                    line1 = line1.replace('Guiding Ends at ', '')

                jd1 = self.readTime(line1.strip())

                line2 = lines[end].replace('Guiding Ends at ', '')
                if len(line2) == len(lines[end]):
                    line2 = line2.replace('Guiding Begins at ', '')

                jd2 = self.readTime(line2)

                guiding = GuidingData()
                guiding.guidingStart = jd1
                guiding.guidingEnd = jd2

                isGuidingData = False
                isDithering = False

                for j in range(start, end):
                    line = lines[j]

                    if not isGuidingData and line.startswith('Frame,'):
                        isGuidingData = True
                    elif isGuidingData:
                        if line.startswith("INFO: DITHER"):
                            isDithering = True

                        if isDithering:
                            if line.startswith("INFO:"):
                                if line.startswith("INFO: SETTLING STATE CHANGE, Settling started"):
                                    continue
                                if line.startswith("INFO: SETTLING STATE CHANGE, Settling complete"):
                                    isDithering = False
                                    continue

                        parts = line.split(',')
                        if parts is not None and len(parts) >= 17 and parts[0].isdigit():
                            frame = GuidingFrame()
                            frameNo = int(parts[0])
                            timeoffset = float(parts[1])
                            if parts[2].startswith('DROP'):
                                continue

                            dx = parseFloat(parts[3])
                            dy = parseFloat(parts[4])
                            raRaw = parseFloat(parts[5])
                            decRaw = parseFloat(parts[6])
                            raGuide = parseFloat(parts[7])
                            decGuide = parseFloat(parts[8])
                            raDuration = parseFloat(parts[9])
                            raDirection = parts[10]
                            decDuration = parseFloat(parts[11])
                            decDirection = parts[12]
                            xStep = parseFloat(parts[13])
                            yStep = parseFloat(parts[14])
                            starMass = parseFloat(parts[15])
                            snr = parseFloat(parts[16])
                            errorCode = int(parts[17])

                            if raGuide is None or decGuide is None:
                                continue

                            frame.frame = frameNo
                            frame.time = jd1 + timeoffset/86400.0
                            frame.dx = dx
                            frame.dy = dy
                            frame.raRawDistance = raRaw
                            frame.decRawDistance = decRaw
                            frame.raGuideDistance = raGuide
                            frame.decGuideDistance = decGuide
                            frame.raDuration = raDuration
                            frame.decDuration = decDuration
                            frame.raDirection = raDirection
                            frame.decDirection = decDirection
                            frame.xStep = xStep
                            frame.yStep = yStep
                            frame.starMass = starMass
                            frame.snr = snr
                            frame.errorCode = errorCode
                            frame.settlingAfterDither = isDithering

                            guiding.maxsnr = max(snr, guiding.maxsnr)
                            guiding.maxStarmass = max(starMass, guiding.maxStarmass)
                            guiding.raRate = raRate
                            guiding.decRate = decRate

                            guiding.frames.append(frame)

                for frame in guiding.frames:
                    frame.snr /= guiding.maxsnr
                    frame.starMass /= guiding.maxStarmass

                self.guidingData.append(guiding)
