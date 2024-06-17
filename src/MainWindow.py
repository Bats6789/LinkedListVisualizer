from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem
from PyQt6.QtGui import QKeyEvent, QBrush
from PyQt6.QtCore import Qt
from NodeItem import NodeItem
from ArrowItem import ArrowItem


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Linked List Visualizer")
        self.showFullScreen()

        brush = QBrush(Qt.BrushStyle.SolidPattern)
        brush.setColor(Qt.GlobalColor.black)

        self.scene = QGraphicsScene(0, 0, 800, 800)
        self.scene.setBackgroundBrush(brush)
        self.view = QGraphicsView(self.scene)

        brush.setColor(Qt.GlobalColor.red)
        self.node1 = NodeItem(0, 0, 120, 100)
        self.node1.setBrush(brush)
        self.node1.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.node1.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True
        )
        self.scene.addItem(self.node1)

        brush.setColor(Qt.GlobalColor.blue)
        self.node2 = NodeItem(0, 0, 120, 100)
        self.node2.setPos(230, 0)
        self.node2.setBrush(brush)
        self.node2.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.node2.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True
        )
        self.scene.addItem(self.node2)

        start = self.node1.pos()
        stop = self.node2.pos()

        start.setX(start.x() + self.node1.rect().width())
        start.setY(start.y() + self.node1.rect().height() / 2)
        stop.setY(stop.y() + self.node2.rect().height() / 2)

        brush.setColor(Qt.GlobalColor.red)
        self.arrow = ArrowItem(start, stop)
        self.arrow.setBrush(brush)
        self.scene.addItem(self.arrow)

        self.node1.next = self.node2
        self.node1.startArrow = self.arrow
        self.node2.stopArrow = self.arrow

        self.button = QPushButton()

        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        self.layout = QVBoxLayout(self.widget)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.view)

    def keyPressEvent(self, e: QKeyEvent):
        match e.key():
            case Qt.Key.Key_Q:
                self.close()
