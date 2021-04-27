from PyQt5.QtWidgets import QWidget, QPushButton
from menues import main_menu, game_place
from menues.dialog_choose_players import ChoosePlayersDialog


class SelectTypeGame(QWidget):
    def __init__(self, mode):
        super().__init__()
        self.resize(400, 200)
        self.setWindowTitle("Renju: select game type")
        self.setStyleSheet("background-color: #f4b3fc;")
        self.mode = mode
        self.bttn_texts = {
            "with Timer": True,
            "w/o Timer": False
        }
        self.main_menu = None
        self.game_place = None
        self.init_UI()

    def init_UI(self):
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
        for text in self.bttn_texts:
            bttn = QPushButton(text, self)
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

    def choose_players(self):
        players, ok = ChoosePlayersDialog.get_players(self.mode)
        if ok:
            return players

    def bttn_clicked(self):
        bttn_text = self.sender().text()
        has_timer = self.bttn_texts[bttn_text]
        if has_timer:
            players = self.choose_players()
            if players is None:
                return
            self.close()
            self.game_place = game_place.GamePlace(
                self.mode, has_timer, players=players)
            self.game_place.show()
        else:
            self.close()
            self.game_place = game_place.GamePlace(self.mode, has_timer)
            self.game_place.show()

    def bttn_back_cliked(self):
        self.close()
        self.main_menu = main_menu.MainMenu()
        self.main_menu.show()
