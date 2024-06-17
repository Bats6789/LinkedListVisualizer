from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsSceneMouseEvent
from PyQt6.QtCore import QVariant
from PyQt6.QtGui import QCursor

changeType = QGraphicsItem.GraphicsItemChange


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
                pos.setX(pos.x() + self.rect().width())
                self.startArrow.start = pos
                self.startArrow.transformArrow()

            if self.stopArrow is not None:
                pos = self.pos()
                self.stopArrow.stop = pos
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
