from PyQt6.QtWidgets import (
    QGraphicsPolygonItem,
    QGraphicsItem,
    QStyleOptionGraphicsItem,
    QWidget,
)
from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtGui import QPolygonF, QBrush, QPainter, QTransform
from PyQt6.QtGui import QPen
from math import sqrt, atan2, degrees

pointF = QPointF | tuple[float, float]


class ArrowItem(QGraphicsItem):
    """docstring for Arrow."""

    def __init__(self, start: pointF, stop: pointF, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.polygon = QPolygonF(
            [
                QPointF(0.0, 0.0),
                QPointF(0.0, 5.0),
                QPointF(50.0, 5.0),
                QPointF(50.0, 13.0),
                QPointF(70.0, 0.0),
                QPointF(50.0, -13.0),
                QPointF(50.0, -5.0),
                QPointF(0.0, -5.0),
                QPointF(0.0, 0.0),
            ]
        )

        self.item = QGraphicsPolygonItem(self.polygon)

        self.start = start
        self.stop = stop

    def setBrush(self, brush: QBrush):
        self.item.setBrush(brush)
        self.item.setPen(QPen(brush.color()))

    def paint(self, paint: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget):
        self.item.paint(paint, option, widget)

    def boundingRect(self) -> QRectF:
        return self.item.boundingRect()

    @property
    def start(self):
        """The start property."""
        return self._start

    @start.setter
    def start(self, value):
        if type(value) is tuple:
            value = QPointF(*value)
        self._start = value

    @property
    def stop(self):
        """The stop property."""
        return self._stop

    @stop.setter
    def stop(self, value):
        if type(value) is tuple:
            value = QPointF(*value)
        self._stop = value

    def transformArrow(self):
        tmp = self.stop - self.start
        length = sqrt(tmp.x()**2 + tmp.y()**2)
        scale = length / 70.0
        rotation = degrees(atan2(tmp.y(), tmp.x()))

        transform = QTransform()
        transform.rotate(rotation)
        transform.scale(scale, 1.0)

        self.setPos(self.start)
        self.setTransform(transform)
