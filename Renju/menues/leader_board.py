from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from menues import main_menu
import os


class LeaderBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Renju: leader board")
        self.setStyleSheet("background-color: #000;")
        self.main_menu = None
        self.print_leader_board()

    def print_leader_board(self):
        directory_folder = "./leader_board.list"
        if not os.path.exists(directory_folder):
            file = open(directory_folder, "w+")
            file.close()
            self.resize(300, 300)
            return
        with open(directory_folder) as file:
            leaders = file.read().split('\n')
        if len(leaders) == 1 and leaders[0] == "":
            self.resize(300, 300)
            self.init_bttn_close(None)
            return
        position = 1
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignHCenter)
        label_style_sheet = "color: #fff;" \
                            "font-size: 20px;" \
                            "text-align: center;" \
                            "font-weight: 700;" \
                            "margin: 20px 30px 0 30px;"
        for leader in leaders:
            if leader == "":
                continue
            label = QLabel(f"{position}. {leader}", self)
            label.setStyleSheet(label_style_sheet)
            layout.addWidget(label)
            position += 1
        self.init_bttn_close(layout)

    def init_bttn_close(self, layout):
        bttn_back = QPushButton("Back", self)
        bttn_back_style_sheet = '''
            QPushButton {
                width: 20px;
                color: #fff;
                border: 1px solid #fff;
                border-radius: 10px;
                margin-top: 20px;
            }
            QPushButton:hover {
                color: #000;
                background-color: #fff;
            }
        '''
        bttn_back.setStyleSheet(bttn_back_style_sheet)
        bttn_back.clicked.connect(self.bttn_back_cliked)
        if layout is not None:
            layout.addWidget(bttn_back)
        else:
            bttn_back.setGeometry(115, 140, 70, 70)

    def bttn_back_cliked(self):
        self.close()
        self.main_menu = main_menu.MainMenu()
        self.main_menu.show()
