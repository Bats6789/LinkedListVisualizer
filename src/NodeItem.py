from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsSceneMouseEvent
from PyQt6.QtCore import QVariant, QPointF, QRectF
from PyQt6.QtGui import QCursor
from typing import Self
from ArrowItem import ArrowItem
from math import sqrt

changeType = QGraphicsItem.GraphicsItemChange


def distance(a: QPointF, b: QPointF) -> float:
    tmp = a - b
    return sqrt(tmp.x() ** 2 + tmp.y() ** 2)


def closestPoint(start: QPointF, rect: QRectF) -> QPointF:
    minDist = 0
    stop = QPointF(0.0, 0.0)
    point = QPointF(0.0, 0.0)

    # Top point
    point.setX(rect.x() + rect.width() / 2)
    point.setY(rect.y())

    # Top point is always the closest seen so far
    stop.setX(point.x())
    stop.setY(point.y())
    minDist = distance(start, point)
    print(f'Top ({point.x()}, {point.y()})')
    print(f'Stop ({stop.x()}, {stop.y()})')
    print(f'Dist {minDist}')

    # Left point
    point.setX(rect.x())
    point.setY(rect.y() + rect.height() / 2)
    print(f'Left ({point.x()}, {point.y()})')

    tmp = distance(start, point)
    if minDist > tmp:
        minDist = tmp
        stop.setX(point.x())
        stop.setY(point.y())
        print(f'Stop ({stop.x()}, {stop.y()})')
        print(f'Dist {tmp}')

    # right point
    point.setX(rect.x() + rect.width())
    point.setY(rect.y() + rect.height() / 2)
    print(f'Right ({point.x()}, {point.y()})')

    tmp = distance(start, point)
    if minDist > tmp:
        minDist = tmp
        stop.setX(point.x())
        stop.setY(point.y())
        print(f'Stop ({stop.x()}, {stop.y()})')
        print(f'Dist {tmp}')

    # bottom point
    point.setX(rect.x() + rect.width() / 2)
    point.setY(rect.y() + rect.height())
    print(f'Bottom ({point.x()}, {point.y()})')

    tmp = distance(start, point)
    if minDist > tmp:
        minDist = tmp
        stop.setX(point.x())
        stop.setY(point.y())
        print(f'Stop ({stop.x()}, {stop.y()})')
        print(f'Dist {tmp}')

    return stop


class NodeItem(QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.next = None

        self._mouseDX = 0
        self._mouseDY = 0
        self.startArrow = None
        self.stopArrow = None

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: QVariant):
        # Boundary
        if change == changeType.ItemPositionChange and self.scene():
            newPos = value
            pos = self.pos()
            rect = self.scene().sceneRect()
            selfRect = self.mapRectToScene(self.rect())

            if not rect.contains(newPos):
                newPos.setX(min(rect.right(), max(newPos.x(), rect.left())))
                newPos.setY(min(rect.bottom(), max(newPos.y(), rect.top())))

            # Collision
            collisions = list(
                filter(lambda item: type(item) == type(self), self.collidingItems())
            )
            if len(collisions) > 0:
                for item in collisions:
                    rect = item.mapRectToScene(item.rect())

                    dx = 0
                    dy = 0

                    if rect.left() <= selfRect.left() <= rect.right():
                        dx = rect.right() - selfRect.left() + 1
                    elif rect.right() >= selfRect.right() >= rect.left():
                        dx = rect.left() - selfRect.right() - 1

                    if rect.top() <= selfRect.top() <= rect.bottom():
                        dy = rect.bottom() - selfRect.top() + 1
                    elif rect.bottom() >= selfRect.bottom() >= rect.top():
                        dy = rect.top() - selfRect.bottom() - 1

                    if dx < dy:
                        pos.setX(pos.x() + dx)
                    else:
                        pos.setY(pos.y() + dy)

                newPos = pos

            cursor = QCursor()
            mousePos = cursor.pos()

            tmp = newPos
            view = self.scene().views()[0]
            tmp2 = view.mapFromScene(tmp)
            globalPos = view.mapToGlobal(tmp2)

            if abs(globalPos.x() + self._mouseDX - mousePos.x()) > 1:
                mousePos.setX(globalPos.x() + self._mouseDX)

            if abs(globalPos.y() + self._mouseDY - mousePos.y()) > 1:
                mousePos.setY(globalPos.y() + self._mouseDY)

            if self.startArrow is not None:
                pos = self.pos()
                pos.setX(pos.x() + self.rect().width() / 2)
                pos.setY(pos.y() + self.rect().height() / 2)
                node = self.next
                stop = closestPoint(pos, node.mapRectToScene(node.rect()))
                self.startArrow.start = pos
                self.startArrow.stop = stop
                self.startArrow.transformArrow()

            if self.stopArrow is not None:
                stop = closestPoint(self.stopArrow.start, self.mapRectToScene(self.rect()))
                self.stopArrow.stop = stop
                pos.setY(pos.y() + self.rect().height() / 2)
                self.stopArrow.transformArrow()

            cursor.setPos(mousePos)
            value = newPos

        return super().itemChange(change, value)

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent):
        self._mouseDX = int(e.pos().x())
        self._mouseDY = int(e.pos().y())
        super().mousePressEvent(e)

    @property
    def next(self):
        """The next node."""
        return self._next

    @next.setter
    def next(self, value):
        self._next = value

    @property
    def startArrow(self) -> ArrowItem:
        """The startArrow property."""
        return self._startArrow

    @startArrow.setter
    def startArrow(self, value: ArrowItem):
        self._startArrow = value
        if value is not None:
            value.transformArrow()

    @property
    def stopArrow(self) -> ArrowItem:
        """The stopArrow property."""
        return self._stopArrow

    @stopArrow.setter
    def stopArrow(self, value: ArrowItem):
        self._stopArrow = value
        if value is not None:
            value.transformArrow()

    def addNode(self, node: Self):
        head = self
        count = 1
        while head.next is not None:
            count += 1
            head = head.next

        head.next = node
        start = head.pos()
        stop = node.pos()

        start.setX(start.x() + self.rect().width() / 2)
        start.setY(start.y() + self.rect().height() / 2)
        stop = closestPoint(start, node.mapRectToScene(node.rect()))
        arrow = ArrowItem(start, stop)
        arrow.setBrush(head.brush())
        self.scene().addItem(arrow)

        head.startArrow = arrow
        head.next.stopArrow = arrow
        arrow.transformArrow()
