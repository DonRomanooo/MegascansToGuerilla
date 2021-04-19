from guerilla import command
import sys


import guerilla_importer as gi

import ui
from PySide import QtGui

# Initialize the UI as a global so it does not get destroyed by the end of scope in the action method
app = QtGui.QApplication.instance()

if app is None:
    app = QtGui.QApplication([])

win = ui.MSToGuerillaWindow()


class Shelf():
    """
    Class to initialize megascan shelf inside of Guerilla Render
    """
    class Listen(command):

        @staticmethod
        def action(luaObj, window, x, y, suffix):
            win.show()

    cmd = Listen("Listen")
    cmd.install("Megascans")
