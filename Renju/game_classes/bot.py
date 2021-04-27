from game_classes.counter_weights import CounterWeights
from game_classes.type_game_object import TypeGameObject
import random


class Bot:
    def __init__(self, game, game_object):
        self.game = game
        self.game_object = game_object
        self.counter_weights = CounterWeights(self.game)

    def make_random_move(self):
        available_cells = []
        for x in range(0, self.game.field_size - 3):
            for y in range(0, self.game.field_size - 3):
                if self.game.get_game_object(x, y) == TypeGameObject.Empty:
                    available_cells.append((x, y))
        return available_cells[random.randint(0, len(available_cells) - 1)]

    def make_turn(self):
        result_x = -1
        result_y = -1
        max_weight = 0
        for x in range(0, self.game.field_size):
            for y in range(0, self.game.field_size):
                if self.game.get_game_object(x, y) != TypeGameObject.Empty:
                    continue
                current_weight = self.counter_weights.count_weight(x, y)
                if current_weight > max_weight:
                    max_weight = current_weight
                    result_x = x
                    result_y = y
        if result_x == -1:
            return self.make_random_move()
        return result_x, result_y
