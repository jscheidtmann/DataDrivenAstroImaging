from SessionImport.Importers.ImporterBase import ImporterBase, ImporterMetaBase
from SessionData import SessionData 
from astropy.io import fits
from collections import defaultdict
import logging, os
from unittest.mock import Mock

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
        self.data = defaultdict(dict)
        self.row = 0
        self.log = logging.getLogger("FitsImporter")

    def wantProcess(self, file: str) -> bool:
        return file.endswith('.fits') or file.endswith('.fit') or file.endswith('.fts')

    def _stripFileType(self, base: str):
        (stripped, _) = base.rsplit('.')
        return stripped
    
    def process(self, file: str) -> bool:
        try:
            fname = os.path.basename(file)
            self.log.info("FitsImporter processing: %s", file)

            # Prefill existing keys with None
            self.log.debug("Preprocess row %i", self.row)
            for k in self.data.keys():
                self.data[k][self.row] = None

            # Handle Id and filename
            self.data["Id"][self.row] = self._stripFileType(fname)
            self.data["filename"][self.row] = file

            # fits header import
            header = fits.getheader(file)
            
            # Now overwrite with header information 
            for item in header:
                self.log.debug("Processiong Header Item: %s", item)
                self.data[item][self.row] = header[item]
                            
            # handle keys, which have been missing from this file
            self.log.debug("Postprocess row %i", self.row)
            for k in self.data.keys():
                if len(self.data[k]) <= self.row:
                    self.log.debug("Fixing key %s", k)
                    for i in range(0, self.row):
                        if self.data[k].get(i) is None: 
                            self.data[k][i] = None

            # Next row
            self.row += 1
            return True
        except (OSError, Exception) as e:
            self.log.error("Skipping %s, due to Error", file)
            self.log.exception(e)
            return False

    def store(self, data: SessionData) -> bool:
        return data.add(self.data)

if __name__ == "__main__":
    chdlr = logging.StreamHandler()
    logging.getLogger().addHandler(chdlr)
    logging.getLogger().setLevel(logging.DEBUG)  
    logging.getLogger().info("Test")

    imp = FitsImporter()
    a = "../testdata/fits/session/A.fits"
    assert imp.wantProcess(a), "FitsImporter should accept 'A.fits'"
    assert imp.process(a), "FitsImporter could not process 'A.fits', that's wrong"
    b = "../testdata/fits/session/B.fits"
    assert imp.wantProcess(b), "FitsImporter should accept 'B.fits'"
    assert imp.process(b), "FitsImporter could not process 'B.fits', that's wrong"

    data = Mock()
    imp.store(data)
    # data.add.assert_called_once_with({"Id": ["A"], "filename": ["testdata/fits/A.fits"], "SIMPLE": [True], "BITPIX": [8], "NAXIS": [0], "AAA": [1]})
    data.add.assert_called_once_with({"Id": {0:"A", 1:"B"}, "filename": {0:a, 1:b}, "SIMPLE": {0:True,1:True}, "BITPIX": {0:8,1:8}, "NAXIS": {0:0,1:0}, 
                                      "AAA": {0:1, 1:None}, "BBB": {0:None, 1:1}})

