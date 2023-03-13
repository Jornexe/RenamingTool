import dearpygui.dearpygui as dpg
import os
import tkinter as tk
from tkinter import filedialog
from os.path import isfile, join
from os import listdir

# assign dir
wdir = r"C:\Projects\RenamingTool"
# assign new dir
def getdirlog():
    root = tk.Tk()
    root.withdraw()
    default_path = os.getcwd()
    options = {'initialdir': default_path}
    wdir = filedialog.askdirectory(**options)
    return wdir
# updates the wdir variable
def update_wdir():
    global wdir
    wdir = getdirlog()

# gets all files in wdir
onlyfiles = [f for f in listdir(wdir+"/dummyfiles") if isfile(join(wdir+"/dummyfiles", f))]

selectedFiles = []

# create context
dpg.create_context()

# file selection
lastSelectedFile = ""
def selectFiles(s, e):
    # multi select
    if (dpg.is_key_down(key=dpg.mvKey_Shift) and not dpg.is_key_down(key=dpg.mvKey_Control)):
        if lastSelectedFile:
            None
        else: 
            selectedFiles.append(e[1])
    # single multi select
    elif (dpg.is_key_down(key=dpg.mvKey_Control) and not dpg.is_key_down(key=dpg.mvKey_Shift)):
        if (e[1] in selectedFiles):
            selectedFiles.remove(e[1])
        else:
            selectedFiles.append(e[1])
    # single select
    else:
        selectedFiles.clear()
        if (e[1] not in selectedFiles):
            selectedFiles.append(e[1])
    lastSelectedFile = e[1]
    print(selectedFiles)

def highlightSelectedFiles():
    for i in selectedFiles:
        dpg.add_theme_color(target=i, )

with dpg.item_handler_registry(tag="fileClickedHandler") as handler:
    dpg.add_item_clicked_handler(callback=selectFiles)

# stage filetable
with dpg.stage():
    with dpg.table(tag="fileTable",header_row=True, resizable=True, borders_innerV=True, height=300, scrollY=True):
        dpg.add_table_column(tag="someTag",label="File Name", width_stretch=False, width_fixed=True)
        dpg.add_table_column(tag="fNewfile",label="New File Name", width_stretch=False, width_fixed=True)
        dpg.add_table_column(tag="fSize",label="Size", width_stretch=False, width_fixed=True)
        dpg.add_table_column(tag="fModified",label="Modified", width_stretch=False, width_fixed=True)
        dpg.add_table_column(tag="fStatus",label="Status", width_stretch=False, width_fixed=True)
        for i in onlyfiles:
            with dpg.table_row():
                # for j in range(0, 5):
                dpg.add_text(f"{i}", tag=i)
                dpg.add_text(f"{i}")
                dpg.add_text(f"{os.path.getsize(wdir + '/dummyfiles/' + i )}")
                dpg.add_text(f"Row 3 Column test")
                dpg.add_text(f"Row 4 Column test")

def unstage():
    dpg.move_item("fileTable", parent="tableWindow")
    for i in onlyfiles:
        dpg.bind_item_handler_registry(item=i, handler_registry="fileClickedHandler")


width, height = 600,600

with dpg.window(tag="Prime", no_close=True, no_collapse=True, no_title_bar=True, no_move=True):
    dpg.add_group(tag="tableWindow")
    with dpg.group(tag="options"):
        dpg.add_text("HEllo!")
        dpg.add_button(tag="testing",label="select working directory", callback=update_wdir)
            # dpg.add_text(label=wdir)
        dpg.add_button(label="get cur dir", callback=lambda: print(wdir))
    
dpg.create_viewport(title='File Name', width=width, height=height)

dpg.setup_dearpygui()
dpg.show_viewport()
try:
    dpg.set_primary_window("Prime", True)
except Exception as e:
    print(e)
unstage()
# updateHeader()
dpg.start_dearpygui()
dpg.destroy_context()