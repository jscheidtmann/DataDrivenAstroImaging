import sys
import os
import random
import time
from PyQt6.QtWidgets import QApplication, QWizard, QWizardPage, QVBoxLayout, QHBoxLayout, QPushButton, \
     QListWidget, QListWidgetItem, QWidget, QLabel, QFileDialog, QProgressBar, QLineEdit
from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtCore import QThread, pyqtSignal

class ImportWizard(QWizard):
    def __init__(self, parent=None):
        super(ImportWizard, self).__init__(parent)
        self.page2widget = ProgressBarWidget()
        self.page1 = self.addPage(ChooseSessionDirectoryWidget())
        self.page2 = self.addPage(self.page2widget)
        self.page3 = self.addPage(PageThree())
        
        self.setWindowTitle("Import Wizard - Fake it, befor you make it")
        
        self.currentIdChanged.connect(self.on_current_id_changed)

    def on_current_id_changed(self, id) -> None:
        if id == self.page1: 
            print("Page1")
        if id == self.page2:
            self.page2widget.reset()
            print("Page2")
        if id == self.page3:
            print("Page3")

class ChooseSessionDirectoryWidget(QWizardPage):
    """
    Import Wizard: Select Directory to import

    Displays a FileSelectionDialog that selects a Directory, 
    also display the import configuration in a list widget.
    """
    def __init__(self):
        super().__init__()

        self.settings = QSettings('Bayer', 'MyTestApp')
        self.init_ui()

    def init_ui(self):
        # Set up the layout
        layout = QVBoxLayout()

        line1 = QHBoxLayout()
        self.directory = QLineEdit()
        line1.addWidget(self.directory)

        # Create the button to open the file dialog
        self.open_button = QPushButton('Select Session Directory')
        self.open_button.clicked.connect(self.open_file_dialog)
        line1.addWidget(self.open_button)

        # Create the list widget to display the file paths
        self.list_widget = QListWidget()
        self.list_widget.addItems(["FITS meta data import", "N.I.N.A. Session Metadata Plugin", "PixInsight(r) Subframe Selector Import"])

        # Add widgets to the layout
        layout.addLayout(line1)
        layout.addWidget(self.list_widget)

        self.add_button = QPushButton('Add')
        self.remove_button = QPushButton('Remove')
        self.up_button = QPushButton('Up')
        self.down_button = QPushButton('Down')

        line2 = QHBoxLayout()
        line2.addWidget(self.add_button)
        line2.addWidget(self.remove_button)
        line2.addWidget(self.up_button)
        line2.addWidget(self.down_button)

        layout.addLayout(line2)

        # Set the layout on the application's window
        self.setLayout(layout)

    def open_file_dialog(self):
        # Get the last used directory from QSettings
        last_used_directory = self.settings.value('lastUsedDirectory', '')

        # Open the file dialog to select a directory
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", last_used_directory)

        # Check if a directory was selected
        if directory:
            # Populate the QLineEdit with the selected directory
            self.directory.setText(directory)
            # Update the last used directory in QSettings
            self.settings.setValue('lastUsedDirectory', directory)


# Worker thread that simulates a task
class Worker(QThread):
    # Signal to update the progress
    progress = pyqtSignal(int)

    def run(self):
        for _ in range(101):
            # Simulate work by sleeping for a random amount of time
            time.sleep(random.uniform(0.01, 0.1))
            # Emit signal to update the progress bar
            self.progress.emit(1)


