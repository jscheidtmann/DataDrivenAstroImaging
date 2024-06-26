import logging

from queue import Queue
from threading import Thread
from SessionData import SessionData

class ImporterBase:
    """
    Base class for importers.

    Assumption is that all relevant data is stored in one or more directories as files.
    The Ìmporter` class instantiates all relevant Importers, given some configuration and then:
     - Starts all Importers using `start()` which executes `run()` in a separate process,
     - iterates over all files in the specified directory,
     - Calls `wantProcess(absolutePathToFile)` on each file and then
     - enqueues all files for which the previous method returned True. 
     - `run` consumes each enqueued file and calls `process()` on them.
     - An end marker is finally enqueued for each Importer with `stop()`, so that `run()` exits.
     - Finally `store()`is called for each Importer with the data object holding the current session. 

    The ImporterBase keeps track of import statistics:
     - total: The number of files processed (number of items which were enqueued)
     - skipped: the number of files which could not be processed successfully (`process()` returned False)
     - processed: the number of files which could be processed.
    """

    def __init__(self):
        """
        Initialize statistics and create a queue.
        """
        self.queue = Queue()
        self.total = 0
        self.processed = 0
        self.skipped = 0
        self.started = False
        self.log = logging.getLogger(self.__class__.__name__)
        if self.__class__ == ImporterBase:
            raise NotImplementedError("You cannot instantiate ImporterBase! Please derive a class from it.")

    def reset(self) -> None:
        self.total = 0
        self.processed = 0
        self.skipped = 0
        self.queue.clear()
        # self.stop()

    def start(self):
        if not self.started:
            self.log.info("Start Import Thread: %s", self.__class__)
            self.thread_ref = Thread(target=self.run)
            self.thread_ref.start()
            self.started = True

    def stop(self):
        if self.started:
            self.queue.put(None)
            self.started = False

    def forceStop(self):
        self.queue.clear()
        self.queue.put(None)

    def enqueue(self, file: str) -> bool:
        self.total += 1
        self.queue.put(file, block=False)

    def run(self) -> None:
        """
        This runs in a separate thread, until the element to process is None.
        For each element in the queue the self.process(item) method is called.
        """

        item = self.queue.get()  # Blocks, if empty
        while item is not None:   # Check for 'end' marker
            if self.process(item):
                self.processed += 1
            else:
                self.skipped += 1
            item = self.queue.get()
        self.log.info("Stopping Import thread: %s", self.__class__)
    
    def isrunning(self) -> bool:
        return not self.queue.empty()
    
    def getProcessedCounts(self) -> tuple[int, int, int]:
        return (self.processed, self.skipped, self.total)

    def getSkipped(self) -> int:
        return self.skipped
    
    def getProcessed(self) -> int:
        return self.processed
    
    def getTotal(self) -> int:
        return self.total

    def process(self, file: str) -> bool:
        """
        Process a file. This method needs to be overriden.

        This method is called in a separate thread, it is called for each file where
        Expectation is that the derived class stores the imported data internally and then updates the data on "store()"

        When the item was processed successfully, return True, if the processing failed and no data is used return False. 
        The item is then considered 'skipped'
        """
        raise NotImplementedError("you called an abstract method, that you need to implement yourself!")

    def wantProcess(self, file:str) -> bool:
        """
        Check if a certain file needs to be processed by this importer.

        This method is called in the interface thread and should return fast, so that the UI is responsive.
        If you need more processing, consider skipping items.
        """
        raise NotImplementedError("you called an abstract method, that you need to implement yourself!")

    def store(self, data: SessionData) -> bool:
        """
        Store information in the passed SessionData object

        If all data was stored, return true, else false.
        """
        raise NotImplementedError("you called an abstract method, that you need to implement yourself!")

class ImporterMetaBase:
    def __init__(self):
        self.instance = None
        if self.__class__ == ImporterMetaBase:
            raise NotImplementedError("You cannot instantiate ImporterMetaBase! Please derive a class from it.")

    def getShortName(self) -> str:
        raise NotImplementedError("you called an abstract method, that you need to implement yourself!")
        
    def getTooltipDescription(self) -> str: 
        raise NotImplementedError("you called an abstract method, that you need to implement yourself!")

    def getInstance(self) -> ImporterBase:
        raise NotImplementedError("you called an abstract method, that you need to implement yourself!")

    def getClass(self):
        raise NotImplementedError("you called an abstract method, that you need to implement yourself!")
    
    def getImpoterClass(self):
        raise NotImplementedError("You called an abstract method, that you need to implement yourself!")