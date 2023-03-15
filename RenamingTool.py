from datetime import datetime
import dearpygui.dearpygui as dpg
import os
import tkinter as tk
from tkinter import filedialog
from os.path import isfile, join
from os import listdir
import re

# create context
dpg.create_context()


# not actually being used right now, but is a place i can hide items.
dpg.add_stage(tag="Staging")


# assign dir and vars
wdir = os.getcwd().replace('\\', '/')
lastDir = ""
selectedRows = []
lastSelectedRowPos = None

# assign new dir
def getdirlog():
    global wdir
    root = tk.Tk()
    root.withdraw()
    if lastDir:
        default_path = lastDir
    else: default_path = wdir
    options = {'initialdir': default_path}
    wdir = filedialog.askdirectory(**options)
    try:
        dpg.configure_item(item="curDir", default_value=wdir)
    except Exception as e:
        print(e)
    selectedRows.clear()
    generateTable()


# gets all files in wdir
onlyfiles = []
def listFilesInDir():
    global onlyfiles
    try:
        onlyfiles = [f for f in listdir(wdir) if isfile(join(wdir, f))]
    except Exception as e:
        None


# theme for selected items
with dpg.theme() as item_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 255, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Header, (60, 60, 60), category=dpg.mvThemeCat_Core)
        # dpg.add_theme_color(dpg.color, (29, 151, 236, 103))


# file selection
def selectFiles(z, e):
    global selectedRows
    global lastSelectedRowPos

    parent = dpg.get_item_parent(item=z)
    gparentChildren = dpg.get_item_children(dpg.get_item_parent(parent))[1]

    # multi select
    if (dpg.is_key_down(key=dpg.mvKey_Shift) and not dpg.is_key_down(key=dpg.mvKey_Control)):
        if lastSelectedRowPos:
            if (lastSelectedRowPos < parent):
                for en, i in enumerate(gparentChildren):
                    if i in range(lastSelectedRowPos, parent+1):
                        if i in selectedRows and en > 1:
                            selectedRows.remove(i)
                        else:    
                            selectedRows.append(i)
            else:
                for en, i in enumerate(gparentChildren):
                    if i in range(parent, lastSelectedRowPos+1):
                        if i in selectedRows and en > 1:
                            selectedRows.remove(i)
                        else:    
                            selectedRows.append(i)
        else: 
            lastSelectedRowPos = parent
            selectedRows.append(parent)
        
    # single multi select
    elif (dpg.is_key_down(key=dpg.mvKey_Control) and not dpg.is_key_down(key=dpg.mvKey_Shift)):
        if parent in selectedRows:
            selectedRows.remove(parent)
        else:
            selectedRows.append(parent)
    
    # single select
    else:
        selectedRows.clear()
        selectedRows.append(parent)
    lastSelectedRowPos = parent
    highlightSelectedFiles()


def highlightSelectedFiles():
    for i in selectedRows:
        for x in dpg.get_item_children(i, 1):
            dpg.set_value(item=x, value=True)
            dpg.bind_item_theme(item=x, theme=item_theme)
    for i in dpg.get_item_children(item="fileTableContent")[1]:
        if i not in selectedRows:
            for x in dpg.get_item_children(i, 1):
                dpg.set_value(item=x, value=False)
                dpg.bind_item_theme(item=x, theme=0)


# generate fileTableGroup
def generateTable():
    listFilesInDir()
    try:
        dpg.delete_item(item="fileTableGroup")
    except Exception as e:
        print("can't delete something that does not exist")
    with dpg.group(tag="fileTableGroup", parent="tableWindow"):
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
                    dpg.add_selectable(label=f"{datetime.fromtimestamp(os.path.getmtime(wdir + '/' + i)).strftime('%Y/%m/%d')}", tag=i+"3")
                    dpg.add_selectable(label=f"", tag=i+"4")
    dpg.move_item("fileTableGroup", parent="tableWindow")


# Main DPG window
with dpg.window(tag="Prime", no_close=True, no_collapse=True, no_title_bar=True, no_move=True):
    dpg.add_input_text(tag="curDir",default_value=wdir, label="Current Directory", callback=lambda e,s : print(e,s))
    dpg.add_button(tag="testing",label="select directory", callback=getdirlog)
    with dpg.table(header_row=False,resizable=True, borders_innerH=True):
        dpg.add_table_column()
        with dpg.table_row():
            dpg.add_group(tag="tableWindow")
        with dpg.table_row():                    
            with dpg.group(tag="options"):
                dpg.add_text("HEllo!")
                with dpg.table(header_row=False):
                    dpg.add_table_column(width_fixed=True)
                    dpg.add_table_column()
                    with dpg.table_row():
                        with dpg.group():
                            dpg.add_text(label="Renaming", default_value="Renaming Style")
                            dpg.add_radio_button(items=["Automatic", "Semi-Automatic", "Manual"])
                        with dpg.group(tag="renamingStyle"):
                            for i in range(50):
                                dpg.add_text(default_value=i)

def updateFTableSize(s,t):
    # try:
    dpg.set_item_height(item="fileTableContent", height=int(dpg.get_item_height(t)/2))
    # except Exception as e:
    #     print(e)
with dpg.item_handler_registry(tag="updateOnViewportChange"):
    dpg.add_item_resize_handler(callback=updateFTableSize)    
dpg.bind_item_handler_registry(item="Prime", handler_registry="updateOnViewportChange")


dpg.create_viewport(title='Renaming Utility', width=600, height=600)


dpg.setup_dearpygui()
dpg.show_viewport()
try:
    dpg.set_primary_window("Prime", True)
except Exception as e:
    print(e)
generateTable()
dpg.start_dearpygui()
dpg.destroy_context()