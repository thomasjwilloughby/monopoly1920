from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game

import os
from tkinter import Tk
import tkinter as tk
from local_view import ttk

from PIL import Image, ImageTk


class JoinMenu:
    def __init__(self, root: Tk, game: Game):
        # Clear root window
        for widget in root.winfo_children():
            widget.destroy()
        print("Displaying Main Menu")

        self._game = game
        self.root = root
        root.title("Monopoly 1920")
        root.minsize(400,600)
        root.geometry("400x600")

        self.main_frame = ttk.Frame(root)

        self.logo_image_orig = Image.open(os.path.join("resources", "images", "monopoly_logo.png"))
        self.logo_image = self.logo_image_orig.copy()
        self.logo_image_tk = ImageTk.PhotoImage(self.logo_image)
        self.logo = tk.Label(self.main_frame, text="A", image=self.logo_image_tk)
        self.logo.pack(side="top")

        self.lable = ttk.Label(self.main_frame, text="Join Game")
        self.lable.pack(side="top")

        self.back = ttk.Button(self.main_frame, text="Back", command=self._game._return_to_menu)
        self.back.pack(side="bottom")

        self.main_frame.pack(side="top", fill="y", expand=True, pady=(20,20))
