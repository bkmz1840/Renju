from game_classes.attack import Attack
from game_classes.type_game_object import TypeGameObject


class CheckerLines:
    def __init__(self, game):
        self.object = None
        self.game = game
        self.attacks = []
        self.current_attack = Attack()
        self.distance_from_center = 1
        self.check_edge = False
        self.len_attack = 1

    def get_object(self, x, y):
        obj = self.game.get_game_object(x, y)
        if obj is None:
            obj = "Border"
        return obj

    def check_edge_cell(self, current_obj):
        if self.check_edge:
            if current_obj == self.game.current_player.game_object \
                    or current_obj == TypeGameObject.Empty:
                self.current_attack.potential += 1
            if self.current_attack.capability > 0:
                self.attacks.append(self.current_attack)

    def check_cell(self, x, y):
        current_obj = self.get_object(x, y)
        if self.distance_from_center == 4 \
                and current_obj == self.object:
            self.check_edge = True
        elif self.distance_from_center == 5:
            self.check_edge_cell(current_obj)
            return "Empty"
        self.distance_from_center += 1
        if current_obj == TypeGameObject.White \
                or current_obj == TypeGameObject.Black:
            if current_obj != self.object:
                self.attacks.append(self.current_attack)
                return current_obj
            self.current_attack.capability += 1
            self.len_attack += 1
        elif current_obj == "Border":
            self.attacks.append(self.current_attack)
            return current_obj
        else:
            if self.current_attack.capability > 0:
                self.current_attack.potential += 1
                self.attacks.append(self.current_attack)
                self.current_attack = Attack()
                self.current_attack.potential += 1
            self.current_attack.divider += 1
            self.len_attack += 1

    def turn_around(self):
        self.distance_from_center = 1
        self.check_edge = False
        self.current_attack = self.attacks[0]
        self.attacks.pop(0)

    def get_attacks(self, cell_x, cell_y, object, dx, dy):
        self.object = object
        self.current_attack.capability += 1
        x = cell_x - dx
        y = cell_y - dy
        while abs(x - cell_x) <= 5 and abs(y - cell_y) <= 5:
            if self.check_cell(x, y) is not None:
                break
            x -= dx
            y -= dy
        self.turn_around()
        x = cell_x + dx
        y = cell_y + dy
        while abs(x - cell_x) <= 5 and abs(y - cell_y) <= 5:
            if self.check_cell(x, y) is not None:
                break
            x += dx
            y += dy
        return self.attacks
