#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2009-2015 Joao Carlos Roseta Matos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""GUI using tkinter."""

# Python 3 compatibility
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# import io  # Python 3 compatibility
import sys
import tkinter as tk
import tkinter.messagebox as tk_msg_box

# from builtins import input  # Python 3 compatibility

import common
import localization as lcl
import shared as shrd

if common.PY < 3:
    import ttk as tk_ttk
else:
    import tkinter.ttk as tk_ttk


def start():
    """Print banner and start GUI."""

    def exit_gui():
        """Exit program."""
        root.destroy()
        sys.exit(0)  # ToDo: other return codes

    def center(window):
        """Center window."""
        window.update_idletasks()
        width = window.winfo_width()
        frm_width = window.winfo_rootx() - window.winfo_x()
        win_width = width + 2 * frm_width
        height = window.winfo_height()
        titlebar_height = window.winfo_rooty() - window.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = window.winfo_screenwidth() // 2 - win_width // 2
        y = window.winfo_screenheight() // 2 - win_height // 2
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        if window.attributes('-alpha') == 0:
            window.attributes('-alpha', 1.0)
        window.deiconify()

    def show_help(*args):
        """Show help message."""
        tk_msg_box.showinfo(lcl.HELP, common.usage())

    print(common.banner())

    root = tk.Tk()
    root.withdraw()
    win = tk.Toplevel(root)

    # for exit confirmation
    win.protocol('WM_DELETE_WINDOW', exit_gui)

    win.title(lcl.WIN_TITLE)

    # not resizable
    win.resizable(False, False)

    # resizable (limits)
    # win.minsize(250, 125)
    # win.maxsize(500, 250)

    # needed by center function?
    # win.attributes('-alpha', 0.0)

    win.bind('<F1>', show_help)

    # menu
    win.option_add('*tearOff', False)
    menubar = tk.Menu(win)
    win.config(menu=menubar)
    filemenu = tk.Menu(menubar)
    helpmenu = tk.Menu(menubar)

    menubar.add_cascade(label=lcl.FILE, menu=filemenu, underline=0)
    menubar.add_cascade(label=lcl.HELP, menu=helpmenu, underline=0)

    filemenu.add_command(label=lcl.EXIT, underline=0, command=exit_gui)

    helpmenu.add_command(label=lcl.HELP, underline=0, command=show_help,
                         accelerator='F1')
    helpmenu.add_separator()
    helpmenu.add_command(label=lcl.ABOUT, underline=0, state='disabled')

    # ToDo: log menu item
    # filemenu.add_separator()
    # check = StringVar(value=1)
    # filemenu.add_checkbutton(label='Log', variable=check, onvalue=1,
    #                          offvalue=0)

    frame = tk_ttk.Frame(win, padding='3 3 3 3')
    frame.grid(column=0, row=0, sticky='WNES')

    # if the main window is resized, the frame should expand
    # frame.columnconfigure(0, weight=1)
    # frame.rowconfigure(0, weight=1)

    private_lbl = tk.StringVar(value=lcl.PRIVATE_IP + shrd.get_private_ip())
    public_lbl = tk.StringVar(value=lcl.PUBLIC_IP + shrd.get_public_ip())

    # 1st row
    tk_ttk.Label(frame, textvariable=private_lbl).grid(column=1, row=1)

    # 2nd row
    tk_ttk.Label(frame, textvariable=public_lbl).grid(column=1, row=2)

    # remove if windows is non resizable
    # tk_ttk.Sizegrip(frame).grid(column=999, row=999, sticky=(E,S))

    # padding around all widgets
    for widget in frame.winfo_children():
        widget.grid_configure(padx=5, pady=5)

    # center window
    center(win)

    root.mainloop()


if __name__ == '__main__':
    # import doctest
    # doctest.testmod(verbose=True)
    pass
