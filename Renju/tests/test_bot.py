from game_classes.bot import Bot
from game_classes.game import Game
from game_classes.type_game_object import TypeGameObject
from game_classes.game_mode import GameMode
import unittest


class TestsBot(unittest.TestCase):
    def setUp(self):
        self.game = Game(None, GameMode.Together, False)
        for i in range(1, 5):
            self.game.game_field[i][i].type = TypeGameObject.Black

    def test_make_random_move(self):
        bot = Bot(self.game, TypeGameObject.Black)
        x, y = bot.make_random_move()
        self.assertEqual(self.game.get_game_object(x, y),
                         TypeGameObject.Empty)

    def test_make_turn(self):
        bot = Bot(self.game, TypeGameObject.Black)
        x, y = bot.make_turn()
        self.assertTupleEqual((x, y), (5, 5))
