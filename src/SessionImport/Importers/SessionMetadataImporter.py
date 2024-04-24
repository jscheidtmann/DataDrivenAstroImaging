from ImporterBase import ImporterBase, ImporterMetaBase

class SessionMetadataImporter(ImporterBase):
    pass

class SessionMetadataImporterMeta(ImporterMetaBase):
    def getShortName(self) -> str:
        return "N.I.N.A. Session Metatdata Plugin Importer"
    
    def getTooltipDescription(self) -> str:
        return "Import session metadata from N.I.N.A's plugin of the same name."
    
    def getInstance(self) -> ImporterBase:
        if self.instance is None:
            self.instance = SessionMetadataImporter()
        return self.instance