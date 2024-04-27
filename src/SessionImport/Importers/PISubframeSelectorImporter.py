from ImporterBase import ImporterBase, ImporterMetaBase
import os
class PISubframeSelectorImporter(ImporterBase):
    def wantProcess(self, file: str) -> bool:
        basename = os.path.basename(file)
        return basename.startswith('SubframeSelector') or basename.startswith('MasterValues')

    def process(self, file: str) -> bool:
        return False

class PISubframeSelectorImporterMeta(ImporterMetaBase):
    def getShortName(self) -> str:
        return "PixInsight Subframe Selector Importer"
    
    def getTooltipDescription(self) -> str:
        return "Import subframe statistics from PixInsight's Subframe Selector."
    
    def getInstance(self) -> ImporterBase:
        if self.instance is None:
            self.instance = PISubframeSelectorImporter()
        return self.instance
    
    def getImpoterClass(self):
        return PISubframeSelectorImporter
    