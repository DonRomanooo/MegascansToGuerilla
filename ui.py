from PySide import QtGui, QtCore
from PySide.QtCore import QThread
import sys


from guerilla_importer import MSToGuerillaWorker as Worker


class MSToGuerillaWindow(QtGui.QWidget):


    def __init__(self, parent=None):
        super(MSToGuerillaWindow, self).__init__(parent)
        self.setWindowTitle("Megascans Bridge")

        self.status_label = QtGui.QLabel(self)
        self.status_label.setText("Status : ")

        self.console_log = QtGui.QPlainTextEdit()
        self.console_log.setReadOnly(True)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.status_label)
        layout.addWidget(self.console_log)

        self.update_thread()
        

    def update_thread(self):
        self.worker = Worker()
        
        self.worker.status.connect(self.update_status, QtCore.Qt.QueuedConnection)
        self.worker.log.connect(self.add_log, QtCore.Qt.QueuedConnection)

        if not self.worker.isRunning():
            self.worker.start()


    def update_status(self, text):
        self.status_label.setText("Status : " + text)

    
    def add_log(self, text):
        self.console_log.appendPlainText(text)

        scrollbar = self.console_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


def launch():

    app = QtGui.QApplication.instance()

    if app is None:
        app = QtGui.QApplication(sys.argv)

    win = MSToGuerillaWindow()
    win.show()

    app.exec_()

launch()

