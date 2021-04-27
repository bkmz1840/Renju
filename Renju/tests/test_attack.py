from game_classes.attack import Attack
import unittest


class TestsAttack(unittest.TestCase):
    def test_get_weight(self):
        attack = Attack(cap=1, pot=1)
        self.assertEqual(attack.get_weight(), 0.1)
        attack = Attack(cap=5, pot=1)
        self.assertEqual(attack.get_weight(), 200)
