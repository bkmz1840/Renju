attack_weight = [[0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0]]
attack_weight[1][1] = 0.1
attack_weight[2][1] = 2
attack_weight[3][1] = 4
attack_weight[4][1] = 6
attack_weight[5][1] = 200
attack_weight[1][2] = 0.25
attack_weight[2][2] = 5
attack_weight[3][2] = 7
attack_weight[4][2] = 100
attack_weight[5][2] = 200
attack_weight[5][0] = 200


class Attack:
    def __init__(self, cap=0, pot=0, div=1):
        self.capability = cap
        self.potential = pot
        self.divider = div

    def get_weight(self):
        return attack_weight[self.capability][self.potential] \
               / self.divider
