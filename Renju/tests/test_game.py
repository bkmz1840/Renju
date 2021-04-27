from game_classes.game import Game
from game_classes.type_game_object import TypeGameObject
from game_classes.game_mode import GameMode
from game_classes.player import Player
from game_classes.undo_redo import UndoRedo
from game_classes.game_object import GameObject
import unittest
import os


class TestsGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(None, GameMode.Together, False)
        for i in range(0, 5):
            self.game.game_field[i][i].type = TypeGameObject.Black
        x = self.game.field_size - 1
        y = 0
        for i in range(0, 5):
            self.game.game_field[x][y].type = TypeGameObject.White
            x -= 1
            y += 1
        for i in range(0, 5):
            self.game.game_field[i][self.game.field_size - 1].type \
                = TypeGameObject.Black
        x = self.game.field_size - 1
        y = self.game.field_size - 6
        for i in range(0, 5):
            self.game.game_field[x][y].type = TypeGameObject.White
            y += 1

    def test_create_game_field(self):
        result = self.game.create_game_field()
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), self.game.field_size)
        self.assertEqual(len(result[0]), self.game.field_size)

    def test_check_line(self):
        self.assertFalse(self.game.check_line(
            7, 7, 1, 0, TypeGameObject.Black))
        for i in range(0, 5):
            self.assertTrue(self.game.check_line(
                i, i, 1, 1, TypeGameObject.Black))
        x = self.game.field_size - 1
        y = 0
        for i in range(0, 5):
            self.assertTrue(self.game.check_line(
                x, y, -1, 1, TypeGameObject.White))
            x -= 1
            y += 1
        for i in range(0, 5):
            self.assertTrue(self.game.check_line(
                i, self.game.field_size - 1, 1, 0, TypeGameObject.Black))
        x = self.game.field_size - 1
        y = self.game.field_size - 6
        for i in range(0, 5):
            self.assertTrue(self.game.check_line(
                x, y, 0, 1, TypeGameObject.White))
            y += 1

    def test_check_end_of_game(self):
        self.game.check_end_of_game(7, 7, TypeGameObject.White)
        self.assertFalse(self.game.is_game_finished)
        self.game.check_end_of_game(2, 2, TypeGameObject.Black)
        self.assertTrue(self.game.is_game_finished)

    def test_get_game_object(self):
        self.assertIsNone(self.game.get_game_object(-1, 0))
        self.assertIsNone(self.game.get_game_object(0, -1))
        self.assertIsNone(self.game.get_game_object(15, 0))
        self.assertIsNone(self.game.get_game_object(0, 15))
        self.assertEqual(self.game.get_game_object(0, 0),
                         TypeGameObject.Black)

    def test_make_turn(self):
        # if everything is good AttributeError will be thrown,
        # because (game_place is None)
        self.game.is_game_finished = True
        self.assertFalse(self.game.make_turn(275, 245))
        self.game.is_game_finished = False
        self.assertFalse(self.game.make_turn(20, 20))
        self.assertFalse(self.game.make_turn(500, 500))
        self.assertFalse(self.game.make_turn(65, 40))
        self.assertRaises(AttributeError, self.game.make_turn, 275, 245)
        self.assertEqual(self.game.get_game_object(7, 7),
                         TypeGameObject.Black)

    def test_convert_play_time_to_str(self):
        p_t_1 = 300
        p_t_2 = 0
        p_t_3 = 340
        p_t_4 = 30
        self.assertEqual("5:00", self.game.convert_play_time_to_str(p_t_1))
        self.assertEqual("0:00", self.game.convert_play_time_to_str(p_t_2))
        self.assertEqual("5:40", self.game.convert_play_time_to_str(p_t_3))
        self.assertEqual("0:30", self.game.convert_play_time_to_str(p_t_4))

    def test_convert_str_play_time_to_int(self):
        s_p_t_1 = "5:00"
        s_p_t_2 = "0:00"
        s_p_t_3 = "5:40"
        s_p_t_4 = "0:30"
        self.assertEqual(300, self.game.convert_str_play_time_to_int(
            s_p_t_1))
        self.assertEqual(0, self.game.convert_str_play_time_to_int(
            s_p_t_2))
        self.assertEqual(340, self.game.convert_str_play_time_to_int(
            s_p_t_3))
        self.assertEqual(30, self.game.convert_str_play_time_to_int(
            s_p_t_4))

    def test_fill_players(self):
        self.game.mode = GameMode.Solo
        self.game.players = []
        self.game.fill_players()
        self.assertEqual(len(self.game.players), 2)
        self.game.mode = GameMode.Foursome
        self.game.players = []
        self.game.fill_players()
        self.assertEqual(4, len(self.game.players))
        objs = [TypeGameObject.Black, TypeGameObject.White,
                TypeGameObject.Red, TypeGameObject.Green]
        i = 0
        for player in self.game.players:
            self.assertEqual("", player.name)
            self.assertEqual(objs[i], player.game_object)
            i += 1

    def test_update_leader_board(self):
        player = Player(TypeGameObject.Black, "%%BOT%%")
        self.assertIsNone(self.game.update_leader_board(player))
        winner = Player(TypeGameObject.Black, "T", 50)
        self.game.update_leader_board(winner)
        directory_folder = "./leader_board.list"
        self.assertTrue(os.path.exists(directory_folder))
        exp_l_b = "T - 0:50\n"
        with open(directory_folder) as file:
            self.assertEqual(exp_l_b, file.read())
        winner = Player(TypeGameObject.Black, "Q", 300)
        self.game.update_leader_board(winner)
        exp_l_b += "Q - 5:00\n"
        with open(directory_folder) as file:
            self.assertEqual(exp_l_b, file.read())

    def test_serialize(self):
        players = [Player(TypeGameObject.Black, "T", 10),
                   Player(TypeGameObject.White, "R", 50),
                   Player(TypeGameObject.Red, "E", 20)]
        game = Game(None, GameMode.Threesome, True, players)
        game.game_field[5][5].type = TypeGameObject.Red
        exp = "{\"mode\": \"3 players\", \"index_player\": 0, " \
              "\"has_timer\": \"True\", " \
              "\"players\": [{\"object\": \"Black\", \"name\": \"T\", " \
              "\"play_time\": 10}, " \
              "{\"object\": \"White\", \"name\": \"R\", " \
              "\"play_time\": 50}, " \
              "{\"object\": \"Red\", \"name\": \"E\", " \
              "\"play_time\": 20}], \"field\": [{\"x\": 210, " \
              "\"y\": 185, \"type\": \"Red\"}]}"
        self.assertEqual(exp, game.serialize())

    def test_load_field(self):
        game = Game(None, GameMode.Together, False)
        field = [{"x": 210, "y": 185, "type": "Red"},
                 {"x": 120, "y": 95, "type": "Green"}]
        game.load_field(field)
        self.assertEqual(TypeGameObject.Red, game.game_field[5][5].type)
        self.assertEqual(TypeGameObject.Green, game.game_field[2][2].type)

    def test_load_players(self):
        game = Game(None, GameMode.Together, False)
        game.players = []
        players = [{"object": "Red", "name": "%%BOT%%", "play_time": 0},
                   {"object": "Green", "name": "D", "play_time": 20}]
        self.assertEqual(TypeGameObject.Red, game.load_players(players))
        self.assertEqual(2, len(game.players))
        self.assertEqual(game.current_player.name, "%%BOT%%")

    def test_load_save(self):
        game = Game(None, GameMode.Load, False)
        path_to_save = "./1.save"
        game.load_save(path_to_save)
        self.assertEqual(game.mode, GameMode.Threesome)
        self.assertEqual(game.index_player, 0)
        self.assertIsNotNone(game.bot)

    def test_redo(self):
        self.game.player_undo_redo = UndoRedo()
        self.game.bot_undo_redo = UndoRedo()
        self.assertIsNone(self.game.redo())
        self.game.bot_undo_redo.redo.append(
            GameObject(6, 6, TypeGameObject.Red))
        self.game.player_undo_redo.redo.append(
            GameObject(7, 7, TypeGameObject.Green))
        self.assertRaises(AttributeError, self.game.redo)

    def test_undo(self):
        self.game.player_undo_redo = UndoRedo()
        self.game.bot_undo_redo = UndoRedo()
        self.assertIsNone(self.game.undo())
        self.game.bot_undo_redo.undo.append(
            GameObject(6, 6, TypeGameObject.Red))
        self.game.player_undo_redo.undo.append(
            GameObject(7, 7, TypeGameObject.Green))
        self.assertRaises(AttributeError, self.game.undo)
