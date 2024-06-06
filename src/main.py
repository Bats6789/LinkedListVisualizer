"""The main entry point for LinkedListVisualizer

This file is the main entry point for the LinkedListVisualizer project.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Linked List Visualizer")
        self.showFullScreen()

    def keyPressEvent(self, e: QKeyEvent):
        match e.key():
            case Qt.Key.Key_Q:
                self.close()


def main():
    app = QApplication(sys.argv)

    app.setStyle('Fusion')

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
