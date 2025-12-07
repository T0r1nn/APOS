from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLineEdit, QLabel, QVBoxLayout, QGridLayout, QStackedWidget, QCheckBox
from PyQt6.QtCore import QSize, Qt, QTimer, QTimerEvent
from PyQt6.QtGui import QIcon, QPixmap, QIntValidator

import sys
import random
from typing import List
import textclientconnect
import logread

class MainWindow(QMainWindow):
    def __init__(self, arg_dict):
        super().__init__()
        update_timer = QTimer(self)
        update_timer.timeout.connect(self.timer_tick)
        update_timer.start(1000)

        self.character = ""
        self.arg_dict = arg_dict

        self.mainScreen = QStackedWidget()

        self.setCentralWidget(self.mainScreen)

        #self.watcher = logread.LogWatcher()

        #watcher_timer = QTimer(self)
        #watcher_timer.timeout.connect(self.watcher_tick)
        #watcher_timer.start(5000)

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

    def timer_tick(self):
        if self.mainScreen.currentWidget() == self.char_select_screen:
            textclientconnect.update_items()
            for i in range(1, len(self.character_select_widgets)):
                self.character_select_widgets[i].setEnabled(textclientconnect.check_character_unlocked(self.characters[i-1]))

    def watcher_tick(self):
        if self.watcher.checkHasPlayedGame():
            self.watcher.most_recent_timestamp = self.watcher.getMostRecentTimestamp()
            data = self.watcher.getLastGameInfo()
            print(data)

    def connect_button_clicked(self):
        self.mainScreen.setCurrentWidget(self.char_select_screen)
        textclientconnect.update_items()
        textclientconnect.process_args(self.arg_dict)
        print(textclientconnect.saves_x, textclientconnect.redirects_x, textclientconnect.orbs_x, textclientconnect.kos_x, textclientconnect.goals_plus_assists_x)
        for i in range(1, len(self.character_select_widgets)):
            self.character_select_widgets[i].setEnabled(textclientconnect.check_character_unlocked(self.characters[i-1]))
    
    def disconnect_button_clicked(self):
        self.mainScreen.setCurrentWidget(self.connect_screen)
    
    def submit_button_clicked(self):
        data = {"Character": self.character, "Won": self.victory_check.isChecked()}
        self.victory_check.setChecked(False)
        for i in range(len(self.text_boxes)):
            data[self.label_names[i]] = int(self.text_boxes[i].text())
            self.text_boxes[i].setText("")
        textclientconnect.send_checks(data)
        self.mainScreen.setCurrentWidget(self.char_select_screen)
    
    def character_select_button_pressed(self, character: str):
        if character == "Random":
            character = random.choice(textclientconnect.get_unlocked_characters())
        self.character = character
        self.char_icon.setPixmap(QPixmap(f"./assets/CloseUp_{character}.png"))
        self.mainScreen.setCurrentWidget(self.show_selected_char)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    args = sys.argv[1:]
    arg_dict = {}
    valid_args = ["cumulative","kos","saves","redirects","orbs","goals_assists"]
    for arg in args:
        arg_parts = arg[2:].split("=")
        if arg_parts[0] not in valid_args:
            raise AttributeError(f"Command line argument {arg_parts[0]} invalid, valid arguments are: {(', '.join(valid_args))}")
        arg_dict[arg_parts[0]] = int(arg_parts[1])

    print(arg_dict)

    window = MainWindow(arg_dict)
    window.show()

    app.exec()