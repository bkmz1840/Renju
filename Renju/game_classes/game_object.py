from game_classes.type_game_object import TypeGameObject


class GameObject:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

    def serialize(self):
        result = "{"
        result += f"\"x\": {self.x}, "
        result += f"\"y\": {self.y}, "
        result += f"\"type\": \"{TypeGameObject.serialize(self.type)}\""
        result += "}"
        return result

    @staticmethod
    def deserialize(obj):
        x = int(obj["x"])
        y = int(obj["y"])
        type = TypeGameObject.deserialize(obj["type"])
        return GameObject(x, y, type)
