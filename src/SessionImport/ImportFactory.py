

import importlib.util
import os
import sys
import logging
from SessionImport.Importers.ImporterBase import ImporterMetaBase, ImporterBase
from SessionImport.Importer import Importer
from SessionData import SessionData

class ImportFactory:
    def __init__(self):
        self.log = logging.getLogger("ImportFactory")
        self.directory = os.path.dirname(self._find_import_factory_location())
        self.log.info("Reading import modules from: %s", self.directory)

        self.importers_meta = self._find_and_instantiate_classes(self.directory, 'Meta')

    def getMetaImporters(self) -> list[ImporterMetaBase]:
        self.log.info("getMetaImporters called")
        return self.importers_meta

    def getImporter(self) -> Importer:
        self.log.info("getImporter called")
        importer = Importer()

        for i in self.getMetaImporters():
            self.log.info("Import module: %s", i.getShortName())
            importer.addImporter(i.getInstance())
    
        return importer

    def _find_import_factory_location(self) -> str:
        """
        Determine the directory, where this source code file is located.
        """

        # Get the module name for this class
        module_name = self.__class__.__module__
        
        # Import the module based on the module name
        module = importlib.import_module(module_name)
        
        # Get the file location of the module
        file_location = getattr(module, '__file__', None)
        
        if file_location:
            return file_location
        else:
            raise RuntimeError("Cannot determine location of ImportFactory.py")


    def _find_and_instantiate_classes(self, base_dir: str, class_suffix: str) -> list[object]:
        instances = []
        
        # Remember the original sys.path
        original_sys_path = sys.path.copy()
  
        # Walk through all subdirectories in the base directory
        for root, dirs, files in os.walk(base_dir):
            for file_name in files:
                # Check if the file is a Python file
                if file_name.endswith('.py'):
                    # Remove the '.py' extension to get the class name
                    class_name = file_name[:-3] + class_suffix
                    # Construct the full path to the file
                    file_path = os.path.join(root, file_name)
                    # Add the directory of the file to sys.path for relative imports
                    if root not in sys.path:
                        sys.path.insert(0, root)
                    # Create a module spec
                    spec = importlib.util.spec_from_file_location("Importers." + class_name, file_path)
                    # Create a module object from the spec
                    module = importlib.util.module_from_spec(spec)
                    # Execute the module in its own namespace
                    spec.loader.exec_module(module)
                    
                    # Get the class from the module
                    klass = getattr(module, class_name, None)
                    if klass:
                        # Instantiate the class and add the instance to the list
                        instances.append(klass())
        
        # Restore the original sys.path
        sys.path = original_sys_path
    
        return instances

if __name__ == "__main__":
    chdlr = logging.StreamHandler()
    logging.getLogger().addHandler(chdlr)
    logging.getLogger().info("Test")
    logging.getLogger().setLevel(logging.DEBUG)  

    factory = ImportFactory()
    factory.log.info("Executing ImportFactory from commandline.")
    imp = factory.getImporter()
    factory.log.info("Retrieved importers, running import.")

    for dir in sys.argv[1:]:
        factory.log.info("Import directory: %s", dir)
        imp.setImportDirectory(dir)
        imp.runImport()
    import time
    while imp.isrunning():
        imp.log.info("Waiting for import to finish") 
        time.sleep(1)
    imp.log.info("Import finished")
    imp.log.info("Storing Data")
    imp.storeData(SessionData())
    sys.exit(0)