class ProgressBarWidget(QWizardPage):
    def __init__(self):
        super().__init__()

        # Set up the layout
        layout = QVBoxLayout()

        # Create and add progress bars to the layout
        self.progress_bars = [QProgressBar(self) for _ in range(4)]
        for bar in self.progress_bars:
            layout.addWidget(bar)

        # Set the layout on the application's window
        self.setLayout(layout)

        # Create and start worker threads
        self.workers = [Worker() for _ in range(4)]
        for bar, worker in zip(self.progress_bars, self.workers):
            worker.progress.connect(lambda value, bar=bar: self.update_progress(bar, value))
            # worker.start()

    def reset(self) -> None:
        for pgb in self.progress_bars:
            pgb.setValue(0)
        for worker in self.workers:
            worker.start()

    def initializePage(self) -> None:
        self.reset()
        return super().initializePage()
    
    def update_progress(self, bar, value):
        # Update the progress bar's value
        bar.setValue(bar.value() + value)

class PageThree(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Findings")

        #  |--------------|    
        #  | List Item 1  |
        #  | List Item 2  |     Details
        #  | ...          |     Details
        #  |              |
        #  |--------------|  |-----------|
        #  | Prev  | Next |  | Show more |
        #  |--------------|  |-----------|
         
        layout = QHBoxLayout()
        column1 = QVBoxLayout()

        self.list_widget = CustomListWidget()
        column1.addWidget(self.list_widget)

        line1 = QHBoxLayout()
        self.but_prev = QPushButton("Previous")
        line1.addWidget(self.but_prev)
        self.but_next = QPushButton("Next")
        line1.addWidget(self.but_next)
        column1.addLayout(line1)

        layout.addLayout(column1)
        
        column2 = QVBoxLayout()
        # Create the QLabel
        self.label = QLabel("Select an item from the list")
        column2.addWidget(self.label)
        column2.addWidget(QPushButton("Show more"))
        layout.addLayout(column2)

        # Connect the itemSelectionChanged signal to the update_label slot
        self.list_widget.itemSelectionChanged.connect(self.update_label)

        self.but_next.clicked.connect(self.next_clicked)
        self.but_prev.clicked.connect(self.prev_clicked)

        self.setLayout(layout)

        self.list_widget.setCurrentRow(0)

    def next_clicked(self):
        row = self.list_widget.currentRow()
        if row + 1 < self.list_widget.count():
            self.list_widget.setCurrentRow(row + 1)

    def prev_clicked(self):
        row = self.list_widget.currentRow()
        if row - 1 >= 0:
            self.list_widget.setCurrentRow(row - 1)

    def update_label(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            # Get the text associated with the first selected item and update the QLabel
            if isinstance(selected_item, QListWidgetItem):
                text = self.list_widget.itemWidget(selected_item).getDescription()
                self.label.setText(text)
            else:
                print(type(selected_item))
        else:
            # No item is selected
            self.label.setText("Select an item from the list")

class CustomListItem(QWidget):
    def __init__(self, title, text, description):
        super().__init__()
        layout = QVBoxLayout()

        # Create the title label with bold text
        title_label = QLabel(f'<b>{title}</b>')
        layout.addWidget(title_label)

        # Create the text label
        text_label = QLabel(text)
        text_label.setWordWrap(True)  # Enable word wrap
        layout.addWidget(text_label)

        self.description = description
        
        self.setLayout(layout)

    def getDescription(self):
        return self.description


class CustomListWidget(QListWidget):
    def __init__(self):
        super().__init__()

        # Add custom items to the list
        self.addItem('Finding 1:', 'Text lorem ipsum dolor sit amet, consectetur adipiscing elit.', 'X is not related to Y')
        self.addItem('Finding 2:', 'Text sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 'Your dithering is too large and never settles')
        self.addItem('Finding 3:', 'Text ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.', 'Blablabla')

    def addItem(self, title, text, description):
        # Create a custom list item widget
        custom_item_widget = CustomListItem(title, text, description)

        # Create a QListWidgetItem
        item = QListWidgetItem(self)

        # Set some size hint
        item.setSizeHint(custom_item_widget.sizeHint())

        # Add the item to the list
        super().addItem(item)

        # Set the custom widget for the item
        self.setItemWidget(item, custom_item_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wizard = ImportWizard()
    wizard.show()
    error = app.exec()
    print(error)
    sys.exit(error)