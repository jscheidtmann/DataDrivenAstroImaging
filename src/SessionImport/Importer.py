from SessionImport.Importers.ImporterBase import ImporterBase
from SessionData import SessionData
import os
import logging

class Importer:
    def __init__(self) -> None:
        self.log = logging.getLogger("Importer")
        self.directory = None
        self.importers = []
        self.total_files = 0

    def addImporter(self, importer : ImporterBase) -> None:
        assert importer is not None, "Do not pass Null object"
        # assert issubclass(ImporterBase, importer.__class__), "Wrong type passed." + str(type(importer))
        self.importers.append(importer)
    
    def setImportDirectory(self, directory) -> None:
        self.directory = directory

    def getImportDirectory(self) -> str:
        return self.directory

    def isrunning(self) -> bool:
        runs = False
        for imp in self.importers:
            if imp.isrunning():
                self.log.debug("Import running for %s", imp.__class__)
            runs |= imp.isrunning()
        return runs
    
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
            self.log.info("Processing Import Directory: %s", self.directory) 
            the_walk = os.walk(self.directory)
            for (root, _, files) in the_walk:
                for f in files:
                    file_path = os.path.join(root, f)
                    self.log.info("File: %s", file_path)
                    self.total_files += 1
                    for imp in self.importers:
                        if imp.wantProcess(file_path):
                            self.log.debug("File '%s' processed by importer '%s'", file_path, imp.__class__)
                            imp.enqueue(file_path)
        except Exception as e:
            self.log.error("Exception in Importer.runImport")
            self.log.exception(e)
        self.log.info("Total files processed: %d", self.total_files)

        # Stop Importers
        for imp in self.importers:
            imp.stop()
        self.log.info("Import finalizing")

    def storeData(self, data: SessionData) -> None:
        self.log.info("Storing Data: start")
        for imp in self.importers:
            self.log.debug("Storing data from importer: %s", imp.__class__)
            imp.store(data)
        self.log.info("Storing Data: Done")