from game_classes.collector_attacks import CollectorAttacks
from game_classes.type_game_object import TypeGameObject


class CounterWeights:
    def __init__(self, game):
        self.game = game
        self.collector_attacks = CollectorAttacks(self.game)

    def count_weight(self, x, y):
        attacks = self.collector_attacks.get_all_attacks(x, y)
        if attacks is None:
            return 0
        sum = 0
        sum += self.count(
            TypeGameObject.Black, attacks[TypeGameObject.Black])
        sum += self.count(
            TypeGameObject.White, attacks[TypeGameObject.White])
        return sum

    def count(self, object, attacks):
        weight = 0
        break_points = 0
        for direction in attacks:
            if self.collector_attacks.is_break_point(attacks[direction]):
                if break_points + 1 == 2:
                    weight += 100
                    break
                break_points += 1
            for attack in attacks[direction]:
                if attack.capability > 4 \
                        and object == self.game.current_player.game_object:
                    weight += 100
                weight += attack.get_weight()
        return weight
