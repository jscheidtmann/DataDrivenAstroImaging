from ImporterBase import ImporterBase, ImporterMetaBase 

class FitsImporter(ImporterBase):
    pass

class FitsImporterMeta(ImporterMetaBase):
    def getShortName(self):
        return "Fits File Importer"

    def getTooltipDescription(self) -> str:
        return "Extracts fits-headers from all fits files."
    
    def getInstance(self) -> ImporterBase:
        if self.instance is None:
            self.instance = FitsImporter()
        return self.instance
    
if __name__ == '__main__':
    importer = FitsImporterMeta()
    print(importer.getShortName())
    print(importer.getTooltipDescription())