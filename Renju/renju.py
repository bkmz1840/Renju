from PyQt5.QtWidgets import QApplication
from menues.main_menu import MainMenu
import sys


def main():
    app = QApplication(sys.argv)
    game = MainMenu()
    game.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 2:
        if args[1] == "-h" or args[1] == "--help":
            print("Usage: renju.py\n")
            print("Turn-based game Renju. Version 1.1\n")
            print("Optional argument:")
            print("  NONE\t\trun the game")
            print("Author: Vasilev Ilya <bkmz1840@gmail.com>")
    else:
        main()
