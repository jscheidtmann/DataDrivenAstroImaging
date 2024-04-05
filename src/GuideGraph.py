from PyQt6.QtCharts import (
    QChartView,
)
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QColor, QPen


class QGuideGraph(QChartView):
    raPulses = None
    decPulses = None
    raRate = 13.5
    decRate = 13.5

    def setRaGuidePulses(self, pulses):
        self.raPulses = pulses

    def setDecGuidePulses(self, pulses):
        self.decPulses = pulses

    def drawForeground(self, painter, rect):
        # r = self.chart().plotArea()
        # h = (r.bottom() - r.top()) / 3.0
        if self.raPulses is not None:
            painter.save()
            pen = QPen(QColor(0x00, 0x00, 0xFF, 0x7F))
            pen.setWidth(2)
            painter.setPen(pen)
            rate = self.raRate / 1000.0

            for pulse in self.raPulses:
                p1 = self.chart().mapToPosition(QPointF(pulse[0], 0))
                p1.setX(p1.x() - 1.0)
                p2 = self.chart().mapToPosition(QPointF(pulse[0], pulse[1] * rate))
                p2.setX(p1.x())
                painter.drawLine(p1, p2)
            painter.restore()

        if self.decPulses is not None:
            painter.save()
            pen = QPen(QColor(0xFF, 0x00, 0x00, 0x7F))
            pen.setWidth(2)
            painter.setPen(pen)
            rate = self.decRate / 1000.0

            for pulse in self.decPulses:
                p1 = self.chart().mapToPosition(QPointF(pulse[0], 0))
                p1.setX(p1.x() + 1.0)
                p2 = self.chart().mapToPosition(QPointF(pulse[0], pulse[1] * rate))
                p2.setX(p1.x())
                painter.drawLine(p1, p2)

            painter.restore()
