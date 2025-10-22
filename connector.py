from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLineEdit, QLabel, QVBoxLayout, QGridLayout, QStackedWidget, QCheckBox
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap, QIntValidator

import sys
import random
from typing import List
import textclientconnect

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.character = ""

        self.mainScreen = QStackedWidget()

        self.setCentralWidget(self.mainScreen)

        self.setWindowTitle("OS Client")
        self.setFixedSize(QSize(800,450))
        self.connect_screen = QWidget()
        self.char_select_screen = QWidget()
        self.show_selected_char = QWidget()
        self.postgame = QWidget()
        self.mainScreen.addWidget(self.postgame)
        self.mainScreen.addWidget(self.show_selected_char)
        self.mainScreen.addWidget(self.char_select_screen)
        self.mainScreen.addWidget(self.connect_screen)
        #setup connect screen
        self.connect_button = QPushButton("Connect to Text Client")
        self.connect_button.clicked.connect(self.connect_button_clicked)
        self.connect_button.setParent(self.connect_screen)
        self.mainScreen.setCurrentWidget(self.connect_screen)

        #setup char select screen
        char_select_grid = QGridLayout(self.char_select_screen)
        self.character_select_widgets : List[QPushButton] = [QPushButton("Random")]
        self.characters = ["Juliette", "Kai", "Dubu", "Estelle", "Atlas", "Juno", "Drek_ar", "Rune", "X", "Era", "Luna", "Ai.Mi", "Asher", "Zentaro", "Rasmus", "Octavia", "Vyce", "Finii", "Kazan", "Nao", "Mako"]
        for character in self.characters:
            self.character_select_widgets.append(QPushButton())
            self.character_select_widgets[-1].setIcon(QIcon(f"./assets/CloseUp_{character}.png"))
            self.character_select_widgets[-1].clicked.connect(lambda _,ch=character:self.character_select_button_pressed(ch))
            self.character_select_widgets[-1].setEnabled(textclientconnect.check_character_unlocked(character))
        
        self.character_select_widgets[0].setFixedHeight(83)
        self.character_select_widgets[0].clicked.connect(lambda: self.character_select_button_pressed("Random"))

        for i in range(len(self.character_select_widgets)):
            self.character_select_widgets[i].setIconSize(QSize(75,75))
            x = i%6
            y = (i-x)/6
            char_select_grid.addWidget(self.character_select_widgets[i], int(y), x)

        #setup show selected character screen
        show_char_layout = QVBoxLayout(self.show_selected_char)
        self.char_icon = QLabel()
        cancel_button = QPushButton("Select a different character")
        continue_button = QPushButton("Confirm")
        show_char_layout.addWidget(self.char_icon)
        show_char_layout.addWidget(cancel_button)
        show_char_layout.addWidget(continue_button)
        show_char_layout.setAlignment(self.char_icon, Qt.AlignmentFlag.AlignCenter)

        cancel_button.clicked.connect(lambda: self.mainScreen.setCurrentWidget(self.char_select_screen))
        continue_button.clicked.connect(lambda: self.mainScreen.setCurrentWidget(self.postgame))


        #setup postgame screen
        self.label_names = ["Goals","Assists","Saves","KOs","Redirects","Orbs"]
        self.labels : List[QLabel] = []
        self.text_boxes : List[QLineEdit] = []

        layout = QVBoxLayout(self.postgame)

        self.victory_check = QCheckBox()
        self.victory_check.setText("Win?")
        layout.addWidget(self.victory_check)

        for i in range(len(self.label_names)):
            temp = QLabel()
            temp.setText(self.label_names[i])
            self.labels.append(temp)
            layout.addWidget(self.labels[i])
            self.text_boxes.append(QLineEdit())
            self.text_boxes[i].setValidator(QIntValidator(0,999))
            layout.addWidget(self.text_boxes[i])

        submit_button = QPushButton("Submit")
        layout.addWidget(submit_button)
        submit_button.clicked.connect(self.submit_button_clicked)
        


    def connect_button_clicked(self):
        self.mainScreen.setCurrentWidget(self.char_select_screen)
        textclientconnect.update_items()
        for i in range(1, len(self.character_select_widgets)):
            self.character_select_widgets[i].setEnabled(textclientconnect.check_character_unlocked(self.characters[i-1]))
    
    def disconnect_button_clicked(self):
        self.mainScreen.setCurrentWidget(self.connect_screen)
    
    def submit_button_clicked(self):
        data = {"Character": self.character, "Won": self.victory_check.isChecked()}
        self.victory_check.setChecked(False)
        for i in range(len(self.text_boxes)):
            data[self.label_names[i]] = int(self.text_boxes[i].text())
            self.text_boxes[i].setText("0000")
        print(data)
        textclientconnect.send_checks(data)
        self.mainScreen.setCurrentWidget(self.char_select_screen)
    
    def character_select_button_pressed(self, character: str):
        if character == "Random":
            character = random.choice(textclientconnect.get_unlocked_characters())
        self.character = character
        self.char_icon.setPixmap(QPixmap(f"./assets/CloseUp_{character}.png"))
        self.mainScreen.setCurrentWidget(self.show_selected_char)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()