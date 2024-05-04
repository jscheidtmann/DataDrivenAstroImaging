from SessionImport.Importers.PHD2Importer import PHD2Importer


def testPHD2ImporterEmptyCreation():
    PHD2Importer()

def testEmptyPHD2ImporterStoresNothing(mocker):
    imp = PHD2Importer()

    data = mocker.Mock()
    assert not imp.store(data), "Empty PHD2Importer stores somthing? What goes?"
    data.add.assert_not_called()