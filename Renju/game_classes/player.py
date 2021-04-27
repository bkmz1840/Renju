from game_classes.type_game_object import TypeGameObject


class Player:
    def __init__(self, game_obj, name, play_time=0):
        self.game_object = game_obj
        self.name = name
        self.play_time = play_time

    def serialize(self):
        result = "{"
        result += "\"object\": " \
                  f"\"{TypeGameObject.serialize(self.game_object)}\", "
        result += f"\"name\": \"{self.name}\", "
        result += f"\"play_time\": {self.play_time}" + "}"
        return result

    @staticmethod
    def deserialize(obj):
        game_obj = TypeGameObject.deserialize(obj["object"])
        play_time = int(obj["play_time"])
        return Player(game_obj, obj["name"], play_time)
