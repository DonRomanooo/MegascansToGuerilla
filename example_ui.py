from PySide.QtCore import QThread, Signal
from PySide import QtGui, QtCore
import time, sys


class Worker(QThread):

    progress = Signal(str)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.exiting = False

    def run(self):
        i = 0
        while True:
            self.progress.emit(str(i))
            i += 1
            time.sleep(0.2)


class Win(QtGui.QWidget):

    def __init__(self, parent=None):
        super(Win, self).__init__(parent)
        self.setWindowTitle("Window")

        self.progress_label = QtGui.QLabel(self)
        self.progress_label.setText("Progress : ")

        layout = QtGui.QVBoxLayout(self)

        layout.addWidget(self.progress_label)

        self.update_thread()
        
    def update_thread(self):
        self.worker = Worker()
        
        self.worker.progress.connect(self.update_label, QtCore.Qt.QueuedConnection)

        if not self.worker.isRunning():
            self.worker.start()

    def update_label(self, text):
        self.progress_label.setText("Progress : " + text)
            

def launch():
    app = QtGui.QApplication.instance()

    if app is None:
	    app = QtGui.QApplication(sys.argv)

    win = Win()
    win.show()

    app.exec_()


launch()