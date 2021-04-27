from game_classes.checker_lines import CheckerLines
from game_classes.type_game_object import TypeGameObject


class CollectorAttacks:
    def __init__(self, game):
        self.game = game

    def get_all_attacks(self, x, y):
        if self.game.get_game_object(x, y) != TypeGameObject.Empty:
            return
        blacks = {}
        whites = {}
        lines = {
            "0": lambda obj: self.get_attacks_in_line(x, y, obj, 1, 0),
            "90": lambda obj: self.get_attacks_in_line(x, y, obj, 0, 1),
            "45": lambda obj: self.get_attacks_in_line(x, y, obj, 1, -1),
            "135": lambda obj: self.get_attacks_in_line(x, y, obj, 1, 1),
        }
        for direction in lines:
            blacks[direction] = lines[direction](TypeGameObject.Black)
            whites[direction] = lines[direction](TypeGameObject.White)
        return {
            TypeGameObject.Black: blacks,
            TypeGameObject.White: whites
        }

    def get_attacks_in_line(self, x, y, object, dx, dy):
        checker = CheckerLines(self.game)
        checker.get_attacks(x, y, object, dx, dy)
        return self.filter_attacks(checker)

    def filter_attacks(self, checker):
        result = []
        if checker.len_attack >= 5:
            for attack in checker.attacks:
                if attack.capability > 0 and attack.potential > 0 \
                        or attack.capability >= 5:
                    result.append(attack)
        checker.attacks = result
        return result

    def is_break_point(self, attack_line):
        if attack_line is None or len(attack_line) == 0:
            return False
        cent_attack = None
        for attack in attack_line:
            if attack.divider == 1:
                cent_attack = attack
        if cent_attack is None:
            return False
        if cent_attack.capability >= 4 \
                or cent_attack.potential == 2 \
                and cent_attack.capability >= 3:
            return True
        for attack in attack_line:
            score = cent_attack.capability
            if attack.divider == 2:
                if cent_attack.potential == 2 and attack.potential == 2:
                    score += 1
                if score + attack.capability >= 4:
                    return True
        return False
