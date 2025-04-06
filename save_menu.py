import tkinter as tk
from tkinter import ttk
import os
from tkinter import messagebox
from typing import Callable

import observer 

def get_save_files() -> list[str]:
    saves_path = os.path.join("saves")
    if not os.path.isdir(saves_path):
        os.mkdir(saves_path)

    return os.listdir(saves_path)

class SaveMenu:
    def __init__(self, root: tk.Tk, close_callback: Callable):
        self.save_menu = tk.Toplevel(root)
        self._onclose = close_callback

        self.save_menu.title("Save/Load Game")
        self.save_menu.geometry("560x300")
        self.save_menu.resizable(True, True)
        self.save_menu.attributes('-type', 'dialog')
        self.save_menu.minsize(560,300)

        self.save_load_frame = ttk.Frame(self.save_menu, relief='raised', borderwidth = 3)

        self.file_name_lable = ttk.Label(self.save_load_frame, text="Save File: ")
        self.file_name_lable.pack(side="left", padx=(5,5), pady=(8,8))

        self.file_name = ttk.Entry(self.save_load_frame)
        self.file_name.pack(side="left", padx=(5,5), pady=(8,8), expand=True, fill="x")
        
        delete_button = ttk.Button(self.save_load_frame, text="Delete")
        delete_button.pack(side="right", padx=(5,5))
        load_button = ttk.Button(self.save_load_frame, text="Load")
        load_button.pack(side="right", padx=(5,5))
        save_button = ttk.Button(self.save_load_frame, text="Save")
        save_button.pack(side="right", padx=(15,5))

        self.save_load_frame.pack(side="top", pady=(10,10), padx=(10,10), anchor="n", fill="x", expand=True)

        self.files = tk.Listbox(self.save_menu, selectmode="single")
        self.files.bind('<<ListboxSelect>>', self._onselect)

        self._update_entries()

        save_button.configure(command=self._save_clicked)
        load_button.configure(command=self._load_clicked)
        delete_button.configure(command=self._delete_save)

        self.files.pack(side="top", fill="both", anchor="s", expand=True, pady=(5,15), padx=(20,20), after=self.save_load_frame)

    def _load_clicked(self):
        observer.Event("load", self.file_name.get())
        self.save_menu.destroy()
        self._onclose()

    def _save_clicked(self):
        observer.Event("save", self.file_name.get())
        self._update_entries()

    def _delete_save(self):
        save_name: str = self.file_name.get()
        if save_name == '':
            return
        saves = get_save_files()
        if (save_name+".json") in saves:
            print(f'Save "{save_name}" exists')
            should_delete = messagebox.askokcancel(f"Delete save '{save_name}'", f"Are you sure you want delete '{save_name}'\n There is no way to undo this.")
            if should_delete:
                print(f"User approved deletion of {save_name}. Proceeding")
                os.remove(os.path.join("saves", f"{save_name}.json"))
                self._update_entries()
            else:
                print(f"User cancelled deletion of {save_name}")
        else:
            messagebox.showinfo("No save found", f"Unable to find save of name '{save_name}'")


    def _onselect(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.file_name.delete(0, len(self.file_name.get()))
        self.file_name.insert(0, value)

    def _update_entries(self):
        entries = get_save_files()
        # print(f"{entries=}")
        self.files.delete(0,'end')
        def add_entry(list, entry):
            list.insert(list.size(), entry)
        [add_entry(self.files, entry.removesuffix(".json")) for entry in entries]



