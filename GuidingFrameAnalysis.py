from enum import Enum

class Quality(Enum):
    Good = 1
    Medium = 2
    Bad = 3


class GuidingFrameAnalysis:
    def __init__(self):
        self.rmsRA = None
        self.rmsDEC = None
        self.rms = None
        self.peakRA = None
        self.peakDEC = None
        self.pixRA = None
        self.pixDEC = None
        self.pixelTotal = None
        self.minRA = None
        self.maxRA = None
        self.minDEC = None
        self.maxDEC = None
        self.numPeaksRA = 0
        self.numPeaksDEC = 0
        self.minSNR = None
        self.maxSNR = None
        self.rmsSNR = None
        self.minStarmass = None


class GuidingSummary:
    def __init__(self):
        self.peakRA = None
        self.peakDEC = None
        self.peakDEC = None