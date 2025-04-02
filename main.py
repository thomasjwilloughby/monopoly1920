#!/usr/bin/env python3
import tkinter as tk

import controller
import view

'''launch the GUI'''
if __name__ == '__main__':

    free_parking_payout = 0
    players_in_jail_collect = True
    property_auctions = False
    root = tk.Tk()
    root.minsize(1500,900)

    view = view.View(root)
    controller = controller.Controller(root)

    root.mainloop()
