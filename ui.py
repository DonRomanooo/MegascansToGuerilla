from PySide import QtGui, QtCore
from PySide.QtCore import QThread, QDataStream
from PySide.QtNetwork import QTcpServer, QHostAddress
import sys


from guerilla_importer import MSToGuerillaWorker


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

        self.__socket = QTcpServer()
        self.__socket.listen(QHostAddress("localhost"), 24981)

        self.__socket.newConnection.connect(self.on_new_connection)


    def on_new_connection(self):
        self.socket = self.__socket.nextPendingConnection()
        self.socket.readyRead.connect(self.on_ready_read)


    def on_ready_read(self):
        self.data = self.socket.readAll()

        worker = MSToGuerillaWorker()
        worker.import_data(str(self.data))
        
        

    
    def add_log(self, text):
        self.console_log.appendPlainText(text)

        scrollbar = self.console_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

