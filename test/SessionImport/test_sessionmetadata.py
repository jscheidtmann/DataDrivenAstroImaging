from SessionImport.Importers.SessionMetadataImporter import SessionMetadataImporter
from SessionImport.Importer import Importer
import time
from pandas import DataFrame

def testEmptySessionMetaDataImporterCreation():
    SessionMetadataImporter()

def testSessionMetadataAcceptance():
    imp = SessionMetadataImporter()
    assert imp.wantProcess("ImageMetaData.csv"), "SessionMetadataImporter does not process ImageMetaData.csv"
    assert imp.wantProcess("AcquisitionDetails.csv"), "SessionMetadataImporter does not process AcquisitionDetails.csv"

def testSessionMetadataNonAcceptance():
    imp = SessionMetadataImporter()
    assert not imp.wantProcess("A.fits"), "SessionMetadataImporter does process A.fit, that's wrong"
    assert not imp.wantProcess("A.xisf"), "SessionMetadataImporter accepts XISF, what's that?"
    assert not imp.wantProcess("A.nef"), "SessionMetadataImporter accepts NEF, what's that?"
    assert not imp.wantProcess("A.cr2"), "SessionMetadataImporter accepts CR2, what's that?"

def testImportNonExistingSessionMetadata():
    imp = SessionMetadataImporter()
    f = "non-existing/ImageMetaData.csv"
    assert imp.wantProcess(f), "SessionMetadataImporter should accept 'non-existing/ImageMetaData.csv'"
    assert not imp.process(f), "SessionMetadataImporter returns true for 'non-existing/ImageMetaData.csv'"


def testProcessImageMetaData(mocker):
    imp = SessionMetadataImporter()
    f = "testdata/sessionmeta/session1/ImageMetaData.csv"
    assert imp.wantProcess(f), "SessionMetadataImporter should accept 'ImageMetaData.csv'"
    assert imp.process(f), "SessionMetadataImporter could not process 'ImageMetaData.csv', that's wrong"

    data = mocker.Mock()
    assert not imp.store(data), "Only one file accepted, should not have data"

def testProcessAcquisitionDetails(mocker):
    imp = SessionMetadataImporter()
    f = "testdata/sessionmeta/session1/AcquisitionDetails.csv"
    assert imp.wantProcess(f), "SessionMetadataImporter should accept 'AcquisitionDetails.csv'"
    assert imp.process(f), "SessionMetadataImporter could not process 'AcquisitionDetails.csv', that's wrong"

    data = mocker.Mock()
    assert not imp.store(data), "Only one file accepted, should not have data"


def are_dicts_equal(dict1, dict2):
    """handle special case that NaN != NaN"""
    if len(dict1) != len(dict2):
        return False

    for key in dict1:
        if key not in dict2:
            return False

        value1 = dict1[key]
        value2 = dict2[key]

        if isinstance(value1, dict) and isinstance(value2, dict):
            if not are_dicts_equal(value1, value2):
                return False
        elif isinstance(value1, float) and isinstance(value2, float):
            if (value1 != value2) and not (value1 != value1 and value2 != value2):
                return False
        elif value1 != value2:
            return False

    # Check if all keys in dict2 are present in dict1
    for key in dict2:
        if key not in dict1:
            return False

    return True


def testProcessImageMetaDataAcqDetails(mocker):
    imp = SessionMetadataImporter()
    f = "testdata/sessionmeta/session1/ImageMetaData.csv"
    assert imp.wantProcess(f), "SessionMetadataImporter should accept 'ImageMetaData.csv'"
    assert imp.process(f), "SessionMetadataImporter could not process 'ImageMetaData.csv', that's wrong"
    g = "testdata/sessionmeta/session1/AcquisitionDetails.csv"
    assert imp.wantProcess(g), "SessionMetadataImporter should accept 'AcquisitionDetails.csv'"
    assert imp.process(g), "SessionMetadataImporter could not process 'AcquisitionDetails.csv', that's wrong"

    data = mocker.Mock()
    assert imp.store(data), "Import did not work, although both files supplied"
    data.add.assert_called_once() 

    # Test if passed argument is as expected:
    # Need to handle floats, that can be NaN, for which NaN != NaN.
    args, kwargs = data.add.call_args
    expected  = {'TargetName': {0: 'M 81 M 82'}, 'RACoordinates': {0: '9h 55m 42s'}, 'DECCoordinates': {0: '69° 18\' 57"'}, 
            'TelescopeName': {0: 'Newton 8"'}, 'FocalLength': {0: 1000}, 'FocalRatio': {0: 5}, 'CameraName': {0: 'ZWO ASI294MC Pro'}, 
            'PixelSize': {0: 4.63}, 'BitDepth': {0: 16}, 'ObserverLatitude': {0: 51.1536}, 'ObserverLongitude': {0: 7.0931}, 'ObserverElevation': {0: 240}, 
            'ExposureNumber': {0: 0}, 'FilePath': {0: 'D:/N.I.N.A/2024-01-10/M 81 M 82/LIGHT/2024-01-10_20-40-01_NoFilter_-14.80_180.00s_0000.fits'}, 
            'FilterName': {0: 'NoFilter'}, 'ExposureStart': {0: '01/10/2024 19:40:01'}, 'Duration': {0: 180}, 'Binning': {0: '1x1'}, 'CameraTemp': {0: -14.8}, 
            'CameraTargetTemp': {0: -15}, 'Gain': {0: 120}, 'Offset': {0: 8}, 'ADUStDev': {0: 1457.3548}, 'ADUMean': {0: 5456.7526}, 'ADUMedian': {0: 5528}, 
            'ADUMin': {0: 2776}, 'ADUMax': {0: 65532}, 'DetectedStars': {0: 119}, 'HFR': {0: 2.9386}, 'HFRStDev': {0: 0.2783}, 'GuidingRMS': {0: 0.1567}, 
            'GuidingRMSArcSec': {0: 0.606}, 'GuidingRMSRA': {0: 0.1149}, 'GuidingRMSRAArcSec': {0: 0.4444}, 'GuidingRMSDEC': {0: 0.1065}, 
            'GuidingRMSDECArcSec': {0: 0.4119}, 'FocuserPosition': {0: float('nan')}, 'FocuserTemp': {0: float('nan')}, 'RotatorPosition': {0: 0}, 'PierSide': {0: 'West'}, 
            'Airmass': {0: 1.4232}}
    
    assert are_dicts_equal(args[0], expected), "Passed argument not equal"


