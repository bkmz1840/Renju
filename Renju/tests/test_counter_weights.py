from game_classes.counter_weights import CounterWeights
from game_classes.type_game_object import TypeGameObject
from game_classes.game import Game
from game_classes.attack import Attack
from game_classes.game_mode import GameMode
import unittest


class TestsCounterWeights(unittest.TestCase):
    def setUp(self):
        self.game = Game(None, GameMode.Together, False)
        for i in range(1, 5):
            self.game.game_field[i][i].type = TypeGameObject.Black

    def test_count(self):
        counter = CounterWeights(self.game)
        a = {
            "0": [Attack(pot=2, div=2), Attack(cap=4, div=2),
                  Attack(pot=2, div=1)],
            "90": [Attack(pot=2, div=2), Attack(cap=4, div=2),
                   Attack(pot=2, div=1)],
            "45": [],
            "135": []
        }
        self.assertEqual(counter.count(TypeGameObject.Black, a), 100)
        a = {
            "0": [Attack(cap=5, pot=1)],
            "90": [Attack(cap=2, pot=1)],
            "45": [],
            "135": []
        }
        self.assertEqual(counter.count(TypeGameObject.Black, a), 302)

    def test_count_weight(self):
        counter = CounterWeights(self.game)
        self.assertEqual(counter.count_weight(1, 1), 0)
        self.assertEqual(counter.count_weight(0, 0), 300.4)
