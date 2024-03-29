import os
import sys

import qdarktheme
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QBrush, QColor, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QComboBox, QToolButton, QTableWidgetItem
from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtWidgets import QTableWidget
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from astropy.coordinates import SkyOffsetFrame

import DataColumn as DataColumn
import ImageData as Data
from GuideGraph import QGuideGraph
from ImageWindow import ImageWindow
from OpenNewSession import OpenNewSession

is_frozen = getattr(sys, 'frozen', False)
frozen_temp_path = getattr(sys, '_MEIPASS', '')

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.leftGraphBox = None
        self.rightGraphBox = None
        self.guidingChartView = None
        self.guidingChart = None
        self.guidingChartAxis = []
        self.tableFrame = None
        self.openSession = None
        self.chartView = None
        self.ditherView = None
        self.ditherChart = None
        self.ditherChartView = None
        self.ditherChartAxis = []
        self.chart = None
        self.main_widget = None
        self.toolbar_widget = None
        self.overviewText = None
        self.imagesTable = None
        self.graphView = None
        self.createWindow()
        self.setWindowTitle("Image Session Analysis")
        self.setMinimumSize(800, 600)
        self.resize(1200, 800)
        self.imageData = Data.ImageData()
        self.imageFolder = None
        self.imageWindow = None
        self.sessionGraphLeft = None
        self.sessionGraphRight = None
        self.sessionGraphAxis = []

    def createToolBar(self):
        self.toolbar_widget = QWidget()
        toolBarLayout = QHBoxLayout()
        self.toolbar_widget.setLayout(toolBarLayout)
        toolBarLayout.setContentsMargins(4, 2, 4, 2)
        self.openSession = QToolButton()
        self.openSession.clicked.connect(self.openNewSession)

        if is_frozen:
            basedir = frozen_temp_path
        else:
            basedir = os.path.dirname(os.path.abspath(__file__))

        self.openSession.setFixedSize(QSize(32, 32))
        self.openSession.setIcon(QIcon(os.path.join(basedir, 'Icons/folder.png')))
        toolBarLayout.addWidget(self.openSession)
        toolBarLayout.addSpacing(8)

        self.changeSettings = QToolButton()
        self.changeSettings.setFixedSize(QSize(32, 32))
        self.changeSettings.setIcon(QIcon(os.path.join(basedir, 'Icons/gearshape.png')))
        toolBarLayout.addWidget(self.changeSettings)

        toolBarLayout.addStretch()

        return self.toolbar_widget

    def createImageTable(self):
        self.tableFrame = QWidget()
        tableFrameLayout = QVBoxLayout()
        tableFrameLayout.setContentsMargins(4, 4, 4, 4)
        self.tableFrame.setLayout(tableFrameLayout)
        self.imagesTable = QTableWidget()
        self.imagesTable.setSortingEnabled(True)

        self.imagesTable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableFrame.layout().addWidget(self.imagesTable)
        self.imagesTable.currentCellChanged.connect(self.OnCurrentTableCellChanged)
        self.imagesTable.cellDoubleClicked.connect(self.showImage)

        self.guidingChart = QChart()
        self.guidingChartView = QGuideGraph(self.guidingChart)
        self.guidingChartView.setFixedHeight(240)
        self.guidingChart.createDefaultAxes()
        self.guidingChart.setAnimationOptions(QChart.AnimationOption.AllAnimations)
        self.guidingChart.legend().setVisible(True)
        self.guidingChart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.guidingChart.setBackgroundBrush(QBrush(QColor(0, 0, 0)))

        self.tableFrame.layout().addWidget(self.guidingChartView)

        return self.tableFrame

    def createGraphView(self):
        self.graphView = QWidget()
        graphLayout = QVBoxLayout()
        self.graphView.setLayout(graphLayout)

        self.chart = QChart()
        self.chartView = QChartView(self.chart)
        self.chart.createDefaultAxes()
        self.chart.setAnimationOptions(QChart.AnimationOption.AllAnimations)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.chart.setBackgroundBrush(QBrush(QColor(0, 0, 0)))

        graphToolsWidget = QWidget()
        graphToolsLayout = QHBoxLayout()
        graphToolsLayout.setContentsMargins(4, 2, 4, 2)
        graphToolsWidget.setLayout(graphToolsLayout)

        self.leftGraphBox = QComboBox()
        self.leftGraphBox.currentIndexChanged.connect(self.OnLeftGraphValueIndexChanged)
        self.rightGraphBox = QComboBox()
        self.rightGraphBox.currentIndexChanged.connect(self.OnRightGraphValueIndexChanged)

        graphToolsLayout.addWidget(self.leftGraphBox)
        graphToolsLayout.addSpacing(32)
        graphToolsLayout.addWidget(self.rightGraphBox)

        graphLayout.addWidget(graphToolsWidget)
        graphLayout.addSpacing(4)
        graphLayout.addWidget(self.chartView)

        return self.graphView

    def createDitherView(self):
        self.ditherView = QWidget()
        graphLayout = QVBoxLayout()
        self.ditherView.setLayout(graphLayout)

        self.ditherChart = QChart()
        self.ditherChartView = QChartView(self.ditherChart)
        self.ditherChart.createDefaultAxes()
        self.ditherChart.setAnimationOptions(QChart.AnimationOption.AllAnimations)
        self.ditherChart.legend().setVisible(True)
        self.ditherChart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.ditherChart.setBackgroundBrush(QBrush(QColor(0, 0, 0)))

        graphLayout.addWidget(self.ditherChartView)

        return self.ditherView

    def createTabWidget(self):
        tabWidget = QTabWidget()
        tabWidget.addTab(self.createImageTable(), "Data")
        tabWidget.addTab(self.createGraphView(), "Charts")
        tabWidget.addTab(self.createDitherView(), "Image Center")

        return tabWidget

    def createWindow(self):
        mainVertical = QVBoxLayout()

        mainVertical.addWidget(self.createToolBar())
        mainVertical.addSpacing(8)
        mainVertical.addWidget(self.createTabWidget())

        self.main_widget = QWidget(self)
        self.main_widget.setLayout(mainVertical)
        self.setCentralWidget(self.main_widget)
        return

    def openNewSession(self):
        dialog = OpenNewSession(self)
        dialog.set(self.imageData)
        dialog.execute()
        if self.imageData is not None and self.imageData.data is not None and self.imageData.data.empty == False:
            self.updateSessionValues()
            self.updateTable()
            self.updateSessionGraph()
            self.updateDitherGraph()
        return

    def OnCurrentTableCellChanged(self):
        self.updateGuideGraph()
        return

    def showImage(self):
        if self.imageData.imageFolder is not None:
            rowIndex = self.imagesTable.currentRow()
            filename = self.imageData.data.iloc[rowIndex][DataColumn.FNAME]
            filepath = os.path.join(self.imageData.imageFolder, filename)
            if self.imageWindow is None:
                self.imageWindow = ImageWindow(self)
            self.imageWindow.show(filepath)

    def updateTable(self):
        headers = list(self.imageData.data)
        self.imagesTable.setRowCount(self.imageData.data.shape[0])
        self.imagesTable.setColumnCount(self.imageData.data.shape[1])
        self.imagesTable.setHorizontalHeaderLabels(headers)

        # getting data from df is computationally costly so convert it to array first
        for row in range(self.imageData.data.shape[0]):
            currentRow = self.imageData.data.iloc[row]
            for i, col in enumerate(self.imageData.getColumns()):
                str = self.imageData.format(currentRow[col], col)
                item = QTableWidgetItem(str)
                item.setForeground(QBrush(self.imageData.getTextColor(currentRow[col], col)))
                self.imagesTable.setItem(row, i, item)

    def updateSessionValues(self):
        values = self.imageData.getChartValues()
        self.leftGraphBox.addItems(values.keys())
        self.rightGraphBox.addItems(values.keys())
        return

    def OnLeftGraphValueIndexChanged(self, index):
        values = self.imageData.getChartValues()
        keys = list(values.keys())
        key = keys[index]
        self.sessionGraphLeft = values[key]
        self.updateSessionGraph()
        return

    def OnRightGraphValueIndexChanged(self, index):
        values = self.imageData.getChartValues()
        keys = list(values.keys())
        key = keys[index]
        self.sessionGraphRight = values[key]
        self.updateSessionGraph()
        return

    def updateDitherGraph(self):

        self.ditherChart.removeAllSeries()
        for axis in self.ditherChartAxis:
            self.ditherChart.removeAxis(axis)
        self.ditherChart.legend().hide()
        self.ditherChartAxis.clear()

        positions = self.imageData.getDitherData()
        center = SkyOffsetFrame(origin=positions[0])
        ditherPositionsRA = []
        ditherPositionsDEC = []
        for pos in positions:
            d = pos.transform_to(center)
            ditherPositionsRA.append(d.lon.degree * 3600.0)
            ditherPositionsDEC.append(d.lat.degree * 3600.0)

        x_axis = QValueAxis()
        x_axis.setRange(min(ditherPositionsRA), max(ditherPositionsRA))
        x_axis.setLabelFormat("%3.1f\"")
        x_axis.setTickType(QValueAxis.TickType.TicksDynamic)
        x_axis.setTickInterval(10)
        x_axis.setGridLineColor(QColor(128, 128, 128, 128))
        x_axis.setTitleText("△RA")
        x_axis.setLabelsColor(QColor(255, 255, 255, 255))
        x_axis.setTitleBrush(QColor(255, 255, 255, 255))
        self.ditherChart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)
        self.ditherChartAxis.append(x_axis)

        y_axis = QValueAxis()
        y_axis.setRange(min(ditherPositionsDEC), max(ditherPositionsDEC))
        y_axis.setLabelFormat("%3.1f\"")
        y_axis.setTickType(QValueAxis.TickType.TicksDynamic)
        y_axis.setTickInterval(10)
        y_axis.setGridLineColor(QColor(128, 128, 128, 128))
        y_axis.setTitleText("△DEC")
        y_axis.setLabelsColor(QColor(255, 255, 255, 255))
        y_axis.setTitleBrush(QColor(255, 255, 255, 255))
        self.ditherChart.addAxis(y_axis, Qt.AlignmentFlag.AlignLeft)
        self.ditherChartAxis.append(y_axis)

        series = QLineSeries()
        series.setPointsVisible(True)

        for i in range(0, len(ditherPositionsRA)):
            series.append(ditherPositionsRA[i], ditherPositionsDEC[i])

        pen = series.pen()
        pen.setColor(QColor(255, 255, 0, 255))
        series.setPen(pen)
        self.ditherChart.addSeries(series)

    def updateSessionGraph(self):
        self.chart.removeAllSeries()
        for axis in self.sessionGraphAxis:
            self.chart.removeAxis(axis)
        self.chart.legend().hide()
        self.sessionGraphAxis.clear()

        exposures = self.getExposures()

        x_axis = QValueAxis()
        x_axis.setRange(1, max(exposures))
        x_axis.setLabelFormat("%d")
        x_axis.setTickType(QValueAxis.TickType.TicksDynamic)
        x_axis.setTickInterval(5)
        x_axis.setGridLineColor(QColor(128, 128, 128, 128))
        x_axis.setTitleText("Exposure")
        x_axis.setLabelsColor(QColor(255, 255, 255, 255))
        x_axis.setTitleBrush(QColor(255, 255, 255, 255))
        self.chart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)
        self.sessionGraphAxis.append(x_axis)

        if self.sessionGraphLeft is not None:
            leftSeries = QLineSeries()
            yvalues = self.createSeries(leftSeries, self.sessionGraphLeft)
            pen = leftSeries.pen()
            pen.setColor(QColor(255, 255, 0, 255))
            leftSeries.setPen(pen)
            self.chart.addSeries(leftSeries)

            miny = min(yvalues)
            maxy = max(yvalues)
            ticks = (maxy - miny) / 10

            yLeft_axis = QValueAxis()
            yLeft_axis.setRange(miny, maxy)
            yLeft_axis.setLabelFormat("%1.3f")
            if self.sessionGraphLeft == DataColumn.DetectedStars or self.sessionGraphLeft == DataColumn.ADUMean or \
                    self.sessionGraphLeft == DataColumn.ADUMedian or self.sessionGraphLeft == DataColumn.ADUMin or \
                    self.sessionGraphLeft == DataColumn.ADUMax:
                yLeft_axis.setLabelFormat("%d")

            yLeft_axis.setTickType(QValueAxis.TickType.TicksDynamic)
            yLeft_axis.setTickInterval(ticks)
            yLeft_axis.setGridLineColor(QColor(128, 128, 128, 128))
            yLeft_axis.setTitleText(self.sessionGraphLeft)
            yLeft_axis.setTitleBrush(QColor(255, 255, 0, 255))
            yLeft_axis.setLabelsColor(QColor(255, 255, 0, 255))
            self.chart.addAxis(yLeft_axis, Qt.AlignmentFlag.AlignLeft)
            self.sessionGraphAxis.append(yLeft_axis)

        if self.sessionGraphRight is not None:
            rightSeries = QLineSeries()
            yvalues = self.createSeries(rightSeries, self.sessionGraphRight)
            pen = rightSeries.pen()
            pen.setColor(QColor(0, 0, 255, 255))
            rightSeries.setPen(pen)
            self.chart.addSeries(rightSeries)

            miny = min(yvalues)
            maxy = max(yvalues)
            ticks = (maxy - miny) / 10

            yRight_axis = QValueAxis()
            yRight_axis.setRange(miny, maxy)
            yRight_axis.setLabelFormat("%1.3f")
            if self.sessionGraphRight == DataColumn.DetectedStars or self.sessionGraphRight == DataColumn.ADUMean or \
                    self.sessionGraphRight == DataColumn.ADUMedian or self.sessionGraphRight == DataColumn.ADUMin or \
                    self.sessionGraphRight == DataColumn.ADUMax:
                yRight_axis.setLabelFormat("%d")

            yRight_axis.setTickType(QValueAxis.TickType.TicksDynamic)
            yRight_axis.setTickInterval(ticks)
            yRight_axis.setGridLineColor(QColor(128, 128, 128, 128))
            yRight_axis.setTitleText(self.sessionGraphRight)
            yRight_axis.setTitleBrush(QColor(0, 0, 255, 255))
            yRight_axis.setLabelsColor(QColor(0, 0, 255, 255))
            self.chart.addAxis(yRight_axis, Qt.AlignmentFlag.AlignRight)
            self.sessionGraphAxis.append(yRight_axis)

    def createSeries(self, series, graphType):
        values = []
        seriesData = self.imageData.data[['INDEX', graphType]]
        for row in range(seriesData.shape[0]):
            currentRow = seriesData.iloc[row]
            index = currentRow[0]
            data = currentRow[1]

            if graphType == DataColumn.MOONALT or graphType == DataColumn.SUNALT \
                    or graphType == DataColumn.AZIMUTH or graphType == DataColumn.ALTITUDE:
                data = data.degree

            series.append(index, data)
            values.append(data)
            print(data)

        return values

    def getExposures(self):
        indices = []
        seriesData = self.imageData.data[['INDEX']]
        for row in range(seriesData.shape[0]):
            currentRow = seriesData.iloc[row]
            index = currentRow[0]
            indices.append(index)

        return indices

    def updateGuideGraph(self):
        rowIndex = self.imagesTable.currentRow()
        jd1 = self.imageData.data.iloc[rowIndex][DataColumn.EXPSTARTJDD]
        duration = self.imageData.data.iloc[rowIndex][DataColumn.EXPOSURE]
        jd2 = jd1 + duration / 86400.0
        frames = self.imageData.guidingData.getGuidingFrames(jd1, jd2)

        seriesRA = QLineSeries()
        seriesDEC = QLineSeries()

        self.guidingChart.removeAllSeries()
        self.guidingChart.legend().hide()

        for axis in self.guidingChartAxis:
            self.guidingChart.removeAxis(axis)

        self.guidingChartAxis.clear()

        maxRA = 0.0
        maxDEC = 0.0

        pulseRA = []
        pulseDEC = []

        for frame in frames:
            t = (frame.time - jd1) * 86400.0
            seriesRA.append(t, frame.raRawDistance)
            seriesDEC.append(t, frame.decRawDistance)
            maxRA = max(maxRA, abs(frame.raRawDistance))
            maxDEC = max(maxDEC, abs(frame.decRawDistance))
            raDir = 1.0
            if frame.raDirection == 'W':
                raDir = -1.0
            pulseRA.append((t, frame.raDuration * raDir))
            decDir = 1.0
            if frame.decDirection == 'S':
                decDir = -1.0
            pulseDEC.append((t, frame.decDuration * decDir))

        x_axis = QValueAxis()
        x_axis.setRange(1, duration)
        x_axis.setLabelFormat("%d")
        x_axis.setTickType(QValueAxis.TickType.TicksDynamic)
        x_axis.setGridLineColor(QColor(60, 60, 60, 128))
        x_axis.setTickInterval(5)
        x_axis.setTitleText("Time")
        self.guidingChart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)
        self.guidingChartAxis.append(x_axis)

        y_axis = QValueAxis()
        y_axis.setRange(-max(maxRA, maxDEC, 1.0), max(maxRA, maxDEC, 1.0))
        y_axis.setLabelFormat("%0.2f")
        y_axis.setTickType(QValueAxis.TickType.TicksDynamic)
        y_axis.setGridLineColor(QColor(60, 60, 60, 128))
        y_axis.setTickInterval(1)

        self.guidingChartAxis.append(y_axis)
        pen = seriesRA.pen()
        pen.setColor(QColor(0, 0, 255, 255))
        seriesRA.setPen(pen)

        self.guidingChart.addAxis(y_axis, Qt.AlignmentFlag.AlignLeft)
        self.guidingChart.addAxis(y_axis, Qt.AlignmentFlag.AlignRight)

        pen2 = seriesDEC.pen()
        pen2.setColor(QColor(255, 0, 0, 255))
        seriesDEC.setPen(pen2)

        self.guidingChart.addSeries(seriesRA)
        self.guidingChart.addSeries(seriesDEC)
        seriesRA.attachAxis(x_axis)
        seriesRA.attachAxis(y_axis)
        seriesDEC.attachAxis(x_axis)
        seriesDEC.attachAxis(y_axis)

        self.guidingChartView.setRaGuidePulses(pulseRA)
        self.guidingChartView.setDecGuidePulses(pulseDEC)

        self.guidingChartView.update()


if __name__ == "__main__":
    os.environ['PYQTGRAPH_QT_LIB'] = 'PyQt6'

    app = QApplication(sys.argv)
    # Apply the complete dark theme to your Qt App.
    qdarktheme.setup_theme()

    win = MainWindow()

    win.show()
    sys.exit(app.exec())
