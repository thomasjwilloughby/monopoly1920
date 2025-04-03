#!/usr/bin/env python3

import tkinter as tk
import os
from tkinter import ttk
import observer

import PIL.Image
import PIL.ImageTk
import PIL


def get_board_square_images():
    """return a List of all the file paths for the board square images"""
    square_images = []
    for i in range(40):
        path = os.path.join("resources", "images", "properties", f"{i}.png")
        square_images.append(path)
    return square_images

def get_player_piece_images() -> list[str]:
    path = os.path.join("resources", "images", "pieces")
    return [os.path.join(path, img) for img in os.listdir(path)]

def get_save_files() -> list[str]:
    saves_path = os.path.join("saves")
    if not os.path.isdir(saves_path):
        os.mkdir(saves_path)

    return os.listdir(saves_path)

class LocalView (observer.Observer):
    """Class to create the GUI for the Monopoly game"""
    width = 1920-100
    height = 1080-100

    def __init__(self, root):
        super().__init__()

        # Clear root window
        for widget in root.winfo_children():
            widget.destroy()
        root.minsize(1500,900)

        # Set-up a simple window
        self.square_images = []
        self.piece_images = []
        self.root = root
        root.title("Monopoly 1920")

        #tight coupling with the controller
        #not ideal, but we will refactor later
        #self.controller = controller

        root.geometry(f'{self.width}x{self.height}')
        root.resizable(True, True)

        self.main_frame = ttk.Frame(root, padding=10, relief='groove')

        #create the frames
        # logo_frame = self._create_logo_frame()
        middle_frame = self._create_middle_frame()
        msg_frame = self._create_msg_frame()

        #pack the frames
        # logo_frame.pack(fill=tk.BOTH, expand=True)
        middle_frame.pack(side='left',fill=tk.BOTH, expand=False)
        msg_frame.pack(side='right',fill=tk.BOTH, expand=True)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self._add_listeners()

        self.current_player_style = ttk.Style()
        self.current_player_style.configure('ActivePlayer.TFrame', background='#ABCBFF')
        self.current_player_style.configure('ActivePlayer.TLabel', background='#ABCBFF')

        #self.setup_game()

    def _add_listeners(self):
        """Add listeners to the view"""
        self.observe("update_players_state", self.update_players_state)
        self.observe("update_card", self.update_card)
        self.observe("update_state", self._update_text)
        self.observe("choice", self._choose)


    def _create_middle_frame(self):
        """Create the middle frame of the GUI"""
        self._preload_images()

        middle_frame = ttk.Frame(self.main_frame, padding=10)
        self.board_image = tk.PhotoImage(file=r"resources/images/monopoly2.png")

        canvas = tk.Canvas(middle_frame,width=800,height=800,background='black')
        canvas.pack(side='left')
        self.canvas = canvas

        self.canvas_images = {}

        self.canvas_images['background'] = canvas.create_image(401,401,image=self.board_image)
        pieces = []
        self.canvas_images['pieces'] = pieces
        pieces.append(canvas.create_image(0,0,image=self.piece_images[0],anchor='nw'))
        pieces.append(canvas.create_image(0,0,image=self.piece_images[1],anchor='nw'))
        pieces.append(canvas.create_image(0,0,image=self.piece_images[3],anchor='nw'))

        # preload all the images for the board squares

        f = ttk.Frame(middle_frame, borderwidth=0)
        card_image = self.square_images[0]
        self.card = ttk.Label(f, image=card_image)

        button_frame = ttk.Frame(f, padding=10)

        #create buttons
        self.mid_buttons = []
        self.roll_button = ttk.Button(button_frame, text="Roll Dice", command=lambda: self._action_taken("roll") )
        self.roll_button.pack(side='top', anchor='center', pady=(10, 10))
        self.mid_buttons.append(self.roll_button)

        self.purchase_button = ttk.Button(button_frame, text="Purchase", command=lambda: self._action_taken("purchase"))
        self.purchase_button.pack(side='top', anchor='center', pady=(10, 10))
        self.mid_buttons.append(self.purchase_button)

        self.mortgage_button = ttk.Button(button_frame, text="Mortgage", command=lambda: self._action_taken("mortgage"))
        self.mortgage_button.pack(side='top', anchor='center', pady=(10, 10))
        self.mid_buttons.append(self.mortgage_button)

        self.unmortgage_button = ttk.Button(button_frame, text="Unmortgage", command=lambda: self._action_taken("unmortgage"))
        self.unmortgage_button.pack(side='top', anchor='center', pady=(10, 10))
        self.mid_buttons.append(self.unmortgage_button)

        self.bankrupt_button = ttk.Button(button_frame, text="Go Bankrupt", command=lambda: self._action_taken("bankrupt"))
        self.bankrupt_button.pack(side='top', anchor='center', pady=(10, 10))
        self.mid_buttons.append(self.bankrupt_button)

        self.end_turn_button = ttk.Button(button_frame, text="End Turn", command=lambda: self._action_taken("end_turn"))
        self.end_turn_button.pack(side='top', anchor='center', pady=(10, 10))
        self.mid_buttons.append(self.end_turn_button)


        button_frame.pack(side='top', anchor='center', pady=(0, 0), padx=(5,5))

        self.card.pack(side='bottom', anchor='n', padx=100, pady=(100, 0))
        f.pack(side='right')

        self.card.image = card_image



        return middle_frame

    def _create_player_card(self, frame: ttk.LabelFrame) -> tuple[ttk.Frame, list[ttk.Label]]:
        f = ttk.Frame(frame, padding=10, relief='raised', borderwidth = 3)
        lables = []
        lables.append(ttk.Label(f, text="Name:  ", width=15))
        lables.append(ttk.Label(f, text="Money:  "))
        lables.append(ttk.Label(f, text="Net Worth:  "))
        lables.append(ttk.Label(f, text="Luck:  "))
        lables.append(ttk.Label(f, text="Position:  "))

        for l in lables:
            l.pack(side='top', anchor='w')

        return (f, lables)

    def _create_players_frame(self, parent: ttk.Frame) -> ttk.LabelFrame:
        players = ttk.LabelFrame(parent, text="Players", padding=10, relief='raised', borderwidth = 3) 

        self.player_cards: list[tuple[ttk.Frame, list[ttk.Label]]] = []
        self.player_cards.append(self._create_player_card(players))
        self.player_cards.append(self._create_player_card(players))
        self.player_cards.append(self._create_player_card(players))

        for (p, _) in self.player_cards:
            p.pack(side='top', fill='both', padx=(5,5), pady=(5,5))

        return players

    def _create_msg_frame(self):
        """Create the frame at the bottom of the screen to display messages"""
        msg_frame = ttk.Frame(self.main_frame, padding=10, relief='raised', borderwidth=3)

        # self.state_box = tk.Text(msg_frame, width=60, height=10, background='black', foreground='white')
        # self.state_box.pack(side='left', padx=(100,30))
        self.player_frame = self._create_players_frame(msg_frame)
        self.player_frame.pack(side='top', padx=(10,10), fill='both')

        self.save_menu_button = ttk.Button(msg_frame, text="Save/Load Game", command=lambda: self._save_menu())
        self.save_menu_button.pack(side='top', padx=(10,10), pady=(40,5))

        self.text_box = tk.Text(msg_frame, width=60, height=10, background='black', foreground='white')
        self.text_box.pack(side='bottom', padx=(10,10))

        return msg_frame

    def _create_logo_frame(self):
        """Create the frame at the top of the screen to display the logo"""
        logo_frame = ttk.Frame(self.main_frame, padding=10)
        # load a logo resource
        logo_image = tk.PhotoImage(file=r"resources/images/monopoly_logo.png")
        logo = ttk.Label(logo_frame, image=logo_image)
        logo.pack(side='top', anchor='n')
        logo.image = logo_image

        return logo_frame

    def _action_taken(self, action):

        if action == "save":
            print("save clicked")
            observer.Event("save", None)

        if action == "load":
            print("save clicked")
            observer.Event("load", None)

        if action == "roll":
            #tell the controller roll was clicked
            print("roll clicked")
            observer.Event("roll", None)

        if action == "purchase":
            observer.Event("purchase", None)

        if action == "mortgage":
            observer.Event("mortgage", None)

        if action == "unmortgage":
            observer.Event("unmortgage", None)

        if action == "mortgage_specific":
            observer.Event("mortgage_specific", 0)

        if action == "end_turn":
            #self.text_box.delete(1.0, tk.END)
            observer.Event("end_turn", self._clear_text)

    def update_state(self, state, text):
        """Function to update the state of the game"""
        if state == "roll":
            self._await_roll(text)
        elif state == "purchase":
            self._await_purchase()
        elif state == "moves":
            self._await_moves()
        elif state == "moves_or_bankrupt":
            self._await_moves_or_bankrupt()

    def purchase(self):
        observer.Event("purchase", None)

    def update_card(self, index):
        card_image = self.square_images[index]
        try:
            self.card['image'] = card_image
        except:
            pass

    def _clear_text(self):
        print("clearing text")
        self.text_box.delete(1.0, tk.END)

    def _update_text(self, text=""):
        #self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, text+"\n")


    def update_players_state(self, update: list[dict]):
        # self.state_box.delete(1.0, tk.END)
        # self.state_box.insert(tk.END, text)
        update.sort(key=lambda u: u['id'])
        if not update:
            return
        for (i, p) in enumerate(update):
            card = self.player_cards[i]

            if p['is_current_player']:
                card[0].configure(style='ActivePlayer.TFrame')
                for lable in card[1]:
                    lable.configure(style='ActivePlayer.TLabel')
            else:
                card[0].configure(style='TFrame')
                for lable in card[1]:
                    lable.configure(style='TLabel')

            card[1][0].configure(text=f"Name: {p['name']}")
            card[1][1].configure(text=f"Money: {p['money']}")
            card[1][2].configure(text=f"Net Worth: {p['net_worth']}")
            card[1][3].configure(text=f"Luck: {p['luck']}")
            card[1][4].configure(text=f"Position: {p['pos']}")

        # Update player piece positions
        positions = self._get_piece_positions([u['pos_id'] for u in update])
        for (i, pos) in enumerate(positions):
            img_id = self.canvas_images['pieces'][i]
            x = int(pos[0]*800)
            y = int(pos[1]*800)
            print(f"Moving image to {x}x{y}")
            self.canvas.moveto(img_id, x, y)
            self.canvas.tag_raise(img_id)


    def _save_menu(self):
        self.save_menu = tk.Toplevel(self.root)

        self.save_menu.title("Save/Load Game")
        self.save_menu.geometry("400x300")
        self.save_menu.resizable(True, True)
        self.save_menu.attributes('-type', 'dialog')
        self.save_menu.minsize(500,300)

        save_load_frame = ttk.Frame(self.save_menu, relief='raised', borderwidth = 3)

        file_name_lable = ttk.Label(save_load_frame, text="Save File: ")
        file_name_lable.pack(side="left", padx=(5,5), pady=(8,8))

        file_name = ttk.Entry(save_load_frame)
        file_name.pack(side="left", padx=(5,5), pady=(8,8), expand=True, fill="x")

        load_button = ttk.Button(save_load_frame, text="Load")
        load_button.pack(side="right", padx=(5,5))
        save_button = ttk.Button(save_load_frame, text="Save")
        save_button.pack(side="right", padx=(15,5))

        save_load_frame.pack(side="top", pady=(10,10), padx=(10,10), anchor="n", fill="x", expand=True)

        files = tk.Listbox(self.save_menu, selectmode="single")

        def onselect(evt):
            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)
            file_name.delete(0, len(file_name.get()))
            file_name.insert(0, value)

        files.bind('<<ListboxSelect>>', onselect)

        def update_entries():
            entries = get_save_files()
            print(f"{entries=}")
            def add_entry(list, entry):
                list.insert(list.size(), entry)
            [add_entry(files, entry.removesuffix(".json")) for entry in entries]

        update_entries()

        save_button.configure(command=lambda: observer.Event("save", file_name.get()+".json"))
        load_button.configure(command=lambda: observer.Event("load", file_name.get()+".json"))

        files.pack(side="top", fill="both", anchor="s", expand=True, pady=(5,15), padx=(20,20), after=save_load_frame)


    def _choose(self, choices):
        #good idea disable all buttons

        self.popup_menu = tk.Menu(self.root,
                                       tearoff=0)

        for c in choices:
            self.popup_menu.add_command(label=c,
                                        command=lambda ch=c: self.pick(ch))
        self.popup_menu.add_separator()

        lbl = "Cancel"
        if len(choices) == 0:
                lbl = "No properties to mortgage (click to cancel)"

        self.popup_menu.add_command(label=lbl,
                                    command=self.popup_menu.grab_release)
        try:
            self.popup_menu.tk_popup(600, 300, 0)
        finally:
            self.popup_menu.grab_release()

    def pick(self, s):
        observer.Event("mortgage_specific", s)

    def _get_piece_positions(self, player_positions: list[int]) -> list[tuple[float,float]]:
        output = []

        for (i, player) in enumerate(player_positions):
            # prev_count = player_positions[:i].count(player) # Get the count previous players at the same position
            dist_along_edge = player % 10
            if player == 10: # Visiting Jail
                output.append((-0.04,1.06))
            elif player < 10:
                output.append((1-dist_along_edge/10, 1))
            elif player < 20:
                output.append((0, 1-dist_along_edge/10))
            elif player < 30:
                output.append((dist_along_edge/10, 0))
            elif player < 40:
                output.append((1, dist_along_edge/10))
            elif player == 40: # In jail
                output.append((0.04, 0.97))
            else:
                raise ValueError(f"Invalid player position {player}")

        return [(x*0.85 + 0.05, y*0.85 + 0.05) for (x,y) in output]

        

    def _preload_images(self):
        '''Function to preload all the images for the board squares'''
        square_images = get_board_square_images()
        for image in square_images:
            img = tk.PhotoImage(file=image)
            self.square_images.append(img)

        self.square_images.append(self.square_images[10]) # Use Jail square for both visiting and in jail

        piece_images = get_player_piece_images()
        for image in piece_images:
            img = PIL.Image.open(image)
            img.thumbnail((40,40), PIL.Image.Resampling.LANCZOS)

            self.piece_images.append(PIL.ImageTk.PhotoImage(img))


