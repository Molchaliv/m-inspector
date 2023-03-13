import sys

from core import QMapCreator

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QTabWidget, QApplication


class QMain(QMainWindow):
    def __init__(self) -> None:
        super(QMain, self).__init__()

        self.setWindowTitle("M-Inspector")
        self.setWindowIcon(QIcon(".\\res\\icon.png"))
        self.setFixedSize(800, 600)

        self._tabs = QTabWidget(self)
        self._tabs.addTab(QMapCreator(), "Map creator")
        self._tabs.resize(800, 600)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = QMain()
    main.show()

    sys.exit(app.exec())
