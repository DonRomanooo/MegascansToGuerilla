from guerilla import command
import sys


import guerilla_importer as gi
from ui import *

from PySide import QtGui



class Shelf():
    """
    Class to initialize megascan shelf inside of Guerilla Render
    """
    class Listen(command):
        @staticmethod
        def action(luaObj, window, x, y, suffix):
            
            gi.MSToGuerillaWindow()

    cmd = Listen("Listen")
    cmd.install("Megascans")
