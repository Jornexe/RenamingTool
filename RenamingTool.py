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

def get_num(s):
    # extract the numeric part using a regular expression
    match = re.search(r'(\d+)(?=\.)', s)
    if match:
        return int(match.group())
    else:
        return 0

# gets all files in wdir
onlyfiles = []
def listFilesInDir():
    global onlyfiles
    try:
        onlyfiles = [f for f in listdir(wdir) if isfile(join(wdir, f))]
    except Exception as e:
        None
    onlyfiles = sorted(onlyfiles, key=get_num)
    # print(onlyfiles)


# theme for selected items
with dpg.theme() as item_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 255, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Header, (60, 60, 60), category=dpg.mvThemeCat_Core)
        # dpg.add_theme_color(dpg.color, (29, 151, 236, 103))

# theme for table categories
with dpg.theme() as renameOptions_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, (60, 255, 60), category=dpg.mvThemeCat_Core)
        # dpg.add_theme_color(dpg.mvThemeCol_bg)

# file selection
def selectFiles(z, e):
    global selectedRows
    global lastSelectedRowPos

    parent = dpg.get_item_parent(item=z)
    gparentChildren = dpg.get_item_children(dpg.get_item_parent(parent))[1]

    # multi select
    if (dpg.is_key_down(key=dpg.mvKey_Shift) and not dpg.is_key_down(key=dpg.mvKey_Control)):
        if lastSelectedRowPos is not None:
            start_idx = min(parent, lastSelectedRowPos)
            end_idx = max(parent, lastSelectedRowPos)

            for i in gparentChildren:
                if start_idx <= i <= end_idx:
                    if i not in selectedRows:
                        selectedRows.append(i)
                    else:
                        if i != parent and i != lastSelectedRowPos:
                            selectedRows.remove(i)
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
            dpg.set_item_label(dpg.get_item_children(i,1)[1], dpg.get_item_label(dpg.get_item_children(i,1)[0]))
            for x in dpg.get_item_children(i, 1):
                dpg.set_value(item=x, value=False)
                dpg.bind_item_theme(item=x, theme=0)
    preRename()


# generate fileTableGroup
def generateTable():
    global onlyfiles
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
                with dpg.table_row():
                    dpg.add_selectable(label=f"{i}", tag=i+"0", callback=selectFiles, span_columns=True)
                    dpg.add_selectable(label=f"{i}", tag=i+"1")
                    dpg.add_selectable(label=f"{os.path.getsize(wdir + '/' + i )}", tag=i+"2")
                    dpg.add_selectable(label=f"{datetime.fromtimestamp(os.path.getmtime(wdir + '/' + i)).strftime('%Y/%m/%d')}", tag=i+"3")
                    dpg.add_selectable(label=f"", tag=i+"4")
    dpg.move_item("fileTableGroup", parent="tableWindow")

def preRename():
    selectedRows.sort(key=lambda x: dpg.get_item_children(x, 1)[0])
    startValue = dpg.get_value(item="start")
    increment = dpg.get_value(item="increment")
    for i in selectedRows:
        fileid = dpg.get_item_children(i, 1)[0]
        fileName = dpg.get_item_label(fileid)
        dpg.set_item_label(dpg.get_item_children(i, 1)[1], re.sub(r'(\d+)(?=\.)', str('{:03d}'.format(startValue)), fileName))
        # print(fileid, fileName)
        startValue+=increment


