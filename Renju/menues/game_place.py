from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QInputDialog
from PyQt5.QtGui import QPixmap, QPainter, QPaintEvent, QMouseEvent
from PyQt5.QtCore import QTimer
from game_classes.type_game_object import TypeGameObject
from game_classes.game import Game
from game_classes.game_mode import GameMode
from menues import main_menu
import random


class GamePlace(QWidget):
    def __init__(self, mode, has_timer, players=None, path_to_save=None):
        super().__init__()
        self.setWindowTitle(f"Renju: {GameMode.serialize(mode)}")
        self.setStyleSheet('''
            background-color: #151b2d;
            color: #fff;
        ''')
        self.resize(600, 535)
        random.seed()
        self.mode = mode
        self.has_timer = has_timer
        self.players = players
        self.main_menu = None
        self.window_end_game = None
        self.winner_field = None
        self.create_window_end_game()
        self.game = Game(self, mode, has_timer, players)
        if self.mode == GameMode.Load:
            self.game.load_save(path_to_save)
            self.mode = self.game.mode
            self.setWindowTitle(
                f"Renju: {GameMode.serialize(self.mode)}")
            self.has_timer = self.game.has_timer
        self.players = self.game.players
        if self.mode == GameMode.Solo:
            self.bttn_undo = None
            self.bttn_redo = None
            self.init_UI()
        self.bttn_save = None
        self.init_bttn_safe()
        if self.has_timer:
            self.timer = QTimer(self)
            self.timer.setInterval(1000)
            self.round_time = 60
            self.timer.timeout.connect(self.timer_tick)
            self.time_label = None
            self.init_time_label()
            self.timer.start()
        self.update()

    def init_time_label(self):
        self.time_label = QLabel("1:00", self)
        self.time_label.setStyleSheet("color: #fff;"
                                      "font-weight: 700;"
                                      "font-size: 20px;")
        self.time_label.move(540, 250)

    def update_time(self):
        self.round_time = 60
        self.time_label.setText("1:00")

    def create_window_end_game(self):
        self.window_end_game = QWidget(self)
        self.window_end_game.setGeometry(85, 190, 400, 160)
        self.window_end_game.setStyleSheet('''
                   background-color: #f4b3fc;
                   border: 1px solid #000;
                   border-radius: 10px;
               ''')
        self.add_label_with_winner(self.window_end_game)
        self.add_buttons(self.window_end_game)
        self.window_end_game.hide()

    def add_label_with_winner(self, window: QWidget):
        self.winner_field = QLabel("", window)
        self.winner_field.move(self.winner_field.width(), 10)

    def add_buttons(self, window):
        bttn_restart = QPushButton("Restart", window)
        bttn_restart.setGeometry(75, 60, 250, 40)
        bttn_restart_style_sheet = '''
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
        bttn_restart.setStyleSheet(bttn_restart_style_sheet)
        bttn_restart.clicked.connect(self.bttn_restart_clicked)
        bttn_back = QPushButton("Back", window)
        bttn_back.setGeometry(165, 120, 70, 20)
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
        bttn_back.clicked.connect(self.bttn_back_clicked)

    def init_UI(self):
        style_sheet = '''
            QPushButton {
                color: #fff;
                font-size: 30px;
                text-align: center;
                border: 1px solid #fff;
                border-radius: 10px;
            }
            QPushButton:hover {
                color: #151b2d;
                background-color: #fff;
            }
        '''
        self.bttn_undo = QPushButton("<", self)
        self.bttn_undo.setGeometry(525, 430, 30, 30)
        self.bttn_undo.setStyleSheet(style_sheet)
        self.bttn_undo.clicked.connect(self.game.undo)
        self.bttn_redo = QPushButton(">", self)
        self.bttn_redo.setGeometry(565, 430, 30, 30)
        self.bttn_redo.setStyleSheet(style_sheet)
        self.bttn_redo.clicked.connect(self.game.redo)

    def init_bttn_safe(self):
        style_sheet = '''
            QPushButton {
                color: #fff;
                font-size: 20px;
                text-align: center;
                border: 1px solid #fff;
                border-radius: 10px;
            }
            QPushButton:hover {
                color: #151b2d;
                background-color: #fff;
            }
        '''
        self.bttn_save = QPushButton("Save", self)
        self.bttn_save.setGeometry(525, 500, 70, 30)
        self.bttn_save.setStyleSheet(style_sheet)
        self.bttn_save.clicked.connect(self.show_dialog_save)

    def change_text_with_winner(self, text):
        self.winner_field.setText(f"{text} is winner!")
        if text == TypeGameObject.White.value:
            self.winner_field.setStyleSheet('''
                color: #fff;
                text-align: center;
                font-size: 30px;
                border: none;
            ''')
        elif text == TypeGameObject.Black.value:
            self.winner_field.setStyleSheet('''
                color: #000;
                text-align: center;
                font-size: 30px;
                border: none;
            ''')
        elif text == TypeGameObject.Red.value:
            self.winner_field.setStyleSheet('''
                color: #f00;
                text-align: center;
                font-size: 30px;
                border: none;
            ''')
        elif text == TypeGameObject.Green.value:
            self.winner_field.setStyleSheet('''
                color: #0f0;
                text-align: center;
                font-size: 30px;
                border: none;
            ''')
        elif text == "Draw":
            self.winner_field.setStyleSheet('''
                color: #151b2d;
                text-align: center;
                font-size: 30px;
                border: none;
            ''')
        else:
            obj_str = self.game.current_player.game_object.value
            self.winner_field.setText(f"{obj_str} is lost!")
            self.winner_field.setStyleSheet('''
                color: #ceb900;
                text-align: center;
                font-size: 30px;
                border: none;
            ''')

    def draw_game_field(self, painter):
        pixmaps = {
            TypeGameObject.Black: QPixmap("./textures/black.png"),
            TypeGameObject.White: QPixmap("./textures/white.png"),
            TypeGameObject.Red: QPixmap("./textures/red.png"),
            TypeGameObject.Green: QPixmap("./textures/green.png")
        }
        for row in self.game.game_field:
            for game_object in row:
                if game_object.type != TypeGameObject.Empty:
                    painter.drawPixmap(game_object.x, game_object.y,
                                       pixmaps[game_object.type])

    def draw_current_turn(self, painter):
        pathes = {
            TypeGameObject.Black: "./textures/black.png",
            TypeGameObject.White: "./textures/white.png",
            TypeGameObject.Red: "./textures/red.png",
            TypeGameObject.Green: "./textures/green.png"
        }
        pathes_current_turn = {
            TypeGameObject.Black: "./textures/turn_black.png",
            TypeGameObject.White: "./textures/turn_white.png",
            TypeGameObject.Red: "./textures/turn_red.png",
            TypeGameObject.Green: "./textures/turn_green.png"
        }
        x = 10
        for player in self.game.players:
            player_obj = player.game_object
            if player_obj == self.game.current_player.game_object:
                current_pixmap = QPixmap(
                    pathes_current_turn[player_obj])
            else:
                current_pixmap = QPixmap(pathes[player_obj])
            painter.drawPixmap(x, 500, current_pixmap)
            x += 40

    def draw_window_end_game(self, painter: QPainter):
        painter.drawPixmap(0, 0, QPixmap("./textures/bg_end_game.png"))
        self.window_end_game.show()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.drawPixmap(50, 25, QPixmap("./textures/board.png"))
        self.draw_game_field(painter)
        if self.mode != GameMode.Solo \
                and self.mode != GameMode.Load:
            self.draw_current_turn(painter)
        if self.game.is_game_finished:
            if self.mode == GameMode.Solo:
                self.bttn_redo.hide()
                self.bttn_undo.hide()
            self.bttn_save.hide()
            if self.has_timer:
                self.timer.stop()
                self.time_label.hide()
            self.draw_window_end_game(painter)
        painter.end()

    def mousePressEvent(self, event: QMouseEvent):
        x = event.x()
        y = event.y()
        is_completed = self.game.make_turn(x, y)
        if self.has_timer and is_completed:
            self.update_time()

    def update_players(self):
        for player in self.players:
            player.play_time = 0

    def bttn_restart_clicked(self):
        self.window_end_game.hide()
        self.game = Game(self, self.mode, self.has_timer, self.players)
        if self.mode == GameMode.Solo:
            self.bttn_undo.show()
            self.bttn_redo.show()
        if self.has_timer:
            self.update_players()
            self.update_time()
            self.time_label.show()
            self.timer.start()
        self.bttn_save.show()
        self.update()

    def bttn_back_clicked(self):
        self.close()
        self.main_menu = main_menu.MainMenu()
        self.main_menu.show()

    def show_dialog_save(self):
        name, ok = QInputDialog.getText(
            self, "Name of save", "Input name of save: ")
        if ok:
            self.game.save_game(name)

    def timer_tick(self):
        self.round_time -= 1
        self.game.current_player.play_time += 1
        seconds_str = "%02d" % self.round_time
        self.time_label.setText(f"0:{seconds_str}")
        if self.round_time == 0:
            self.game.time_out_round_time()
