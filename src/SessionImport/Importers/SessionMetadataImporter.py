from SessionImport.Importers.ImporterBase import ImporterBase, ImporterMetaBase
from SessionData import SessionData 
from collections import defaultdict
import logging, os
import pandas as pd


class SessionMetadataImporter(ImporterBase):
    def __init__(self):
        super().__init__()
        self.imd = None
        self.acd = None
        self.df = None
        self.log = logging.getLogger("SessionMetadataImporter")

    def wantProcess(self, file: str) -> bool:
        basename = os.path.basename(file)
        return basename == 'AcquisitionDetails.csv' or basename == 'ImageMetaData.csv'

    def process(self, file: str) -> bool:
        if not os.path.exists(file):
            self.log.warn("File to import does not exist: %s", file)
            return False
        
        # The N.I.N.A. plugin creates two files in the same directory
        if file.endswith("ImageMetaData.csv"):
            self.log.info("Import ImageMetaData: %s", file)
            self.imd = file
            print(os.path.dirname(self.imd))
        
        if file.endswith("AcquisitionDetails.csv"):
            self.log.info("Import AcquisitionDetails: %s", file)
            self.acd = file
            print(os.path.dirname(self.acd))

        # Once both files have been detected, import them
        if self.imd is not None and self.acd is not None and os.path.dirname(self.imd) == os.path.dirname(self.acd):
            self.log.info("Both metadata files found: import start")
            try:
                self.log.info("Importing SessionMetaData plugin information: %s, %s", self.imd, self.acd)
                df_acd = pd.read_csv(self.acd)
                df_meta = pd.read_csv(self.imd)
                if self.df is None:
                    self.df = df_acd.merge(df_meta, how='cross')
                else:
                    self.df = pd.concat([self.df, df_acd.merge(df_meta, how='cross')])    
                self.log.debug("Imported dataframe size %s", str(self.df.shape))
            except (OSError, Exception) as e:
                self.log.error("Skipping %s, due to IOError", file)
                self.log.exception(e)
                return False
            else:
                self.log.info("Import finished")
        else:
            self.log.debug("Import condition not met.")

        return True

    def store(self, data: SessionData) -> bool:
        if self.df is not None:
            data.add(self.df.to_dict())
            return True
        return False

class SessionMetadataImporterMeta(ImporterMetaBase):
    def getShortName(self) -> str:
        return "N.I.N.A. Session Metatdata Plugin Importer"
    
    def getTooltipDescription(self) -> str:
        return "Import session metadata from N.I.N.A's plugin of the same name."
    
    def getInstance(self) -> ImporterBase:
        if self.instance is None:
            self.instance = SessionMetadataImporter()
        return self.instance

    def getImpoterClass(self):
        return SessionMetadataImporter

if __name__ == "__main__":
    chdlr = logging.StreamHandler()
    logging.getLogger().addHandler(chdlr)
    logging.getLogger().setLevel(logging.DEBUG)  
    logging.getLogger().info("Test")

    imp = SessionMetadataImporter()
    f = "../testdata/sessionmeta/session1/ImageMetaData.csv"
    assert imp.wantProcess(f), "SessionMetadataImporter should accept 'ImageMetaData.csv'"
    assert imp.process(f), "SessionMetadataImporter could not process 'ImageMetaData.csv', that's wrong"
    g = "../testdata/sessionmeta/session1/AcquisitionDetails.csv"
    assert imp.wantProcess(g), "SessionMetadataImporter should accept 'AcquisitionDetails.csv'"
    assert imp.process(g), "SessionMetadataImporter could not process 'AcquisitionDetails.csv', that's wrong"

    imported= imp.df.to_dict()

    expected = {'TargetName': {0: 'M 81 M 82'}, 'RACoordinates': {0: '9h 55m 42s'}, 'DECCoordinates': {0: '69° 18\' 57"'}, 
            'TelescopeName': {0: 'Newton 8"'}, 'FocalLength': {0: 1000}, 'FocalRatio': {0: 5}, 'CameraName': {0: 'ZWO ASI294MC Pro'}, 
            'PixelSize': {0: 4.63}, 'BitDepth': {0: 16}, 'ObserverLatitude': {0: 51.1536}, 'ObserverLongitude': {0: 7.0931}, 'ObserverElevation': {0: 240}, 
            'ExposureNumber': {0: 0}, 'FilePath': {0: 'D:/N.I.N.A/2024-01-10/M 81 M 82/LIGHT/2024-01-10_20-40-01_NoFilter_-14.80_180.00s_0000.fits'}, 
            'FilterName': {0: 'NoFilter'}, 'ExposureStart': {0: '01/10/2024 19:40:01'}, 'Duration': {0: 180}, 'Binning': {0: '1x1'}, 'CameraTemp': {0: -14.8}, 
            'CameraTargetTemp': {0: -15}, 'Gain': {0: 120}, 'Offset': {0: 8}, 'ADUStDev': {0: 1457.3548}, 'ADUMean': {0: 5456.7526}, 'ADUMedian': {0: 5528}, 
            'ADUMin': {0: 2776}, 'ADUMax': {0: 65532}, 'DetectedStars': {0: 119}, 'HFR': {0: 2.9386}, 'HFRStDev': {0: 0.2783}, 'GuidingRMS': {0: 0.1567}, 
            'GuidingRMSArcSec': {0: 0.606}, 'GuidingRMSRA': {0: 0.1149}, 'GuidingRMSRAArcSec': {0: 0.4444}, 'GuidingRMSDEC': {0: 0.1065}, 
            'GuidingRMSDECArcSec': {0: 0.4119}, 'FocuserPosition': {0: float('nan')}, 'FocuserTemp': {0: float('nan')}, 'RotatorPosition': {0: 0}, 'PierSide': {0: 'West'}, 
            'Airmass': {0: 1.4232}}
    
    for key in expected.keys():
        if expected[key] != imported[key]:
            print("Key: ", key)
            print("Expected: ", expected[key])
            print("Imported: ", imported[key])
            
    # data = SessionData()
    # assert imp.store(data), "Import did not work, although both files supplied"
