from PIL.ImageQt import ImageQt
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QLabel
from PyQt6.QtWidgets import QVBoxLayout

from FitsImage import FitsImage


class ImageWindow(QDialog):
    imageWidget = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.createDialog()

    def createDialog(self):
        layout = QVBoxLayout()
        self.setFixedSize(QSize(800, 600))
        self.imageWidget = QLabel()
        layout.addWidget(self.imageWidget)

        self.setLayout(layout)

    def loadImage(self, filename):
        image = FitsImage()
        image.fromFile(filename)
        # image.analyse()

        qim = ImageQt(image.imageDisplaySaturated)
        pixmap = QPixmap.fromImage(qim)
        self.imageWidget.setPixmap(pixmap)
        self.imageWidget.setScaledContents(True)

    def show(self, filename):
        self.loadImage(filename)
        self.showNormal()
