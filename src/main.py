"""The main entry point for LinkedListVisualizer

This file is the main entry point for the LinkedListVisualizer project.
"""

import sys
from PyQt6.QtWidgets import QApplication
from MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
