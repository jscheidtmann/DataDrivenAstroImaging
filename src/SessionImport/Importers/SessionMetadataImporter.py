from ImporterBase import ImporterBase, ImporterMetaBase
import os

class SessionMetadataImporter(ImporterBase):
    def wantProcess(self, file: str) -> bool:
        basename = os.path.basename(file)
        return basename.startswith('AcquisitionDetails') or basename.startswith('ImageMetaData')

    def process(self, file: str) -> bool:
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
    