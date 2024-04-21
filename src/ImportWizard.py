import sys
import os
import random
import time
from PyQt6.QtWidgets import QApplication, QWizard, QWizardPage, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QWidget, QLabel, QFileDialog, QProgressBar
from PyQt6.QtCore import QSettings
from PyQt6.QtCore import QThread, pyqtSignal

class ImportWizard(QWizard):
    def __init__(self, parent=None):
        super(ImportWizard, self).__init__(parent)
        self.page2widget = ProgressBarWidget()
        self.page1 = self.addPage(ChooseSessionDirectoryWidget())
        self.page2 = self.addPage(self.page2widget)
        self.page3 = self.addPage(PageThree())
        
        self.setWindowTitle("PyQt6 Wizard Example")
        
        self.currentIdChanged.connect(self.on_current_id_changed)

    def on_current_id_changed(self, id):
        if id == self.page1: 
            print("Page1")
        if id == self.page2:
            self.page2widget.reset()
            print("Page2")
        if id == self.page3:
            print("Page3")

class ChooseSessionDirectoryWidget(QWizardPage):
    def __init__(self):
        super().__init__()

        self.settings = QSettings('Bayer', 'MyTestApp')
        self.init_ui()

    def init_ui(self):
        # Set up the layout
        layout = QVBoxLayout()

        # Create the button to open the file dialog
        self.open_button = QPushButton('Open File Dialog')
        self.open_button.clicked.connect(self.open_file_dialog)

        # Create the list widget to display the file paths
        self.list_widget = QListWidget()

        # Add widgets to the layout
        layout.addWidget(self.open_button)
        layout.addWidget(self.list_widget)

        # Set the layout on the application's window
        self.setLayout(layout)

    def open_file_dialog(self):
        # Get the last used directory from QSettings
        last_used_directory = self.settings.value('lastUsedDirectory', '')

        # Open the file dialog and get the selected file paths
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select files", last_used_directory)

        # Clear out list widget
        self.list_widget.clear()

        # Populate the list widget with the selected file paths
        for path in file_paths:
            base = os.path.basename(path)
            item = QListWidgetItem(base)
            item.setToolTip(path)
            self.list_widget.addItem(item)

        if file_paths:
            # Extract the directory from the last selected file's path
            last_directory = os.path.dirname(file_paths[-1])
            self.settings.setValue('lastUsedDirectory', last_directory)


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
        self.setTitle("Page 3")
        layout = QVBoxLayout()

        layout.addWidget(CustomListWidget())

        self.setLayout(layout)

class CustomListItem(QWidget):
    def __init__(self, title, text):
        super().__init__()
        layout = QVBoxLayout()

        # Create the title label with bold text
        title_label = QLabel(f'<b>{title}</b>')
        layout.addWidget(title_label)

        # Create the text label
        text_label = QLabel(text)
        text_label.setWordWrap(True)  # Enable word wrap
        layout.addWidget(text_label)

        self.setLayout(layout)

class CustomListWidget(QListWidget):
    def __init__(self):
        super().__init__()

        # Add custom items to the list
        self.addItem('Finding 1:', 'Text lorem ipsum dolor sit amet, consectetur adipiscing elit.')
        self.addItem('Finding 2:', 'Text sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.')
        self.addItem('Finding 3:', 'Text ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.')

    def addItem(self, title, text):
        # Create a custom list item widget
        custom_item_widget = CustomListItem(title, text)

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