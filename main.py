#!/usr/bin/env python3
import tkinter as tk

import local_controller
import local_view

def main():

    root = tk.Tk()
    root.minsize(1500,900)

    view = local_view.LocalView(root)
    controller = local_controller.LocalController()

    root.mainloop()




'''launch the GUI'''
if __name__ == '__main__':
    main()
