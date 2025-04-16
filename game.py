from typing import Literal
from tkinter import Tk

from join_menu import JoinMenu
from local_controller import LocalController
from local_view import LocalView
from main_menu import MainMenu

class Game:
    def __init__(self, root: Tk) -> None:
        self._root = root

        self._controler: None | LocalController = None
        self._view: None | list[LocalView] = None

        self._menu: MainMenu | JoinMenu | None = MainMenu(root, self._start_game)

    # Callbacks
    def _start_game(self, game_type: Literal["local", "multi_join", "multi_host"]):
        print(f"Starting game of type '{type}'")
        self._menu = None
        for widget in self._root.winfo_children():
            widget.destroy()

        if game_type == "local":
            self._view = [LocalView(self._root, self._quit_game)]
            self._controler = LocalController()
        elif game_type == "multi_join":
            self._menu = JoinMenu(self._root, self._return_to_menu)
        elif game_type == "multi_host":
            ...

    # Return to main menu from sub-menu
    def _return_to_menu(self):
        self._menu = MainMenu(self._root, self._start_game)

    def _quit_game(self):
        print("Exiting Game")
        self._view = None
        self._controler = None

        self._menu = MainMenu(self._root, self._start_game)
