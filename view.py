#!/usr/bin/env python3

import tkinter as tk
import os
from tkinter import ttk
import controller
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

class View (observer.Observer):
    """Class to create the GUI for the Monopoly game"""
    width = 1920-100
    height = 1080-100

    def __init__(self, root):
        super().__init__()
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

        self.canvas_images = {}

        self.canvas_images['background'] = canvas.create_image(401,401,image=self.board_image)
        self.canvas_images['test_piece'] = canvas.create_image(0,0,image=self.piece_images[2],anchor='nw')

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
        self.purchase_button.state(['active'])
        self.mid_buttons.append(self.purchase_button)

        self.mortgage_button = ttk.Button(button_frame, text="Mortgage", command=lambda: self._action_taken("mortgage"))
        self.mortgage_button.pack(side='top', anchor='center', pady=(10, 10))
        self.mortgage_button.state(['active'])
        self.mid_buttons.append(self.mortgage_button)

        self.unmortgage_button = ttk.Button(button_frame, text="Unmortgage", command=lambda: self._action_taken("unmortgage"))
        self.unmortgage_button.pack(side='top', anchor='center', pady=(10, 10))
        self.unmortgage_button.state(['active'])
        self.mid_buttons.append(self.unmortgage_button)

        self.bankrupt_button = ttk.Button(button_frame, text="Go Bankrupt", command=lambda: self._action_taken("bankrupt"))
        self.bankrupt_button.pack(side='top', anchor='center', pady=(10, 10))
        self.bankrupt_button.state(['active'])
        self.mid_buttons.append(self.bankrupt_button)

        self.end_turn_button = ttk.Button(button_frame, text="End Turn", command=lambda: self._action_taken("end_turn"))
        self.end_turn_button.pack(side='top', anchor='center', pady=(10, 10))
        self.end_turn_button.state(['active'])
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



    def _preload_images(self):
        '''Function to preload all the images for the board squares'''
        square_images = get_board_square_images()
        for image in square_images:
            img = tk.PhotoImage(file=image)
            self.square_images.append(img)
        
        piece_images = get_player_piece_images()
        for image in piece_images:
            img = PIL.Image.open(image)
            img.thumbnail((40,40), PIL.Image.Resampling.LANCZOS)

            self.piece_images.append(PIL.ImageTk.PhotoImage(img))

'''launch the GUI'''
if __name__ == '__main__':

    free_parking_payout = 0
    players_in_jail_collect = True
    property_auctions = False
    root = tk.Tk()
    root.minsize(1500,900)
    controller = controller.Controller(root)

    root.mainloop()

