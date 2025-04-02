#!/usr/bin/env python3
import tkinter as tk

import local_controller
import local_view

'''launch the GUI'''
if __name__ == '__main__':

    free_parking_payout = 0
    players_in_jail_collect = True
    property_auctions = False
    root = tk.Tk()
    root.minsize(1500,900)

    view = local_view.LocalView(root)
    controller = local_controller.LocalController(root)

    root.mainloop()
