from .utils import make_maps, place_pixmap

from PySide6.QtWidgets import QWidget, QLabel, QFrame, QPushButton, QLineEdit, QSpinBox, QTabWidget, QFileDialog


class QConfigureTab(QWidget):
    def __init__(self, preview_0: QLabel, preview_1: QLabel, parent: QWidget = None) -> None:
        super(QConfigureTab, self).__init__(parent=parent)

        # Constants

        self._preview_0 = preview_0
        self._preview_1 = preview_1

        self._background_tuple = (255, 0, 255)

        # Labels

        self._label_0 = QLabel("Change image resolution:", self)
        self._label_0.move(10, 10)

        self._label_1 = QLabel("Change chunk resolution:", self)
        self._label_1.move(10, 40)

        self._label_2 = QLabel("Change background:", self)
        self._label_2.move(10, 90)

        self._label_3 = QLabel("Change image:", self)
        self._label_3.move(10, 130)

        self._label_4 = QLabel("Change export path:", self)
        self._label_4.move(10, 160)

        self._label_5 = QLabel("x", self)
        self._label_5.move(265, 13)

        self._label_6 = QLabel("x", self)
        self._label_6.move(265, 43)

        # Editors

        self._image_width = QSpinBox(self)
        self._image_width.setMinimum(8)
        self._image_width.setMaximum(65536)
        self._image_width.resize(80, 22)
        self._image_width.move(180, 10)

        self._image_height = QSpinBox(self)
        self._image_height.setMinimum(8)
        self._image_height.setMaximum(65536)
        self._image_height.resize(80, 22)
        self._image_height.move(280, 10)

        self._chunk_width = QSpinBox(self)
        self._chunk_width.setMinimum(8)
        self._chunk_width.setMaximum(65536)
        self._chunk_width.resize(80, 20)
        self._chunk_width.move(180, 40)

        self._chunk_height = QSpinBox(self)
        self._chunk_height.setMinimum(8)
        self._chunk_height.setMaximum(65536)
        self._chunk_height.resize(80, 20)
        self._chunk_height.move(280, 40)

        self._background = QFrame(self)
        self._background.resize(16, 16)
        self._background.move(140, 90)

        self._input_change = QLineEdit(self)
        self._input_change.setReadOnly(True)
        self._input_change.resize(190, 20)
        self._input_change.move(140, 130)

        self._input_change_btn = QPushButton("...", self)
        self._input_change_btn.pressed.connect(self.openNewImage)
        self._input_change_btn.resize(30, 20)
        self._input_change_btn.move(340, 130)

        self._output_change = QLineEdit(self)
        self._output_change.setReadOnly(True)
        self._output_change.resize(190, 20)
        self._output_change.move(140, 160)

        self._output_change_btn = QPushButton("...", self)
        self._output_change_btn.pressed.connect(self.openNewDirectory)
        self._output_change_btn.resize(30, 20)
        self._output_change_btn.move(340, 160)

        self._preview_button = QPushButton("Preview", self)
        self._preview_button.pressed.connect(self.createPreview)
        self._preview_button.resize(90, 25)
        self._preview_button.move(10, 205)

        self._export_button = QPushButton("Export", self)
        self._export_button.pressed.connect(self.createFinally)
        self._export_button.resize(90, 25)
        self._export_button.move(10, 240)

        self.updateBackgroundPreview()

    def openNewImage(self) -> None:
        file, _ = QFileDialog.getOpenFileName(self, "Open Image", filter="Images (*.png, *.jpg, *.jpeg)")
        if file:
            pixmap, size = place_pixmap(file, self._preview_0.size().toTuple())

            self._image_width.setValue(size[0])
            self._image_height.setValue(size[1])
            self._input_change.setText(file)
            self._preview_0.setPixmap(pixmap)

    def openNewDirectory(self) -> None:
        file = QFileDialog.getExistingDirectory(self, "Open Folder")
        if file:
            self._output_change.setText(file)

    def createPreview(self) -> None:
        if self._input_change.text():
            path = self._input_change.text()
            chunk_size = (self._chunk_width.value(), self._chunk_height.value())
            image_size = (self._image_width.value(), self._image_height.value())
            background = self._background_tuple

            self._preview_1.setPixmap(
                place_pixmap(make_maps(path, chunk_size, image_size, background, None),
                             self._preview_1.size().toTuple())[0]
            )

    def createFinally(self) -> None:
        if self._input_change.text() and self._output_change.text():
            path = self._input_change.text()
            chunk_size = (self._chunk_width.value(), self._chunk_height.value())
            image_size = (self._image_width.value(), self._image_height.value())
            background = self._background_tuple
            output = self._output_change.text()

            self._preview_1.setPixmap(
                place_pixmap(make_maps(path, chunk_size, image_size, background, output),
                             self._preview_1.size().toTuple())[0]
            )

    def updateBackgroundPreview(self) -> None:
        self._background.setStyleSheet(f"border-radius: 6px; background: rgb{self._background_tuple}; margin: 2px;")


class QMapCreator(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super(QMapCreator, self).__init__(parent=parent)

        # Graphics views

        self._input_image = QLabel(self)
        self._input_image.setStyleSheet("border: 1px solid black;")
        self._input_image.resize(385, 240)
        self._input_image.move(10, 10)

        self._output_image = QLabel(self)
        self._output_image.setStyleSheet("border: 1px solid black;")
        self._output_image.resize(385, 240)
        self._output_image.move(405, 10)

        self._tabs = QTabWidget(self)
        self._tabs.resize(385, 300)
        self._tabs.move(10, 260)

        # Tabs

        self._tabs.addTab(QConfigureTab(self._input_image, self._output_image), "Configure")
