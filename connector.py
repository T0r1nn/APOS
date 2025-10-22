from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLineEdit, QLabel, QVBoxLayout, QGridLayout
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon

import sys
from typing import List

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OS Client")
        self.setFixedSize(QSize(800,450))
        self.connect_screen = QWidget()
        self.char_select_screen = QWidget()
        self.postgame = QWidget()
        #setup connect screen
        self.connect_button = QPushButton("Connect to Text Client")
        self.connect_button.clicked.connect(self.connect_button_clicked)
        self.connect_button.setParent(self.connect_screen)
        self.setCentralWidget(self.connect_screen)

        #setup char select screen
        char_select_grid = QGridLayout(self.char_select_screen)
        character_select_widgets : List[QPushButton] = [QPushButton("Random")]
        characters = ["Juliette", "Kai", "Dubu", "Estelle", "Atlas", "Juno", "Drek_ar", "Rune", "X", "Era", "Luna", "Ai-Mi", "Asher", "Zentaro", "Rasmus", "Octavia", "Vyce", "Finii", "Kazan", "Nao", "Mako"]
        for character in characters:
            character_select_widgets.append(QPushButton())
            character_select_widgets[-1].setIcon(QIcon(f"./assets/CloseUp_{character}.png"))
        
        for i in range(len(character_select_widgets)):
            character_select_widgets[i]
            x = i%6
            y = (i-x)/6
            char_select_grid.addWidget(character_select_widgets[i], int(y), x)

        #setup postgame screen
        self.labels : List[QLabel] = ["Goals","Assists","Saves","KOs","Redirects","Orbs"]
        self.text_boxes : List[QLineEdit] = []

        layout = QVBoxLayout(self.postgame)

        for i in range(len(self.labels)):
            temp = QLabel()
            temp.setText(self.labels[i])
            self.labels[i] = temp
            layout.addWidget(self.labels[i])
            self.text_boxes.append(QLineEdit())
            self.text_boxes[i].setInputMask("9999")
            self.text_boxes[i].setText("0000")
            layout.addWidget(self.text_boxes[i])

        submit_button = QPushButton("Submit")
        layout.addWidget(submit_button)
        submit_button.clicked.connect(self.submit_button_clicked)
        


    def connect_button_clicked(self):
        self.setCentralWidget(self.char_select_screen)

    def char_select_button_clicked(self):
        self.setCentralWidget(self.postgame)
    
    def disconnect(self):
        self.setCentralWidget(self.connect_screen)
    
    def submit_button_clicked(self):
        data = {}
        for i in range(len(self.text_boxes)):
            data[self.labels[i].text()] = self.text_boxes[i].text()
            self.text_boxes[i].clear()
        self.setCentralWidget(self.char_select_screen)
        print(data)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()