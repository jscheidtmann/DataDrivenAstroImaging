
from SessionImport.Importers.FitsImporter import FitsImporter

def testEmptyFitsImporterCreation():
    FitsImporter()

def testFitsAcceptance():
    imp = FitsImporter()
    assert imp.wantProcess("A.fits"), "FitsImporter does not process A.fits"
    assert imp.wantProcess("A.fts"), "FitsImporter does not process A.fts"
    assert imp.wantProcess("A.fit"), "FitsImporter does not process A.fit"

def testNonAcceptance():
    imp = FitsImporter()
    assert not imp.wantProcess("A.xisf"), "FitsImporter accepts XISF, what's that?"
    assert not imp.wantProcess("A.nef"), "FitsImporter accepts NEF, what's that?"
    assert not imp.wantProcess("A.cr2"), "FitsImporter accepts CR2, what's that?"

def testImportInvalidFits():
    imp = FitsImporter()
    f = "testdata/invalidfits/invalid.fits"
    assert imp.wantProcess(f), "FitsImporter should accept 'invalid.fits'"
    assert not imp.process(f), "FitsImporter returns true for 'invalid.fits'"

def testImportNonExistingFits():
    imp = FitsImporter()
    f = "non-existing-file.fits"
    assert imp.wantProcess(f), "FitsImporter should accept 'non-existing-file.fits'"
    assert not imp.process(f), "FitsImporter returns true for 'non-existing-file.fits'"


def testProcessAFits(mocker):
    imp = FitsImporter()
    f = "testdata/fits/A.fits"
    assert imp.wantProcess(f), "FitsImporter should accept 'A.fits'"
    assert imp.process(f), "FitsImporter could not process 'A.fits', that's wrong"

    data = mocker.Mock()
    imp.store(data)
    data.add.assert_called_once()
    