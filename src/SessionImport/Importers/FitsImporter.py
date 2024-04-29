from SessionImport.Importers.ImporterBase import ImporterBase, ImporterMetaBase
from SessionData import SessionData 
from astropy.io import fits
import logging

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
        try:
            header = fits.getheader(file)
            return True
        except OSError as e:
            self.log.error("Skipping %s, due to IOError", file)
            self.log.exception(e)
            return False
        except Exception as e:
            self.log.error("Skipping %s, due to exception:", file)
            self.log.exception(e)
            return False
    
    def store(self, data: SessionData) -> bool:
        return data.add()
