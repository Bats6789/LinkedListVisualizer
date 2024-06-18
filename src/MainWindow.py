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

        self.nodeCount = 1
        self.colors = [
            Qt.GlobalColor.red,
            Qt.GlobalColor.green,
            Qt.GlobalColor.cyan,
            Qt.GlobalColor.lightGray,
            Qt.GlobalColor.yellow,
            Qt.GlobalColor.magenta,
            Qt.GlobalColor.gray,
            Qt.GlobalColor.white,
            Qt.GlobalColor.darkBlue,
            Qt.GlobalColor.darkRed,
            Qt.GlobalColor.darkGreen,
            Qt.GlobalColor.darkGray,
            Qt.GlobalColor.darkCyan,
            Qt.GlobalColor.darkYellow,
            Qt.GlobalColor.darkMagenta,
            Qt.GlobalColor.blue,
        ]

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
            case Qt.Key.Key_A:
                node = NodeItem(0, 0, 120, 100)
                node.setPos(500, 500)
                node.setBrush(self.colors[self.nodeCount % len(self.colors)])
                self.node1.addNode(node)
                self.nodeCount += 1
                node.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
                node.setFlag(
                    QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True
                )
                self.scene.addItem(node)
