import math
import os

import pandas as pd
from PyQt6.QtGui import QColor
from astropy import units as u
from astropy.coordinates import FK5, SkyCoord

import DataColumn
import DataColumn as Columns
import FitsHeader as fh
import FitsHeaderKeys as fhk
from GuidingData import GuidingSessionData
from GuidingFrameAnalysis import GuidingFrameAnalysis
from JulianDate import convertToJulianDate
from Spherical import getMoonAltAz, getSunAltAz, formatHMS, formatDMS, formatAngle, formatDMSLow


class ImageData:

    def __init__(self):
        self.imageFolder = None
        self.guidingData = None
        self.data = None

    def createNew(self):
        self.data = pd.DataFrame(columns=Columns.Columns)
        self.guidingData = GuidingSessionData()
        self.imageFolder = None

    def getColumns(self):
        return self.data.columns

    def getHeader(self):
        header = dict()
        for column in self.data.columns:
            if column == DataColumn.RA:
                header['RA'] = column
            elif column == DataColumn.DEC:
                header['DEC'] = column
            elif column == DataColumn.RMS:
                header['RMS'] = column
            elif column == DataColumn.AIRMASS:
                header['Airmass'] = column
            elif column == DataColumn.EXPOSURE:
                header['Exposure'] = column
            elif column == DataColumn.SUNALT:
                header['Altitude Sun'] = column
            elif column == DataColumn.MOONALT:
                header['Altitude Moon'] = column
            elif column == DataColumn.AZIMUTH:
                header['Azimuth'] = column
            elif column == DataColumn.ALTITUDE:
                header['Altitude'] = column
            elif column == DataColumn.GUIDINGMINSTARMASS:
                header['Starmass (Min)'] = column
            elif column == DataColumn.GUIDINGPIX:
                header['Guiding px'] = column
            elif column == DataColumn.GUIDINGPIXRA:
                header['Guiding px (RA)'] = column
            elif column == DataColumn.GUIDINGMINSNR:
                header['Guuiding SNR (Min)'] = column
            elif column == DataColumn.GUIDINGRMSSNR:
                header['Guiding SNR (Max)'] = column
            elif column == DataColumn.GUIDINGMINRA:
                header['Guiding RA (Min)'] = column
            elif column == DataColumn.GUIDINGMAXRA:
                header['Guiding RA (Max)'] = column
            elif column == DataColumn.GUIDINGMINDEC:
                header['Guiding DEC (Min)'] = column
            elif column == DataColumn.GUIDINGMAXDEC:
                header['Guiding DEC (Max)'] = column
            elif column == DataColumn.GUIDINGPEAKSRA:
                header['Guiding RA (Peaks)'] = column
            elif column == DataColumn.GUIDINGPEAKSDEC:
                header['Guiding DEC (Peaks)'] = column

        return header

    def getChartValues(self):
        header = dict()
        header['None'] = None

        for column in self.data.columns:
            if column == DataColumn.RMS:
                header['RMS'] = column
            elif column == DataColumn.AIRMASS:
                header['Airmass'] = column
            elif column == DataColumn.EXPOSURE:
                header['Exposure'] = column
            elif column == DataColumn.SUNALT:
                header['Altitude Sun'] = column
            elif column == DataColumn.MOONALT:
                header['Altitude Moon'] = column
            elif column == DataColumn.AZIMUTH:
                header['Azimuth'] = column
            elif column == DataColumn.ALTITUDE:
                header['Altitude'] = column
            elif column == DataColumn.GUIDINGMINSTARMASS:
                header['Starmass (Min)'] = column
            elif column == DataColumn.GUIDINGPIX:
                header['Guiding px'] = column
            elif column == DataColumn.GUIDINGPIXRA:
                header['Guiding px (RA)'] = column
            elif column == DataColumn.GUIDINGMINSNR:
                header['Guuiding SNR (Min)'] = column
            elif column == DataColumn.GUIDINGRMSSNR:
                header['Guiding SNR (Max)'] = column
            elif column == DataColumn.GUIDINGMINRA:
                header['Guiding RA (Min)'] = column
            elif column == DataColumn.GUIDINGMAXRA:
                header['Guiding RA (Max)'] = column
            elif column == DataColumn.GUIDINGMINDEC:
                header['Guiding DEC (Min)'] = column
            elif column == DataColumn.GUIDINGMAXDEC:
                header['Guiding DEC (Max)'] = column
            elif column == DataColumn.GUIDINGPEAKSRA:
                header['Guiding RA (Peaks)'] = column
            elif column == DataColumn.GUIDINGPEAKSDEC:
                header['Guiding DEC (Peaks)'] = column
            elif column == DataColumn.HFR:
                header['HFR'] = column
            elif column == DataColumn.FWHM:
                header['FWHM'] = column
            elif column == DataColumn.Eccentricity:
                header['Eccentricity'] = column
            elif column == DataColumn.HFRStDev:
                header['HFRStdDev'] = column
            elif column == DataColumn.DetectedStars:
                header['#Stars'] = column
            elif column == DataColumn.ADUMean:
                header['ADU Mean'] = column
            elif column == DataColumn.ADUMedian:
                header['ADU Median'] = column
            elif column == DataColumn.ADUMin:
                header['ADU Min'] = column
            elif column == DataColumn.ADUMax:
                header['ADU Max'] = column
            elif column == DataColumn.DEWPOINT:
                header['Dew Point'] = column
            elif column == DataColumn.HUMIDITY:
                header['Humidity'] = column
            elif column == DataColumn.PRESSURE:
                header['Air Pressure'] = column

        return header

    def readGuidingData(self, filename):
        self.guidingData = GuidingSessionData()
        self.guidingData.readGuidingSessionData(filename)

    def readMetaData(self, filename):
        print(filename)
        df = pd.read_csv(filename)
        df['FilePath'] = df['FilePath'].apply(lambda path: os.path.basename(path))
        df = df.rename(columns={'FilePath': DataColumn.FNAME, })
        df = df[[DataColumn.FNAME, DataColumn.HFR, DataColumn.HFRStDev, DataColumn.DetectedStars,
                 DataColumn.ADUMean, DataColumn.ADUMedian, DataColumn.ADUMin, DataColumn.ADUMax
                 # , DataColumn.FWHM, DataColumn.Eccentricity
                 ]]

        self.data = self.data.merge(df, on=DataColumn.FNAME)

    def getFilters(self):
        return list(set(self.data[Columns.FILTER]))

    def getFramesPerFilter(self, filter):
        return self.data[self.data[Columns.FILTER] == filter]

    def getMin(self, column):
        return self.data[column].min()

    def getMax(self, column):
        return self.data[column].max()

    def getTextColor(self, value, column):
        if value is None:
            return QColor(0, 0, 0)  # Black
        if (column == Columns.FNAME or column == Columns.BAYERPAT or column == Columns.CAMERA
                or column == Columns.TELESCOPE or column == Columns.CCDSETTEMP or column == Columns.CCDTEMP):
            return QColor(160, 160, 160)
        if column == Columns.FOCALLENGTH or column == Columns.FOCRATIO:
            return QColor(160, 160, 160)
        if column == Columns.RMS or column == Columns.RMSRA or column == Columns.RMSDEC:
            pxs = self.getPixelScale()
            if value < 0.66 * pxs:
                return QColor(0, 255, 0)
            elif value < pxs:
                return QColor(255, 255, 0)
            else:
                return QColor(255, 0, 0)
        if column == Columns.DetectedStars:
            maxStars = self.getMax(Columns.DetectedStars)
            if value < 0.75 * maxStars:
                return QColor(255, 0, 0)
            elif value < 0.9 * maxStars:
                return QColor(255, 255, 0)
            else:
                return QColor(0, 255, 0)

        if column == Columns.ADUMean or column == Columns.ADUMedian:
            minValue = self.getMin(column)
            if value > 1.25 * minValue:
                return QColor(255, 0, 0)
            elif value > 1.1 * minValue:
                return QColor(255, 255, 0)
            else:
                return QColor(0, 255, 0)

        if column == Columns.SUNALT:
            if value.deg < -18.0:
                return QColor(0, 255, 0)
            elif value.deg < -12.0:
                return QColor(255, 255, 0)
            else:
                return QColor(255, 0, 0)

        if column == Columns.MOONALT:
            if value.deg < 0.0:
                return QColor(0, 255, 0)
            elif value.deg < 10.0:
                return QColor(255, 255, 0)
            else:
                return QColor(255, 0, 0)

        if column == Columns.HUMIDITY:
            if value < 70.0:
                return QColor(0, 255, 0)
            elif value < 90.0:
                return QColor(255, 255, 0)
            else:
                return QColor(255, 0, 0)

        if column == Columns.AIRMASS:
            minValue = self.getMin(column)
            if value > 3.0 * minValue:
                return QColor(255, 0, 0)
            elif value > 1.5 * minValue:
                return QColor(255, 255, 0)
            else:
                return QColor(0, 255, 0)

        if column == Columns.HFR:
            minValue = self.getMin(column)
            if value < 1.1 * minValue:
                return QColor(0, 255, 0)
            elif value < 1.25 * minValue:
                return QColor(255, 255, 0)
            else:
                return QColor(255, 0, 0)

        if column == Columns.FWHM:
            minValue = self.getMin(column)
            if value < 1.1 * minValue:
                return QColor(0, 255, 0)
            elif value < 1.25 * minValue:
                return QColor(255, 255, 0)
            else:
                return QColor(255, 0, 0)

        if column == Columns.GUIDINGPIXRA or column == Columns.GUIDINGPIXDEC or column == Columns.GUIDINGPIX:
            if value < 0.66:
                return QColor(0, 255, 0)
            elif value < 0.9:
                return QColor(255, 255, 0)
            else:
                return QColor(255, 0, 0)

        if column == Columns.GUIDINGMINRA or column == Columns.GUIDINGMINDEC or \
                column == Columns.GUIDINGMAXRA or column == Columns.GUIDINGMAXDEC:
            pxs = self.getPixelScale()
            if abs(value) < 0.8 * pxs:
                return QColor(0, 255, 0)
            elif abs(value) < pxs:
                return QColor(255, 255, 0)
            else:
                return QColor(255, 0, 0)

        if column == Columns.Eccentricity:
            if value < 0.3:
                return QColor(0, 255, 0)
            elif value < 0.5:
                return QColor(255, 255, 0)
            else:
                return QColor(255, 0, 0)

        return QColor(255, 255, 255)  # TODO Depends on UI mode: Dark mode needs white, else black

    def format(self, value, column):
        if value is None:
            return "n/a"
        if column == Columns.FNAME:
            return value
        if column == Columns.FOCALLENGTH:
            return str(value)
        if column == Columns.FOCRATIO:
            return str(value)
        if column == Columns.RMS:
            return "{value:.3f}".format(value=value)
        if column == Columns.RMSRA:
            return "{value:.3f}".format(value=value)
        if column == Columns.RMSDEC:
            return "{value:.3f}".format(value=value)
        if column == Columns.GUIDINGPEAKSRA:
            return str(value)
        if column == Columns.GUIDINGPEAKSDEC:
            return str(value)
        if column == Columns.GUIDINGMINRA or column == Columns.GUIDINGMAXRA:
            return "{value:.3f}".format(value=value)
        if column == Columns.GUIDINGMINDEC or column == Columns.GUIDINGMAXDEC:
            return "{value:.3f}".format(value=value)
        if column == Columns.GUIDINGRMSSNR or column == Columns.GUIDINGMINSNR or column == Columns.GUIDINGMAXSNR:
            return "{value:.3f}".format(value=value)
        if column == Columns.GUIDINGPIX or column == Columns.GUIDINGPIXRA or column == Columns.GUIDINGPIXDEC:
            return "{value:.2f}".format(value=value)
        if column == Columns.GUIDINGMINSTARMASS:
            return "{value:.3f}".format(value=value)
        if column == Columns.AIRMASS:
            return "{value:.3f}".format(value=value)
        if column == Columns.RA:
            return formatHMS(value / 15.0)
        if column == Columns.DEC:
            return formatDMS(value)
        if column == Columns.ALTITUDE or column == Columns.AZIMUTH:
            return formatDMSLow(value)
        if column == Columns.SITELONG or column == Columns.SITELAT:
            return formatDMSLow(value)
        if column == Columns.MOONALT:
            return formatAngle(value)
        if column == Columns.SUNALT:
            return formatAngle(value)
        if column == Columns.DEWPOINT:
            return "{value:.1f}".format(value=value)

        if column == Columns.AMBIENTTEMP:
            return "{value:.1f}".format(value=value)
        if column == Columns.HFR or column == Columns.FWHM or column == Columns.Eccentricity:
            return "{value:.2f}".format(value=value)
        if column == Columns.HFRStDev:
            return "{value:.2f}".format(value=value)
        if column == Columns.ADUMean:
            return "{value:.2f}".format(value=value)

        return str(value)

    def parseLightFrames(self, folder, filenames):
        self.imageFolder = folder

        fnames = []
        exposures = []
        startexposuresJdd = []
        startexposures = []
        gains = []
        offsets = []
        resolutions = []
        cameras = []
        setTemps = []
        sensorTemps = []
        bayers = []
        telescopes = []
        focalLengths = []
        focalRatios = []
        focuserPositions = []
        focuserTemps = []
        ras = []
        decs = []
        altitudes = []
        azimuths = []
        airmasses = []
        piersides = []
        elevations = []
        latitudes = []
        longitudes = []
        filters = []
        objects = []
        rotations = []
        dewPoints = []
        humidities = []
        pressures = []
        ambientTemps = []
        windDirections = []
        windSpeeds = []

        for fname in filenames:
            header = fh.getFitsHeader(os.path.join(folder, fname))
            fnames.append(fname)
            exposures.append(header[fhk.EXPOSURE])
            startexposures.append(header[fhk.STARTTIME])
            jdd = convertToJulianDate(header[fhk.STARTTIME])
            startexposuresJdd.append(jdd)
            gains.append(header[fhk.GAIN])
            offsets.append(header[fhk.OFFSET])
            resolutions.append(header[fhk.XPIXSZ])
            cameras.append(header[fhk.CAMERA])
            setTemps.append(header[fhk.CCDSETTEMP])
            sensorTemps.append(header[fhk.CCDTEMP])
            bayers.append(header[fhk.BAYERPATTERN])
            telescopes.append(header[fhk.TELESCOPE])
            focalLengths.append(header[fhk.FOCALLENGTH])
            focalRatios.append(header[fhk.FOCALRATIO])
            focuserPositions.append(header.get(fhk.FOCPOS))
            focuserTemps.append(header.get(fhk.FOCTEMP))

            ras.append(header[fhk.RA])
            decs.append(header[fhk.DEC])
            altitudes.append(header[fhk.ALTITUDE])
            azimuths.append(header[fhk.AZIMUTH])
            airmasses.append(header[fhk.AIRMASS])
            piersides.append(header[fhk.PIERSIDE])
            elevations.append(header[fhk.OBS_ELEVATION])
            latitudes.append(header[fhk.OBS_LAT])
            longitudes.append(header[fhk.OBS_LONG])
            filters.append(header[fhk.FILTER])
            objects.append(header[fhk.TARGET])
            rotations.append(header[fhk.TARGETROTATION])
            dewPoints.append(header.get(fhk.DEWPOINT))
            humidities.append(header.get(fhk.HUMIDITY))
            pressures.append(header.get(fhk.PRESSURE))
            ambientTemps.append(header.get(fhk.AMBTEMP))
            windDirections.append(header.get(fhk.WINDDIR))
            windSpeeds.append(header.get(fhk.WINDSPD))

        indices = []
        startTimes = list(startexposuresJdd)
        startTimes.sort()

        for time in startexposuresJdd:
            index = startTimes.index(time) + 1
            indices.append(index)

        records = {
            Columns.INDEX: indices,
            Columns.FNAME: fnames,
            Columns.EXPOSURE: exposures,
            Columns.EXPSTART: startexposures,
            Columns.EXPSTARTJDD: startexposuresJdd,
            Columns.GAIN: gains,
            Columns.OFFSET: offsets,
            Columns.PIXSIZE: resolutions,
            Columns.CAMERA: cameras,
            Columns.CCDSETTEMP: setTemps,
            Columns.CCDTEMP: sensorTemps,
            Columns.BAYERPAT: bayers,
            Columns.TELESCOPE: telescopes,
            Columns.FOCALLENGTH: focalLengths,
            Columns.FOCRATIO: focalRatios,
            Columns.RA: ras,
            Columns.DEC: decs,
            Columns.ALTITUDE: altitudes,
            Columns.AZIMUTH: azimuths,
            Columns.AIRMASS: airmasses,
            Columns.PIERSIDE: piersides,
            Columns.SITEELEV: elevations,
            Columns.SITELONG: longitudes,
            Columns.SITELAT: latitudes,
            Columns.FILTER: filters,
            Columns.OBJECT: objects,
            Columns.ROTATION: rotations,
            Columns.FOCUSERPOS: focuserPositions,
            Columns.FOCUSERTEMP: focuserTemps,
            Columns.DEWPOINT: dewPoints,
            Columns.HUMIDITY: humidities,
            Columns.PRESSURE: pressures,
            Columns.AMBIENTTEMP: ambientTemps,
            Columns.WINDDIR: windDirections,
            Columns.WINDSPD: windSpeeds,
        }

        self.data = pd.DataFrame(records).sort_values(Columns.INDEX)

    def process(self):
        if self.guidingData.count() > 0 and not self.data.empty:
            self.analyzeGuidingFrames()
            self.calculateSunMoonPositions()

            return

    def calculateSunMoonPositions(self):
        sunAlt = []
        moonAlt = []

        for rowIndex, image in self.data.iterrows():
            lon = image[Columns.SITELONG]
            lat = image[Columns.SITELAT]
            jd = image[Columns.EXPSTARTJDD]
            moonAlt.append(getMoonAltAz(jd, lon, lat).alt)
            sunAlt.append(getSunAltAz(jd, lon, lat).alt)

        self.data[Columns.MOONALT] = moonAlt
        self.data[Columns.SUNALT] = sunAlt

    def getDitherData(self):
        positions = []
        for rowIndex, image in self.data.iterrows():
            ra = image[Columns.RA]
            dec = image[Columns.DEC]
            positions.append(SkyCoord(frame=FK5, ra=ra * u.degree, dec=dec * u.degree))

        return positions

    def analyzeGuidingFrames(self):
        self.analyzeAllGuidingFrames(self.guidingData, self.data)

    def getPixelScale(self):
        for rowIndex, image in self.data.iterrows():
            focalLength = image[Columns.FOCALLENGTH]
            if focalLength <= 0.0:
                continue
            return 206.0 * image[Columns.PIXSIZE] / focalLength

    def analyzeAllGuidingFrames(self, guidingData, imageData):

        rmsRA = []
        rmsDEC = []
        rms = []
        pixelRA = []
        pixelDEC = []
        pixelGuiding = []
        minRA = []
        maxRA = []
        minDEC = []
        maxDEC = []
        numPeaksRA = []
        numPeaksDEC = []
        minSNR = []
        maxSNR = []
        rmsSNR = []
        minStarmass = []

        for rowIndex, image in imageData.iterrows():
            focalLength = image[Columns.FOCALLENGTH]
            if focalLength <= 0.0:
                continue
            pixSize = 206.0 * image[Columns.PIXSIZE] / focalLength
            jd1 = image[Columns.EXPSTARTJDD]
            jd2 = jd1 + image[Columns.EXPOSURE] / 86400.0
            guidingFrames = guidingData.getGuidingFrames(jd1, jd2)

            if guidingFrames is not None and len(guidingFrames) > 0:
                analyse = self.analyseFrames(guidingFrames, pixSize)
                rmsRA.append(analyse.rmsRA)
                rmsDEC.append(analyse.rmsDEC)
                rms.append(analyse.rms)
                pixelRA.append(analyse.pixelRA)
                pixelDEC.append(analyse.pixelDEC)
                pixelGuiding.append(analyse.pixelTotal)
                minRA.append(analyse.minRA)
                maxRA.append(analyse.maxRA)
                minDEC.append(analyse.minDEC)
                maxDEC.append(analyse.maxDEC)
                numPeaksRA.append(analyse.numPeaksRA)
                numPeaksDEC.append(analyse.numPeaksDEC)
                minSNR.append(analyse.minSNR)
                maxSNR.append(analyse.maxSNR)
                rmsSNR.append(analyse.rmsSNR)
                minStarmass.append(analyse.minStarmass)

        if imageData.shape[0] == len(rms):
            imageData[Columns.RMS] = rms
            imageData[Columns.RMSRA] = rmsRA
            imageData[Columns.RMSDEC] = rmsDEC
            imageData[Columns.GUIDINGPIXRA] = pixelRA
            imageData[Columns.GUIDINGPIXDEC] = pixelDEC
            imageData[Columns.GUIDINGPIX] = pixelGuiding
            imageData[Columns.GUIDINGMINRA] = minRA
            imageData[Columns.GUIDINGMAXRA] = maxRA
            imageData[Columns.GUIDINGMINDEC] = minDEC
            imageData[Columns.GUIDINGMAXDEC] = maxDEC
            imageData[Columns.GUIDINGPEAKSRA] = numPeaksRA
            imageData[Columns.GUIDINGPEAKSDEC] = numPeaksDEC
            imageData[Columns.GUIDINGMINSNR] = minSNR
            imageData[Columns.GUIDINGMAXSNR] = maxSNR
            imageData[Columns.GUIDINGRMSSNR] = rmsSNR
            imageData[Columns.GUIDINGMINSTARMASS] = minStarmass

    @staticmethod
    def analyseFrames(guidingFrames, pixelSize):
        avgRA = 0.0
        avgDEC = 0.0
        peakRA = 0.0
        peakDEC = 0.0
        pixelRA = 0.0
        pixelDEC = 0.0
        minRA = 0.0
        maxRA = 0.0
        minDEC = 0.0
        maxDEC = 0.0
        numPeaksRA = 0
        numPeaksDEC = 0
        minSNR = 1.0
        maxSNR = 0.0
        avgSNR = 0.0
        minStarmass = 1.0

        count = len(guidingFrames)
        for frame in guidingFrames:

            if frame.raRawDistance is None or frame.decRawDistance is None \
                    or frame.starMass is None or frame.snr is None:
                continue

            avgRA += pow(frame.raRawDistance, 2)
            avgDEC += pow(frame.decRawDistance, 2)
            peakRA = max(peakRA, abs(frame.raRawDistance))
            peakDEC = max(peakDEC, abs(frame.decRawDistance))
            pixRA = pow((frame.raRawDistance) / pixelSize, 2)
            pixDEC = pow((frame.decRawDistance) / pixelSize, 2)
            pixelRA = pixelRA + pixRA
            pixelDEC = pixelDEC + pixDEC
            minRA = min(frame.raRawDistance, minRA)
            maxRA = max(frame.raRawDistance, maxRA)
            minDEC = min(frame.decRawDistance, minDEC)
            maxDEC = max(frame.decRawDistance, maxDEC)
            minSNR = min(frame.snr, minSNR)
            maxSNR = max(frame.snr, maxSNR)
            avgSNR += pow(frame.snr, 2)
            minStarmass = min(frame.starMass, minStarmass)
            if abs(frame.raRawDistance) > pixelSize:
                numPeaksRA += 1
            if abs(frame.decRawDistance) > pixelSize:
                numPeaksDEC += 1

        analysis = GuidingFrameAnalysis()
        analysis.rmsRA = math.sqrt(avgRA / count)
        analysis.rmsDEC = math.sqrt(avgDEC / count)
        analysis.rms = math.sqrt((avgRA + avgDEC) / count)
        analysis.peakRA = peakRA
        analysis.peakDEC = peakDEC
        analysis.pixelRA = math.sqrt(pixelRA / count)
        analysis.pixelDEC = math.sqrt(pixelDEC / count)
        analysis.pixelTotal = math.sqrt((pixelRA + pixelDEC) / count)
        analysis.minRA = minRA
        analysis.maxRA = maxRA
        analysis.minDEC = minDEC
        analysis.maxDEC = maxDEC
        analysis.numPeaksRA = numPeaksRA
        analysis.numPeaksDEC = numPeaksDEC
        analysis.minSNR = minSNR
        analysis.maxSNR = maxSNR
        analysis.rmsSNR = math.sqrt(avgSNR / count)
        analysis.minStarmass = minStarmass

        return analysis
