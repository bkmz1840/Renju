from PyQt5.QtWidgets import QWidget, QPushButton
from menues import load_game, select_type_game, leader_board
from game_classes.game_mode import GameMode


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 440)
        self.setWindowTitle("Renju")
        self.setStyleSheet("background-color: #151b2d;")
        self.select_type_game = None
        self.load_game = None
        self.leader_board = None
        self.init_UI()

    def init_bttn_game_modes(self):
        style_sheet = '''
            QPushButton {
                color: white;
                font-size: 30px;
                border: 1px solid white;
                border-radius: 10px;
            }
            QPushButton:hover {
                color: #151b2d;
                background-color: #fff;
            }
        '''
        texts = ["1 player", "2 players", "3 players",
                 "4 players", "Load", "Leader board"]
        y = 30
        for text in texts:
            bttn = QPushButton(text, self)
            bttn.setGeometry(75, y, 250, 40)
            bttn.setStyleSheet(style_sheet)
            if text == "Load":
                bttn.clicked.connect(self.bttn_load_clicked)
            elif text == "Leader board":
                bttn.clicked.connect(self.bttn_leader_board_clicked)
            else:
                bttn.clicked.connect(self.bttn_clicked)
            y += 60
        return y

    def init_UI(self):
        y = self.init_bttn_game_modes()
        bttn_quit = QPushButton("Quit", self)
        bttn_quit.setGeometry(165, y, 70, 20)
        bttn_quit_style_sheet = '''
            QPushButton {
                color: white;
                border: 1px solid white;
                border-radius: 10px;
            }
            QPushButton:hover {
                color: #151b2d;
                background-color: #fff;
            }
        '''
        bttn_quit.setStyleSheet(bttn_quit_style_sheet)
        bttn_quit.clicked.connect(self.close)

    def bttn_clicked(self):
        bttn_text = self.sender().text()
        mode = GameMode.deserialize(bttn_text)
        self.close()
        self.select_type_game = select_type_game.SelectTypeGame(mode)
        self.select_type_game.show()

    def bttn_load_clicked(self):
        self.close()
        self.load_game = load_game.LoadGame()
        self.load_game.show()

    def bttn_leader_board_clicked(self):
        self.close()
        self.leader_board = leader_board.LeaderBoard()
        self.leader_board.show()
