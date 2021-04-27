from game_classes.game import Game
from game_classes.checker_lines import CheckerLines
from game_classes.collector_attacks import CollectorAttacks
from game_classes.type_game_object import TypeGameObject
from game_classes.attack import Attack
from game_classes.game_mode import GameMode
import unittest


class TestsCollectorAttacks(unittest.TestCase):
    def setUp(self):
        self.game = Game(None, GameMode.Together, False)
        for i in range(1, 4):
            self.game.game_field[i][i].type = TypeGameObject.Black

    def test_get_all_attacks(self):
        collector = CollectorAttacks(self.game)
        self.assertIsNone(collector.get_all_attacks(1, 1))
        a = collector.get_all_attacks(0, 0)
        self.assertIn(TypeGameObject.Black, a)
        self.assertIn("0", a[TypeGameObject.Black])
        self.assertEqual(len(a[TypeGameObject.Black]["0"]), 1)
        self.assertIn("90", a[TypeGameObject.Black])
        self.assertEqual(len(a[TypeGameObject.Black]["90"]), 1)
        self.assertIn("45", a[TypeGameObject.Black])
        self.assertListEqual(a[TypeGameObject.Black]["45"], [])
        self.assertIn("135", a[TypeGameObject.Black])
        self.assertEqual(len(a[TypeGameObject.Black]["135"]), 1)
        self.assertIn(TypeGameObject.White, a)
        self.assertIn("0", a[TypeGameObject.White])
        self.assertEqual(len(a[TypeGameObject.White]["0"]), 1)
        self.assertIn("90", a[TypeGameObject.White])
        self.assertEqual(len(a[TypeGameObject.White]["90"]), 1)
        self.assertIn("45", a[TypeGameObject.White])
        self.assertListEqual(a[TypeGameObject.White]["45"], [])
        self.assertIn("135", a[TypeGameObject.White])
        self.assertListEqual(a[TypeGameObject.White]["135"], [])

    def test_assertListEqual(self):
        collector = CollectorAttacks(self.game)
        al = collector.get_attacks_in_line(0, 0, TypeGameObject.White, 0, 1)
        self.assertEqual(len(al), 1)
        self.assertEqual(al[0].capability, 1)
        self.assertEqual(al[0].potential, 1)

    def test_filter_attacks(self):
        checker = CheckerLines(self.game)
        collector = CollectorAttacks(self.game)
        checker.len_attack = 5
        a = Attack(cap=4, pot=2)
        checker.attacks = [a, Attack(), Attack()]
        self.assertListEqual(collector.filter_attacks(checker), [a])
        self.assertListEqual(checker.attacks, [a])

    def test_is_break_point(self):
        collector = CollectorAttacks(self.game)
        self.assertFalse(collector.is_break_point([]))
        a = Attack(div=0)
        self.assertFalse(collector.is_break_point([a]))
        a = Attack(cap=4, pot=1)
        self.assertTrue(collector.is_break_point([a]))
        self.assertFalse(collector.is_break_point([a, Attack()]))
        self.assertTrue(collector.is_break_point(
            [Attack(pot=2, div=2), Attack(cap=4, div=2),
             Attack(pot=2, div=1)]))
