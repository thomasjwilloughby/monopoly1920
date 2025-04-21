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

        self._menu: MainMenu | JoinMenu | None = MainMenu(root, self)

    def open_menu(self, menu_type: Literal["main", "multi_join", "multi_host"]):
        assert self._controler == None
        assert self._view == None

        self._menu = None
        match menu_type:
            case "main":
                self._menu = MainMenu(self._root, self)
            case "multi_join":
                self._menu = JoinMenu(self._root, self)
            case "multi_host":
                raise NotImplementedError # TODO

    # Callbacks
    def _start_game(self, game_type: Literal["local", "multi_join", "multi_host"]):
        print(f"Starting game of type '{game_type}'")
        self._menu = None
        for widget in self._root.winfo_children():
            widget.destroy()

        if game_type == "local":
            self._view = [LocalView(self._root, self._quit_game)]
            self._controler = LocalController()
        elif game_type == "multi_join":
            raise NotImplementedError # TODO
        elif game_type == "multi_host":
            raise NotImplementedError # TODO

    # Return to main menu from sub-menu
    def _return_to_menu(self):
        self._menu = MainMenu(self._root, self)

    def _quit_game(self):
        print("Exiting Game")
        self._view = None
        self._controler = None

        self.open_menu("main")
