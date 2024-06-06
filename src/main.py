"""The main entry point for LinkedListVisualizer

This file is the main entry point for the MazeViewer project.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow


def main():
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
