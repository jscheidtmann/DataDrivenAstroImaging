from ImporterBase import ImporterBase, ImporterMetaBase 

class FitsImporterMeta(ImporterMetaBase):
    def getShortName(self):
        return "Fits File Importer"

    def getTooltipDescription(self) -> str:
        return "Extracts fits-headers from all fits files."
    
    def getInstance(self) -> ImporterBase:
        if self.instance is None:
            self.instance = FitsImporter()
        return self.instance
    
    def getImporterClass(self):
        return FitsImporter

class FitsImporter(ImporterBase):
    def wantProcess(self, file: str) -> bool:
        return file.endswith('.fits') or file.endswith('.fit') or file.endswith('.fts')

    def process(self, file: str) -> bool:
        return False
