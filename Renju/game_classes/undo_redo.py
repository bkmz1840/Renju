class UndoRedo:
    def __init__(self):
        self.undo = list()
        self.redo = list()
        self.is_redo_pressed = False

    def add_obj_to_undo(self, obj):
        if len(self.undo) == 3:
            self.undo.pop(0)
            self.undo.append(obj)
        else:
            self.undo.append(obj)
