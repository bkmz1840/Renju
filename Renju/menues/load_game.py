from PyQt5.QtWidgets import QWidget, QPushButton
from menues.game_place import GamePlace
from menues import main_menu
from game_classes.game_mode import GameMode
from os import listdir, path


class LoadGame(QWidget):
    def __init__(self):
        super().__init__()
        self.saves = {}
        self.setWindowTitle("Renju: load game")
        self.setStyleSheet("background-color: #f4b3fc;")  # 151b2d
        self.get_saves()
        self.resize(400, len(self.saves) * 60 + 80)
        self.game_place = None
        self.main_menu = None
        self.init_saves()

    def get_saves(self):
        path_to_saves = "./saves/"
        names_saves = [f
                       for f in listdir(path_to_saves)
                       if path.isfile(path.join(path_to_saves, f))]
        for name_save in names_saves:
            name = name_save[:name_save.find(".save")]
            self.saves[name] = path_to_saves + "/" + name_save

    def init_saves(self):
        style_sheet = '''
            QPushButton {
                color: #151b2d;
                font-size: 30px;
                border: 1px solid #151b2d;
                border-radius: 10px;
            }
            QPushButton:hover {
                color: #f4b3fc;
                background-color: #151b2d;
            }
        '''
        y = 30
        for save_name in self.saves:
            bttn = QPushButton(save_name, self)
            bttn.setGeometry(75, y, 250, 40)
            bttn.setStyleSheet(style_sheet)
            bttn.clicked.connect(self.bttn_clicked)
            y += 60
        bttn_back = QPushButton("Back", self)
        bttn_back.setGeometry(225, y, 70, 20)
        bttn_back_style_sheet = '''
            QPushButton {
                color: #151b2d;
                border: 1px solid #151b2d;
                border-radius: 10px;
            }
            QPushButton:hover {
                color: #f4b3fc;
                background-color: #151b2d;
            }
        '''
        bttn_back.setStyleSheet(bttn_back_style_sheet)
        bttn_back.clicked.connect(self.bttn_back_cliked)

    def bttn_clicked(self):
        bttn_text = self.sender().text()
        path_to_save = self.saves[bttn_text]
        self.close()
        self.game_place = GamePlace(
            GameMode.Load, False, path_to_save=path_to_save)
        self.game_place.show()

    def bttn_back_cliked(self):
        self.close()
        self.main_menu = main_menu.MainMenu()
        self.main_menu.show()
