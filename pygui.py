import dearpygui.dearpygui as dpg
import os
import tkinter as tk
from tkinter import filedialog

def getdirlog():
    root = tk.Tk()
    root.withdraw()

    default_path = "/path/with/ø/æ/å/characters"

    options = {
        'initialdir': default_path,
    }

    dirpath = filedialog.askdirectory(**options)

    print(dirpath)

dpg.create_context()

width, height = 600,600
with dpg.window(tag="Prime", no_close=True, no_collapse=True, no_title_bar=True, no_move=True):
    dpg.add_button(label="test",callback=lambda : print(getdirlog()))

dpg.create_viewport(title='File Name', width=width, height=height)

dpg.setup_dearpygui()
dpg.show_viewport()
try:
    dpg.set_primary_window("Prime", True)
except Exception as e:
    print(e)

dpg.start_dearpygui()
dpg.destroy_context()