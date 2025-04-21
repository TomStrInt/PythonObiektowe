import sys
import unicodedata
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QVBoxLayout, QHBoxLayout, QRadioButton, QCheckBox,
    QLineEdit, QPushButton, QScrollArea, QMessageBox, QFileDialog
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

def stylizuj_tekst(tekst):
    return f"<div style='border: 2px solid #ff8c00; color:black; padding:10px;'><b>{tekst}</b></div>"

def normalize_text(text):
    text = unicodedata.normalize("NFKD", text)
    text = "".join([c for c in text if not unicodedata.combining(c)])
    return " ".join(text.split()).lower()

class Quiz(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Harry Potter Quiz")
        self.resize(700, 800)

        scroll_area = QScrollArea()
        central_widget = QWidget()
        scroll_area.setWidget(central_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: #2c2f33;")
        self.setCentralWidget(scroll_area)

        main_layout = QVBoxLayout()

        # Question 1
        q1_layout = QVBoxLayout()
        self.q1_label = QLabel(stylizuj_tekst("1. Jak nazywa się najlepszy przyjaciel Harry'ego Pottera?"))
        self.q1_radio1 = QRadioButton("Ron Weasley")
        self.q1_radio2 = QRadioButton("Draco Malfoy")
        self.q1_radio3 = QRadioButton("Neville Longbottom")
        self.q1_radios = [self.q1_radio1, self.q1_radio2, self.q1_radio3]

        q1_layout.addWidget(self.q1_label)
        for radio in self.q1_radios:
            q1_layout.addWidget(radio)
        main_layout.addLayout(q1_layout)

        # Question 2
        q2_layout = QVBoxLayout()
        self.q2_label = QLabel(stylizuj_tekst("2. Kto był nauczycielem eliksirów w Hogwarcie?"))
        self.q2_checkbox1 = QCheckBox("Severus Snape")
        self.q2_checkbox2 = QCheckBox("Minerva McGonagall")
        self.q2_checkbox3 = QCheckBox("Rubeus Hagrid")
        self.q2_checkboxes = [self.q2_checkbox1, self.q2_checkbox2, self.q2_checkbox3]

        q2_layout.addWidget(self.q2_label)
        for checkbox in self.q2_checkboxes:
            q2_layout.addWidget(checkbox)
        main_layout.addLayout(q2_layout)

        # Image Manipulation Section
        img_layout = QVBoxLayout()
        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.setStyleSheet("background-color: #f0f0f0;")
        img_layout.addWidget(self.img_label)

        self.open_file_button = QPushButton("Otwórz plik graficzny")
        self.open_file_button.clicked.connect(self.open_image)
        img_layout.addWidget(self.open_file_button)

        self.save_file_button = QPushButton("Zapisz obraz pod inną nazwą")
        self.save_file_button.clicked.connect(self.save_image)
        img_layout.addWidget(self.save_file_button)

        main_layout.addLayout(img_layout)

        # Submit Button
        footer_layout = QHBoxLayout()
        self.check_button = QPushButton("Sprawdź")
        self.check_button.clicked.connect(self.sprawdzenie_odp)
        footer_layout.addWidget(self.check_button)
        main_layout.addLayout(footer_layout)

        central_widget.setLayout(main_layout)

        self.current_pixmap = None  # Placeholder for loaded image

    def open_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Wybierz obraz", "", "Obrazy (*.png *.jpg *.jpeg)")
        if file_path:
            self.current_pixmap = QPixmap(file_path)
            self.img_label.setPixmap(self.current_pixmap.scaled(self.img_label.size(), Qt.KeepAspectRatio))

    def save_image(self):
        if self.current_pixmap:
            file_dialog = QFileDialog()
            save_path, _ = file_dialog.getSaveFileName(self, "Zapisz obraz", "", "Obrazy (*.png *.jpg *.jpeg)")
            if save_path:
                self.current_pixmap.save(save_path)

    def sprawdzenie_odp(self):
        punkty = 0

        # Question 1: Ron Weasley
        if self.q1_radio1.isChecked():
            punkty += 1
        self.q1_radio1.setStyleSheet("color: green;")

        # Question 2: Severus Snape
        if self.q2_checkbox1.isChecked() and not self.q2_checkbox2.isChecked() and not self.q2_checkbox3.isChecked():
            punkty += 1
        self.q2_checkbox1.setStyleSheet("color: green;")

        QMessageBox.information(self, "Wynik", f"Zdobyłeś {punkty} na 2 punktów!")

app = QApplication([])
quiz = Quiz()
quiz.show()
app.exec()
