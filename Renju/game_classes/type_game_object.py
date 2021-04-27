from enum import Enum


class TypeGameObject(Enum):
    Empty = "Empty"
    Black = "Black"
    White = "White"
    Red = "Red"
    Green = "Green"

    @staticmethod
    def serialize(type):
        types = {
            TypeGameObject.Empty: TypeGameObject.Empty.value,
            TypeGameObject.Black: TypeGameObject.Black.value,
            TypeGameObject.White: TypeGameObject.White.value,
            TypeGameObject.Red: TypeGameObject.Red.value,
            TypeGameObject.Green: TypeGameObject.Green.value
        }
        if type not in types:
            return None
        return types[type]

    @staticmethod
    def deserialize(str):
        types_by_str = {
            TypeGameObject.Empty.value: TypeGameObject.Empty,
            TypeGameObject.Black.value: TypeGameObject.Black,
            TypeGameObject.White.value: TypeGameObject.White,
            TypeGameObject.Green.value: TypeGameObject.Green,
            TypeGameObject.Red.value: TypeGameObject.Red
        }
        if str not in types_by_str:
            return None
        return types_by_str[str]