def rStyle(s,e):
    if dpg.does_item_exist(item="renamingStyle"):
        if dpg.get_item_children(item="renamingStyle", slot=1):
            dpg.delete_item(item="renamingStyle", children_only=True)
    with dpg.group(tag="rStyleOptions", parent="renamingStyle"):
        if e == "Automatic":
            dpg.add_text(default_value="Numbering")
            # dpg.add_input_int(label="Start", width=int(dpg.get_text_size(text="000000000+Start")[0]))
            dpg.add_input_int(tag="start", label="Start", default_value=1, width=int(dpg.get_text_size(text="000000000+Start")[0]), callback=preRename)
            dpg.add_input_int(tag="increment", label="Increment", default_value=1, width=int(dpg.get_text_size(text="000000000+Start")[0]))
            dpg.add_button(label="Rename")
        elif e == "Semi-Automatic":
            dpg.add_text(default_value="Numbering")
            dpg.add_input_int(label="Replace From", width=int(dpg.get_text_size(text="000000000+Start")[0]))
            dpg.add_input_int(label="Start", width=int(dpg.get_text_size(text="000000000+Start")[0]))
            dpg.add_input_int(label="Increment", default_value=1, width=int(dpg.get_text_size(text="000000000+Start")[0]))
            dpg.add_button(label="Rename")
        elif e == "Manual":
            Mwidth = int(dpg.get_text_size(text="000000000+Add Number")[0])
            with dpg.table(header_row=False):
                dpg.add_table_column(label="Option", width_fixed=True)
                dpg.add_table_column(label="Value")
                with dpg.table_row() as row1:
                    dpg.add_text("String Replacement")
                    dpg.bind_item_theme(item=row1,theme=renameOptions_theme)
                    # print(dpg.getitem)
                with dpg.table_row():
                    a = dpg.add_text("Replace From")
                    b = dpg.add_input_text(label="", width=Mwidth)
                    dpg.bind_item_theme(item=a,theme=renameOptions_theme)
                with dpg.table_row():
                    dpg.add_text("Replace To")
                    dpg.add_input_text(label="", width=Mwidth)
                with dpg.table_row():
                    dpg.add_text("Regex Replacement")
                with dpg.table_row():
                    dpg.add_text("Regex")
                    dpg.add_input_text(label="", width=Mwidth)
                with dpg.table_row():
                    dpg.add_text("Replace With")
                    dpg.add_input_text(label="", width=Mwidth)
                with dpg.table_row():
                    dpg.add_text("Numbering")
                with dpg.table_row():
                    dpg.add_text("Start")
                    dpg.add_input_int(label="", width=Mwidth)
                with dpg.table_row():
                    dpg.add_text("Increment")
                    dpg.add_input_int(label="", default_value=1, width=Mwidth)
                with dpg.table_row():
                    dpg.add_text("Add")
                with dpg.table_row():
                    dpg.add_text("Add Text")
                    dpg.add_input_text(label="", width=Mwidth)
                with dpg.table_row():
                    dpg.add_button(label="Rename")


# Main DPG window
with dpg.window(tag="Prime", no_close=True, no_collapse=True, no_title_bar=True, no_move=True):
    dpg.add_input_text(tag="curDir",default_value=wdir, label="Current Directory", readonly=True)
    dpg.add_button(tag="testing",label="select directory", callback=getdirlog)
    with dpg.table(header_row=False,resizable=True, borders_innerH=True):
        dpg.add_table_column()
        with dpg.table_row():
            dpg.add_group(tag="tableWindow")
        with dpg.table_row():                    
            with dpg.group(tag="options"):
                with dpg.table(header_row=False):
                    dpg.add_table_column(width_fixed=True)
                    dpg.add_table_column()
                    with dpg.table_row():
                        with dpg.group():
                            dpg.add_text(label="Renaming", default_value="Renaming Style")
                            # dpg.add_radio_button(items=["Automatic", "Semi-Automatic", "Manual"], callback=rStyle)
                            dpg.add_radio_button(items=["Automatic"], callback=rStyle)
                        with dpg.group(tag="renamingStyle"):
                            None

# implement drag for the bottom of the ftable for resizing
ftableH = 0
def updateFTableSize(s,t):
    # try:
    tH = dpg.get_item_height(t)
    dpg.set_item_height(item="fileTableContent", height=int(tH/2+(min(max(ftableH,-(tH/3)),tH/3))))
    # except Exception as e:
    #     print(e)
# with dpg.item_handler_registry(tag="updateOnTableSizeChange"):
#     dpg.additemc
with dpg.item_handler_registry(tag="updateOnViewportChange"):
    dpg.add_item_resize_handler(callback=updateFTableSize)    
dpg.bind_item_handler_registry(item="Prime", handler_registry="updateOnViewportChange")


dpg.create_viewport(title='Renaming Utility', width=600, height=800)


dpg.setup_dearpygui()
dpg.show_viewport()
try:
    dpg.set_primary_window("Prime", True)
except Exception as e:
    print(e)
generateTable()

# jank solution to select Automatic on startup
def on_main_window_visible(sender, app_data):
    rStyle(None, "Automatic")
    dpg.bind_item_handler_registry(item="Prime", handler_registry="updateOnViewportChange")

with dpg.item_handler_registry(tag="main_window_handler"):
    dpg.add_item_visible_handler(callback=on_main_window_visible)
dpg.bind_item_handler_registry("Prime", "main_window_handler")

dpg.start_dearpygui()
dpg.destroy_context()