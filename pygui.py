import dearpygui.dearpygui as dpg
import os
import tkinter as tk
from tkinter import filedialog
from os.path import isfile, join
from os import listdir
import re

# assign dir
wdir = os.getcwd()
lastDir = ""
print(wdir)
# assign new dir
def getdirlog():
    root = tk.Tk()
    root.withdraw()
    if lastDir:
        default_path = lastDir
    else: default_path = os.getcwd()
    options = {'initialdir': default_path}
    wdir = filedialog.askdirectory(**options)
    return wdir
# updates the wdir variable
def update_wdir():
    global wdir
    wdir = getdirlog()

# gets all files in wdir

onlyfiles = [f for f in listdir(wdir) if isfile(join(wdir, f))]

selectedFiles = []

# create context
dpg.create_context()

# theme
with dpg.theme() as item_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 255, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Header, (60, 60, 60), category=dpg.mvThemeCat_Core)
        # dpg.add_theme_color(dpg.color, (29, 151, 236, 103))
        
# file selection
lastSelectedFile = ""
def selectFiles(s, e):
    s = re.sub(r'\d+$', '', s)
    global lastSelectedFile
    global selectedFiles
    # print(lastSelectedFile)
    # multi select
    def test(a, b):
        for x in range(a, b+1):
            new_string = re.sub(r"\d+(?=\.[^.]*$)", str(x).zfill(3), lastSelectedFile)
            selectedFiles.append(new_string)
    if (dpg.is_key_down(key=dpg.mvKey_Shift) and not dpg.is_key_down(key=dpg.mvKey_Control)):
        if lastSelectedFile:
            a = int(re.search(r"\d+(?=\.[^.]*$)", lastSelectedFile).group())
            b = int(re.search(r"\d+(?=\.[^.]*$)", s).group())
            if (a < b):
                test(a, b)
            else: test(b, a)  
        else: 
            selectedFiles.append(s)
    # single multi select
    elif (dpg.is_key_down(key=dpg.mvKey_Control) and not dpg.is_key_down(key=dpg.mvKey_Shift)):
        if (s in selectedFiles):
            selectedFiles.remove(s)
        else:
            selectedFiles.append(s)
    # single select
    else:
        selectedFiles.clear()
        selectedFiles.append(s)
    lastSelectedFile = s
    highlightSelectedFiles()
    print(selectedFiles)

def highlightSelectedFiles():
    for i in selectedFiles:
        for x in range(0, 5):
            dpg.set_value(i+"0", True)
            dpg.bind_item_theme(item=i+str(x), theme=item_theme)
            # dpg.set_item
            
    for i in onlyfiles:
        if i not in selectedFiles:
            for x in range(0, 5):
                dpg.set_value(i+"0", False)
                dpg.bind_item_theme(item=i+str(x), theme= 0)

# stage fileTableGroup
with dpg.stage(tag="Staging"):
    with dpg.group(tag="fileTableGroup"):
        dpg.add_group(tag="fileTableHeadersGroup")
        with dpg.table(tag="fileTableContent", header_row=True, resizable=True, borders_innerV=True, height=300, scrollY=True, freeze_rows=1, freeze_columns=1) as theFileTable:
            dpg.add_table_column(tag="someTag",label="File Name", width_stretch=False, width_fixed=True)
            dpg.add_table_column(tag="fNewfile",label="New File Name", width_stretch=False, width_fixed=True)
            dpg.add_table_column(tag="fSize",label="Size", width_stretch=False, width_fixed=True)
            dpg.add_table_column(tag="fModified",label="Modified", width_stretch=False, width_fixed=True)
            dpg.add_table_column(tag="fStatus",label="Status", width_stretch=False, width_fixed=True)
            for i in onlyfiles:
                with dpg.table_row() as theTableRow:
                    dpg.add_selectable(label=f"{i}", tag=i+"0", callback=selectFiles, span_columns=True)
                    dpg.add_selectable(label=f"{i}", tag=i+"1")
                    dpg.add_selectable(label=f"{os.path.getsize(wdir + '/' + i )}", tag=i+"2")
                    dpg.add_selectable(label=f"Row 3 Column test", tag=i+"3")
                    dpg.add_selectable(label=f"Row 4 Column test", tag=i+"4")
dpg.move_item("fileTableGroup", parent="tableWindow")

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

dpg.start_dearpygui()
dpg.destroy_context()