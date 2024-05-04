
from SessionImport.Importers.FitsImporter import FitsImporter
from SessionImport.Importer import Importer
import time

def testEmptyFitsImporterCreation():
    FitsImporter()

def testEmptyFitsImporterStoresNothing(mocker):
    imp = FitsImporter()

    data = mocker.Mock()
    assert not imp.store(data), "FitsImporters stores, although nothing was imported? What goes?"
    data.ass.assert_not_called()

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
    f = "testdata/fits/session/A.fits"
    assert imp.wantProcess(f), "FitsImporter should accept 'A.fits'"
    assert imp.process(f), "FitsImporter could not process 'A.fits', that's wrong"

    data = mocker.Mock()
    imp.store(data)
    # data.add.assert_called_once_with({"Id": ["A"], "filename": ["testdata/fits/A.fits"], "SIMPLE": [True], "BITPIX": [8], "NAXIS": [0], "AAA": [1]})
    data.add.assert_called_once_with({"Id": {0: "A"}, "filename": {0:f}, "SIMPLE": {0:True}, "BITPIX": {0:8}, "NAXIS": {0:0}, "AAA": {0:1}})

def testProcessABFits(mocker):
    imp = FitsImporter()
    a = "testdata/fits/session/A.fits"
    assert imp.wantProcess(a), "FitsImporter should accept 'A.fits'"
    assert imp.process(a), "FitsImporter could not process 'A.fits', that's wrong"
    b = "testdata/fits/session/B.fits"
    assert imp.wantProcess(b), "FitsImporter should accept 'B.fits'"
    assert imp.process(b), "FitsImporter could not process 'B.fits', that's wrong"

    data = mocker.Mock()
    imp.store(data)
    # data.add.assert_called_once_with({"Id": ["A"], "filename": ["testdata/fits/A.fits"], "SIMPLE": [True], "BITPIX": [8], "NAXIS": [0], "AAA": [1]})
    data.add.assert_called_once_with({"Id": {0:"A", 1:"B"}, "filename": {0:a, 1:b}, "SIMPLE": {0:True,1:True}, "BITPIX": {0:8,1:8}, "NAXIS": {0:0,1:0}, 
                                      "AAA": {0:1, 1:None}, "BBB": {0:None, 1:1}})

def testProcessABABFits(mocker):
    imp = FitsImporter()
    f = "testdata/fits/session/A.fits"
    g = "testdata/fits/session/B.fits"
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
    data.add.assert_called_once_with({"Id": {0:"A", 1:"B", 2:"A", 3:"B"}, "filename": {0:f,1:g,2:f,3:g}, "SIMPLE": {0:True,1:True,2:True,3:True}, 
                                      "BITPIX": {0:8,1:8,2:8,3:8}, "NAXIS": {0:0,1:0,2:0,3:0}, 
                                      "AAA": {0:1, 1:None, 2:1, 3:None}, "BBB": {0:None, 1:1, 2:None, 3:1}})
    
def testFitsImport(mocker):
    importer = Importer()
    imp = FitsImporter()
    importer.addImporter(imp)
    importer.setImportDirectory('testdata/fits/session/')
    importer.runImport()
    while importer.isrunning():
        time.sleep(0.05)
    
    data = mocker.Mock()
    importer.storeData(data)
    # data.add.assert_called_once_with({"Id": ["A"], "filename": ["testdata/fits/A.fits"], "SIMPLE": [True], "BITPIX": [8], "NAXIS": [0], "AAA": [1]})
    data.add.assert_called_once_with({"Id": {0:"A", 1:"B", 2:"C"}, "filename": {0:"testdata/fits/session/A.fits", 1:"testdata/fits/session/B.fits", 2:"testdata/fits/session/C.fits"},
                                      "SIMPLE": {0:True,1:True,2:True}, "BITPIX": {0:8,1:8,2:8}, "NAXIS": {0:0,1:0,2:0}, 
                                      "AAA": {0:1, 1:None, 2:None}, "BBB": {0:None, 1:1, 2:None}, "CCC": {0:None, 1:None, 2:1}})


if __file__ == "__main__":
    from unittest.mock import Mock
    imp = FitsImporter()
    f = "testdata/fits/session/A.fits"
    assert imp.wantProcess(f), "FitsImporter should accept 'A.fits'"
    assert imp.process(f), "FitsImporter could not process 'A.fits', that's wrong"
    g = "testdata/fits/session/B.fits"
    assert imp.wantProcess(g), "FitsImporter should accept 'B.fits'"
    assert imp.process(g), "FitsImporter could not process 'B.fits', that's wrong"

    data = Mock()
    imp.store(data)
    # data.add.assert_called_once_with({"Id": ["A"], "filename": ["testdata/fits/A.fits"], "SIMPLE": [True], "BITPIX": [8], "NAXIS": [0], "AAA": [1]})
    data.add.assert_called_once_with({"Id": {0:"A", 1:"B"}, "filename": {0:f, 1:g}, "SIMPLE": {0:True,1:True}, "BITPIX": {0:8,1:8}, "NAXIS": {0:0,1:0}, 
                                      "AAA": {0:1, 1:None}, "BBB": {0:None, 1:1}})
