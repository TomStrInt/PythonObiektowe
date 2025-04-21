import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout,
    QHBoxLayout, QPushButton, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage

class PersistentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Persistent Window")
        self.setGeometry(800, 200, 400, 400)  # Określenie pozycji i rozmiaru okna
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.image_label = QLabel("Brak obrazu")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def display_image(self, pixmap):
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
        self.show()

    def hide_window(self):
        self.hide()


class OnDemandWindow(QMainWindow):
    def __init__(self, persistent_window):
        super().__init__()
        self.setWindowTitle("On Demand Window")
        self.setGeometry(400, 200, 400, 300)
        self.persistent_window = persistent_window

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.gray_button = QPushButton("Skala szarości")
        self.gray_button.clicked.connect(self.apply_grayscale)
        self.layout.addWidget(self.gray_button)

        self.mirror_button = QPushButton("Odbicie lustrzane")
        self.mirror_button.clicked.connect(self.apply_mirror)
        self.layout.addWidget(self.mirror_button)

        self.resize_button = QPushButton("Przeskalowanie")
        self.resize_button.clicked.connect(self.apply_resize)
        self.layout.addWidget(self.resize_button)

        self.crop_button = QPushButton("Kadrowanie")
        self.crop_button.clicked.connect(self.apply_crop)
        self.layout.addWidget(self.crop_button)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def apply_grayscale(self):
        if self.persistent_window.image_label.pixmap():
            pixmap = self.persistent_window.image_label.pixmap()
            image = pixmap.toImage().convertToFormat(QImage.Format_Grayscale8)
            self.persistent_window.display_image(QPixmap.fromImage(image))

    def apply_mirror(self):
        if self.persistent_window.image_label.pixmap():
            pixmap = self.persistent_window.image_label.pixmap()
            image = pixmap.toImage().mirrored(True, False)
            self.persistent_window.display_image(QPixmap.fromImage(image))

    def apply_resize(self):
        if self.persistent_window.image_label.pixmap():
            pixmap = self.persistent_window.image_label.pixmap()
            resized_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
            self.persistent_window.display_image(resized_pixmap)

    def apply_crop(self):
        if self.persistent_window.image_label.pixmap():
            pixmap = self.persistent_window.image_label.pixmap()
            image = pixmap.toImage()
            cropped_image = image.copy(50, 50, 200, 200)  # Kadrowanie obrazu
            self.persistent_window.display_image(QPixmap.fromImage(cropped_image))


class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application")
        self.setGeometry(200, 200, 600, 400)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.open_file_button = QPushButton("Otwórz plik graficzny")
        self.open_file_button.clicked.connect(self.open_image)
        self.layout.addWidget(self.open_file_button)

        self.show_persistent_button = QPushButton("Pokaż persistent window")
        self.show_persistent_button.clicked.connect(self.show_persistent_window)
        self.layout.addWidget(self.show_persistent_button)

        self.show_on_demand_button = QPushButton("Pokaż on demand window")
        self.show_on_demand_button.clicked.connect(self.show_on_demand_window)
        self.layout.addWidget(self.show_on_demand_button)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.persistent_window = PersistentWindow()
        self.on_demand_window = OnDemandWindow(self.persistent_window)

    def open_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Wybierz obraz", "", "Obrazy (*.png *.jpg *.jpeg)")
        if file_path:
            pixmap = QPixmap(file_path)
            self.persistent_window.display_image(pixmap)

    def show_persistent_window(self):
        if self.persistent_window.image_label.pixmap():
            self.persistent_window.show()

    def show_on_demand_window(self):
        self.on_demand_window.show()


app = QApplication([])
main_app = MainApplication()
main_app.show()
app.exec()
