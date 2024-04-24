from ImporterBase import ImporterBase, ImporterMetaBase

class PIMasterImporter(ImporterBase):
    def wantProcess(self, file: str) -> bool:
        return file.endswith('.xisf')

    def process(self, file: str) -> bool:
        return False

class PIMasterImporterMeta(ImporterMetaBase):
    def getShortName(self) -> str:
        return "PixInsight Master Importer"
    
    def getTooltipDescription(self) -> str:
        return "Import master files created from WBPP from PixInsight."
    
    def getInstance(self) -> ImporterBase:
        if self.instance is None:
            self.instance = PIMasterImporter()
        return self.instance
    
    def getImpoterClass(self):
        return PIMasterImporter
    