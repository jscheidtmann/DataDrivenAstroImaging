from ImporterBase import ImporterBase, ImporterMetaBase

class PISubframeSelectorImporter(ImporterBase):
    pass

class PISubframeSelectorImporterMeta(ImporterMetaBase):
    def getShortName(self) -> str:
        return "PixInsight Subframe Selector Importer"
    
    def getTooltipDescription(self) -> str:
        return "Import subframe statistics from PixInsight's Subframe Selector."
    
    def getInstance(self) -> ImporterBase:
        if self.instance is None:
            self.instance = PISubframeSelectorImporter()
        return self.instance