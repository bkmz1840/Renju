from enum import Enum


class GameMode(Enum):
    Load = 0
    Solo = "1 player"
    Together = "2 players"
    Threesome = "3 players"
    Foursome = "4 players"

    @staticmethod
    def get_count_players_by_mode(mode):
        players_by_mode = {
            GameMode.Solo: 1,
            GameMode.Together: 2,
            GameMode.Threesome: 3,
            GameMode.Foursome: 4
        }
        return players_by_mode[mode]

    @staticmethod
    def deserialize(str):
        game_modes = {
            GameMode.Solo.value: GameMode.Solo,
            GameMode.Together.value: GameMode.Together,
            GameMode.Threesome.value: GameMode.Threesome,
            GameMode.Foursome.value: GameMode.Foursome
        }
        if str not in game_modes:
            return None
        return game_modes[str]

    @staticmethod
    def serialize(mode):
        types = {
            GameMode.Solo: GameMode.Solo.value,
            GameMode.Together: GameMode.Together.value,
            GameMode.Threesome: GameMode.Threesome.value,
            GameMode.Foursome: GameMode.Foursome.value
        }
        if mode not in types:
            return None
        return types[mode]
