#!/usr/bin/env python3
import tkinter as tk

from game import Game

def main():

    root = tk.Tk()
    root.attributes('-type', 'dialog')

    game = Game(root)

    root.mainloop()


'''launch the GUI'''
if __name__ == '__main__':
    main()
