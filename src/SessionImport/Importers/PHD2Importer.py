from ImporterBase import ImporterBase, ImporterMetaBase

class PHD2Importer(ImporterBase):
    def wantProcess(self, file: str) -> bool:
        return file.startswith('PHDGuidelog')

    def process(self, file: str) -> bool:
        return False

class PHD2ImporterMeta(ImporterMetaBase):
    def getShortName(self) -> str:
        return "PHD2 Guidelog Importer"
    
    def getTooltipDescription(self) -> str:
        return "Import guidelogs for each subframe from a PHD2 guidelog."
    
    def getInstance(self) -> ImporterBase:
        if self.instance is None:
            self.instance = PHD2Importer()
        return self.instance
    
    def getImporterClass(self):
        return PHD2Importer
    