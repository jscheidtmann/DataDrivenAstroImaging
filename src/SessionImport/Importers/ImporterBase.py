class ImporterBase:
    def process(self, file: str) -> bool:
        assert False, "You need to implement this method in a derived class"

class ImporterMetaBase:
    def __init__(self):
        self.instance = None

    def getShortName(self) -> str:
        assert False, "You need to implement this method in a derived class"
        
    def getTooltipDescription(self) -> str: 
        assert False, "You need to implement this method in a derived class"

    def getInstance(self) -> ImporterBase:
        assert False, "You need to implement this method in a derived class and return an instance of the respective Importer class"
         
        