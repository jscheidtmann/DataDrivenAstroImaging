from Importers.ImporterBase import ImporterBase
import os
import logging

class Importer:
    def __init__(self) -> None:
        self.log = logging.getLogger("Importer")
        self.directory = None
        self.importers = []

    def addImporter(self, importer : ImporterBase) -> None:
        assert importer is not None, "Do not pass Null object"
        # assert issubclass(ImporterBase, importer.__class__), "Wrong type passed." + str(type(importer))
        self.importers.append(importer)
    
    def setImportDirectory(self, directory) -> None:
        self.directory = directory

    def getImportDirectory(self) -> str:
        return self.directory

    def runImport(self):
        """
        Recursive descent into directory, ask each importer in turn, if they want to process and if yes, enqueue.
        """
        self.log.info("Import started")
        # Start Importers
        for imp in self.importers:
            imp.start()
        self.log.info("Import running")

        try: 
            self.log.info("Processing Import: %s", self.directory) 
            the_walk = os.walk(self.directory)
            for (root, _, files) in the_walk:
                for f in files:
                    file_path = os.path.join(root, f)
                    self.log.info("File: %s", file_path)
                    for imp in self.importers:
                        if imp.wantProcess(file_path):
                            imp.enqueue(file_path)
        except Exception as e:
            self.log.error("Exception in Importer.runImport")
            self.log.exception(e)

        # Stop Importers
        for imp in self.importers:
            imp.stop()
        self.log.info("Import stopped")
