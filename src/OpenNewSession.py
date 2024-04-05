from os import walk

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QTableWidget
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QWidget, QDialog, QGroupBox, QPushButton, QTableWidgetItem, QLabel


class OpenNewSession(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.imageData = None
        self.imagesTable = None
        self.loadImages = None
        self.loadMetadata = None
        self.loadGuidingLog = None
        self.guidingText = None
        self.createDialog()

    def set(self, imageData):
        self.imageData = imageData

    def createDialog(self):
        layout = QVBoxLayout()
        self.setFixedSize(QSize(800, 600))

        widget1 = QWidget()
        hLayout1 = QHBoxLayout()
        widget1.setLayout(hLayout1)
        layout.addWidget(widget1)

        imagesData = QGroupBox()
        imagesData.setTitle("Image data")
        hLayout1.addWidget(imagesData)

        imagesLayout = QVBoxLayout()
        imagesData.setLayout(imagesLayout)

        imageDataLayout = QHBoxLayout()
        imagesLayout.addLayout(imageDataLayout, 8)

        self.loadImages = QPushButton()
        self.loadImages.setText('Select Light frames...')
        self.loadImages.setStyleSheet('QPushButton { '
                                  'background-color: #2B5DD1; color: #FFFFFF ; '
                                  'padding: 2px; padding-left: 32px; padding-right: 32px; font: bold 14px ; '
                                  'border-width: 0px; border-radius: 4px;  }'
                                  'QPushButton:pressed {'
                                  ' background-color: #2B5FF1; color: #FFFF00; }'
                                  'QPushButton:hover:!pressed {'
                                  ' background-color: #1B2DA1; color: #FFFF00;  }')
        self.loadImages.pressed.connect(self.OnLoadLightFrames)

        imageDataLayout.addWidget(self.loadImages)

        self.loadMetadata = QPushButton()
        self.loadMetadata.setText('Load Metadata...')
        self.loadMetadata.setStyleSheet('QPushButton { '
                                      'background-color: #2B5DD1; color: #FFFFFF ; '
                                      'padding: 2px; padding-left: 32px; padding-right: 32px; font: bold 14px ; '
                                      'border-width: 0px; border-radius: 4px;  }'
                                      'QPushButton:pressed {'
                                      ' background-color: #2B5FF1; color: #FFFF00; }'
                                      'QPushButton:hover:!pressed {'
                                      ' background-color: #1B2DA1; color: #FFFF00;  }')
        self.loadMetadata.pressed.connect(self.OnLoadMetadata)
        self.loadMetadata.setEnabled(False)
        imageDataLayout.addWidget(self.loadMetadata)

        self.imagesTable = QTableWidget()
        imagesLayout.addWidget(self.imagesTable)

        widget = QWidget()
        layout.addWidget(widget)

        hLayout2 = QHBoxLayout()
        widget.setLayout(hLayout2)

        sessionGuidingData = QGroupBox()
        sessionGuidingData.setTitle("Guiding Log")

        guidingLayout = QVBoxLayout()
        sessionGuidingData.setLayout(guidingLayout)

        self.loadGuidingLog = QPushButton()
        self.loadGuidingLog.setText('Load Guiding Log...')
        self.loadGuidingLog.setStyleSheet('QPushButton { '
                                      'background-color: #2B5DD1; color: #FFFFFF ; '
                                      'padding: 2px; padding-left: 32px; padding-right: 32px; font: bold 14px ; '
                                      'border-width: 0px; border-radius: 4px;  }'
                                      'QPushButton:pressed {'
                                      ' background-color: #2B5FF1; color: #FFFF00; }'
                                      'QPushButton:hover:!pressed {'
                                      ' background-color: #1B2DA1; color: #FFFF00;  }')

        self.loadGuidingLog.pressed.connect(self.OnLoadGuidingLog)
        guidingLayout.addWidget(self.loadGuidingLog)

        self.guidingText = QLabel()
        self.guidingText.setText("No Guiding Data")
        self.guidingText.setStyleSheet("color: #CCCCCC")
        guidingLayout.addWidget(self.guidingText)

        hLayout2.addWidget(sessionGuidingData)

        bottomWidget = QWidget()
        bottomLayout = QHBoxLayout()
        bottomWidget.setLayout(bottomLayout)

        okButton = QPushButton()
        okButton.setText("OK")
        okButton.setContentsMargins(32, 4, 32, 4)
        okButton.setStyleSheet('QPushButton { '
                               'background-color: #2B5DD1; color: #FFFFFF ; border-style: outset; '
                               'padding: 2px; padding-left: 32px; padding-right: 32px; font: bold 14px ; '
                               'border-width: 2px; border-radius: 10px; border-color: #2752B8; }'
                               'QPushButton:pressed {'
                               ' background-color: #2B5FF1; color: #FFFF00; border-color: #1712FF; border-style: none  }'
                               'QPushButton:hover:!pressed {'
                               ' background-color: #1B2DA1; color: #FFFF00; border-color: #1712FF }')

        okButton.pressed.connect(self.OnOkPressed)

        cancelButton = QPushButton()
        cancelButton.setText("Cancel")
        cancelButton.setContentsMargins(32, 4, 32, 4)
        cancelButton.setStyleSheet('QPushButton { background-color: #2B5DD1; color: #FFFFFF ; border-style: outset; '
                               'padding: 2px; padding-left: 32px; padding-right: 32px; font: bold 14px ; '
                               'border-width: 2px; border-radius: 10px; border-color: #2752B8; }'
                               'QPushButton:pressed {'
                               ' background-color: #2B5FF1; color: #FFFF00; border-color: #1712FF; border-style: none }'
                               'QPushButton:hover:!pressed {'
                               ' background-color: #1B2DA1; color: #FFFF00; border-color: #1712FF }')

        cancelButton.pressed.connect(self.OnCancelPressed)

        bottomLayout.addWidget(okButton)
        bottomLayout.addStretch()
        bottomLayout.addWidget(cancelButton)

        layout.addWidget(bottomWidget)

        self.setLayout(layout)

    def execute(self):
        self.exec()

    def OnOkPressed(self):
        self.close()

    def OnCancelPressed(self):
        self.close()

    def OnLoadGuidingLog(self):
        logFile = QFileDialog.getOpenFileName(self, "Select the Guiding Log file...", filter="Text Files (*.txt)")
        if logFile is not None:
            self.imageData.readGuidingData(logFile[0])
            self.guidingText.setText(str(self.imageData.guidingData.count()) + " Guiding Frames loaded...")
            self.imageData.process()

        return

    def OnLoadLightFrames(self):
        lightFramesDir = QFileDialog.getExistingDirectory(self, "Select directory containing the light frames...")
        fileNames = []
        for (dirpath, dirnames, filenames) in walk(lightFramesDir):
            for fname in filenames:
                if fname.endswith('.fits') or fname.endswith('.fit'):
                    fileNames.append(fname)
            break

        self.imageData.imageFolder = lightFramesDir
        self.imageData.createNew()
        self.imageData.parseLightFrames(lightFramesDir, fileNames)

        self.imageData.process()

        headers = list(self.imageData.data)
        self.imagesTable.setRowCount(self.imageData.data.shape[0])
        self.imagesTable.setColumnCount(self.imageData.data.shape[1])
        self.imagesTable.setHorizontalHeaderLabels(headers)

        # getting data from df is computationally costly so convert it to array first
        for row in range(self.imageData.data.shape[0]):
            currentRow = self.imageData.data.iloc[row]
            for i, col in enumerate(self.imageData.getColumns()):
                self.imagesTable.setItem(row, i, QTableWidgetItem(str(currentRow[col])))

        self.loadMetadata.setEnabled(len(headers)>0)
        return

    def OnLoadMetadata(self):
        metafile = QFileDialog.getOpenFileName(self, "Select the Metadata file...", filter="CSV Files (*.csv)")
        if metafile is not None:
            self.imageData.readMetaData(metafile[0])
        return