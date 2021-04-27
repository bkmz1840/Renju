from game_classes.undo_redo import UndoRedo
from game_classes.game_object import GameObject
from game_classes.type_game_object import TypeGameObject
import unittest


class TestsUndoRedo(unittest.TestCase):
    def test_add_obj_to_undo(self):
        undo_redo = UndoRedo()
        obj = GameObject(0, 0, TypeGameObject.Red)
        undo_redo.undo.append(obj)
        undo_redo.undo.append(obj)
        self.assertEqual(2, len(undo_redo.undo))
        undo_redo.add_obj_to_undo(obj)
        obj_1 = GameObject(1, 1, TypeGameObject.Green)
        undo_redo.add_obj_to_undo(obj_1)
        self.assertEqual(3, len(undo_redo.undo))
        self.assertNotEqual(undo_redo.undo[0].type, undo_redo.undo[-1].type)
        obj_2 = GameObject(2, 2, TypeGameObject.Black)
        undo_redo.add_obj_to_undo(obj_2)
        self.assertEqual(3, len(undo_redo.undo))
        self.assertNotEqual(undo_redo.undo[0].type, undo_redo.undo[1].type)
        self.assertNotEqual(undo_redo.undo[1].type, undo_redo.undo[2].type)
        self.assertNotEqual(undo_redo.undo[0].type, undo_redo.undo[2].type)
