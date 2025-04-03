from typing import Literal
from tkinter import Tk

from local_controller import LocalController
from local_view import LocalView
from main_menu import MainMenu

class Game:
    def __init__(self, root: Tk) -> None:
        self._root = root

        self._controler: None | LocalController = None
        self._view: None | LocalView = None

        self._menu: MainMenu | None = MainMenu(root, self._start_game)

    # Callbacks
    def _start_game(self, type: Literal["local"]):
        print(f"Starting game of type '{type}'")
        self._menu = None

        self._view = LocalView(self._root)
        self._controler = LocalController()
