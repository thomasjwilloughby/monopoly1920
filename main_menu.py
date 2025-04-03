import os
from tkinter import Tk, font
from typing import Callable

import tkinter as tk


from local_view import ttk

from PIL import Image, ImageTk
import PIL


class MainMenu:

    def __init__(self, root: Tk, start_game: Callable):
        # Clear root window
        for widget in root.winfo_children():
            widget.destroy()
        print("Displaying Main Menu")

        self.root = root
        root.title("Monopoly 1920")
        root.minsize(400,600)

        self.main_frame = ttk.Frame(root)

        self.logo_image_orig = Image.open(os.path.join("resources", "images", "monopoly_logo.png"))
        self.logo_image = self.logo_image_orig.copy()
        self.logo_image_tk = ImageTk.PhotoImage(self.logo_image)
        self.logo = tk.Label(self.main_frame, text="A", image=self.logo_image_tk)
        self.logo.pack(side="top")

        self.button_style = ttk.Style()
        self.button_style.configure('MainMenu.TButton', font=("TkDefaultFont", 16))

        self.local_game = ttk.Button(self.main_frame, text="Local Game", command=lambda: start_game("local"), padding=(10,2,10,2), style="MainMenu.TButton")
        self.local_game.pack(side="top", pady=(40,10))

        self.host_game= ttk.Button(self.main_frame, text="Host Multiplayer", command=lambda: start_game("multi_host"), padding=(10,2,10,2), style="MainMenu.TButton")
        self.host_game.pack(side="top", pady=(10,10))
        self.host_game.state(['disabled'])

        self.join_game = ttk.Button(self.main_frame, text="Join Multiplayer", command=lambda: start_game("multi_join"), padding=(10,2,10,2), style="MainMenu.TButton")
        self.join_game.pack(side="top", pady=(10,10))
        self.join_game.state(['disabled'])

        self.local_game = ttk.Button(self.main_frame, text="Quit", command=lambda: self._exit(), padding=(10,2,10,2), style="MainMenu.TButton")
        self.local_game.pack(side="bottom", pady=(30,20))

        self.main_frame.pack(side="top", fill="y", expand=True, pady=(20,20))

    def _exit(self):
        self.root.destroy()
