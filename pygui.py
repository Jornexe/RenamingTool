import dearpygui.dearpygui as dpg
import os
import tkinter as tk
from tkinter import filedialog


wdir = "C:/"
def getdirlog():
    root = tk.Tk()
    root.withdraw()
    default_path = os.getcwd()
    options = {'initialdir': default_path}
    wdir = filedialog.askdirectory(**options)
    return wdir
def update_wdir():
    global wdir
    wdir = getdirlog()

dpg.create_context()

width, height = 600,600
with dpg.window(tag="Prime", no_close=True, no_collapse=True, no_title_bar=True, no_move=True):
    dpg.add_listbox()
    
    dpg.add_button(label="select working directory", callback=lambda: update_wdir())
        # dpg.add_text(label=wdir)
    dpg.add_button(label="get cur dir", callback=lambda: print(wdir))
with dpg.window(tag="FileList"):
    with dpg.table():
        dpg.add_table_column()

dpg.create_viewport(title='File Name', width=width, height=height)

dpg.setup_dearpygui()
dpg.show_viewport()
try:
    dpg.set_primary_window("Prime", True)
except Exception as e:
    print(e)

dpg.start_dearpygui()
dpg.destroy_context()