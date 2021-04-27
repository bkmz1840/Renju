from game_classes.checker_lines import CheckerLines
from game_classes.attack import Attack
from game_classes.game import Game
from game_classes.type_game_object import TypeGameObject
from game_classes.game_mode import GameMode
import unittest


class TestsCheckerLines(unittest.TestCase):
    def setUp(self):
        self.game = Game(None, GameMode.Together, False)
        for i in range(1, 4):
            self.game.game_field[i][i].type = TypeGameObject.Black

    def test_get_object(self):
        checker = CheckerLines(self.game)
        self.assertEqual(checker.get_object(-1, 0), "Border")
        self.assertEqual(checker.get_object(1, 1), TypeGameObject.Black)

    def test_check_edge_cell(self):
        # check element after row of elements
        checker = CheckerLines(self.game)
        checker.check_edge = True
        checker.check_edge_cell(TypeGameObject.Empty)
        self.assertEqual(checker.current_attack.potential, 1)
        checker.current_attack.capability += 1
        checker.check_edge_cell(TypeGameObject.Empty)
        self.assertEqual(checker.current_attack.potential, 2)
        self.assertEqual(len(checker.attacks), 1)

    def test_turn_around(self):
        checker = CheckerLines(self.game)
        a1 = Attack(cap=2, pot=2)
        a2 = Attack(cap=3, pot=1)
        checker.attacks.append(a1)
        checker.attacks.append(a2)
        checker.turn_around()
        self.assertEqual(len(checker.attacks), 1)
        self.assertEqual(checker.current_attack, a1)
        self.assertEqual(checker.attacks[0], a2)

    def test_check_cell(self):
        checker = CheckerLines(self.game)
        checker.object = TypeGameObject.White
        self.assertEqual(checker.check_cell(1, 1), TypeGameObject.Black)
        self.assertEqual(len(checker.attacks), 1)
        checker.object = TypeGameObject.Black
        checker.check_cell(1, 1)
        self.assertEqual(checker.current_attack.capability, 1)
        self.assertEqual(checker.len_attack, 2)
        self.assertEqual(checker.check_cell(-1, 0), "Border")
        self.assertEqual(len(checker.attacks), 2)
        self.assertIsNone(checker.check_cell(0, 0))
        self.assertEqual(checker.current_attack.potential, 1)
        self.assertEqual(len(checker.attacks), 3)
        self.assertEqual(checker.current_attack.capability, 0)
        self.assertEqual(checker.current_attack.potential, 1)
        self.assertEqual(checker.current_attack.divider, 2)
        self.assertEqual(checker.len_attack, 3)

    def test_get_attacks(self):
        checker = CheckerLines(self.game)
        a1 = checker.get_attacks(0, 0, TypeGameObject.Black, 1, 0)
        self.assertEqual(len(a1), 1)
        self.assertEqual(a1[0].capability, 1)
        self.assertEqual(a1[0].potential, 1)
        checker.object = TypeGameObject.Black
        a2 = checker.get_attacks(0, 0, TypeGameObject.Black, 1, 1)
        self.assertEqual(len(a2), 1)
        self.assertEqual(a2[0].capability, 4)
        self.assertEqual(a2[0].potential, 2)
