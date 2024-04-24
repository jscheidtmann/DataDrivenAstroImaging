

import importlib.util
import os
import sys
from Importers.ImporterBase import ImporterMetaBase, ImporterBase

class ImportFactory:
    def __init__(self):
        self.directory = os.path.dirname(self.find_import_factory_location())

        self.importers_meta = self.find_and_instantiate_classes(self.directory, 'Meta')

    def getMetaImporters(self) -> list[ImporterMetaBase]:
        return self.importers_meta

    def find_import_factory_location(self) -> str:
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


    def find_and_instantiate_classes(self, base_dir: str, class_suffix: str) -> list[object]:
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
    factory = ImportFactory()
    for imp in factory.getMetaImporters():
        print(imp.getShortName())
    sys.exit(0)