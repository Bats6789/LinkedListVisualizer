from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtGui import QKeyEvent, QBrush
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Linked List Visualizer")
        self.showFullScreen()

        self.scene = QGraphicsScene(0, 0, 800, 800)
        brush: QBrush = self.scene.backgroundBrush()
        brush.setColor(Qt.GlobalColor.red)
        self.item = QGraphicsRectItem(0, 0, 100, 100)
        self.scene.setBackgroundBrush(brush)
        self.scene.addItem(self.item)
        self.view = QGraphicsView(self.scene)
        self.view.setBackgroundBrush(brush)
        self.button = QPushButton()

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.button)
        self.layout.addWidget(self.view)

        self.widget = QWidget()

        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def keyPressEvent(self, e: QKeyEvent):
        match e.key():
            case Qt.Key.Key_Q:
                self.close()
