from PySide import QtGui
import sys

import guerilla_importer as gi

class MegascansListener(QtGui.QWidget):
    def __init__(self):
        super(MegascansListener, self).__init__()
        self.setWindowTitle("Megascans Bridge")

        self.button = QtGui.QPushButton("Megascans Bridge")

        layout = QtGui.QVBoxLayout()

        layout.addWidget(self.button)

        self.setLayout(layout)

        #gi.listen()