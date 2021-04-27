from game_classes.game_object import GameObject
from game_classes.type_game_object import TypeGameObject
from game_classes.bot import Bot
from game_classes.undo_redo import UndoRedo
from game_classes.game_mode import GameMode
from game_classes.player import Player
import random
import os
import json
import re


class Game:
    def __init__(self, game_place, mode, has_timer, players=None):
        self.cell_size = 30
        self.field_size = 15
        self.count_free_cells = self.field_size * self.field_size
        self.game_field = self.create_game_field()
        self.is_game_finished = False
        self.mode = mode
        self.game_place = game_place
        self.has_timer = has_timer
        if mode == GameMode.Load:
            self.players = []
            self.index_player = 0
            return
        if self.has_timer:
            self.players = players
            self.index_player = 0
        else:
            self.players = []
            self.index_player = 0
            self.fill_players()
        self.current_player = self.players[0]
        if self.mode == GameMode.Solo:
            if self.players[0].name == "%%BOT%%":
                bot_object = self.players[0].game_object
            else:
                bot_object = self.players[1].game_object
            self.bot = Bot(self, bot_object)
            self.bot_undo_redo = UndoRedo()
            self.player_undo_redo = UndoRedo()
            if bot_object == TypeGameObject.Black:
                self.set_game_object(7, 7, TypeGameObject.Black)

    def choose_object_for_bot(self):
        objects = [TypeGameObject.Black, TypeGameObject.White]
        return objects[random.randint(0, 1)]

    def get_game_object(self, x, y):
        if x < 0 or y < 0 or x >= self.field_size or y >= self.field_size:
            return None
        return self.game_field[x][y].type

    def set_game_object(self, x, y, value):
        self.count_free_cells -= 1
        self.game_field[x][y].type = value
        if self.mode == GameMode.Solo:
            current_obj = self.current_player.game_object
            if self.current_player.name == "%%BOT%%":
                self.bot_undo_redo.add_obj_to_undo(
                    GameObject(x, y, current_obj))
            else:
                self.player_undo_redo.add_obj_to_undo(
                    GameObject(x, y, current_obj))
        self.check_end_of_game(x, y, value)
        if self.is_game_finished:
            self.game_place.change_text_with_winner(
                self.get_game_object(x, y).value)
            self.update_leader_board(self.current_player)
        elif self.count_free_cells == 0:
            self.is_game_finished = True
            self.game_place.change_text_with_winner("Draw")
        self.index_player += 1
        next_player = self.players[self.index_player
                                   % len(self.players)]
        self.current_player = next_player
        self.game_place.update()

    def del_game_object(self, x, y):
        self.game_field[x][y].type = TypeGameObject.Empty
        self.count_free_cells += 1

    def create_game_field(self):
        game_field = []
        for x in range(0, 15):
            row = []
            for y in range(0, self.field_size):
                row.append(GameObject(
                    60 + x * self.cell_size, 35 + y * self.cell_size,
                    TypeGameObject.Empty))
            game_field.append(row)
        return game_field

    def undo(self):
        if len(self.player_undo_redo.undo) == 0 \
                or len(self.bot_undo_redo.undo) == 0:
            return
        current_obj_bot = self.bot_undo_redo.undo.pop()
        self.del_game_object(current_obj_bot.x, current_obj_bot.y)
        self.bot_undo_redo.redo.append(current_obj_bot)
        current_obj_player = self.player_undo_redo.undo.pop()
        self.del_game_object(current_obj_player.x, current_obj_player.y)
        self.player_undo_redo.redo.append(current_obj_player)
        self.game_place.update()

    def redo(self):
        if len(self.player_undo_redo.redo) == 0 \
                or len(self.bot_undo_redo.redo) == 0:
            return
        current_obj_bot = self.bot_undo_redo.redo.pop()
        self.set_game_object(current_obj_bot.x, current_obj_bot.y,
                             current_obj_bot.type)
        current_obj_player = self.player_undo_redo.redo.pop()
        self.set_game_object(current_obj_player.x, current_obj_player.y,
                             current_obj_player.type)

    def get_turn_by_bot(self):
        x, y = self.bot.make_turn()
        self.set_game_object(x, y, self.bot.game_object)

    def make_turn(self, x, y):
        if self.is_game_finished:
            return False
        if x < 60 or y < 35 or x > 510 or y > 485:
            return False
        x = (x - 60) // 30
        y = (y - 35) // 30
        chosen_game_object = self.get_game_object(x, y)
        if chosen_game_object != TypeGameObject.Empty:
            return False
        self.set_game_object(x, y, self.current_player.game_object)
        if not self.is_game_finished \
                and self.mode == GameMode.Solo:
            self.bot_undo_redo.redo.clear()
            self.player_undo_redo.redo.clear()
            self.bot_undo_redo.is_redo_pressed = False
            self.player_undo_redo.is_redo_pressed = False
            self.get_turn_by_bot()
        return True

    def check_line(self, x, y, dx, dy, type):
        score = 0
        while 0 <= x - dx < self.field_size \
                and 0 <= y - dy < self.field_size \
                and self.get_game_object(x - dx, y - dy) == type:
            x -= dx
            y -= dy
        while 0 <= x < self.field_size \
                and 0 <= y < self.field_size \
                and self.get_game_object(x, y) == type:
            x += dx
            y += dy
            score += 1
        return score >= 5

    def check_end_of_game(self, x, y, value):
        lines = [lambda: self.check_line(x, y, 0, 1, value),
                 lambda: self.check_line(x, y, 1, 0, value),
                 lambda: self.check_line(x, y, 1, 1, value),
                 lambda: self.check_line(x, y, 1, -1, value)]
        for line in lines:
            result = line()
            if result:
                self.is_game_finished = True
                return
        self.is_game_finished = False

    def serialize(self):
        result = "{"
        result += f"\"mode\": \"{GameMode.serialize(self.mode)}\", "
        result += f"\"index_player\": {self.index_player}, "
        result += f"\"has_timer\": \"{self.has_timer}\", "
        result += "\"players\": ["
        for player in self.players:
            result += player.serialize() + ", "
        result = result[:-2]
        result += "], "
        result += "\"field\": ["
        for row in self.game_field:
            for game_object in row:
                if game_object.type != TypeGameObject.Empty:
                    result += game_object.serialize() + ", "
        result = result[:-2]
        result += "]}"
        return result

    def save_game(self, name):
        serialized_game = self.serialize()
        directory_folder = f"./saves/{name}.save"
        if not os.path.exists(directory_folder):
            file = open(directory_folder, "w+")
            file.close()
        with open(directory_folder, "w") as file:
            file.write(serialized_game)

    def load_field(self, field):
        for obj in field:
            deserialized_obj = GameObject.deserialize(obj)
            x = (deserialized_obj.x - 60) // 30
            y = (deserialized_obj.y - 35) // 30
            self.game_field[x][y] = deserialized_obj
            self.count_free_cells -= 1

    def load_players(self, players):
        bot_obj = None
        for player in players:
            current_player = Player.deserialize(player)
            self.players.append(current_player)
            if current_player.name == "%%BOT%%":
                bot_obj = current_player.game_object
        self.current_player = self.players[self.index_player
                                           % len(self.players)]
        return bot_obj

    def load_save(self, path_to_save):
        with open(path_to_save) as file:
            data = json.loads(file.read())
        self.mode = GameMode.deserialize(data["mode"])
        self.index_player = int(data["index_player"])
        bool_str = data["has_timer"]
        if bool_str == "False":
            self.has_timer = False
        else:
            self.has_timer = True
        bot_obj = self.load_players(data["players"])
        if bot_obj is not None:
            self.bot = Bot(self, bot_obj)
            self.bot_undo_redo = UndoRedo()
            self.player_undo_redo = UndoRedo()
        self.load_field(data["field"])

    def fill_players(self):
        if self.mode == GameMode.Solo:
            player_objs = {
                TypeGameObject.Black: TypeGameObject.White,
                TypeGameObject.White: TypeGameObject.Black
            }
            bot_obj = self.choose_object_for_bot()
            player_obj = player_objs[bot_obj]
            if bot_obj == TypeGameObject.Black:
                self.players.append(Player(bot_obj, "%%BOT%%"))
                self.players.append(Player(player_obj, ""))
            else:
                self.players.append(Player(player_obj, ""))
                self.players.append(Player(bot_obj, "%%BOT%%"))
            return
        game_objects = [TypeGameObject.Black, TypeGameObject.White,
                        TypeGameObject.Red, TypeGameObject.Green]
        for i in range(GameMode.get_count_players_by_mode(self.mode)):
            self.players.append(Player(game_objects[i], ""))

    def time_out_round_time(self):
        self.is_game_finished = True
        self.game_place.change_text_with_winner("Time out")
        self.game_place.update()

    def update_leader_board(self, winner):
        if winner.name == "%%BOT%%" or winner.name == "":
            return
        directory_folder = "./leader_board.list"
        if not os.path.exists(directory_folder):
            file = open(directory_folder, "w+")
            file.close()
        with open(directory_folder) as file:
            data = file.read().split('\n')
        records = []
        for line in data:
            if line == "":
                continue
            record = re.split(r" - ", line)
            records.append(
                (record[0],
                 self.convert_str_play_time_to_int(record[1])))
        records.append((winner.name, winner.play_time))
        records.sort(key=lambda record: record[1])
        leader_table = ""
        count_records = 0
        for record in records:
            leader_table += f"{record[0]} - " \
                            f"{self.convert_play_time_to_str(record[1])}\n"
            count_records += 1
            if count_records == 10:
                break
        with open(directory_folder, 'w') as leader_board:
            leader_board.write(leader_table)

    def convert_str_play_time_to_int(self, str):
        split_str = str.split(":")
        return int(split_str[0]) * 60 + int(split_str[1])

    def convert_play_time_to_str(self, play_time):
        minutes = play_time // 60
        seconds = play_time % 60
        seconds_str = "%02d" % seconds
        return f"{minutes}:{seconds_str}"
