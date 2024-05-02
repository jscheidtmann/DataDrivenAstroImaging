from SessionImport.Importers.ImporterBase import ImporterBase, ImporterMetaBase
from SessionData import SessionData 
from astropy.io import fits
from collections import defaultdict
import logging, os

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
    def __init__(self):
        super().__init__()
        self.data = defaultdict(list)
        self.expected = 0

    def wantProcess(self, file: str) -> bool:
        return file.endswith('.fits') or file.endswith('.fit') or file.endswith('.fts')

    def _stripFileType(self, base: str):
        (stripped, _) = base.rsplit('.')
        return stripped
    
    def process(self, file: str) -> bool:
        self.expected += 1
        try:
            fname = os.path.basename(file)

            # Handle Id and filename
            self.data["Id"].append(self._stripFileType(fname))
            self.data["filename"].append(file)

            # fits header import
            header = fits.getheader(file)
            for item in header:
                self.data[item].append(header[item])
                # prepend None, until same number of items is reached 
                # for keys, which where missing from previous files
                while len(self.data[item]) < self.expected:
                    self.data[item].insert(-1, None) 
            
            # handle keys, which have been missing from this file
            for k in self.data.keys():
                while len(self.data[k]) < self.expected:
                    self.data[k].append(None)

            return True
        except (OSError, Exception) as e:
            self.log.error("Skipping %s, due to IOError", file)
            self.log.exception(e)
            return False

    def store(self, data: SessionData) -> bool:
        return data.add(self.data)
