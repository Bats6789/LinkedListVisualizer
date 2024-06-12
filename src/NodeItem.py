from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsItem
from PyQt6.QtCore import QVariant

changeType = QGraphicsItem.GraphicsItemChange


class NodeItem(QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.next = None

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: QVariant):
        # Boundary
        if change == changeType.ItemPositionChange and self.scene():
            newPos = value
            rect = self.scene().sceneRect()

            if not rect.contains(newPos):
                newPos.setX(min(rect.right(), max(newPos.x(), rect.left())))
                newPos.setY(min(rect.bottom(), max(newPos.y(), rect.top())))

            # Collision
            collisions = self.collidingItems()
            if len(collisions) > 0:
                newPos = self.pos()
                selfRect = self.rect()

                for item in collisions:
                    rect = item.rect()

                    if selfRect.left() <= rect.right():
                        newPos.setX(rect.right() + 1)
                    elif selfRect.right() >= rect.left():
                        newPos.setX(rect.left() - (selfRect.width() + 1))
                    elif selfRect.top() <= rect.bottom():
                        newPos.setY(rect.bottom() + 1)
                    elif selfRect.bottom() >= rect.top():
                        newPos.setY(rect.top() - (selfRect.height() + 1))

                return newPos

        return super().itemChange(change, value)

    @property
    def next(self):
        """The next node."""
        return self._next

    @next.setter
    def next(self, value):
        self._next = value
