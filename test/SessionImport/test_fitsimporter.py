
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
    # data.add.assert_called_once_with({"Id": ["A"], "filename": ["testdata/fits/A.fits"], "SIMPLE": [True], "BITPIX": [8], "NAXIS": [0], "AAA": [1]})
    data.add.assert_called_once_with({"Id": ["A"], "filename": [f], "SIMPLE": [True], "BITPIX": [8], "NAXIS": [0], "AAA": [1]})

def testProcessABFits(mocker):
    imp = FitsImporter()
    f = "testdata/fits/A.fits"
    assert imp.wantProcess(f), "FitsImporter should accept 'A.fits'"
    assert imp.process(f), "FitsImporter could not process 'A.fits', that's wrong"
    g = "testdata/fits/B.fits"
    assert imp.wantProcess(g), "FitsImporter should accept 'B.fits'"
    assert imp.process(g), "FitsImporter could not process 'B.fits', that's wrong"

    data = mocker.Mock()
    imp.store(data)
    # data.add.assert_called_once_with({"Id": ["A"], "filename": ["testdata/fits/A.fits"], "SIMPLE": [True], "BITPIX": [8], "NAXIS": [0], "AAA": [1]})
    data.add.assert_called_once_with({"Id": ["A", "B"], "filename": [f,g], "SIMPLE": [True,True], "BITPIX": [8,8], "NAXIS": [0,0], "AAA": [1, None], "BBB": [None, 1]})

def testProcessABABFits(mocker):
    imp = FitsImporter()
    f = "testdata/fits/A.fits"
    g = "testdata/fits/B.fits"
    assert imp.wantProcess(f), "FitsImporter should accept 'A.fits'"
    assert imp.process(f), "FitsImporter could not process 'A.fits', that's wrong"
    assert imp.wantProcess(g), "FitsImporter should accept 'B.fits'"
    assert imp.process(g), "FitsImporter could not process 'B.fits', that's wrong"
    assert imp.wantProcess(f), "FitsImporter should accept 'A.fits' (for second time)"
    assert imp.process(f), "FitsImporter could not process 'A.fits' (for second time), that's wrong"
    assert imp.wantProcess(g), "FitsImporter should accept 'B.fits' (for second time)"
    assert imp.process(g), "FitsImporter could not process 'B.fits' (for second time), that's wrong"

    data = mocker.Mock()
    imp.store(data)
    # data.add.assert_called_once_with({"Id": ["A"], "filename": ["testdata/fits/A.fits"], "SIMPLE": [True], "BITPIX": [8], "NAXIS": [0], "AAA": [1]})
    data.add.assert_called_once_with({"Id": ["A", "B", "A", "B"], "filename": [f,g,f,g], "SIMPLE": [True,True,True,True], "BITPIX": [8,8,8,8], 
                                      "NAXIS": [0,0,0,0], "AAA": [1, None, 1, None], "BBB": [None, 1, None, 1]})
