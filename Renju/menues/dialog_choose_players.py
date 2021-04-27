from PyQt5.QtWidgets import QDialog, QDialogButtonBox,\
    QLabel, QVBoxLayout, QLineEdit, QComboBox
from PyQt5.QtCore import Qt
from game_classes.game_mode import GameMode
from game_classes.player import Player
from game_classes.type_game_object import TypeGameObject
import random
import os


class ChoosePlayersDialog(QDialog):
    def __init__(self, mode):
        super().__init__()
        self.setWindowTitle("Choose players")
        self.setStyleSheet('''
            background-color: #151b2d;
            color: #fff;
        ''')
        self.mode = mode
        self.count_players = GameMode.get_count_players_by_mode(self.mode)
        self.name_players = set()
        self.upload_players()
        self.editors = []
        self.init_UI()
        self.players = []

    def upload_players(self):
        directory_folder = "./players.list"
        if not os.path.exists(directory_folder):
            file = open(directory_folder, "w+")
            file.close()
        with open(directory_folder) as file:
            players = file.read().split('\n')
        for player in players:
            self.name_players.add(player)

    def get_combo_box(self, index_edit):
        combo_box = QComboBox(self)
        for player in self.name_players:
            combo_box.addItem(player)
        combo_box.setObjectName(str(index_edit))
        combo_box.activated[str].connect(self.change_edit)
        return combo_box

    def change_edit(self, text):
        index_edit = int(self.sender().objectName())
        self.editors[index_edit].setText(text)

    def init_UI(self):
        layout = QVBoxLayout(self)
        texts_for_labels = ["First player:", "Second player:",
                            "Third player:", "Fourth player:"]
        for i in range(self.count_players):
            label = QLabel(texts_for_labels[i], self)
            label.setStyleSheet("margin-top: 10px;"
                                "font-weight: 700;"
                                "font-size: 17px;")
            layout.addWidget(label)
            edit = QLineEdit(self)
            self.editors.append(edit)
            layout.addWidget(edit)
            label_or = QLabel("Or", self)
            layout.addWidget(label_or)
            layout.addWidget(self.get_combo_box(i))
        bttn_box = QDialogButtonBox(self)
        bttn_box.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        bttn_box.setCenterButtons(True)
        bttn_box.rejected.connect(self.reject)
        bttn_box.accepted.connect(self.accept_clicked)
        layout.addWidget(bttn_box)

    def save_unique_players_names(self, unique_names):
        with open("./players.list", 'a') as file:
            for name in unique_names:
                file.write(name + '\n')

    def get_player_with_bot(self):
        player_name = self.editors[0].text()
        if player_name not in self.name_players:
            self.save_unique_players_names([player_name])
        random.seed()
        game_objects = [TypeGameObject.Black, TypeGameObject.White]
        index = random.randint(0, 1)
        if index == 0:
            self.players.append(Player(game_objects[index], "%%BOT%%"))
            self.players.append(Player(game_objects[1], player_name))
        else:
            self.players.append(Player(game_objects[0], player_name))
            self.players.append(Player(game_objects[index], "%%BOT%%"))

    def accept_clicked(self):
        if self.mode == GameMode.Solo:
            self.get_player_with_bot()
            self.accept()
            return
        game_objects = [TypeGameObject.Black, TypeGameObject.White,
                        TypeGameObject.Red, TypeGameObject.Green]
        unique_names = []
        index_obj = 0
        for edit in self.editors:
            edit_text = edit.text()
            if edit_text not in self.name_players:
                unique_names.append(edit_text)
            self.players.append(Player(
                game_objects[index_obj], edit_text))
            index_obj += 1
        if len(unique_names) > 0:
            self.save_unique_players_names(unique_names)
        self.accept()

    @staticmethod
    def get_players(mode):
        dialog = ChoosePlayersDialog(mode)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.show()
        if dialog.exec_() == QDialog.Accepted:
            dialog.deleteLater()
            return dialog.players, True
        return None, False
