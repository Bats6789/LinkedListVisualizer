from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem
from PyQt6.QtGui import QKeyEvent, QBrush
from PyQt6.QtCore import Qt
from NodeItem import NodeItem


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
        self.node1.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.scene.addItem(self.node1)

        brush.setColor(Qt.GlobalColor.blue)
        self.node2 = NodeItem(0, 0, 120, 100)
        self.node2.setPos(130, 0)
        self.node2.setBrush(brush)
        self.node2.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.node2.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.scene.addItem(self.node2)

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
